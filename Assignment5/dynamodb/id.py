#!/usr/bin/env python2.7

from boto.dynamodb2.fields import HashKey, RangeKey, AllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item
from boto.dynamodb2.layer1 import DynamoDBConnection
import boto.dynamodb2.exceptions
import helpers
import sys

employees = helpers.Init()


"""
Prints the employee with the given id.
Usage: python id.py <employee id>
"""
try:
    emp = employees.get_item(etype='E', id=sys.argv[1])
except boto.dynamodb2.exceptions.ItemNotFound:
    print "No such employee."
else:
    helpers.PrintItem(emp)
