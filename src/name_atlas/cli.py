"""Command-line entry point for the local workbench."""

import argparse
import logging
import os
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path

import uvicorn

from name_atlas.app import create_app
from name_atlas.cases import CardDisplayOrigin, MigrationCaseError, default_case_path
from name_atlas.config import DEFAULT_PORT, LOOPBACK_HOST, RuntimeConfig
from name_atlas.decision_cards import (
    BudgetLedgerError,
    DecisionCardProviderError,
    LiveDecisionCardProvider,
    RecordedReplayDecisionCardProvider,
    ReplayProviderError,
)
from name_atlas.domain import RunMode
from name_atlas.folder_app import (
    PLANNER_LABEL,
    create_folder_app,
)
from name_atlas.folder_job_service import JobBackedFolderRunService
from name_atlas.folder_refactor.job import default_job_path
from name_atlas.folder_refactor.portable_artifacts import (
    CHANGE_RECEIPT_PATH as FOLDER_CHANGE_RECEIPT_PATH,
)
from name_atlas.folder_refactor.portable_artifacts import (
    SOURCE_SNAPSHOT_PATH as FOLDER_SOURCE_SNAPSHOT_PATH,
)
from name_atlas.folder_refactor.portable_artifacts import (
    FolderPortableArtifactError,
)
from name_atlas.folder_refactor.portable_artifacts import (
    read_regular_bytes as read_folder_artifact_bytes,
)
from name_atlas.folder_refactor.portable_artifacts import (
    strict_json_object as strict_folder_json_object,
)
from name_atlas.folder_refactor.receipt_contracts import (
    FolderReceiptVerificationStatus,
)
from name_atlas.folder_refactor.receipt_verifier import (
    FolderReceiptCandidateError,
    verify_folder_receipt,
)
from name_atlas.package_import import PackageImportError
from name_atlas.receiver_verifier import (
    ReceiptCandidateError,
    ReceiptVerificationStatus,
    verify_receipt,
)
from name_atlas.restore import RestoreError, restore_receipt
from name_atlas.verification import BagItPackageValidator
from name_atlas.workflow import UnavailableReplayDecisionCardProvider, WorkflowSession

LOGGER = logging.getLogger(__name__)


def _runtime_roots(package_root: Path, working_directory: Path) -> tuple[Path, Path]:
    """Return the writable project root and deterministic bundled hero root."""

    checkout_root = package_root.parents[1]
    running_from_checkout = (checkout_root / "pyproject.toml").is_file() and (
        checkout_root / "src" / "name_atlas"
    ).resolve() == package_root
    if running_from_checkout:
        return checkout_root, checkout_root / "sample_data" / "hero"
    return working_directory, package_root / "sample_data" / "hero"


PACKAGE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT, HERO_SOURCE_ROOT = _runtime_roots(PACKAGE_ROOT, Path.cwd())
FOLDER_A1_SOURCE_ROOT = HERO_SOURCE_ROOT.parent / "folder_a1"
REPLAY_RECORD_PATH = PACKAGE_ROOT / "recordings" / "hero_decision_card.json"
OUTPUT_ROOT = PROJECT_ROOT / ".name-atlas" / "stages"
FOLDER_OUTPUT_ROOT = PROJECT_ROOT / ".name-atlas" / "folder-results"
BUDGET_LEDGER_PATH = PROJECT_ROOT / ".name-atlas" / "api_budget.json"
CASE_DIRECTORY = PROJECT_ROOT / ".name-atlas" / "cases"
_FOLDER_RECONSTRUCTION_CODES = frozenset(
    {
        "destination_exists",
        "destination_must_be_absolute",
        "destination_must_share_result_parent",
        "destination_overlaps_result",
        "destination_parent_invalid",
        "destination_type_invalid",
        "pending_cleanup_failed",
        "pending_destination_conflict",
        "promotion_failed",
        "receipt_verification_blocked",
        "receipt_reparse_failed",
        "reconstructed_inventory_mismatch",
        "reconstruction_copy_failed",
    }
)


