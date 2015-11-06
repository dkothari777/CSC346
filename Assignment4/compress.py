import ConfigParser
import dropbox
import gzip
import shutil
import boto.sqs
from pprint import pprint
from boto.sqs.message import Message
config =ConfigParser.RawConfigParser()
config.read("settings.cfg")
token = config.get('Dropbox', 'token')
region = config.get('Amazon', 'region')
queue = config.get('Amazon', 'queue')
client = dropbox.client.DropboxClient(token)
conn = boto.sqs.connect_to_region(region)
q = conn.create_queue(queue, 20)

def getFileFromPath(filename):
	split_path = filename.split('/')
	return split_path[-1]

def compress(filename):
    local_tmp_file = getFileFromPath(filename)
    print "File to compress: " + local_tmp_file
    try:
        f, metadata = client.get_file_and_metadata(filename)
        with gzip.open(local_tmp_file+".gz", "wb") as f_out:
            shutil.copyfileobj(f, f_out)
        with open(local_tmp_file+".gz", 'rb') as f_out:
            client.put_file(filename+".gz", f_out)
    except:
        return False
    return True

while True:
    m = q.read(wait_time_seconds = 4)
    if m is None:
        continue
    else:
       isCompress = compress(m.get_body())
       if(isCompress):
           q.delete_message(m)
       else:
           print "failed to compress " + m.get_body()
           q.delete_message(m)



