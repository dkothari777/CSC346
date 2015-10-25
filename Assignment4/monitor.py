from flask import Flask
from ppringt import pprint
import dropbox
import ConfigParser
app = Flask(__name__)
app.config['DEBUG'] = True

cursor = None
changes = []
config = ConfigParser.RawConfigParser()
config.read("settings.cfg")
token = config.get('Dropbox', 'token')
client = dropbox.client.DropboxClient(token)

@app.route("/webhook", methods=['GET'])
def verify():
    '''Respon to the webhook verficaton (GET request) by echoing back the challenge parameter.'''
    return request.args.get('challenge')

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error. """
    return 'Sorry, nothing at this URL', 404

if __name__ == "__main__":
    app.run()
