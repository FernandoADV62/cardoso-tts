# Cardoso TTS
Narração neural brasileira para Reels da Cardoso Advocacia Estratégica.

## Gerar a narração
Em **Actions → Gerar narração → Run workflow**, selecione main, cole o roteiro público, escolha a voz, velocidade, idioma e nome sem extensão. Padrões: pf_dora, 1.00, pt-br e narracao. Abra a execução concluída e baixe o pacote em **Artifacts**. O ZIP contém WAV PCM para edição, MP3 para escuta e JSON com duração, tempo de síntese e codificação, pico original e memória máxima do processo Python. O pico é ajustado antes de gravar o WAV.

## Produzir um Reels pelo Work
Envie o link da notícia e o MP4 da animação. O Work consulta a fonte, confere a decisão jurídica e prepara o texto falado. Use apenas texto destinado a publicação no workflow público. Com sessão GitHub autorizada, o Work pode disparar o formulário pelo navegador e consultar o resultado em Actions. A recuperação do artefato depende de acesso autenticado. Se o download estiver indisponível, a mesma geração pode rodar em ambiente Linux isolado no Work. Para um novo vídeo, forneça a animação ou peça sua criação como etapa editorial separada.

Execute `python integrar_video.py animacao.mp4 narracao.wav reels.mp4`. O FFmpeg mapeia apenas as imagens do MP4 e a nova voz, normaliza o volume e ajusta o quadro com margens quando necessário. Se a voz terminar antes, completa com silêncio. Se durar mais, mantém o último quadro. Essa sincronização por duração preserva as cenas e requer revisão editorial quando palavras precisam coincidir com uma cena específica. Saída H.264/AAC em 1080 × 1920, sem música. Confira enquadramento, pronúncia de nomes e siglas e alinhamento das legendas antes da publicação.

## Execução isolada
Use Linux, Python 3.12 e FFmpeg/FFprobe. Crie um venv e instale requirements.txt. Baixe kokoro-v1.0.onnx e voices-v1.0.bin do release model-files-v1.0 para models/ conforme o workflow. Defina TEXT, VOICE, SPEED, LANGUAGE e OUTPUT e rode `python generate_audio.py`. As saídas ficam em output/.

## Fontes e custo
[Kokoro ONNX](https://github.com/thewh1teagle/kokoro-onnx) usa MIT. [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) declara Apache-2.0 e distribui as vozes, incluindo pf_dora. Essas licenças permitem uso comercial sujeito aos seus termos. Preserve os avisos aplicáveis ao redistribuir código e pesos. O workflow baixa os pesos do release oficial. Usa runner Linux padrão público e cache pip, sem chave de API. Artefatos expiram em um dia. [Condições do GitHub Actions](https://docs.github.com/en/billing/concepts/product-billing/github-actions).
