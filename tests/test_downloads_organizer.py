import unittest
from pathlib import Path
import tempfile

from python_dz.downloads_organizer import organize


class TestDownloadsOrganizer(unittest.TestCase):
    def test_organize_creates_folders_and_moves(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            # create sample files
            (root / 'image.jpg').write_text('data')
            (root / 'doc.pdf').write_text('data')
            (root / 'unknown.xyz').write_text('data')

            organize(root)

            self.assertTrue((root / 'Images' / 'image.jpg').exists())
            self.assertTrue((root / 'Documents' / 'doc.pdf').exists())
            self.assertTrue((root / 'Other' / 'unknown.xyz').exists())


if __name__ == '__main__':
    unittest.main()
