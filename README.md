# Preditor de Redes


## Reprodução
Python 3.11+ recomendado; veja as versões exatas executadas em `dist/results.json` e `requirements.txt`. Crie um ambiente virtual e instale com `pip install -r requirements.txt`.

Baixe KDDTrain+.txt pela página de origem https://www.unb.ca/cic/datasets/nsl.html . Espelho utilizado: https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain%2B.txt . Cite NSL-KDD e Tavallaee et al., 2009. O hash SHA-256 do arquivo executado está nos resultados; confira antes de comparar números. Não incluímos a base no pacote ou repositório.

Na raiz do projeto, execute:
```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python notebooks/experimento.py --data dados/KDDTrain+.txt
python -m http.server 8000 --directory dist
```
No PowerShell, defina as variáveis com `$env:OPENBLAS_NUM_THREADS="1"` e `$env:OMP_NUM_THREADS="1"` e execute o comando Python sem os prefixos. Abra http://localhost:8000 . Requer internet somente para instalar dependências e baixar dados. O site não tem backend, rastreadores nem fontes externas.

## Método
126.973 registros de KDDTrain+, 41 atributos. Divisão estratificada 75/25 com semente 42. Não usamos KDDTest+; resultados não representam a divisão oficial. Três folds estratificados exclusivamente no treino; Pipeline ajusta OneHotEncoder para atributos 1, 2, 3 em cada fold. Rótulo e dificuldade excluídos. Dois candidatos por modelo; F1 de ataque determina a configuração. Sem SMOTE, ajuste de limiar ou decisões baseadas no teste. Avaliação final uma única vez por configuração escolhida; repetições de predict servem apenas ao tempo. Configurações e resultados brutos em results.json.

O tempo de ajuste final exclui a busca; search_s inclui CV e o primeiro refit. A medição fit_s é um segundo ajuste idêntico para isolar custo de treino. Inferência inclui transformação: mediana de 30 consultas unitárias e cinco lotes, com aquecimento. Um processo por estimador. Tempos variam por máquina e carga, embora a semente seja fixa. O ambiente e hash constam em results.json; não há promessa de reprodução bit a bit dos tempos.

## Arquivos
- dist/index.html, style.css, app.js: site acessível e responsivo, diagramas em SVG e HTML.
- dist/results.json: métricas, matrizes, tempos, ambiente e hash.
- notebooks/experimento.py: script executável completo.
- apresentacao.md: roteiro de 5 minutos para distribuir entre todos os integrantes.
- requirements.txt: versões fixadas.

## Observações
Referências analisadas: página NSL-KDD (fonte pública, limitações históricas) e artigo original de Chen/Guestrin (objetivo regularizado e escalabilidade). Decisões: classificação binária; seleção por F1 via CV sem teste; latência individual separada de lote. Não fazer: coleta real ou bloqueio automático.

## Publicação no GitHub
Repositório público ainda não criado: falta conexão com a conta do grupo. Crie um repositório vazio e envie este conteúdo. Mantenha o dataset fora do Git. Para GitHub Pages, configure uma GitHub Action que publique `dist/`, ou copie seu conteúdo para a raiz de uma branch `gh-pages`. Não publique `.openai/`, credenciais ou bases. Acrescente o URL real do repositório e o canal de Issues ao site e a este README. Não há Lighthouse executado nem notas inventadas. Inspeção visual em navegador não realizada neste ambiente; validar antes da apresentação.

## Autores e privacidade
Autor: Victor Gabriel Alves — Ciência da Computação, 3º semestre, interesse em Data Center. GitHub: https://github.com/Valvezs . LinkedIn: https://www.linkedin.com/in/victor-gabriel-alves-a60134199/ . Foto fornecida e autorizada para este projeto. Consentimento explícito registrado na conversa de 19/10/2026 para publicar nome, foto, mini-bio e perfis, com possibilidade de retirada posterior. Outros integrantes devem enviar dados e autorização antes da inclusão. Contato via Issues quando configurado; sem e-mails, telefones ou endereços pessoais. Sem IPs ou tráfego confidencial.

Código sob licença MIT; texto/diagramas CC BY 4.0. Base sob condições da origem e devida citação. Última revisão: 19/10/2026.
