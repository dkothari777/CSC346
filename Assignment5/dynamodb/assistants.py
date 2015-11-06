#!/usr/bin/env python2.7

from boto.dynamodb2.fields import HashKey, RangeKey, AllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item
from boto.dynamodb2.layer1 import DynamoDBConnection
import helpers

employees = helpers.Init()

# Print all Assistant Bottle Washers
assistants = employees.query_2(etype__eq='E', title__eq='Assistant Bottle Washer', reverse=True, index='TitleIndex')
for emp in assistants:
    print
    helpers.PrintItem(emp)
