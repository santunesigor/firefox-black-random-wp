from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from testar_nativo import prepare_profile, render_css


class NativeWallpaperTest(unittest.TestCase):
    def test_css_covers_all_images_and_quotes_names(self):
        css = render_css([Path('a.png'), Path('imagem "2".jpg')])
        self.assertIn('random(0, 1, 1)', css)
        self.assertIn('0.00000000% { background-image: url("wallpapers/a.png")', css)
        self.assertIn('50.00000000% { background-image: url("wallpapers/imagem%20%222%22.jpg")', css)
        self.assertNotIn('background-image', render_css([]))
        self.assertIn('random(0, 0, 1)', render_css([Path('a.png')]))

    def test_profile_updates_collection_without_touching_other_files(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            image = root / 'a.png'
            image.write_bytes(b'test image')
            profile = root / 'test-profile'
            prepare_profile(profile, [image])
            self.assertEqual((profile / 'chrome/wallpapers/a.png').read_bytes(), b'test image')
            prefs = profile / 'prefs.js'
            prefs.write_text('// Existing Firefox preferences')
            prepare_profile(profile, [])
            self.assertFalse((profile / 'chrome/wallpapers/a.png').exists())
            self.assertEqual(prefs.read_text(), '// Existing Firefox preferences')
            self.assertEqual(image.read_bytes(), b'test image')


if __name__ == '__main__':
    unittest.main()
