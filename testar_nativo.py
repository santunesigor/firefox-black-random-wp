"""Abre a nova guia nativa com wallpapers em um perfil de teste separado."""

from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent


def render_css(images):
    if not images:
        return '/* Coleção vazia: usa o fundo nativo do Firefox. */\n'
    frames = '\n'.join(
        f'    {100 * index / len(images):.8f}% {{ background-image: url("wallpapers/{quote(image.name)}"); }}'
        for index, image in enumerate(images)
    )
    return f'''/* Gerado por testar_nativo.py. Altere a pasta wallpapers do projeto. */
@-moz-document url("about:newtab"), url("about:home") {{
  body {{
    background-position: center !important;
    background-size: cover !important;
    background-repeat: no-repeat !important;
    background-attachment: fixed !important;
    animation: native-wallpaper {len(images)}s steps(1, end) both paused !important;
    animation-delay: calc(-1s * random(0, {len(images) - 1}, 1) - 0.5s) !important;
  }}
  @keyframes native-wallpaper {{
{frames}
    100% {{ background-image: url("wallpapers/{quote(images[-1].name)}"); }}
  }}
}}
'''


def prepare_profile(profile, images):
    chrome = profile / 'chrome'
    destination = chrome / 'wallpapers'
    destination.mkdir(parents=True, exist_ok=True)
    for image in images:
        shutil.copy2(image, destination / image.name)
    for old in destination.iterdir():
        if old.is_file() and old.name not in {image.name for image in images}:
            old.unlink()
    (chrome / 'userContent.css').write_text(render_css(images), encoding='utf-8')
    # shortcut: o sorteio usa CSS experimental no Firefox 158; revisar quando a opção se tornar padrão.
    (profile / 'user.js').write_text('''user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);
user_pref("layout.css.random.enabled", true);
user_pref("browser.newtab.preload", false);
''', encoding='utf-8')


def main():
    firefox = shutil.which('firefox')
    if not firefox:
        sys.exit('Firefox não encontrado. Instale o Firefox para executar este teste.')
    version = subprocess.check_output([firefox, '--version'], text=True)
    match = re.search(r'Firefox (\d+)', version)
    if not match or int(match[1]) < 158:
        sys.exit('Este teste precisa do Firefox 158 ou mais recente (recurso CSS random).')
    profile = ROOT / 'native-test' / 'profile'
    images = sorted(image for image in (ROOT / 'wallpapers').iterdir()
                    if image.is_file() and image.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.avif'})
    prepare_profile(profile, images)
    print(f'Abrindo perfil de teste com {len(images)} imagens. Seu perfil pessoal não será alterado.', flush=True)
    print('Abra várias guias com Ctrl+T. Feche esta janela antes de rodar o teste de novo.', flush=True)
    subprocess.run([firefox, '-no-remote', '-profile', str(profile), 'about:newtab'], check=True)


if __name__ == '__main__':
    try:
        main()
    except (OSError, subprocess.SubprocessError) as error:
        sys.exit(f'Não foi possível abrir o teste: {error}')
