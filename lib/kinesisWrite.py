import boto3
import json
import datetime
import os

from helpers.errorHelpers import KinesisError
from helpers.logHelpers import createLog
from helpers.clientHelpers import createAWSClient

logger = createLog('kinesis_write')

class KinesisOutput():
    """Class for managing connections and operations with AWS Kinesis"""
    KINESIS_CLIENT = createAWSClient('kinesis')

    def __init__(self):
        pass

    @classmethod
    def putRecord(cls, outputObject, stream):
        """Put an event into the specific Kinesis stream"""
        logger.info("Writing results to Kinesis")

        # The default lambda function here converts all objects into dicts
        kinesisStream = KinesisOutput._convertToJSON(outputObject)

        partKey = outputObject['data'].identifiers[0].identifier

        try:
            kinesisResp = cls.KINESIS_CLIENT.put_record(
                StreamName=stream,
                Data=kinesisStream,
                PartitionKey=partKey
            )
        except:
            logger.error('Kinesis Write error!')
            raise KinesisError('Failed to write result to output stream!')
    
    @staticmethod
    def _convertToJSON(obj):
        """Converts an object or dict to a JSON string.
        the DEFAULT parameter implements a lambda function to get the values
        from an object using the vars() builtin."""
        return json.dumps(obj, ensure_ascii=False, default=lambda x: vars(x))
