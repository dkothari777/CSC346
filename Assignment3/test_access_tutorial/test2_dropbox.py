"""Testing for Dropbox API"""
#This tests if I can successfully upload a file to dropbox
#If Success: You will see the file that was uploaded to Dropbox
#Else: Errors or the file wasn't uploaded.
import dropbox
path_to_token = '/Users/Darshan/DropboxAccessToken.txt'
token = ''
with open(path_to_token) as f:
    token = f.read()

dbx = dropbox.Dropbox(token.strip())
def printFilesinDropbox():
    for entry in dbx.files_list_folder('').entries:
        print(entry.name)

print("old")
printFilesinDropbox()
print
dbx.files_upload("Doctor Strange is the best superhero ever!", '/truths_about_superheroes.txt')
print "new"
printFilesinDropbox()
