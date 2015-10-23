from flask import Flask
from pprint import pprint
import dropbox
import ConfigParser
app = Flask(__name__)
app.config['DEBUG'] = True


# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
cursor = None
changes = []
config = ConfigParser.RawConfigParser()
config.read("settings.cfg")
token = config.get('Dropbox', 'token')
client = dropbox.client.DropboxClient(token)

def getStringFromChanges(changes):
    s = ""
    for fil in changes:
        pprint(fil[1])
        dic = fil[1]
        if("modified" in dic):
            s += dic['client_mtime']+"&#09;"+fil[0] +"&#09; modified <br/>"
        elif("created" in dic):
            s += dic['client_mtime']+"&#09;"+fil[0] +"&#09; created <br/>"
        else:
            s += time.ctime()+"&#09;"+fil[0] +"&#09; deleted <br/>"
    return s

@app.route('/changes.txt')
def getChanges():
    global cursor, changes, client
    while True:
        delta = client.delta(cursor)
        changes += delta['entries']
        cursor = delta['cursor']
        if delta['has_more'] is False:
            break
    if(len(changes) < 20):
         return getStringFromChanges(changes)
    else:
         return getStringFromChanges(changes[len(changes)-20:len(changes)])

@app.route('/<path:name>')
def process(name):
    global client
    f, metadata = client.get_file_and_metadata(name)
    if metadata.isdir():
        return name
    else:
        return f.read()

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
