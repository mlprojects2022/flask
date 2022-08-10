import multiprocessing
import gcsconnect
import os
from DBcode import mongoDB
from multiprocessing import Process,Pipe    
def preprocess():
    result=mongoDB.updateReturn({'status':'On Queue'},{'status':'In Progress'})
    print(result)
    if result:
        path='Contract/'+result['name']
        parent,child=Pipe() 
        #p=Process(target=preprocess,args={(path,result['_id'],parent),})
        p2=Process(target=worker_pre,args={child,})
        p2.start()
        
        print(path)
        #pageinfo=convert_pdf_to_image_split('Contract/Residential-Lease-Agreement-4/','Contract/Residential-Lease-Agreement-4.pdf')
        import time
        st=time.time()
        p=Process(target=gcsconnect.convert_pdf_to_image_split,args={(path.rstrip('.pdf')+'/',path,parent),})
        p.start()
        p.join()
        print("spliting done")
        #print(pageinfo)
        p2.join()
        print("ocr generation done")
        print("meta clause identification started")
        meta_set=multiprocessing.Manager().dict()
        p3=Process(target=gcsconnect.meta_check,args={(path.rstrip('.pdf')+'/',meta_set),})
        p3.start()
        p3.join()
        print("meta clause identification finished")
        #print(gcsconnect.ocr_maker(pageinfo))
        print(list(list(meta_set.values())[0]))
        mongoDB.update(result['_id'],'Validation1','Ready',list(list(meta_set.values())[0]))
        print("pre process time",time.time()-st)
        #mongoDB.update(id,'Validation1','Ready')
        print('updated')
    else:
        print("all done")
def worker_pre(receiver):
    print('workerpre started')
    while 1:
        msg=receiver.recv()
        print(os.getpid())
        if msg=="END":
            print("end")
            break
        print("received msg : ",msg,os.getpid())
        p2=Process(target=gcsconnect.ocr_maker_1,args={msg,})
        p2.start()