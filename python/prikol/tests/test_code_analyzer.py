import unittest
from pathlib import Path
import tempfile
import json

from python_dz.code_analyzer import analyze_project


class TestCodeAnalyzer(unittest.TestCase):
    def test_analyze_simple(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            # create files
            f1 = root / 'a.py'
            f1.write_text('print(1)\n# comment\n')
            f2 = root / 'b.js'
            f2.write_text('// js file\nconsole.log(1);')

            report = analyze_project(root, exts=['.py', '.js'])

            self.assertIn('.py', report['by_extension'])
            self.assertIn('.js', report['by_extension'])
            self.assertEqual(report['summary']['total_files'], 2)


if __name__ == '__main__':
    unittest.main()
