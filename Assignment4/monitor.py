from flask import Flask
from pprint import pprint
from hashlib import sha256
import hmac
import threading
import dropbox
import ConfigParser
app = Flask(__name__)
app.config['DEBUG'] = True

cursor = None
changes = []
config = ConfigParser.RawConfigParser()
config.read("settings.cfg")
token = config.get('Dropbox', 'token')
APP_SECRET = config.get('Dropbox', 'secret')
client = dropbox.client.DropboxClient(token)
@app.route("/webhook", methods=['GET'])
def verify():
    '''Response to the webhook verficaton (GET request) by echoing back the challenge parameter.'''
    return request.args.get('challenge')

@app.route("/webhook", methods=['POST'])
def webhook():
    '''Receive a list of changed user IDs from Dropbox and process each.'''
    signature = request.headers.get('X-Dropbox-Signature')
    if signature != hmac.new(APP_SECRET, request.data, sha256).hexdigest():
        abort(403)

    for d in json.loads(request.data)['delta']:
        #do stuff
        threading.Thread(target=process_delta, args=(d,)).start()
    return

@app.errorhandler(403)
def page_not_found(e):
    """Return a custom 403 error. """
    return 'Sorry, secret does not match signature', 403

if __name__ == "__main__":
    app.run()
