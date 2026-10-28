"""Encontra arquivos com conteúdo idêntico sem alterar ou apagar nada."""
import argparse
import hashlib
import json
from pathlib import Path


def encontrar(pasta):
    raiz = Path(pasta)
    if not raiz.is_dir():
        raise ValueError('Informe uma pasta existente.')
    tamanhos = {}
    erros = []
    # Não segue links: mantém a análise dentro da árvore escolhida.
    for atual, dirs, arquivos in __import__('os').walk(raiz, followlinks=False):
        dirs[:] = sorted(d for d in dirs if not (Path(atual) / d).is_symlink())
        for nome in sorted(arquivos):
            p = Path(atual) / nome
            if p.is_symlink() or not p.is_file():
                continue
            try:
                tamanhos.setdefault(p.stat().st_size, []).append(p)
            except OSError as e:
                erros.append({'arquivo': str(p), 'erro': str(e)})
    grupos = []
    for tamanho, caminhos in sorted(tamanhos.items()):
        if len(caminhos) < 2:
            continue
        hashes = {}
        for p in caminhos:
            try:
                h = hashlib.sha256()
                with p.open('rb') as f:
                    for bloco in iter(lambda: f.read(1024 * 1024), b''):
                        h.update(bloco)
                hashes.setdefault(h.hexdigest(), []).append(str(p.relative_to(raiz)))
            except OSError as e:
                erros.append({'arquivo': str(p), 'erro': str(e)})
        for digest, nomes in sorted(hashes.items()):
            if len(nomes) > 1:
                grupos.append({'sha256': digest, 'bytes_por_arquivo': tamanho,
                               'arquivos': sorted(nomes),
                               'bytes_redundantes': tamanho * (len(nomes) - 1)})
    return {'grupos': grupos, 'bytes_redundantes': sum(g['bytes_redundantes'] for g in grupos), 'erros': erros}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pasta')
    args = parser.parse_args()
    try:
        resultado = encontrar(args.pasta)
    except ValueError as e:
        parser.error(str(e))
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 1 if resultado['erros'] else 0

if __name__ == '__main__':
    raise SystemExit(main())
