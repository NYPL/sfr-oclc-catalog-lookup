from lxml import etree
import unittest
from unittest.mock import MagicMock, Mock, patch, DEFAULT

from lib.parsers.parseOCLC import extractHoldingsLinks 
from lib.parsers.parse856Holding import HoldingParser
from lib.dataModel import WorkRecord
from helpers.errorHelpers import HoldingError

class TestOCLCParse(unittest.TestCase):
    @patch.multiple(
        HoldingParser,
        parseField=DEFAULT,
        extractBookLinks=DEFAULT
    )
    def test_holdings_extraction(self, parseField, extractBookLinks):
        mock_instance = MagicMock()
        mock_holding = MagicMock()
        extractHoldingsLinks([mock_holding], mock_instance)
        parseField.assert_called_once()
        extractBookLinks.assert_called_once()
    
    @patch.multiple(
        HoldingParser,
        parseField=DEFAULT,
        extractBookLinks=DEFAULT
    )
    def test_holdings_raise_error(self, parseField, extractBookLinks):
        parseField.side_effect = HoldingError('Test Error')
        mock_holding = MagicMock()
        mock_instance = MagicMock()
        extractHoldingsLinks([mock_holding], mock_instance)
        parseField.assert_called_once()
        extractBookLinks.assert_not_called()
    
    '''
    Move all tests below to new file for testing HoldingParser as all of these
    methods have moved to that class
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
    
    @patch('lib.parsers.parseOCLC._checkIAItemStatus', return_value=True)
    def test_match_ia_ebook_skip(self, mockIACheck):
        ia_regex = {
            'internetarchive': r'archive.org\/details\/[a-z0-9]+$',
        }

        outcome = _matchRegexEbook(
            MagicMock(),
            'https://archive.org/details/test00',
            ia_regex,
            1
        )

        self.assertEqual(outcome, None)


    @patch('lib.parsers.parseOCLC.requests')
    def test_check_ia_item_status_restricted(self, mockReq):
        mockResp = MagicMock()
        mockResp.status_code = 200
        mockResp.json.return_value = {
            'metadata': {'access-restricted-item': True}
        }
        mockReq.get.return_value = mockResp
        self.assertTrue(_checkIAItemStatus('https://archive.org/details/test00'))
    
    @patch('lib.parsers.parseOCLC.requests')
    def test_check_ia_item_status_open(self, mockReq):
        mockResp = MagicMock()
        mockResp.status_code = 200
        mockResp.json.return_value = {
            'metadata': {'access-restricted-item': False}
        }
        mockReq.get.return_value = mockResp
        self.assertFalse(_checkIAItemStatus('https://archive.org/details/test00'))
    '''
