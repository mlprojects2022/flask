import sqlite3
def Connection():
    return sqlite3.connect('tcs_sample.db')
def Create():
    try:
        conn=Connection()
        conn.execute("""
        create table if not exists documents(
            slno varchar(72) primary key,
            name varchar(500) not null,
            upload_date varchar(50),
            queue varchar(20),
            status varchar(20),
            doc_type varchar(100));
            """)
        conn.close()
        return "completed"
    except Exception as e:
        return str(e)

def execute(query):
    try:
        conn=Connection()
        cur=conn.execute("insert into documents (slno,name,doc_type,queue,status,upload_date) values ('12364327-6b2d-45b4-9c3f-1cde136b2159','a.pdf','lease aggrement','Scan','On Queue', '2022-07-26 23:50:36'")
        conn.commit()
        conn.close()
        return cur
    except Exception as e:
        return "insert"+str(e)


