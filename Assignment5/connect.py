import ConfigParser
from boto.dynamodb2.fields import HashKey, RangeKey, AllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item
from boto.dynamodb2.layer1 import DynamoDBConnection

conn = None
config = None

def getConnection():
    global conn
    if conn == None:
        config = getConfigParser()
        local = config.get('Twitter', 'local')
        if local == 'True':
            conn = createLocalConnection()
        else:
            conn = AmazonConnection()
    return conn

def createLocalConnection():
    return DynamoDBConnection(host='localhost', port=8000, aws_secret_access_key='anything', is_secure=False)

def AmazonConnection():
    conn = getConfigParser()
    access_key = config.get('Twitter', 'aws_access_key_id')
    secret_access = config.get('Twitter', 'aws_secret_access_key')
    region = config.get('Twitter', 'region')
    return boto.dynamodb2.connect_to_region(region, aws_access_key_id=access_key, aws_secret_access_key=secret_access)

def getConfigParser():
    global config
    if config == None:
        config = ConfigParser.RawConfigParser()
        config.read("settings.cfg")
    return config
