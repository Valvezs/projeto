# Preditor de Redes
Artigo técnico que compara Árvore de Decisão, Random Forest e XGBoost num detector de intrusão em redes, usando o conjunto de dados NSL-KDD

Página publicada: https://valvezs.github.io/projeto/ 

## Reprodução
Python 3.11+ recomendado; veja as versões exatas executadas em `dist/results.json` e `requirements.txt`. Crie um ambiente virtual e instale com `pip install -r requirements.txt`.

Baixe KDDTrain+.txt pela página de origem https://www.unb.ca/cic/datasets/nsl.html . Espelho utilizado: https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain%2B.txt . Cite NSL-KDD e Tavallaee et al., 2009. O hash SHA-256 do arquivo executado está nos resultados; confira antes de comparar números. Não incluímos a base no pacote ou repositório.

Na raiz do projeto, execute:
```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python notebooks/experimento.py --data dados/KDDTrain+.txt
python -m http.server 8000 --directory dist
```
No PowerShell, defina as variáveis com `$env:OPENBLAS_NUM_THREADS="1"` e `$env:OMP_NUM_THREADS="1"` e execute o comando Python sem os prefixos. Abra http://localhost:8000 . Requer internet somente para instalar dependências e baixar dados. O site não tem backend, rastreadores nem fontes externas.

## Arquivos
- dist/index.html, style.css, app.js: site acessível e responsivo, diagramas em SVG e HTML.
- dist/results.json: métricas, matrizes, tempos, ambiente e hash.
- notebooks/experimento.py: script executável completo.
- apresentacao.md: roteiro de 5 minutos para distribuir entre todos os integrantes.
- requirements.txt: versões fixadas.

## Observações
Referências analisadas: página NSL-KDD (fonte pública, limitações históricas) e artigo original de Chen/Guestrin (objetivo regularizado e escalabilidade). Decisões: classificação binária; seleção por F1 via CV sem teste; latência individual separada de lote. Não fazer: coleta real ou bloqueio automático.


## Autores e privacidade
Autor: Victor Gabriel Alves — Ciência da Computação, 3º semestre, interesse em Data Center. GitHub: https://github.com/Valvezs . LinkedIn: https://www.linkedin.com/in/victor-gabriel-alves-a60134199/ . Foto fornecida e autorizada para este projeto. Consentimento em 19/10/2026 para publicar nome, foto, mini-bio e perfis, com possibilidade de retirada posterior. Outros integrantes devem enviar dados e autorização antes da inclusão. Contato via Issues quando configurado; sem e-mails, telefones ou endereços pessoais. Sem IPs ou tráfego confidencial.

Código sob licença MIT; texto/diagramas CC BY 4.0. Base sob condições da origem e devida citação. Última revisão: 19/10/2026.
