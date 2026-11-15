from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from aplicar_principal import IMPORT, PREFS, install


class MainProfileTest(unittest.TestCase):
    def test_install_preserves_and_backs_up_existing_settings(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            profile = root / 'profile'
            (profile / 'chrome').mkdir(parents=True)
            user = 'user_pref("browser.uidensity", 1);\n'
            css = 'body { color: white; }\n'
            (profile / 'user.js').write_text(user)
            (profile / 'prefs.js').write_text('// Firefox settings\n')
            (profile / 'chrome/userContent.css').write_text(css)
            image = root / 'a.png'
            image.write_bytes(b'original image')
            backup = install(profile, [image])
            self.assertEqual((backup / 'user.js').read_text(), user)
            self.assertEqual((backup / 'chrome/userContent.css').read_text(), css)
            self.assertEqual((profile / 'user.js').read_text(), user + '\n' + PREFS)
            self.assertEqual((profile / 'chrome/userContent.css').read_text(), IMPORT + '\n' + css)
            self.assertEqual((profile / 'prefs.js').read_text(), '// Firefox settings\n')
            self.assertEqual((profile / 'chrome/random-wallpapers/wallpapers/a.png').read_bytes(), image.read_bytes())
            install(profile, [])
            self.assertEqual((profile / 'user.js').read_text().count(PREFS), 1)
            self.assertEqual((profile / 'chrome/userContent.css').read_text().count(IMPORT), 1)
            self.assertNotIn('background-image', (profile / 'chrome/random-wallpapers/random-wallpapers.css').read_text())
            self.assertEqual(list((profile / 'chrome/random-wallpapers/wallpapers').iterdir()), [])
            self.assertTrue(image.exists())

    def test_rejects_a_folder_that_is_not_an_existing_profile(self):
        with TemporaryDirectory() as directory:
            profile = Path(directory)
            with self.assertRaises(ValueError):
                install(profile, [])
            self.assertEqual(list(profile.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
