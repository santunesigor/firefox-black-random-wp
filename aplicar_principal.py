"""Instala o fundo aleatório sem substituir a nova guia ou as preferências existentes."""

from datetime import datetime
from pathlib import Path
import shutil
import sys
import tempfile

from testar_nativo import ROOT, render_css

IMPORT = '@import url("random-wallpapers/random-wallpapers.css");'
PREFS = '''// Wallpapers aleatórios na nova guia original.
user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);
user_pref("layout.css.random.enabled", true);
user_pref("browser.newtab.preload", false);
'''


def write_atomic(path, text):
    with tempfile.NamedTemporaryFile('w', dir=path.parent, delete=False, encoding='utf-8') as temporary:
        temporary.write(text)
        source = Path(temporary.name)
    try:
        source.replace(path)
    finally:
        source.unlink(missing_ok=True)


def install(profile, images):
    if not (profile / 'prefs.js').is_file():
        raise ValueError('A pasta indicada não parece ser um perfil existente do Firefox.')
    backup = profile / 'wallpapers-backups' / datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    backup.mkdir(parents=True, mode=0o700)
    for name in ['user.js', 'prefs.js', 'chrome/userContent.css', 'chrome/random-wallpapers/random-wallpapers.css']:
        original = profile / name
        if original.is_file():
            destination = backup / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(original, destination)

    folder = profile / 'chrome/random-wallpapers'
    wallpapers = folder / 'wallpapers'
    wallpapers.mkdir(parents=True, exist_ok=True)
    for image in images:
        shutil.copy2(image, wallpapers / image.name)
    write_atomic(folder / 'random-wallpapers.css', render_css(images))

    css_file = profile / 'chrome/userContent.css'
    css = css_file.read_text(encoding='utf-8') if css_file.exists() else ''
    if IMPORT not in css:
        write_atomic(css_file, IMPORT + '\n' + css)

    user_file = profile / 'user.js'
    user = user_file.read_text(encoding='utf-8') if user_file.exists() else ''
    if not user.endswith(PREFS):
        write_atomic(user_file, user + '\n' + PREFS)
    names = {image.name for image in images}
    for old in wallpapers.iterdir():
        if old.is_file() and old.name not in names:
            old.unlink()
    return backup


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Uso: python3 aplicar_principal.py /caminho/do/perfil')
    try:
        profile = Path(sys.argv[1]).expanduser().resolve()
        images = sorted(image for image in (ROOT / 'wallpapers').iterdir()
                        if image.is_file() and image.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.avif'})
        backup = install(profile, images)
        print(f'Instalado em: {profile}\nImagens: {len(images)}\nBackup: {backup}\nReinicie o Firefox para aplicar.')
    except (OSError, ValueError) as error:
        sys.exit(f'Não foi possível instalar: {error}')
