#! /usr/bin/python2.7
import sys
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
    if len(args) <3:
        print "Wrong Arguments"
        exit(1)
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
    conn = getConnection()
    tables = conn.list_tables()
    if 'Users' not in tables['TableNames']:
        createUserTable()
    if 'Tags' not in tables['TableNames']:
        createTagTable()
    post(user, message, tags)

def post(username, message, tags = []):
    global conn
    usersTable = Table('Users', connection = conn)
    tagsTable = Table('Tags', connection = conn)
    if(username[0] != '@'):
        username = '@' + username
    while(True):
        try:
            tweet_time = time.asctime(time.localtime())
            userEntry = { 'User': username, 'Message': message, 'Time': tweet_time}
            usersTable.put_item(data=userEntry, overwrite=False)
        except:
            time.sleep(1)
        else:
            break
    for t in tags:
        while(True):
            try:
                tweet_time = time.asctime(time.localtime())
                tagEntry = {'User': username, 'Message': message, 'Time': tweet_time, 'Tag': t}
                tagsTable.put_item(data=tagEntry, overwrite=False)
            except:
                time.sleep(1)
            else:
                break

def createUserTable():
    Table.create('Users', schema = [HashKey('User'), RangeKey('Time')],connection = conn)
    while True:
        time.sleep(5)
        try:
            conn.describe_table('Users')
        except Exception, e:
            print e
        else:
            break

def createTagTable():
    Table.create('Tags', schema = [HashKey('Tag'), RangeKey('Time')],connection = conn)
    while True:
        time.sleep(5)
        try:
            conn.describe_table('Tags')
        except Exception, e:
            print e
        else:
            break

def scan():
    global conn
    twitterTable = Table('Twitter', connection = conn)
    for tweet in twitterTable.scan():
        tweet_lst = tweet.items()
        print
        print "%s \t %s \t %s" % (tweet_lst[2][1], tweet_lst[1][1], tweet_lst[0][1])

if __name__ == '__main__':
    main(sys.argv)

