"""Testing for Dropbox API"""

import dropbox
path_to_token = '/Users/Darshan/DropboxAccessToken.txt'
token = ''

with open(path_to_token) as f:
    token = f.read()
print token.strip()
dbx = dropbox.Dropbox(token.strip())

print dbx.users_get_current_account()
