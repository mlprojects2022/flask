import pymongo,os
from pymongo import MongoClient
from urllib.parse import quote_plus
import uuid
from datetime import datetime
print(quote_plus("tcstest"))
def Connection():
    cluster=MongoClient("mongodb+srv://"+quote_plus(os.environ["mongouser"])+":"+quote_plus(os.environ["mongopass"])+"@contract.13hzq.mongodb.net/?retryWrites=true&w=majority")
    db=cluster["contract"]
    collections=db["documents"]
    return collections
def insert(query):
    return Connection().insert_one(query)
# post={"name":"b","upload_date":datetime.now().strftime(("%d/%m/%Y %H:%M:%S")),"queue":"Scan","status":"On Queue","doc_type":"Lease"}
# #res=collections.find_one({"name":"b"})
# res=insert({"name":"b","upload_date":datetime.now().strftime(("%d/%m/%Y %H:%M:%S")),"queue":"Scan","status":"On Queue","doc_type":"Lease"}
# )
def delete(query):
    return Connection().delete_many(query)
#print(delete({"name":"b"}))
# print((res))

