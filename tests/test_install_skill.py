import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("install_skill", ROOT / "install_skill.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        self.source.mkdir()
        (self.source / "SKILL.md").write_text("first", encoding="utf-8")
        (self.source / "references").mkdir()
        (self.source / "references" / "example.md").write_text("reference", encoding="utf-8")
        self.destination = self.root / "client" / "skills"

    def test_new_install_copies_references(self):
        target, backup = module.install(self.source, self.destination)
        self.assertIsNone(backup)
        self.assertEqual((target / "references" / "example.md").read_text(), "reference")

    def test_existing_install_is_preserved_without_upgrade(self):
        target, _ = module.install(self.source, self.destination)
        (target / "SKILL.md").write_text("custom")
        with self.assertRaises(FileExistsError):
            module.install(self.source, self.destination)
        self.assertEqual((target / "SKILL.md").read_text(), "custom")

    def test_upgrade_and_restore_keep_both_versions_outside_discovery(self):
        target, _ = module.install(self.source, self.destination)
        (target / "SKILL.md").write_text("custom")
        target, backup = module.install(self.source, self.destination, upgrade=True)
        self.assertNotIn(self.destination, backup.parents)
        self.assertEqual((backup / "SKILL.md").read_text(), "custom")
        target, newer_backup = module.install(backup, self.destination, upgrade=True)
        self.assertEqual((target / "SKILL.md").read_text(), "custom")
        self.assertEqual((newer_backup / "SKILL.md").read_text(), "first")

    def test_invalid_source_does_not_touch_existing_install(self):
        target, _ = module.install(self.source, self.destination)
        with self.assertRaises(ValueError):
            module.install(self.root / "missing", self.destination, upgrade=True)
        self.assertEqual((target / "SKILL.md").read_text(), "first")

    def test_overlapping_paths_are_rejected(self):
        with self.assertRaises(ValueError):
            module.install(self.source, self.source / "nested", upgrade=True)

    def test_failed_final_move_restores_old_install(self):
        target, _ = module.install(self.source, self.destination)
        (target / "SKILL.md").write_text("custom")
        original_rename = Path.rename

        def fail_staged_move(path, new_path):
            if path.parent.name.startswith("paper-page-stage-"):
                raise OSError("simulated move failure")
            return original_rename(path, new_path)

        with patch.object(Path, "rename", fail_staged_move):
            with self.assertRaises(OSError):
                module.install(self.source, self.destination, upgrade=True)
        self.assertEqual((target / "SKILL.md").read_text(), "custom")


if __name__ == "__main__":
    unittest.main()