class _FolderRestoreBlocked(RuntimeError):
    """Stable CLI projection of one generic-folder reconstruction blocker."""

    def __init__(self, code: str, failed_check_ids: tuple[str, ...] = ()) -> None:
        super().__init__(code)
        self.code = code
        self.failed_check_ids = failed_check_ids


def build_parser() -> argparse.ArgumentParser:
    """Build the stable judge-facing command parser."""

    parser = argparse.ArgumentParser(prog="name-atlas")
    subparsers = parser.add_subparsers(dest="command", required=True)

    demo = subparsers.add_parser(
        "demo",
        help="Run the loopback-only Reversible Name Atlas application.",
    )
    demo.add_argument(
        "--mode",
        choices=[mode.value for mode in RunMode],
        required=True,
        help="Use a recorded response or the live gpt-5.6 provider.",
    )
    demo.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Loopback port (default: {DEFAULT_PORT}).",
    )
    demo.add_argument(
        "--source",
        type=Path,
        default=HERO_SOURCE_ROOT,
        help="Supported package root (default: the included hero package).",
    )
    demo.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_ROOT,
        help="Copy-only staging parent (default: .name-atlas/stages).",
    )
    demo.add_argument(
        "--case",
        type=Path,
        default=None,
        help="Migration Case file (default: deterministic .name-atlas/cases path).",
    )

    folder_run = subparsers.add_parser(
        "run",
        help="Run the AI-first connected-folder application.",
    )
    folder_run.add_argument(
        "--mode",
        choices=("development",),
        required=True,
        help="Use the truthful deterministic A2 planner with no API call.",
    )
    folder_run.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Loopback port (default: {DEFAULT_PORT}).",
    )
    folder_run.add_argument(
        "--source",
        type=Path,
        default=FOLDER_A1_SOURCE_ROOT,
        help="Ordinary folder root (default: the included A1 folder).",
    )
    folder_run.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Existing result parent (default: .name-atlas/folder-results).",
    )
    folder_run.add_argument(
        "--job",
        type=Path,
        default=None,
        help=(
            "Resume this exact job file, or create it if absent "
            "(default: a new UUID-named .name-atlas/jobs file)."
        ),
    )

    verify = subparsers.add_parser(
        "verify-receipt",
        help="Independently verify one received portable handoff.",
    )
    verify.add_argument("received_bag", type=Path)
    verify.add_argument(
        "--source",
        type=Path,
        default=None,
        help="Optionally compare the committed source description to this root.",
    )

    restore = subparsers.add_parser(
        "restore-receipt",
        help="Reconstruct the supported source package from a verified handoff.",
    )
    restore.add_argument("received_bag", type=Path)
    restore.add_argument("restore_destination", type=Path)
    return parser


