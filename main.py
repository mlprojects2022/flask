from datetime import datetime
from distutils.log import debug
import uuid
from flask import Flask,render_template
app=Flask(__name__)
import os
print(os.environ['dbname'])
@app.route('/')
def hello():
    return render_template('upload.html')

if __name__=="__main__":
    try:
        from DBcode import DBconnect
        import uuid,datetime
        print(DBconnect.Create())
        print(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        print(("insert into documents (slno,name,doc_type,queue,status,upload_date) values ('%s','%s','%s','%s','%s', '2022-07-26 23:50:36')")%(str(uuid.uuid4()),"a.pdf","lease aggrement","Scan","On Queue"))
        print(DBconnect.execute("insert into documents (slno,name,doc_type,queue,status,upload_date) values ('12364327-6b2d-45b4-9c3f-1cde136b2159','a.pdf','lease aggrement','Scan','On Queue', '2022-07-26 23:50:36'"))
        print()
    except Exception as e:
        print(str(e))
    app.run(debug=True,host="0.0.0.0",port=5000)
    