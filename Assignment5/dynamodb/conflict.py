#!/usr/bin/env python2.7

from boto.dynamodb2.fields import HashKey, RangeKey, AllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item
from boto.dynamodb2.layer1 import DynamoDBConnection
import helpers

employees = helpers.Init()


"""
Concurrent update example. Change John's name simultaneously to Jane and Joe. 
Setting it to Joe will fail because of the conflicting change to Jane. If you
don't want this to fail then comment out the emp2.save line.
"""
emp = employees.get_item(etype='E', id='123456789')
emp2 = employees.get_item(etype='E', id='123456789')
emp['first_name'] = 'Jane'
emp.save()

emp2['first_name'] = 'Joe'
print emp2.save()