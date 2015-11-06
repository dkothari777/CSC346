#! /usr/bin/python2.7
import sys
import ConfigParser
import time
from boto.dynamodb2.fields import HashKey, RangeKey, AllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item
from boto.dynamodb2.layer1 import DynamoDBConnection
from connect import getConnection
conn = None

def main(args):
    global conn
    user = ""
    message = ""
    tags = []
    if(len(args[1]) <= 10):
        user = args[1]
    else:
        print "User name %s is longer that 10 characters!" % args[1]
        exit(1)
    inTag = False
    message = args[2]
    tag = ""
    for char in message:
        if char == '#':
            inTag = True
        if char == ' ':
            inTag = False
            if tag != "":
                tags.append(tag)
                tag = ""
        if inTag:
            tag += char
    if tag != "":
        tags.append(tag)
    if(len(message) > 140):
        print "Message is longer than 140 characters!"
        exit(1)
    #conn = getConnection()
    #tables = conn.list_tables()
    #if 'Twitter' not in tables['TableNames']:
    #    createTable()
    #post method goes here
    #post(user, message)
    #scan method goes here after
    #scan()
    print user, message, tags

def post(username, message, tags = ''):
    global conn
    twitterTable = Table('Twitter', connection = conn)
    entry = { 'User': username, 'Message': message}
    twitterTable.put_item(data=entry, overwrite=True)

def createTable():
    print "Creating Table!"
    Table.create('Twitter',
            schema = [HashKey('Time')],
            indexes = [AllIndex('Tweet', parts = [
                HashKey('User'), RangeKey('Message')])],
            connection = conn)
    while True:
        time.sleep(5)
        try:
            conn.describe_table('Twitter')
        except Exception, e:
            print e
        else:
            break

def scan():
    global conn
    twitterTable = Table('Twitter', connection = conn)
    for tweet in twitterTable.scan():
        print
        for (field, val) in tweet.items():
            print "%s: %s" % (field, val)

if __name__ == '__main__':
    main(sys.argv)

