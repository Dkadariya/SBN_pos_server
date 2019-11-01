import json
import os

# getting current working directory to form the path
cwd = os.getcwd()

# Making the path to the file directory
path=cwd+"/trans_files"

# if path doesnot exist, create the directory to complete the path
if not os.path.exists(path):
    os.mkdir(path)

# function to write the passed json data to file
def commit_file(data):
    # load json from passed raw data. if it is not a valid json, return without commiting to file
    try:
        data=json.loads(data)
    except:
        return "not a valid JSON data"
    # throw an exception if error in writing to file
    try:
        with open(path+"/"+data['Order No']+".json", 'w') as f:
            json.dump(data, f)
    except:
        return "File IO error"
    
    return "write successful"
