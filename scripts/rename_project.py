#!/usr/bin/env python3
"""Rename this template from ``ditto`` to your own project.

Run once, immediately after generating a repository from the ditto template::

    python scripts/rename_project.py my_package --owner my-github-user --repo my-repo

The script uses only the standard library, so it runs on any Python >=3.12
interpreter without creating an environment first.

What it does
------------
1. Renames ``src/ditto/`` to ``src/<package>/``.
2. Renames the generated API stubs under ``docs/source/api/generated/``.
3. Rewrites every textual occurrence of the template name, preserving case
   (``ditto`` -> ``my_package``, ``Ditto`` -> ``My_package``, ``DITTO`` ->
   ``MY_PACKAGE``), plus the distribution name and GitHub owner/repo slugs.
4. Resets ``CHANGELOG.md`` and ``NEWS.md`` to an empty ``0.1.0`` entry.
5. Removes itself and ``TEMPLATE.md`` unless ``--keep-template-files`` is given.

Everything is written in one pass at the end, so a failure part-way through
leaves the tree untouched.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

# The template's own identifiers. Change these only if you fork the template
# itself under a different name.
TEMPLATE_PACKAGE = "ditto"
TEMPLATE_OWNER = "nolmacdonald"
TEMPLATE_REPO = "ditto"
TEMPLATE_TITLE = "Development Infrastructure Template Tool for Optimization"

REPO_ROOT = Path(__file__).resolve().parent.parent

# Directories that are never rewritten: VCS metadata, caches, build output and
# the virtual environment.
SKIP_DIRS = {
    ".git",
    ".venv",
    ".ruff_cache",
    ".pytest_cache",
    ".mypy_cache",
    "__pycache__",
    "dist",
    "build",
    "_build",
    "node_modules",
    ".idea",
    ".vscode",
}

# Binary-ish suffixes we never open as text.
SKIP_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".woff", ".woff2"}

# Files removed after a successful rename unless --keep-template-files is set.
TEMPLATE_ONLY_FILES = ("TEMPLATE.md", "scripts/rename_project.py")

# A Python module name: importable, lowercase-with-underscores.
VALID_PACKAGE = re.compile(r"^[a-z][a-z0-9_]*$")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="rename_project.py",
        description="Rename the ditto template to your own project name.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "example:\n"
            "  python scripts/rename_project.py plasma_solver \\\n"
            "      --owner jane-doe --repo plasma-solver \\\n"
            '      --description "Kinetic plasma solver" --author "Jane Doe"'
        ),
    )
    parser.add_argument(
        "package",
        help="Importable package name (lowercase, underscores), e.g. plasma_solver",
    )
    parser.add_argument(
        "--dist-name",
        help="PyPI distribution name. Defaults to the package name with "
        "underscores replaced by hyphens.",
    )
    parser.add_argument("--owner", help="GitHub user or organisation.")
    parser.add_argument(
        "--repo", help="GitHub repository name. Defaults to --dist-name."
    )
    parser.add_argument("--description", help="One-line project description.")
    parser.add_argument("--author", help="Author name for pyproject.toml and the docs.")
    parser.add_argument(
        "--keep-template-files",
        action="store_true",
        help="Keep TEMPLATE.md and this script instead of deleting them.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would change without writing anything.",
    )
    return parser.parse_args(argv)


def iter_text_files(root: Path):
    """Yield every candidate text file below ``root``."""
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        # Skip anything inside an excluded directory.
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path.suffix.lower() in SKIP_SUFFIXES:
            continue
        yield path


def build_replacements(args: argparse.Namespace) -> list[tuple[str, str]]:
    """Build the ordered list of literal (old, new) substitutions.

    Order matters: longer and more specific strings are replaced before the
    bare package name, so that ``nolmacdonald/ditto`` becomes ``owner/repo``
    rather than ``nolmacdonald/new_name``.
    """
    package = args.package
    dist_name = args.dist_name or package.replace("_", "-")
    owner = args.owner or TEMPLATE_OWNER
    repo = args.repo or dist_name

    pairs: list[tuple[str, str]] = [
        # GitHub slugs and Pages URLs first, before the bare name.
        (f"{TEMPLATE_OWNER}.github.io/{TEMPLATE_REPO}", f"{owner}.github.io/{repo}"),
        (f"github.com/{TEMPLATE_OWNER}/{TEMPLATE_REPO}", f"github.com/{owner}/{repo}"),
        (TEMPLATE_OWNER, owner),
    ]
    if args.description:
        pairs.append((TEMPLATE_TITLE, args.description))
    if args.author:
        pairs.append(("Nolan MacDonald", args.author))

    # The distribution name may differ from the module name (hyphens are legal
    # in a PyPI name but not in an import), so the places that name the
    # *distribution* are rewritten before the bare-name rule below.
    #
    # The pyproject/uv.lock rule is anchored to a newline on purpose: an
    # unanchored `name = "ditto"` would also match inside
    # `module-name = "ditto"`, which must keep the importable module name.
    if dist_name != package:
        pairs.extend(
            [
                (f'\nname = "{TEMPLATE_PACKAGE}"', f'\nname = "{dist_name}"'),
                (f"uv add {TEMPLATE_PACKAGE}", f"uv add {dist_name}"),
                (f"uv pip install {TEMPLATE_PACKAGE}", f"uv pip install {dist_name}"),
                (f"pip install {TEMPLATE_PACKAGE}", f"pip install {dist_name}"),
            ]
        )

    # Case-preserving forms of the bare template name.
    pairs.extend(
        [
            (TEMPLATE_PACKAGE.upper(), package.upper()),
            (TEMPLATE_PACKAGE.capitalize(), package.capitalize()),
            (TEMPLATE_PACKAGE, package),
        ]
    )
    return pairs


def apply_replacements(text: str, pairs: list[tuple[str, str]]) -> str:
    """Apply every literal substitution in order."""
    for old, new in pairs:
        text = text.replace(old, new)
    return text


# Punctuation characters reStructuredText accepts as section adornments.
RST_ADORNMENTS = set("=-`:.'\"~^_*+#<>")


def is_adornment(line: str) -> bool:
    """True if ``line`` is a run of a single RST section-adornment character."""
    stripped = line.rstrip()
    return (
        len(stripped) >= 2
        and stripped[0] in RST_ADORNMENTS
        and stripped == stripped[0] * len(stripped)
    )


def fix_rst_underlines(text: str) -> str:
    """Re-length RST section adornments after a title has been renamed.

    A longer package name leaves ``=====`` too short for its title, which
    Sphinx reports as a warning — and CI builds docs with ``-W``. Adornments
    that are already long enough are left alone, so hand-styled over-long
    underlines survive untouched.
    """
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if i == 0 or not is_adornment(line):
            continue
        title = lines[i - 1].rstrip()
        # Skip overlines and transitions: the previous line must be real text.
        if not title or is_adornment(title):
            continue
        if len(line.rstrip()) < len(title):
            lines[i] = line.rstrip()[0] * len(title)
    return "\n".join(lines)


def changelog_stub(dist_name: str, owner: str, repo: str) -> str:
    """Return a fresh CHANGELOG for a project that has not released yet."""
    return f"""# Changelog