def run(
    argv: Sequence[str] | None = None,
    *,
    environ: Mapping[str, str] | None = None,
) -> int:
    """Run the CLI and return a process exit code."""

    args = build_parser().parse_args(argv)
    if args.command == "verify-receipt":
        received_bag = args.received_bag.expanduser()
        supplied_source = args.source.expanduser() if args.source is not None else None
        folder_receipt_schema = _folder_receipt_schema(received_bag)
        if _unsupported_folder_receipt_schema(folder_receipt_schema):
            print("BLOCKED receipt_schema_invalid")
            return 1
        if folder_receipt_schema == "folder-change-receipt.v2":
            from name_atlas.folder_refactor.connected_change.verification import (
                ConnectedReceiptVerificationStatus,
                verify_connected_result,
            )

            connected_result = verify_connected_result(
                received_bag,
                source_root=supplied_source,
            )
            if connected_result.status is ConnectedReceiptVerificationStatus.VERIFIED:
                print(f"VERIFIED {connected_result.receipt_fingerprint}")
                return 0
            print(f"BLOCKED {' '.join(connected_result.failed_check_ids)}")
            return 1
        if _is_folder_receipt(received_bag):
            try:
                folder_result = verify_folder_receipt(
                    received_bag,
                    source_root=supplied_source,
                )
            except FolderReceiptCandidateError as exc:
                print(f"Receipt input error: {exc}", file=sys.stderr)
                return 2
            if folder_result.status is FolderReceiptVerificationStatus.VERIFIED:
                print(f"VERIFIED {folder_result.receipt_fingerprint}")
                return 0
            print(f"BLOCKED {' '.join(folder_result.failed_check_ids)}")
            return 1
        try:
            result = verify_receipt(
                received_bag,
                source_root=supplied_source,
            )
        except (ReceiptCandidateError, RuntimeError) as exc:
            print(f"Receipt input error: {exc}", file=sys.stderr)
            return 2
        if result.status is ReceiptVerificationStatus.VERIFIED:
            print(f"VERIFIED {result.receipt_fingerprint}")
            return 0
        print(f"BLOCKED {' '.join(result.failed_check_ids)}")
        return 1

    if args.command == "restore-receipt":
        received_bag = args.received_bag.expanduser()
        restore_destination = args.restore_destination.expanduser()
        folder_receipt_schema = _folder_receipt_schema(received_bag)
        if _unsupported_folder_receipt_schema(folder_receipt_schema):
            print("RESTORE BLOCKED receipt_schema_invalid", file=sys.stderr)
            return 1
        if folder_receipt_schema == "folder-change-receipt.v2":
            try:
                connected_report = _restore_connected_receipt(
                    received_bag,
                    restore_destination,
                )
            except _FolderRestoreBlocked as exc:
                details = " ".join((exc.code, *exc.failed_check_ids))
                print(f"RESTORE BLOCKED {details}", file=sys.stderr)
                return 1
            print(
                "RESTORED "
                f"{connected_report.receipt_fingerprint} "
                f"{connected_report.destination}"
            )
            return 0
        if _is_folder_receipt(received_bag):
            try:
                folder_report = _restore_folder_receipt(
                    received_bag,
                    restore_destination,
                )
            except FolderReceiptCandidateError as exc:
                print(f"Restore input error: {exc}", file=sys.stderr)
                return 2
            except _FolderRestoreBlocked as exc:
                details = " ".join((exc.code, *exc.failed_check_ids))
                print(f"RESTORE BLOCKED {details}", file=sys.stderr)
                return 1
            print(
                "RESTORED "
                f"{folder_report.receipt_fingerprint} {folder_report.destination}"
            )
            return 0
        try:
            report = restore_receipt(
                received_bag,
                restore_destination,
            )
        except ReceiptCandidateError as exc:
            print(f"Restore input error: {exc}", file=sys.stderr)
            return 2
        except RestoreError as exc:
            print(f"Restore BLOCKED: {exc}", file=sys.stderr)
            return 1
        print(f"RESTORED {report.receipt_fingerprint} {report.destination}")
        return 0

    if args.command == "run":
        return _run_development_folder_app(args)

    mode = RunMode(args.mode)
    selected_environment = os.environ if environ is None else environ
    try:
        output_root = args.output.expanduser().resolve(strict=False)
        source_candidate = args.source.expanduser().resolve(strict=False)
        explicit_case_path = (
            args.case.expanduser().resolve(strict=False)
            if args.case is not None
            else None
        )
        case_path = (
            explicit_case_path
            if explicit_case_path is not None
            else default_case_path(source_candidate, case_directory=CASE_DIRECTORY)
        )
        resuming_existing_case = os.path.lexists(case_path)
        source_root = (
            source_candidate
            if resuming_existing_case
            else args.source.expanduser().resolve(strict=True)
        )
    except OSError as exc:
        print(
            f"Startup blocked: source package cannot be opened: {exc}",
            file=sys.stderr,
        )
        return 2
    uses_hero_source = source_root == HERO_SOURCE_ROOT.resolve()
    replay_record_path = REPLAY_RECORD_PATH if uses_hero_source else None

    replay_record_configured = False
    if (
        mode is RunMode.REPLAY
        and replay_record_path is not None
        and replay_record_path.is_file()
    ):
        try:
            decision_card_provider = RecordedReplayDecisionCardProvider(
                replay_record_path.read_bytes()
            )
        except (OSError, ReplayProviderError) as exc:
            print(f"Replay startup blocked: {exc}", file=sys.stderr)
            return 2
    elif mode is RunMode.REPLAY:
        decision_card_provider = UnavailableReplayDecisionCardProvider()
    else:
        decision_card_provider = None

    api_key_configured = bool(selected_environment.get("OPENAI_API_KEY", "").strip())
    if mode is RunMode.LIVE and not api_key_configured:
        print(
            "Live mode is blocked: configure OPENAI_API_KEY locally, then rerun. "
            "Do not paste the key into chat.",
            file=sys.stderr,
        )
        return 2

    if mode is RunMode.LIVE:
        decision_card_provider = LiveDecisionCardProvider.from_api_key(
            selected_environment["OPENAI_API_KEY"]
        )

    assert decision_card_provider is not None
    try:
        workflow = WorkflowSession(
            source_root=source_root,
            output_root=output_root,
            decision_card_provider=decision_card_provider,
            package_validator=BagItPackageValidator(),
            replay_record_path=replay_record_path,
            budget_ledger_path=(BUDGET_LEDGER_PATH if mode is RunMode.LIVE else None),
            case_path=case_path,
        )
    except (BudgetLedgerError, MigrationCaseError, PackageImportError) as exc:
        print(f"Startup blocked: {exc}", file=sys.stderr)
        return 2
    try:
        durable_replay_record = (
            mode is RunMode.REPLAY
            and workflow.case is not None
            and any(
                record.display_origin is CardDisplayOrigin.RECORDED_REPLAY
                for record in workflow.case.card_records
            )
        )
        if durable_replay_record:
            replay_record_configured = True
        elif (
            mode is RunMode.REPLAY
            and replay_record_path is not None
            and replay_record_path.is_file()
        ):
            try:
                workflow.require_replay_record_compatible()
            except DecisionCardProviderError as exc:
                print(f"Replay startup blocked: {exc}", file=sys.stderr)
                return 2
            replay_record_configured = True
        config = RuntimeConfig.from_environment(
            mode=mode,
            port=args.port,
            environ=selected_environment,
            replay_record_configured=replay_record_configured,
        )

        logging.basicConfig(level=logging.INFO)
        LOGGER.info("Starting Reversible Name Atlas: %s", config.safe_diagnostics())
        print(f"Reversible Name Atlas: http://{LOOPBACK_HOST}:{config.port}")
        print(config.provider_status)
        print(f"Migration Case: {case_path}")
        uvicorn.run(
            create_app(config, workflow),
            host=LOOPBACK_HOST,
            port=config.port,
            log_level="info",
        )
        return 0
    finally:
        workflow.close()


