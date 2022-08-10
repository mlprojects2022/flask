print("hello.py",__name__)
from unittest import result
from flask import Flask, render_template, url_for, request, redirect
from werkzeug.utils import secure_filename
import datetime
from pre_process import preprocess
from datetime import datetime as dt
from DBcode import mongoDB
from flask_cors import CORS,cross_origin
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
app = Flask(__name__,static_url_path='', 
            static_folder='app/static')
cors=CORS(app,resources={r'*':{"origins":"*"}})
import os,io
from multiprocessing import Process,Pipe
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
def sched():
    print("Schedular started")
    p=Process(target=preprocess)
    p.start()
    p.join()

#schedular for preprocessing

scheduler = BackgroundScheduler()
scheduler.add_job(sched,trigger="interval",seconds=15,max_instances=1)
print("schedular before start")
scheduler.start()
print("schedular after start")
#print(scheduler.shutdown())
atexit.register(lambda:scheduler.shutdown())
print("scheduler finished")
#scheduler.shutdown()
#atexit.register(lambda:sched())


@app.route("/upload", methods=["GET","POST","PUT"])
def upload():
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
        mongoDB.insert({"name":secure_filename(file.filename),"upload_date":dt.now().strftime(("%d/%m/%Y %H:%M:%S")),"queue":"Scan","status":"On Queue","doc_type":"Lease Agreement"})
        return render_template("home.html",status=1)
    else:
        return render_template('home.html')
    return render_template('home.html')
@app.route('/')
def home():
    return render_template('index3.html')
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

@app.route('/getData')
def getData():
    date=request.values.get('date')
    print("date",date)
    #print(mongoDB.findall_json('1'))
    return mongoDB.findall_json(date)
    
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
print("hello")
if __name__ == "__main__":
    app.run(debug = True, port = 5000)
    #print(app.config)