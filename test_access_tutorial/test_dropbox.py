"""Testing for Dropbox API"""
#This test if I can get access to dropbox through the token
#If success: then you will print out users information on dropbox
#Else: Get a bunch of Errors
import dropbox
path_to_token = '/Users/Darshan/DropboxAccessToken.txt' #hardcoded path to token
token = ''
with open(path_to_token) as f:
    token = f.read()

dbx = dropbox.Dropbox(token.strip())
print dbx.users_get_current_account()
