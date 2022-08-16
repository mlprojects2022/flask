import pymongo,os
from pymongo import MongoClient
from urllib.parse import quote_plus
import uuid
import bson.objectid
from datetime import datetime
import json
print(quote_plus("tcstest"))
def my_handler(x):
    if isinstance(x, datetime):
        return x.isoformat()
    elif isinstance(x, bson.objectid.ObjectId):
        return str(x)
    else:
        raise TypeError(x)
def Connection():
    cluster=MongoClient("mongodb+srv://"+quote_plus(os.environ["mongouser"])+":"+quote_plus(os.environ["mongopass"])+"@contract.13hzq.mongodb.net/?retryWrites=true&w=majority")
    db=cluster["contract"]
    collections=db["documents"]
    return collections
def Connection2():
    cluster=MongoClient("mongodb+srv://"+quote_plus(os.environ["mongouser"])+":"+quote_plus(os.environ["mongopass"])+"@contract.13hzq.mongodb.net/?retryWrites=true&w=majority")
    db=cluster["contract"]
    collections=db["metainfo"]
    return collections
def getMetaInfo():
    return json.dumps(list(Connection2().find()),default=my_handler)
def addMetaInfo(query):
    if 'key_clause' in query:
        query['key_clause']=query['key_clause'].split(',')
    return Connection2().insert_one(query)
def editMetaInfo(id,query):
    print(id,query)
    if 'key_clause' in query:
        query['key_clause']=query['key_clause'].split(',')
    return Connection2().update_one({'_id':bson.objectid.ObjectId(id)},{'$set':query})
def insert(query):
    return Connection().insert_one(query)
def updateReturn(filter,data):
    return Connection().find_one_and_update(filter,{'$set':data}) 
# post={"name":"b","upload_date":datetime.now().strftime(("%d/%m/%Y %H:%M:%S")),"queue":"Scan","status":"On Queue","doc_type":"Lease"}
# #res=collections.find_one({"name":"b"})
# res=insert({"name":"b","upload_date":datetime.now().strftime(("%d/%m/%Y %H:%M:%S")),"queue":"Scan","status":"On Queue","doc_type":"Lease"}
# )
def delete_all():
    return Connection2().delete_many({})
def findall_json(date=None):
    if date:
        import bson
        #regx = bson.regex.Regex('/'+date+'/')
        return json.dumps(list(Connection().find({'upload_date':{'$regex':date}})),default=my_handler)
    return json.dumps(list(Connection().find()),default=my_handler)
def update(id,que,metaset):
    return Connection().update_one({'_id':id},{"$set":{'queue':que,'metaclause':metaset}})
def delete(query):
    return Connection().delete_many(query)
#print(delete({"name":"b"}))
# print((res))

