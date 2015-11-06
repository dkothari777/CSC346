from google.appengine.api import taskqueue
from flask import Flask
from flask import abort
from flask import json
from hashlib import sha256
from flask import request
import logging
import hmac
import dropbox
import ConfigParser
import boto.sqs
from boto.sqs.message import Message
app = Flask(__name__)
app.config['DEBUG'] = True

config = ConfigParser.RawConfigParser()
config.read("settings.cfg")
token = config.get('Dropbox', 'token')
APP_SECRET = config.get('Dropbox', 'secret')
region = config.get('Amazon', 'region')
queue = config.get('Amazon', 'queue')
client = dropbox.client.DropboxClient(token)
conn = boto.sqs.connect_to_region(region)
q = conn.create_queue(queue, 20)
@app.route("/webhook", methods=['GET'])
def verify():
    '''Response to the webhook verficaton (GET request) by echoing back the challenge parameter.'''
    return request.args.get('challenge')

@app.route("/webhook", methods=['POST'])
def webhook():
    '''Receive a list of changed user IDs from Dropbox and process each.'''
    global client
    logging.debug("Received Notification!")
    signature = request.headers.get('X-Dropbox-Signature')
    if signature != hmac.new(APP_SECRET, request.data, sha256).hexdigest():
        abort(403)
    taskqueue.add(url='/backend', params={'delta': 'hello'})
    return "Checking Dropbox"

@app.errorhandler(403)
def page_not_found(e):
    """Return a custom 403 error. """
    return 'Sorry, secret does not match signature', 403

@app.route('/backend', methods=['POST'])
def processDelta():
    global client
    if request.headers.get('X-AppEngine-QueueName') is None:
        abort(403)
    request.form.get('delta')
    cursorfile = None
    cursor = None
    changes = []
    try:
        cursorfile = client.get_file('/.cursor')
    except:
        cursorfile = None

    if cursorfile != None:
        cursor = cursorfile.read()
        cursorfile.close()
    else:
        cursor = None
    while True:
        delta = client.delta(cursor)
        changes += delta['entries']
        cursor = delta['cursor']
        if changes[0][0] == '/.cursor' and len(changes) <=1:
            changes = None
            break
        if delta['has_more'] is False:
            break
    if changes != None:
        fillst = getFileChanges(changes)
        if fillst is not None:
            for fil in fillst:
                logging.debug("Sending " + str(fil))
                send(str(fil))
            client.put_file('/.cursor', cursor, overwrite = True)
    return ''

def getFileChanges(changes):
    lst = []
    for fil in changes:
        filename = fil[0]
        crud = fil[1]
        if crud is None:
            continue
        if("deleted" not in crud):
            if(filename[-3:] != '.gz' and filename != '/.cursor'):
                lst.append(filename)
    return lst if len(lst) > 0 else None

def send(message):
    global q
    m = Message()
    m.set_body(message)
    q.write(m)

if __name__ == "__main__":
    app.run()
