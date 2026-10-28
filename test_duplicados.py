import tempfile
import unittest
from pathlib import Path
from duplicados import encontrar

class DuplicadosTest(unittest.TestCase):
    def test_conteudo_e_nao_nome_ou_tamanho(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p/'sub').mkdir()
            (p/'a.txt').write_bytes(b'abc')
            (p/'sub'/'copia.bin').write_bytes(b'abc')
            (p/'outro.txt').write_bytes(b'xyz')
            r = encontrar(p)
            self.assertEqual(len(r['grupos']), 1)
            self.assertEqual(r['grupos'][0]['arquivos'], ['a.txt', str(Path('sub')/'copia.bin')])
            self.assertEqual(r['bytes_redundantes'], 3)
            self.assertEqual((p/'a.txt').read_bytes(), b'abc')
            self.assertEqual(len(list(p.rglob('*'))), 4)
    def test_vazios(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            for n in ['a','b']: (p/n).touch()
            r = encontrar(p)
            self.assertEqual(len(r['grupos']), 1)
            self.assertEqual(r['bytes_redundantes'], 0)
    def test_sem_duplicados(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(encontrar(d)['grupos'], [])
    def test_inexistente(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError): encontrar(Path(d)/'ausente')

if __name__ == '__main__': unittest.main()
