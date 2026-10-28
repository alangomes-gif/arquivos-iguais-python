# Arquivos Iguais

Programa de portfólio para localizar cópias com conteúdo idêntico em uma pasta. Exemplo: duas cópias do mesmo documento com nomes diferentes. Funciona apenas no terminal. Não apaga nem modifica arquivos.

## Executar
Requer Python 3.10 ou superior, sem dependências externas.

```sh
python duplicados.py pasta_exemplo
python -m unittest -v
```

A saída JSON mostra os grupos de arquivos, SHA-256, tamanho e bytes redundantes. O último valor é uma estimativa lógica: não mede espaço real recuperável em disco. Os caminhos listados são relativos à pasta analisada. Erros de leitura aparecem na saída e resultam no código de saída 1.

## Como funciona
Primeiro agrupa por tamanho. Depois lê os candidatos em blocos de 1 MiB e compara seus hashes SHA-256. Links simbólicos são ignorados; diretórios ligados não são percorridos.

## Limites
Não possui interface gráfica, remoção automática ou vigilância em tempo real. Arquivos podem mudar durante a leitura: execute sobre uma pasta estável. Hash igual é evidência prática de igualdade, não comparação byte a byte. Hard links podem aparecer como cópias e o espaço redundante não considera isso. A ferramenta lê os arquivos da pasta indicada; use apenas pastas que você deseja analisar. Os testes usam dados fictícios em diretórios temporários.
