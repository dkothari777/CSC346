#!/usr/bin/env python2.7

from boto.dynamodb2.fields import HashKey, RangeKey, AllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item
from boto.dynamodb2.layer1 import DynamoDBConnection
import helpers

employees = helpers.Init()


"""
Add an additional attribute to John Doe.
"""
emp = employees.get_item(etype='E', id='123456789')
emp['nickname'] = 'Jack'
emp.save()
