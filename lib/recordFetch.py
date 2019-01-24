import os

from helpers.errorHelpers import OCLCError, DataError
from helpers.logHelpers import createLog
from lib.readers.oclcLookup import lookupRecord
from lib.parsers.parseOCLC import readFromMARC
from lib.kinesisWrite import KinesisOutput

logger = createLog('enhancer')


def fetchData(record):
    """Takes a single input identifier and queries the OCLC Lookup API for
    the corresponding record."""

    try:
        dataBlock = record['data']
        idenType = dataBlock['type']
        identifier = dataBlock['identifier']
    except KeyError as e:
        logger.error('Missing attribute in data block!')
        logger.debug(e)
        logger.debug(record)
        raise DataError('Required attribute missing from data block')
    except TypeError as e:
        logger.error('Could not read data from source')
        logger.debug(e)
        raise DataError('Kinesis data contains non-dictionary value')

    if idenType != 'oclc':
        logger.error('Catalog lookup requires an OCLC identifier')
        raise OCLCError('OCLC Catalog lookup requires an OCLC Number')

    logger.info('Loading MARC for record {}'.format(identifier))

    try:
        marcData = lookupRecord(identifier)

        parsedData = readFromMARC(marcData)

        outputObject = {
            'status': 200,
            'type': 'instance',
            'method': 'update',
            'data': parsedData
        }
        KinesisOutput.putRecord(outputObject, os.environ['OUTPUT_KINESIS'])

    except OCLCError as err:
        logger.error('OCLC Query failed with message: {}'.format(err.message))
        raise err

    return True
