#!/usr/bin/env python2.7

import boto
from boto.dynamodb2.fields import HashKey, RangeKey, AllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item
from boto.dynamodb2.layer1 import DynamoDBConnection
from pprint import *
import inspect
import ConfigParser
import time

""" 
Initialize the demos by connecting to DynamoDB, creating the 'employees' table if it doesn't
already exist, and return the 'employees' table.
"""

def Init():
    """
    Connect to DynamoDB Local. If you want to connect to the real DynamoDB set the 'local'
    variable below to Fals, but make sure either you have a .boto file or you
    pass both the aws_access_key_id and aws_secret_access_key parameters to the create
    (this code fetches them from settings.cfg).
    """
    local = True

    if local:
        # Connect to local DynamoDB server. Make sure you have that running first.
        conn = DynamoDBConnection(
            host='localhost',
            port=8001,
            aws_secret_access_key='anything',
            is_secure=False)
    else:
        # Connect to the real DynamoDB.
        config = ConfigParser.RawConfigParser()
        config.read("settings.cfg")
        id = config.get('DynamoDB', 'aws_access_key_id')
        key = config.get('DynamoDB', 'aws_secret_access_key')

        conn = boto.dynamodb2.connect_to_region('us-west-2',
            aws_access_key_id = id, aws_secret_access_key = key)

    # Get a list of all tables from DynamoDB.
    tables = conn.list_tables()
    #print "Tables:", tables

    """
    If there isn't an employees table then create it. The table has a primary key of the
    employee type and id, allowing you to query them. It has a secondary index on the 
    employee type and title, allowing you to query them as well.
    """

    if 'employees' not in tables['TableNames']:
        # Create table of employees
        print "Creating new table"
        employees = Table.create('employees',
                                 schema = [HashKey('etype'), RangeKey('id')],
                                 indexes = [AllIndex('TitleIndex', parts = [
                                                HashKey('etype'),
                                                RangeKey('title')])],
                                 connection = conn)
        # Wait for table to be created (DynamoDB has eventual consistency)
        while True:
            time.sleep(5)
            try:
                conn.describe_table('employees')
            except Exception, e:
                print e
            else:
                break

    else:
        # Use the existing table.
        employees = Table('employees', connection=conn)

    return employees


def PrintItem(item):
    for (field, val) in item.items():
        print "%s: %s" % (field, val)
