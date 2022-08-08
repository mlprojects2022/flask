import gcsconnect
from DBcode import mongoDB
def preprocess(path):
    id=path[1]
    path=path[0]
    #pageinfo=convert_pdf_to_image_split('Contract/Residential-Lease-Agreement-4/','Contract/Residential-Lease-Agreement-4.pdf')
    pageinfo=gcsconnect.convert_pdf_to_image_split(path.rstrip('.pdf')+'/',path)
    print(gcsconnect.ocr_maker(pageinfo))
    mongoDB.update(id,'Validation1','Ready')
    print('updated')