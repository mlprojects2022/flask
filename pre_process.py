import gcsconnect
from DBcode import mongoDB
from multiprocessing import Process
import os
def preprocess(path):
    print(path)
    id=path[1]
    parent=path[2]
    path=path[0]
    #pageinfo=convert_pdf_to_image_split('Contract/Residential-Lease-Agreement-4/','Contract/Residential-Lease-Agreement-4.pdf')
    import time
    st=time.time()
    print(parent)
    pageinfo=gcsconnect.convert_pdf_to_image_split(path.rstrip('.pdf')+'/',path,parent,id)
    print(pageinfo)
    #print(gcsconnect.ocr_maker(pageinfo))
    print("pre process time",time.time()-st)
    #mongoDB.update(id,'Validation1','Ready')
    print('updated')
def worker_pre(receiver):
    print('workerpre started')
    while 1:
        msg=receiver[0].recv()
        print(os.getpid())
        if msg=="END":
            print("end")
            mongoDB.update(receiver[1],'Validation1','Ready')
            break
        print("received msg : ",msg,os.getpid())
        p2=Process(target=gcsconnect.ocr_maker_1,args={msg,})
        p2.start()