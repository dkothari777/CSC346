#!/usr/bin/env python2.7

from boto.dynamodb2.fields import HashKey, RangeKey, AllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item
from boto.dynamodb2.layer1 import DynamoDBConnection
import helpers

employees = helpers.Init()

"""
Fill in the initial employee data. The "overwrite" parameter is True so it will overwrite
any existing employee data.
"""

for data in [{'etype' : 'E', 'first_name' : 'John', 'last_name': 'Doe', 'id' : '123456789',
             'title' : 'Head Bottle Washer', 'hiredate' : 'June 5 1986'}, 
            {'etype' : 'E', 'first_name' : 'Alice', 'last_name': 'Kramden', 'id' : '007',
             'title' : 'Assistant Bottle Washer', 'hiredate' : 'July 1 1950'},
            {'etype' : 'E', 'first_name' : 'Bob', 'last_name': 'Dylan', 'id' : '42',
             'title' : 'Assistant Bottle Washer', 'hiredate' : 'January 1 1970'}]:

    employees.put_item(data=data, overwrite=True)              
