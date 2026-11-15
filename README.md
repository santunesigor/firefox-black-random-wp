# Firefox Black Random Wallpapers

Um wallpaper aleatório a cada nova guia, mantendo **a página original do Firefox**:
pesquisa, clima, atalhos e personalização continuam sendo os do navegador.

Sem extensão, assinatura, conta ou dependências Python extras. As imagens ficam no
seu computador. Funciona também na página inicial `about:home`.

## Requisitos

- Linux com Firefox **158 ou mais recente**. Testado no Ubuntu com Firefox Snap.
- Python 3.
- Git, se for baixar pelo terminal. Você também pode usar **Code → Download ZIP**.

O sorteio usa o recurso experimental [CSS `random()` do Firefox](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Experimental_features#random_css_function),
habilitado pelo script. Atualizações do navegador podem afetar essa personalização.

## 1. Baixar

```bash
git clone https://github.com/santunesigor/firefox-black-random-wp.git
cd firefox-black-random-wp
```

Se baixou o ZIP, extraia e abra o terminal dentro da pasta extraída.

## 2. Experimentar sem alterar seu perfil

```bash
python3 testar_nativo.py
```

Abre uma janela separada do Firefox. Pressione **Ctrl+T** algumas vezes para ver os
fundos sorteados. Seu perfil pessoal não é alterado.

Esse perfil de teste tem suas próprias configurações, então favoritos, extensões,
tema, cidade do clima e mecanismo de pesquisa podem diferir do seu Firefox habitual.
Feche a janela de teste antes de executar o comando novamente.

## 3. Aplicar no seu Firefox habitual

1. No Firefox habitual, abra **`about:support`**.
2. Encontre **Pasta do perfil → Abrir pasta** e copie o caminho dessa pasta.
3. No terminal do projeto, execute o comando abaixo, substituindo o caminho entre aspas:

```bash
python3 aplicar_principal.py "/caminho/da/pasta/do/perfil"
```

4. **Feche e abra novamente o Firefox.**

Pronto. O script copia os wallpapers, instala o CSS e preserva as configurações
existentes. Antes de alterar arquivos, cria um backup em `wallpapers-backups`,
dentro do perfil, e mostra o caminho no terminal. Não precisa de `sudo`.

Se estiver usando uma extensão que substitui a nova guia, desative-a para voltar
à página original. O script não desativa extensões automaticamente.

## Adicionar ou remover imagens

1. Coloque suas imagens na pasta **`wallpapers/`** ou tire as que não quiser.
2. Execute novamente `aplicar_principal.py` com o mesmo caminho do perfil.
3. Feche e abra o Firefox.

Aceita **PNG, JPG/JPEG, WebP, GIF e AVIF**, diretamente dentro da pasta, sem
subpastas. O script sincroniza as cópias usadas pelo sorteio; os originais da
pasta do projeto não são alterados. Se remover todas, volta ao fundo nativo.

Para atualizar só o teste, feche sua janela e execute `python3 testar_nativo.py`.

**O lápis original continua funcionando**, mas o seletor de wallpapers do Firefox
não gerencia esta coleção. Enquanto o CSS estiver instalado, o sorteio prevalece
sobre a imagem escolhida no seletor nativo.

## O que esperar

- Cada nova guia sorteia um fundo. Uma imagem pode se repetir.
- O fundo fica parado naquela guia; um GIF pode continuar animado.
- A imagem preenche a tela e pode ter as bordas cortadas.
- Pesquisa e clima seguem as configurações e a disponibilidade do próprio Firefox.
- Outros sites não recebem essa personalização.

## Desfazer

1. Feche o Firefox.
2. No `user.js` do perfil, remova o bloco iniciado por
   `// Wallpapers aleatórios na nova guia original.` e suas três linhas `user_pref`.
   Se não fez outras alterações desde a instalação, também pode restaurar o
   `user.js` do **backup anterior à primeira instalação**.
3. Em `chrome/userContent.css`, remova somente esta linha:

   ```css
   @import url("random-wallpapers/random-wallpapers.css");
   ```

4. Abra o Firefox e, em **`about:config`**, restaure os valores anteriores destas
   preferências. Se não as personalizava antes, use o botão de redefinir:

   - `toolkit.legacyUserProfileCustomizations.stylesheets`
   - `layout.css.random.enabled`
   - `browser.newtab.preload`

5. Reinicie o Firefox. Depois, pode apagar `chrome/random-wallpapers` do perfil.

O backup de `prefs.js` serve como referência dos valores anteriores. Evite
restaurá-lo inteiro depois de usar o navegador, pois isso perderia ajustes recentes.
Para remover apenas o teste, feche sua janela e apague a pasta `native-test/` do projeto.

## Arquivos e testes

| Arquivo | Para que serve |
| --- | --- |
| `wallpapers/` | Sua coleção de imagens |
| `testar_nativo.py` | Gera o CSS e abre um perfil de teste separado |
| `aplicar_principal.py` | Instala ou atualiza a coleção no perfil escolhido, com backup |
| `test_nativo.py`, `test_principal.py` | Testes do sorteio, instalação e preservação das configurações |

Para rodar os testes, sem abrir o Firefox:

```bash
python3 -m unittest discover -v
```

Os perfis gerados ficam fora do Git. O repositório contém apenas os scripts,
testes, instruções e wallpapers; não contém dados do seu navegador.
