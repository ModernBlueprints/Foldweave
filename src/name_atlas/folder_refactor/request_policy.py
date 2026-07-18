"""Deterministic blockers for requests outside the copy-only folder contract."""

from __future__ import annotations

import re
from dataclasses import dataclass

from name_atlas.folder_refactor.contracts import FolderInventory


@dataclass(frozen=True, slots=True)
class UnsupportedRequest:
    """One stable reason a request cannot enter automatic planning."""

    code: str
    message: str


_RULES = (
    (
        "file_deletion_unsupported",
        re.compile(
            r"\b(?:delete|discard|omit|exclude|drop|purge|eliminate|erase|trash|"
            r"destroy|remove|cull|wipe|prune|throw away)\b"
            r".{0,50}\b(?:file|files|folder|folders|document|documents|photo|"
            r"photos|image|images|draft|drafts|junk|material|items?|versions?)\b|"
            r"\bget rid of\b.{0,50}\b(?:file|files|folder|folders|document|"
            r"documents|photo|photos|image|images|draft|drafts|junk)\b|"
            r"\b(?:remove|eliminate|erase|trash|cull|wipe|prune)\b.{0,20}"
            r"\b(?:old|outdated|obsolete|unused|unwanted|junk)\b.{0,20}"
            r"\b(?:file|files|document|documents|photo|photos|image|images|"
            r"draft|drafts)\b",
        ),
        "Name Atlas keeps every file; deletion or omission is unsupported.",
    ),
    (
        "file_deletion_unsupported",
        re.compile(
            r"\b(?:weed|clear|clean|strip|filter|pare|thin) out\b.{0,60}"
            r"\b(?:obsolete|old|outdated|unused|unwanted|junk|draft|drafts|"
            r"file|files|material|items?)\b|"
            r"\bleave behind\b.{0,40}\b(?:obsolete|old|outdated|unused|"
            r"unwanted|junk|draft|drafts|file|files|material|items?)\b|"
            r"\b(?:take|pull)\b.{0,50}\b(?:draft|drafts|file|files|document|"
            r"documents|material|items?)\b.{0,20}\bout of\b.{0,30}"
            r"\b(?:folder|project|collection)\b|"
            r"\b(?:strip|clear|clean)\b.{0,30}\b(?:folder|project|collection)\b"
            r".{0,15}\bof\b.{0,50}\b(?:draft|drafts|file|files|document|"
            r"documents|material|items?)\b|"
            r"\bpare\b.{0,30}\b(?:folder|project|collection)\b.{0,15}"
            r"\bdown\b|"
            r"\bdispose of\b.{0,50}\b(?:draft|drafts|file|files|document|"
            r"documents|material|items?)\b"
        ),
        "Name Atlas keeps every file; deletion or omission is unsupported.",
    ),
    (
        "deduplication_unsupported",
        re.compile(r"\b(?:deduplicate|dedupe|remove duplicates?)\b"),
        "Name Atlas does not remove or merge duplicate files.",
    ),
    (
        "merge_unsupported",
        re.compile(
            r"\b(?:merge|combine|concatenate|consolidate)\b.{0,30}"
            r"\b(?:file|files|document|documents|photo|photos)\b"
        ),
        "Name Atlas cannot merge source files.",
    ),
    (
        "selection_unsupported",
        re.compile(
            r"\b(?:keep only|only keep|select only|retain only)\b|"
            r"\b(?:set aside|retain|select)\b.{0,20}\bonly\b|"
            r"\bonly\b.{0,20}\b(?:final|approved|best|current)\b.{0,30}"
            r"\b(?:file|files|version|versions|document|documents)\b|"
            r"\b(?:good|best|final) (?:file|files|version|versions) only\b|"
            r"\bkeep\b.{0,30}\b(?:final|best|approved)\b.{0,20}"
            r"\b(?:version|versions|file|files)\b.{0,30}"
            r"\b(?:leave|omit|exclude|discard)\b.{0,20}"
            r"\b(?:rest|others?|everything else)\b"
        ),
        "Name Atlas cannot select a subset; every source file must remain.",
    ),
    (
        "archive_extraction_unsupported",
        re.compile(r"\b(?:extract|unzip|unpack|decompress)\b"),
        "Archive extraction and format conversion are unsupported.",
    ),
    (
        "content_editing_unsupported",
        re.compile(
            r"\b(?:rewrite|edit|summarize|translate)\b.{0,40}"
            r"\b(?:content|contents|body|bodies|text|documents?)\b"
        ),
        "Name Atlas reorganizes paths but does not edit document bodies.",
    ),
    (
        "code_refactor_unsupported",
        re.compile(
            r"\b(?:refactor|rewrite|fix|update)\b.{0,40}"
            r"\b(?:imports?|source code|build system|configuration|database)\b"
        ),
        "Code, import, build-system, configuration, and database refactoring "
        "are unsupported.",
    ),
)


