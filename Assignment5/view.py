import sys
from connect import getConnection
from boto.dynamodb2.fields import HashKey, RangeKey, AllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item
from boto.dynamodb2.layer1 import DynamoDBConnection
conn = None

def main(args):
    global conn
    limit = -1
    if len(args) == 3:
        limit = args[2]
    elif len(args) == 2:
        limit = -1
    else:
        usage()
    key = args[1]
    conn = getConnection()
    try:
        if key[0] == '#':
            searchTagTable(key, int(limit))
        else:
            if key[0] != '@':
                key = '@' + key
            searchUserTable(key, int(limit))
    except ValueError:
        print "No Results Found!"

def searchTagTable(key, limit):
    tagTable =Table('Tags', connection = conn)
    query = tagTable.query_2(Tag__eq=key, reverse=True)
    for item in query:
        printTagQuery(item.items())
        limit = limit - 1
        if limit == 0:
            break

def searchUserTable(key, limit):
    userTable = Table('Users', connection = conn)
    query = userTable.query_2(User__eq=key, reverse = True)
    for item in query:
        printUserQuery(item.items())
        limit -= 1
        if limit == 0:
            break

def printItem(item):
    print item

def printTagQuery(item):
    username = item[2][1]
    username = username[1:]
    time = item[3][1]
    mesg = item[0][1]
    print "%s\t%s\t%s" % (username, time, mesg)

def printUserQuery(item):
    username = item[1][1]
    username = username[1:]
    time = item[2][1]
    mesg = item[0][1]
    print "%s\t%s\t%s" % (username, time, mesg)

def usage():
    print "python view.py 'key' [limit]"
    exit(1)

if __name__ == '__main__':
    main(sys.argv)
