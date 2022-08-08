from flask import Flask, render_template, url_for, request, redirect
from werkzeug.utils import secure_filename
import datetime
from datetime import datetime as dt
from DBcode import mongoDB
from flask_cors import CORS,cross_origin
app = Flask(__name__)
cors=CORS(app,resources={r'*':{"origins":"*"}})
import os,io
from multiprocessing import Process
def read_file(filename):
    blob=bucket.blob(filename)
    return blob.download_as_string()
def write_file(filename,content):
    blob=bucket.blob(filename)
    blob.upload_from_string(content)
    return 'completed'
try:
    from google.cloud import storage
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']=os.environ['gcp']
    storage_client = storage.Client()
    bucket_name=os.environ['bucket_name']
    bucket = storage_client.bucket(bucket_name)
except Exception as e:
    print("GCP connection error",str(e))

@app.route("/", methods=["GET","POST","PUT"])
def home():
    if request.method == "POST":
        file = request.files['file_upload']
        #print(type(file).read())
        f=io.BytesIO()
        file.save(f)
        f.seek(0)
        write_file("Contract/"+file.filename,f.read())
        path="Contract/"+file.filename
        print(path)
        print("POST")
        id=mongoDB.insert({"name":secure_filename(file.filename),"upload_date":dt.now().strftime(("%d/%m/%Y %H:%M:%S")),"queue":"Scan","status":"On Queue","doc_type":"Lease Agreement"}).inserted_id
        import pre_process 
        p=Process(target=pre_process.preprocess,args={(path,id),})
        p.start()
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
    app.run(debug = True, port = 5000)
    #print(app.config)