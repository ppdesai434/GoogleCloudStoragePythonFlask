# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging
import os
# [START imports]
from google.cloud import storage
from flask import Flask, render_template, request
import base64
from google.cloud import storage
from google.cloud.storage import Blob
# [END imports]

# [START create_app]
app = Flask(__name__)
key = 'brtJUWneL92g5q0N2gyDSnlPSYAiIy0='
bucket_name = 'your-bucket-name'
pic_bucket = 'your-pics-bucket-name'
other_bucket = 'your-other-bucket-name'
# [END create_app]



@app.route('/')
def index():
    return """<h1>Parth Desai </h1><form method="POST" action="/upload" enctype="multipart/form-data">
    <input type="file" name="file">
    <input type="submit">
	</form>
	"""
	
@app.route('/download', methods=['GET','POST'])
def download():
	file_name = request.form["filename"]
	new_name = request.form['foldername']
	client1 = storage.Client()
	extension = os.path.splitext(filename)[1]
	
	
	if extension == jpg:
		bucket_name = pic_bucket
	bucket1 =  client1.get_bucket(other_bucket)
	blob = bucket1.blob(file_name)
	new_blob = bucket1.rename_blob(blob, new_name)
	#encryption_key1 = base64.b64encode(key).decode('utf-8')
	#blob1 = Blob(file_name, bucket1, encryption_key=key)
	
	#blob1.download_to_filename(file_name)
	#blob1.download_to_filename('/static/downloads/'+file_name)
	return "Rename done"


@app.route('/listfiles',methods=['GET','POST'])
def list_blobs():
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    object_list=[]

    blobs = bucket.list_blobs()

    for blob in blobs:
        print(blob.name)
        object_list.append(blob.name)
        object_list.append("\n")
    str1 = ''.join(object_list)
    return str1
	
	
@app.route('/downloadform')
def downloadform():
    return """
    <h3>Rename a file from the database</h3>
    <form id="download_form" action="/download" method="POST">
    Old File Name: <input type="text" name="filename" placeholder="Enter file name"><br><br>
    New Folder Name: <input type="text" name="foldername" id="foldername"  placeholder = "Enter folder Name" ><br>
     <input type="submit" name="download" value="Download">
   </form>
   <hr>"""	
   
@app.route('/createbucket')
def createbuckets():
	client = storage.Client()
	client.create_bucket(pic_bucket)
	client.create_bucket(other_bucket)
	return "<h1>Parth Desai</h1><br>Buckets Created"
   
   
	
@app.route('/upload', methods=['POST'])
def upload():
    """Process the uploaded file and upload it to Google Cloud Storage."""
    uploaded_file = request.files['file']
    bucket_name = other_bucket
    size = len(uploaded_file.read())
    extension = os.path.splitext(uploaded_file.filename)[1]
    jpg = ".jpg"
    
    
    
#    if size > 2000:
#    	return "Cannot allow file larger than 20 kb"
    
    
    if extension == jpg:
		bucket_name = pic_bucket
		
    client = storage.Client()
    
    bucket =  client.get_bucket(bucket_name)
    
    #encoded_key = base64.b64encode(key).decode('utf-8')
    
    #encryption_key = base64.b64decode(encoded_key)
    blob = Blob(uploaded_file.filename, bucket)
    blob.upload_from_string(uploaded_file.read())
    #blob.make_public()
    
    
    
#    if blob.exists():
#    	return "already exists"
#    else:
#    	return "doesnt exist"
    	
#    blob.upload_from_file(uploaded_file)
#    #Print filesize
#    object_list=[]
#    total_size = 0
#    blobs = bucket.list_blobs()
#    for blob in blobs:
#        object_list.append(blob.name+' '+str(blob.size))
#        object_list.append("<br>")
#        total_size = total_size + blob.size
#    str1 = ''.join(object_list)
    
    
#    return str1 + 'Total Size:' +str(total_size) + '<br>' + 'Time Created' + blob.metadata
    return str(blob.time_created)    
    
@app.route('/delete')
def delete():
    return """
<h4>Delete File</h4>
<form action="deletefile" method="post">
           <div class="form-group">
        <input type="text" name="deletefoldername" id="deletefoldername"  placeholder = "Enter Bucket Name" >
        </div>
           <div class="form-group">
        <input type="text" name="deletefilename" id="deletefilename"  placeholder = "Enter File Name" >
        </div>
        <div class="form-group">
         <button type="submit"  name="delfile" id="delfile" class="btn btn-primary" >Delete File</button>
         </div>
</form>
"""   
@app.route('/deletefile',methods=['GET','POST'])
def deletefile():
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)    #request.form['deletefoldername'])
    blob = bucket.blob(request.form['deletefilename'])
    blob.delete()
    return "File deleted suceesfully"    



@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
