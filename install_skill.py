"""Install the self-contained paper-project-page skill with backup upgrades."""
import argparse
import os
from pathlib import Path
import shutil
import tempfile
import uuid

SKILL_NAME = "paper-project-page"


def install(source: Path, destination: Path, *, upgrade: bool = False) -> tuple[Path, Path | None]:
    source = source.expanduser().resolve()
    destination = destination.expanduser().resolve()
    target = destination / SKILL_NAME
    if not (source / "SKILL.md").is_file():
        raise ValueError("Source is not a skill directory: " + str(source))
    if source == target or source in target.parents or target in source.parents:
        raise ValueError("Source and installed skill must be separate directories")
    if target.exists() and not upgrade:
        raise FileExistsError("Skill already exists; use --upgrade to keep a backup: " + str(target))
    if target.exists() and not target.is_dir():
        raise ValueError("Installation target is not a directory: " + str(target))

    destination.mkdir(parents=True, exist_ok=True)
    # Stage outside skill discovery so an interrupted copy is not a second skill.
    with tempfile.TemporaryDirectory(prefix="paper-page-stage-", dir=destination.parent) as stage:
        staged = Path(stage) / SKILL_NAME
        shutil.copytree(source, staged, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git", ".DS_Store"))
        backup = None
        if target.exists():
            backup_root = destination.parent / "skill-backups" / SKILL_NAME
            backup_root.mkdir(parents=True, exist_ok=True)
            backup = backup_root / uuid.uuid4().hex
            target.rename(backup)
        try:
            staged.rename(target)
        except OSError:
            if backup is not None:
                backup.rename(target)
            raise
    return target, backup


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", type=Path, default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skills", help="Parent skills directory")
    parser.add_argument("--upgrade", action="store_true", help="Back up an existing skill before replacing it")
    parser.add_argument("--restore", type=Path, help="Install from a saved backup; preserve the current skill first")
    args = parser.parse_args()
    source = args.restore or Path(__file__).resolve().parent / "skills" / SKILL_NAME
    try:
        target, backup = install(source, args.dest, upgrade=args.upgrade or args.restore is not None)
    except (OSError, ValueError) as exc:
        parser.exit(1, str(exc) + "\n")
    print("Installed skill:", target)
    if backup is not None:
        print("Previous skill backup:", backup)
    print("Use $paper-project-page after your assistant refreshes its skills. No account settings were changed.")


if __name__ == "__main__":
    main()
