import os,io
from google.cloud import storage
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=os.environ['gcp']
storage_client = storage.Client()
bucket_name=os.environ['bucket_name']
bucket = storage_client.bucket(bucket_name)
from google.cloud import vision
import time
from pdf2image import convert_from_bytes
import io,json

def read_file(filename):
    blob=bucket.blob(filename)
    return blob.download_as_string()
def read_file_io(filename):
    blob=bucket.blob(filename)
    f=io.BytesIO()
    blob.download_to_file(f)
    f.seek(0)
    return f
def write_file_io(filename,content):
    blob=bucket.blob(filename)
    blob.upload_from_file(content)
    return 'completed'
def write_file(filename,content):
    blob=bucket.blob(filename)
    blob.upload_from_string(content)
    return 'completed'
def list_blob_all(prefix=None):
    blobs = storage_client.list_blobs(os.environ['bucket_name'],prefix=prefix)
    for blob in blobs:
        print(blob.name)
def download_to_local(filename,name):
    blob=bucket.blob(filename)
    blob.download_to_filename(name)


def ocr_maker(pageinfo):
    bucket_name=os.environ['bucket_name']
    client = vision.ImageAnnotatorClient()
    print(client)
    st=time.time()
    image = vision.Image()
    for key,value in pageinfo.items():
        image.source.image_uri="gs://"+bucket_name+"/"+value
        print(value)
        #print(image)
        # Performs label detection on the image file
        response = client.text_detection(image=image)
        print(time.time()-st)
        # print(response)
        texts = response.text_annotations
        write_file(value+'_ocr.txt',texts[0].description)
    print('ocr_completed')
    return 'ocr-completed'
def convert_pdf_to_image_split(savepath,filename):
    images = convert_from_bytes(read_file_io(filename).read(),poppler_path='poppler-22.04.0/Library/bin')
    pageinfo=dict()
    for page in range(len(images)):
        try:
            page_byte=io.BytesIO()
            print(page)
            images[page].save(page_byte,"JPEG")
            page_byte.seek(0)
            write_file_io(savepath+filename.split('/')[-1]+f'__{page}.jpg',page_byte)
            pageinfo[page]=savepath+filename.split('/')[-1]+f'__{page}.jpg'
            del page_byte
        except Exception as e:
            print(str(e))
    return pageinfo
#pageinfo=convert_pdf_to_image_split('Contract/Residential-Lease-Agreement-4/','Contract/Residential-Lease-Agreement-4.pdf')