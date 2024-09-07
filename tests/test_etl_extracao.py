import os
import time
import unittest
from unittest.mock import MagicMock, patch

# Importe o módulo que contém suas funções
from etl import extracao


class TestExtracao(unittest.TestCase):
    @patch(
        "builtins.open",
        unittest.mock.mock_open(
            read_data="[Paths]\ndownload_dir=/downloads\ntransformacao_dir=/transformation"
        ),
    )
    def test_carregar_configuracoes(self):
        """Teste para verificar se as configurações são carregadas corretamente."""
        transformacao_dir, download_dir = extracao.carregar_configuracoes()
        self.assertEqual(transformacao_dir, "/transformation")
        self.assertEqual(download_dir, "/downloads")

    @patch("os.path.exists")
    @patch("os.rename")
    def test_espera_download(self, mock_rename, mock_exists):
        """Testa a função espera_download."""
        mock_exists.side_effect = [
            False,
            False,
            True,
        ]  # Simula o arquivo sendo baixado após 3 segundos
        result = extracao.espera_download(
            "01/2024", "RelatorioSaudeProducao.csv", "/downloads"
        )
        self.assertTrue(result)
        mock_rename.assert_called_once_with(
            "/downloads/RelatorioSaudeProducao.csv",
            "/transformation/producao_profissionais_individual_01-2024.csv",
        )

    @patch("os.path.exists", return_value=True)
    @patch("os.remove")
    def test_verifica_arquivo_existe(self, mock_remove, mock_exists):
        """Teste para verificar se o arquivo já foi baixado e removido."""
        result = extracao.verifica_arquivo("RelatorioSaudeProducao.csv")
        self.assertFalse(result)
        mock_remove.assert_called_once_with(
            "/downloads/RelatorioSaudeProducao.csv"
        )

    @patch("extracao.WebDriverWait.until")
    def test_seleciona_xpath(self, mock_wait):
        """Testa a função que seleciona o elemento pelo XPath."""
        driver = MagicMock()
        mock_element = MagicMock()
        mock_wait.return_value = mock_element
        result = extracao.seleciona_xpath(driver, "//*[@id='example']")
        self.assertTrue(result)
        mock_element.click.assert_called_once()

    @patch("extracao.WebDriverWait.until")
    @patch("extracao.time.sleep", return_value=None)
    def test_fazer_download(self, mock_sleep, mock_wait):
        """Testa a função que faz o download e espera pela conclusão."""
        driver = MagicMock()
        mock_element = MagicMock()
        mock_wait.side_effect = [
            mock_element,
            mock_element,
        ]  # Simula o botão sendo encontrado
        result = extracao.fazer_download(
            driver, "01/2024", "RelatorioSaudeProducao.csv"
        )
        self.assertTrue(result)
        mock_element.click.assert_called()

    @patch("extracao.WebDriverWait.until")
    def test_selecionar_primeiro_item(self, mock_wait):
        """Testa a seleção do primeiro item da lista."""
        driver = MagicMock()
        mock_element = MagicMock()
        mock_wait.side_effect = [mock_element, mock_element]
        result = extracao.selecionar_primeiro_item(driver, "//*[@id='botao']")
        self.assertTrue(result)
        mock_element.click.assert_called()


if __name__ == "__main__":
    unittest.main()
