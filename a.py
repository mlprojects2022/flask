from sched import scheduler
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from DBcode import mongoDB
from multiprocessing import Process,Pipe
from pre_process import preprocess,worker_pre
def pre_pool():
    result=mongoDB.updateReturn({'status':'On Queue'},{'$set':{'status':'In Progress'}})
    if result:
        path='Critical/'+result['name']
        parent,child=Pipe() 
        p=Process(target=preprocess,args={(path,id,parent),})
        p2=Process(target=worker_pre,args={(child,id),})
        p2.start()
        p.start()
        p.join()