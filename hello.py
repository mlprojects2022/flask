from flask import Flask, render_template, url_for, request, redirect
from werkzeug.utils import secure_filename
import datetime
from DBcode import mongoDB
from flask_cors import CORS
app = Flask(__name__)
cors=CORS(app,resources={r"*":{"origins":"*"}})
import os
try:
    from google.cloud import storage
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']=os.environ['gcp']
    storage_client = storage.Client()
    bucket_name=os.environ['bucket_name']
except Exception as e:
    print("GCP connection error",str(e))

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        file = request.files['file_upload']
        #print(type(file).read())
        file.save(f"./upload_files/{secure_filename(file.filename)}")
        print("POST")
        #mongoDB.insert({"name":secure_filename(file.filename),"upload_date":datetime.now().strftime(("%d/%m/%Y %H:%M:%S")),"queue":"Scan","status":"On Queue","doc_type":"Lease"})
        return redirect("/")
    else:
        return render_template('home.html')
    return render_template('home.html')
@app.route('/getSignedurl')
def getSignedurl():
    bucket = storage_client.bucket(bucket_name)
    filename=request.args.get('filename')
    action = request.args.get('action')
    print(filename,action)
    blob=bucket.blob(filename)
    url=blob.generate_signed_url(
        expiration=datetime.timedelta(minutes=2),
        method=action,
        version='v4'
    )
    return url
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == "__main__":
    app.run(debug = True,host= "0.0.0.0", port = 5000)