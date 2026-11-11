import unittest
from funcao_nome import nome_formatado

class NomesTestCase(unittest.TestCase):
    def test_nome_apelido(self):
        """'Amália Rodrigues' funciona?"""
        formatado = nome_formatado('amália', 'rodrigues')
        self.assertEqual(formatado, 'Amália Rodrigues')

if __name__ == '__main__':
    unittest.main()
