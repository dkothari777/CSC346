#!/usr/bin/env python2.7

from boto.dynamodb2.fields import HashKey, RangeKey, AllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item
from boto.dynamodb2.layer1 import DynamoDBConnection
import helpers


employees = helpers.Init()

# Use scan to dump all employees
for emp in employees.scan():
    print
    helpers.PrintItem(emp)

