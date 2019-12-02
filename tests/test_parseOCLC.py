from lxml import etree
import unittest
from unittest.mock import MagicMock, Mock, patch

from lib.parsers.parseOCLC import (
    extractHoldingsLinks,
    _loadURIIdentifier,
    _matchURIIdentifier,
    _matchRegexEbook
)
from lib.dataModel import WorkRecord

class TestOCLCParse(unittest.TestCase):

    @patch('lib.parsers.parseOCLC._loadURIIdentifier')
    @patch('lib.parsers.parseOCLC._matchRegexEbook', return_value=False)
    @patch('lib.parsers.parseOCLC._matchURIIdentifier', return_value=False)
    def test_holdings_extraction(self, mock_load, mock_match, mock_matchURI):
        mock_instance = MagicMock()
        mock_holding = MagicMock()
        mock_holding.ind1 = '4'
        extractHoldingsLinks([mock_holding], mock_instance)
    

    def test_holdings_skip_field(self):
        mock_holding = MagicMock()
        mock_holding.ind1 = '0'
        
        mock_add = MagicMock()
        mock_instance = MagicMock()
        mock_instance.addLink = mock_add
        extractHoldingsLinks([mock_holding], mock_instance)
        mock_add.assert_not_called()
    
    def test_holdings_bad_uri(self):
        mock_holding = MagicMock()
        mock_holding.ind1 = '4'
        mock_holding.subfield.side_effect = IndexError
        mock_add = MagicMock()
        mock_instance = MagicMock()
        mock_instance.addLink = mock_add
        extractHoldingsLinks([mock_holding], mock_instance)
        mock_add.assert_not_called()

    def test_load_identifier(self):
        uriID = _loadURIIdentifier('http://test.org/a1b2c3c4')
        self.assertEqual(uriID, 'a1b2c3c4')
    
    def test_load_identifier_uri(self):
        uriID = _loadURIIdentifier('http://test.org/a1b2c3c4/')
        self.assertEqual(uriID, 'http://test.org/a1b2c3c4/')
    
    def test_match_identifier(self):
        mock_add = MagicMock()
        mock_instance = MagicMock()
        mock_instance.addIdentifier = mock_add
        test_regex = {
            'test': 'test/([0-9]+)$'
        }
        _matchURIIdentifier(
            mock_instance,
            'http://test.org/test/12345',
            test_regex
        )
        mock_add.assert_called_once()
    
    def test_match_identifier_skip(self):
        mock_add = MagicMock()
        mock_instance = MagicMock()
        mock_instance.addIdentifier = mock_add
        test_regex = {
            'test': 'test/([0-9]+)$'
        }
        _matchURIIdentifier(
            mock_instance,
            'http://test.org/other/12345',
            test_regex
        )
        mock_add.assert_not_called()
    
    def test_match_ebook(self):
        mock_add = MagicMock()
        mock_instance = MagicMock()
        mock_instance.addFormat = mock_add
        test_regex = {
            'test': 'test/([0-9]+).epub$'
        }
        _matchRegexEbook(
            mock_instance,
            'http://test.org/test/12345.epub',
            test_regex,
            '12345'
        )
        mock_add.assert_called_once()
    
    def test_match_ebook_skip(self):
        mock_add = MagicMock()
        mock_instance = MagicMock()
        mock_instance.addFormat = mock_add
        test_regex = {
            'test': 'test/([0-9]+).epub$'
        }
        _matchRegexEbook(
            mock_instance,
            'http://test.org/other/12345',
            test_regex,
            '12345'
        )
        mock_add.assert_not_called()
