import unittest
from unittest.mock import patch, mock_open, call

from lib.recordFetch import fetchData
from helpers.errorHelpers import OCLCError, DataError


class TestFetcher(unittest.TestCase):

    @patch.dict('os.environ', {'OUTPUT_KINESIS': 'tester', 'OUTPUT_REGION': 'us-test-1'})
    @patch('lib.recordFetch.readFromMARC')
    @patch('lib.recordFetch.lookupRecord')
    @patch('lib.recordFetch.KinesisOutput.putRecord')
    def test_basic_fetcher(self, mock_parse, mock_lookup, mock_put):
        testRec = {
            'type': 'oclc',
            'identifier': '000000000'
        }

        res = fetchData(testRec)
        self.assertTrue(res)

    def test_basic_enhancer_missing_field(self):
        testRec = {
            'source': 'test',
            'recordID': 1
        }

        try:
            res = fetchData(testRec)
        except DataError:
            pass
        self.assertRaises(DataError)

    def test_enhancer_err(self):
        testRec = {
            'source': 'test',
            'recordID': 1,
            'data': 'some data'
        }

        try:
            res = fetchData(testRec)
        except DataError:
            pass
        self.assertRaises(DataError)

    def test_non_oclc_identifier(self):
        testRec = {
            'type': 'isbn',
            'identifier': '0000000000'
        }

        try:
            res = fetchData(testRec)
        except OCLCError:
            pass
        self.assertRaises(OCLCError)
