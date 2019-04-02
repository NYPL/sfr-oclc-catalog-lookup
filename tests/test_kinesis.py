import unittest
from unittest.mock import patch, mock_open, call, MagicMock
from botocore.stub import Stubber
import botocore
import json
import os
os.environ['OUTPUT_REGION'] = 'us-test-1'

from lib.kinesisWrite import KinesisOutput
from helpers.errorHelpers import KinesisError

class TestKinesis(unittest.TestCase):

    @patch.dict('os.environ', {'OUTPUT_KINESIS': 'tester', 'OUTPUT_STAGE': 'test'})
    @patch('lib.kinesisWrite.KinesisOutput._convertToJSON', return_value='testing')
    def test_putRecord(self, mock_convert):
        kinesis = KinesisOutput()
        stubber = Stubber(kinesis.KINESIS_CLIENT)
        expResp = {
            'ShardId': '1',
            'SequenceNumber': '0'
        }

        mock_id = MagicMock()
        mock_id.identifier = 'test'
        mock_data = MagicMock()
        mock_data.test = 'data'
        mock_data.identifiers = [mock_id]
        record = {
            'type': 'work',
            'method': 'update',
            'data': mock_data
        }

        expected_params = {
            'Data': 'testing',
            'StreamName': 'testStream',
            'PartitionKey': 'test'
        }

        stubber.add_response('put_record', expResp, expected_params)
        stubber.activate()

        kinesis.putRecord(record, 'testStream')

    @patch.dict('os.environ', {'OUTPUT_KINESIS': 'tester', 'OUTPUT_STAGE': 'test'})
    @patch('lib.kinesisWrite.KinesisOutput._convertToJSON', return_value='testing')
    def test_putRecord_err(self, mock_convert):
        kinesis = KinesisOutput()
        stubber = Stubber(kinesis.KINESIS_CLIENT)

        mock_id = MagicMock()
        mock_id.identifier = 'test'
        mock_data = MagicMock()
        mock_data.test = 'data'
        mock_data.identifiers = [mock_id]
        record = {
            'type': 'work',
            'method': 'update',
            'data': mock_data
        }

        expected_params = {
            'Data': 'testing',
            'StreamName': 'tester',
            'PartitionKey': '0'
        }

        expected_params = {
            'Data': 'testing',
            'StreamName': 'tester',
            'PartitionKey': '0'
        }

        stubber.add_client_error('put_record', expected_params=expected_params)
        stubber.activate()
        try:
            kinesis.putRecord(record, 'testStream')
        except KinesisError:
            pass
        self.assertRaises(KinesisError)