All notable changes to {dist_name} will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial project scaffolding generated from the
  [ditto](https://github.com/{TEMPLATE_OWNER}/{TEMPLATE_REPO}) template.

[Unreleased]: https://github.com/{owner}/{repo}/commits/main
"""


def news_stub(dist_name: str) -> str:
    """Return a fresh NEWS file for a project that has not released yet."""
    return f"""# News

No releases yet. The first release of **{dist_name}** will be announced here.
"""


def main(argv: list[str] | None = None) -> int:
    """Entry point. Returns a process exit code."""
    args = parse_args(argv)

    if not VALID_PACKAGE.match(args.package):
        print(
            f"error: '{args.package}' is not a valid package name; use lowercase "
            "letters, digits and underscores, starting with a letter.",
            file=sys.stderr,
        )
        return 2
    if args.package == TEMPLATE_PACKAGE:
        print(
            f"error: the new name is identical to the template name "
            f"('{TEMPLATE_PACKAGE}'); nothing to do.",
            file=sys.stderr,
        )
        return 2

    src_dir = REPO_ROOT / "src" / TEMPLATE_PACKAGE
    if not src_dir.is_dir():
        print(
            f"error: {src_dir} not found. Has this template already been renamed?",
            file=sys.stderr,
        )
        return 1

    dist_name = args.dist_name or args.package.replace("_", "-")
    owner = args.owner or TEMPLATE_OWNER
    repo = args.repo or dist_name
    pairs = build_replacements(args)

    # --- Collect the edits without touching the working tree. --------------
    edits: dict[Path, str] = {}
    for path in iter_text_files(REPO_ROOT):
        try:
            original = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            # Binary file or unreadable; leave it alone.
            continue
        updated = apply_replacements(original, pairs)
        if path.suffix == ".rst":
            updated = fix_rst_underlines(updated)
        if updated != original:
            edits[path] = updated

    # Reset the release history: it belongs to the template, not to the new project.
    edits[REPO_ROOT / "CHANGELOG.md"] = changelog_stub(dist_name, owner, repo)
    edits[REPO_ROOT / "NEWS.md"] = news_stub(dist_name)

    # Directories and files whose *names* contain the template name.
    renames: list[tuple[Path, Path]] = [(src_dir, REPO_ROOT / "src" / args.package)]
    # Autosummary stubs are checked in, so their filenames must track the
    # package name; Sphinx regenerates them on the next build either way.
    generated = REPO_ROOT / "docs" / "source" / "api" / "generated"
    if generated.is_dir():
        for stub in sorted(generated.glob(f"{TEMPLATE_PACKAGE}*.rst")):
            new_name = stub.name.replace(TEMPLATE_PACKAGE, args.package, 1)
            renames.append((stub, stub.with_name(new_name)))

    # Logo assets are referenced by filename from README.md and the docs, and
    # those references have just been rewritten, so the files must follow.
    logos = REPO_ROOT / "docs" / "source" / "_static" / "logo"
    if logos.is_dir():
        for asset in sorted(logos.glob(f"{TEMPLATE_PACKAGE}*")):
            new_name = asset.name.replace(TEMPLATE_PACKAGE, args.package, 1)
            renames.append((asset, asset.with_name(new_name)))

    removals = (
        []
        if args.keep_template_files
        else [REPO_ROOT / name for name in TEMPLATE_ONLY_FILES]
    )

    if args.dry_run:
        print(f"Dry run: {TEMPLATE_PACKAGE} -> {args.package} (dist: {dist_name})")
        print(f"         GitHub: {TEMPLATE_OWNER}/{TEMPLATE_REPO} -> {owner}/{repo}\n")
        for old, new in renames:
            src = old.relative_to(REPO_ROOT)
            dst = new.relative_to(REPO_ROOT)
            print(f"  rename  {src} -> {dst}")
        for path in sorted(edits):
            print(f"  edit    {path.relative_to(REPO_ROOT)}")
        for path in removals:
            if path.exists():
                print(f"  remove  {path.relative_to(REPO_ROOT)}")
        print(f"\n{len(edits)} file(s) would be edited, {len(renames)} renamed.")
        return 0

    # --- Commit the changes. -----------------------------------------------
    for path, content in edits.items():
        path.write_text(content, encoding="utf-8")
    for old, new in renames:
        shutil.move(str(old), str(new))
    for path in removals:
        if path.is_file():
            path.unlink()
    # Drop scripts/ once this script has removed itself and nothing else is left.
    scripts_dir = REPO_ROOT / "scripts"
    if scripts_dir.is_dir() and not any(scripts_dir.iterdir()):
        scripts_dir.rmdir()

    print(f"Renamed {TEMPLATE_PACKAGE} -> {args.package} (distribution: {dist_name}).")
    print(f"Edited {len(edits)} file(s); renamed {len(renames)} path(s).")
    print("\nNext steps:")
    print("  1. Review the diff:            git diff")
    print("  2. Re-lock dependencies:       uv lock")
    print("  3. Verify the environment:     uv sync && uv run pytest")
    print("  4. Replace the logos in        docs/source/_static/logo/")
    print("  5. Update LICENSE copyright and the description in pyproject.toml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
