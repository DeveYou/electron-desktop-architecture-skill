"""Offline smoke checks for bundled helper scripts; run: python3 -m unittest discover -s tests."""
from pathlib import Path
import importlib.util
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / f'{name}.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class HelpersTest(unittest.TestCase):
    def test_skill_validation(self):
        self.assertEqual(load('validate_skill').validate(ROOT), [])

    def test_module_generation(self):
        with tempfile.TemporaryDirectory() as td:
            files = load('new_module').generate(Path(td), 'activity-feed', True)
            names = {str(path) for path in files}
            self.assertTrue(any(name.endswith('ActivityFeedPage.tsx') for name in names))
            self.assertTrue(any(name.endswith('shared/contracts/activity-feed.ts') for name in names))
            self.assertTrue(all(path.is_relative_to(Path(td)) for path in files))

    def test_boundary_detection(self):
        with tempfile.TemporaryDirectory() as td:
            file = Path(td) / 'src/renderer/src/unsafe.ts'
            file.parent.mkdir(parents=True)
            file.write_text("import { ipcRenderer } from 'electron'\n", encoding='utf-8')
            findings = load('check_boundaries').scan(Path(td))
            self.assertTrue(any('electron' in item for item in findings))


if __name__ == '__main__':
    unittest.main()
