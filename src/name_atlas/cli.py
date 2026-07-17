"""Command-line entry point for the local workbench."""

import argparse
import logging
import os
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path

import uvicorn

from name_atlas.app import create_app
from name_atlas.config import DEFAULT_PORT, LOOPBACK_HOST, RuntimeConfig
from name_atlas.decision_cards import (
    BudgetLedgerError,
    DecisionCardProviderError,
    LiveDecisionCardProvider,
    RecordedReplayDecisionCardProvider,
    ReplayProviderError,
)
from name_atlas.domain import RunMode
from name_atlas.package_import import PackageImportError
from name_atlas.verification import BagItPackageValidator
from name_atlas.workflow import UnavailableReplayDecisionCardProvider, WorkflowSession

LOGGER = logging.getLogger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
HERO_SOURCE_ROOT = PROJECT_ROOT / "sample_data" / "hero"
REPLAY_RECORD_PATH = (
    PROJECT_ROOT / "src" / "name_atlas" / "recordings" / "hero_decision_card.json"
)
OUTPUT_ROOT = PROJECT_ROOT / ".name-atlas" / "stages"
BUDGET_LEDGER_PATH = PROJECT_ROOT / ".name-atlas" / "api_budget.json"


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
    return parser


def run(
    argv: Sequence[str] | None = None,
    *,
    environ: Mapping[str, str] | None = None,
) -> int:
    """Run the CLI and return a process exit code."""

    args = build_parser().parse_args(argv)
    mode = RunMode(args.mode)
    selected_environment = os.environ if environ is None else environ
    source_root = args.source.expanduser().resolve()
    output_root = args.output.expanduser().resolve()
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
            budget_ledger_path=BUDGET_LEDGER_PATH,
        )
    except (BudgetLedgerError, PackageImportError) as exc:
        print(f"Startup blocked: {exc}", file=sys.stderr)
        return 2
    if (
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
    uvicorn.run(
        create_app(config, workflow),
        host=LOOPBACK_HOST,
        port=config.port,
        log_level="info",
    )
    return 0


def main() -> None:
    """Console-script entry point."""

    raise SystemExit(run())


if __name__ == "__main__":
    main()