def classify_unsupported_request(
    request: str,
    inventory: FolderInventory,
) -> UnsupportedRequest | None:
    """Return the first stable blocker, or None for a potentially supported request."""

    normalized = " ".join(request.casefold().split())
    normalized_for_rules = _mask_supported_non_destructive_language(normalized)
    for code, pattern, message in _RULES:
        if pattern.search(normalized_for_rules):
            return UnsupportedRequest(code=code, message=message)

    protected_request = _mask_protected_preservation_language(normalized)
    protected_action = re.search(
        r"\b(?:move|rename|relocate|inspect|read|open|organize|restructure)\b",
        protected_request,
    )
    if protected_action is not None:
        if _mentions_present_protected_class(protected_request, inventory):
            return UnsupportedRequest(
                code="protected_member_request_unsupported",
                message=(
                    "The request requires control of protected members that "
                    "must remain fixed and evidence-denied."
                ),
            )
        for source_file in inventory.files:
            if (
                source_file.protected
                and source_file.relative_path.casefold() in protected_request
            ):
                return UnsupportedRequest(
                    code="protected_member_request_unsupported",
                    message=(
                        "The request requires control of a protected member that "
                        "must remain fixed and evidence-denied."
                    ),
                )
    return None


def _mask_supported_non_destructive_language(value: str) -> str:
    """Keep explicit preservation and label-removal wording out of delete rules."""

    masked = re.sub(
        r"\b(?:do not|don't|never)\s+"
        r"(?:delete|remove|discard|omit|exclude|drop|purge|erase|trash)\b",
        "preserve",
        value,
    )
    masked = re.sub(
        r"\bwithout\s+(?:deleting|removing|discarding|omitting|excluding)\b",
        "while preserving",
        masked,
    )
    return re.sub(
        r"\bremove\b(?=.{0,80}\bfrom\b.{0,30}"
        r"\b(?:file names?|filenames?|path names?|paths?)\b)",
        "rename",
        masked,
    )


def _mask_protected_preservation_language(value: str) -> str:
    """Remove clauses that explicitly preserve or avoid protected members."""

    delimiter = r"(?=(?:[;,]|\.(?=\s|$)|\b(?:and|but|then)\b|$))"
    masked = re.sub(
        r"\b(?:do not|don't|never)\s+"
        r"(?:move|rename|relocate|inspect|read|open|organize|restructure)\b"
        rf".*?{delimiter}",
        " preserve ",
        value,
    )
    return re.sub(
        r"\b(?:keep|leave)\b.{0,120}?"
        r"\b(?:where (?:it|they) (?:is|are)|in place|unchanged)\b",
        " preserve ",
        masked,
    )


def _mentions_present_protected_class(
    request: str,
    inventory: FolderInventory,
) -> bool:
    """Match generic protected classes only when that class exists in the source."""

    protected = tuple(item for item in inventory.files if item.protected)
    categories = (
        (
            r"\b(?:hidden|dotfile|dotfiles)\b",
            lambda item: "dot_path" in item.protection_reasons,
        ),
        (
            r"\b(?:secret|secrets|credential|credentials)\b",
            lambda item: any(
                reason in {"sensitive_basename", "sensitive_prefix"}
                for reason in item.protection_reasons
            ),
        ),
        (
            r"\b(?:configuration file|configuration files|config file|config files)\b",
            lambda item: any(
                reason in {"environment_file", "sensitive_basename"}
                for reason in item.protection_reasons
            ),
        ),
        (
            r"\b(?:env file|env files|environment file|environment files)\b",
            lambda item: "environment_file" in item.protection_reasons,
        ),
        (
            r"\b(?:certificate|certificates|private key|private keys|key file|"
            r"key files|ssh key|ssh keys)\b",
            lambda item: (
                "sensitive_suffix" in item.protection_reasons
                or item.relative_path.rsplit("/", 1)[-1].casefold().startswith("id_")
            ),
        ),
        (
            r"\b(?:password database|password databases)\b",
            lambda item: item.relative_path.casefold().endswith(".kdbx"),
        ),
    )
    return any(
        re.search(pattern, request) is not None
        and any(predicate(item) for item in protected)
        for pattern, predicate in categories
    )