def _is_folder_receipt(candidate: Path) -> bool:
    """Detect the generic receipt schema without initializing runtime services."""

    if _folder_receipt_schema(candidate) in {
        "folder-change-receipt.v1",
        "folder-change-receipt.v2",
    }:
        return True
    try:
        snapshot_bytes = read_folder_artifact_bytes(
            candidate,
            FOLDER_SOURCE_SNAPSHOT_PATH,
        )
        snapshot = strict_folder_json_object(snapshot_bytes)
    except FolderPortableArtifactError:
        return False
    return snapshot.get("schema_version") == "folder-inventory.v1"


def _folder_receipt_schema(candidate: Path) -> str | None:
    """Read only the strict receipt discriminator for early command dispatch."""

    try:
        raw_receipt = read_folder_artifact_bytes(
            candidate,
            FOLDER_CHANGE_RECEIPT_PATH,
        )
        envelope = strict_folder_json_object(raw_receipt)
    except FolderPortableArtifactError:
        return None
    receipt = envelope.get("receipt")
    if not isinstance(receipt, dict):
        return None
    schema_version = receipt.get("schema_version")
    return schema_version if isinstance(schema_version, str) else None


def _unsupported_folder_receipt_schema(schema_version: str | None) -> bool:
    """Reject declared folder-receipt versions outside the closed registry."""

    return (
        schema_version is not None
        and schema_version.startswith("folder-change-receipt.")
        and schema_version
        not in {"folder-change-receipt.v1", "folder-change-receipt.v2"}
    )


def _restore_folder_receipt(result_root: Path, destination: Path) -> object:
    """Call generic reconstruction and retain only its bounded failure surface."""

    from name_atlas.folder_refactor.reconstruction import (
        FolderReconstructionError,
        restore_folder_receipt,
    )

    try:
        return restore_folder_receipt(result_root, destination)
    except FolderReconstructionError as exc:
        raw_code = exc.code
        code = raw_code.value if hasattr(raw_code, "value") else str(raw_code)
        if code not in _FOLDER_RECONSTRUCTION_CODES:
            raise RuntimeError(
                "Generic reconstruction returned an unknown failure code."
            ) from exc
        failed_check_ids = tuple(exc.failed_check_ids)
        raise _FolderRestoreBlocked(code, failed_check_ids) from exc


def _restore_connected_receipt(result_root: Path, destination: Path) -> object:
    """Call v2 reconstruction and retain the bounded folder failure surface."""

    from name_atlas.folder_refactor.connected_change.reconstruction import (
        restore_connected_result,
    )
    from name_atlas.folder_refactor.reconstruction import FolderReconstructionError

    try:
        return restore_connected_result(result_root, destination)
    except FolderReconstructionError as exc:
        raw_code = exc.code
        code = raw_code.value if hasattr(raw_code, "value") else str(raw_code)
        if code not in _FOLDER_RECONSTRUCTION_CODES:
            raise RuntimeError(
                "Connected Change reconstruction returned an unknown failure code."
            ) from exc
        raise _FolderRestoreBlocked(code, tuple(exc.failed_check_ids)) from exc


def _run_development_folder_app(args: argparse.Namespace) -> int:
    """Start the truthful deterministic A2 browser product on loopback."""

    if not 1 <= args.port <= 65_535:
        print("Startup blocked: port must be between 1 and 65535.", file=sys.stderr)
        return 2
    job_path = (
        args.job.expanduser().resolve(strict=False)
        if args.job is not None
        else default_job_path(base_directory=PROJECT_ROOT)
    )
    service = JobBackedFolderRunService(job_path=job_path)
    initial_source: Path | None = None
    initial_output_parent: Path | None = None
    try:
        if not os.path.lexists(job_path):
            initial_source = args.source.expanduser().resolve(strict=True)
            if args.output is None:
                output_candidate = FOLDER_OUTPUT_ROOT.resolve(strict=False)
            else:
                output_candidate = args.output.expanduser().resolve(strict=True)
            _require_folder_state_separation(
                source_root=initial_source,
                output_parent=output_candidate,
                job_path=job_path,
            )
            if args.output is None:
                output_candidate.mkdir(parents=True, exist_ok=True)
                initial_output_parent = output_candidate.resolve(strict=True)
            else:
                initial_output_parent = output_candidate
            if not initial_source.is_dir() or not initial_output_parent.is_dir():
                raise NotADirectoryError(
                    "source and result location must be directories"
                )
        app = create_folder_app(
            service,
            initial_source=initial_source,
            initial_output_parent=initial_output_parent,
            planner_label=PLANNER_LABEL,
        )
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"Startup blocked: folder job cannot be opened: {exc}", file=sys.stderr)
        return 2
    logging.basicConfig(level=logging.INFO)
    LOGGER.info("Starting AI-first A2 Reversible Name Atlas on loopback; no API call.")
    print(f"Reversible Name Atlas: http://{LOOPBACK_HOST}:{args.port}")
    print(PLANNER_LABEL)
    print(f"FolderRefactorJob: {job_path}")
    uvicorn.run(
        app,
        host=LOOPBACK_HOST,
        port=args.port,
        log_level="info",
    )
    return 0


def _require_folder_state_separation(
    *,
    source_root: Path,
    output_parent: Path,
    job_path: Path,
) -> None:
    """Reject source/output/local-state overlap before creating any path."""

    source = source_root.resolve(strict=True)
    output = output_parent.resolve(strict=False)
    job = job_path.resolve(strict=False)
    if _paths_overlap(source, output):
        raise ValueError("source and result location may not contain one another")
    if _paths_overlap(source, job) or _paths_overlap(output, job):
        raise ValueError("folder job state must be outside source and result trees")


def _paths_overlap(left: Path, right: Path) -> bool:
    return left == right or left in right.parents or right in left.parents


def main() -> None:
    """Console-script entry point."""

    raise SystemExit(run())


if __name__ == "__main__":
    main()
