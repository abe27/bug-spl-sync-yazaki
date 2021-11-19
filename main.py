import pathlib
import os
import sys
import sqlite3
import nanoid
import time
import datetime
import cx_Oracle
from yazaki.app import Yazaki

from dotenv import load_dotenv

app_path = f"{pathlib.Path().absolute()}"
env_path = f"{app_path}/.env"
load_dotenv(env_path)

y = Yazaki()
conn = sqlite3.connect(f"data/{os.getenv('DB_LITE_NAME')}.db")


def read():
    cur = conn.cursor()
    cur.execute("""select * from gedi_files where download=0 order by id""")
    obj = cur.fetchall()
    i = 0
    while i < len(obj):
        r = obj[i]
        doc = y.read_batch_file(r[1], r[11], os.path.join(r[13], r[5]))
        if len(doc) > 0:
            print(os.getenv("ORA_STR"))
            __oracon = cx_Oracle.connect(os.getenv("ORA_STR"))
            __oracur = __oracon.cursor()
            if r[1] == "CK":
                plantype = doc[0]["plantype"]
                if plantype == "RECEIVE":
                    ### create header

                    ### create body

                    ### check part

                    print(f"RECEIVE")

                else:
                    print(f"ORDERPLAN")

                print(f"update gedi_files set download='1' where id='{r[0]}'")

            if __oracur:
                __oracur.close()

            if __oracon:
                __oracon.close()

            print(f"{i} ==> update download file {r[5]} set symc := 1")
        i += 1
    conn.close()


def main():
    try:
        cur = conn.cursor()
        # Create table
        cur.execute(
            """create table if not exists gedi_files (
                id	integer primary key autoincrement,
                objtype	text not null,
                mailbox	text not null,
                batchid	text not null unique,
                size	real,
                batchfile	text,
                currentdate	numeric,
                flags	text,
                formats	text,
                orgname	text,
                factory	text,
                filetype	text,
                download	integer,
                destination text,
                linkfile	text)"""
        )
        conn.commit()
        doc = y.get_gedi()
        if doc != False:
            i = 0
            while i < len(doc):
                r = doc[i]
                # Insert a row of data
                id = str(nanoid.generate())
                timestamp = datetime.datetime.timestamp(r.currentdate)
                sql = f"""insert into gedi_files(objtype,mailbox,batchid,size,batchfile,currentdate,flags,formats,orgname,factory,filetype,download,destination,linkfile) 
                values('{r.objtype}','{r.mailbox}','{r.batchid}',{r.size},'{r.batchfile}',{timestamp},'{r.flags}','{r.formats}','{r.orgname}','{r.factory}','{r.filetype}',0,'{r.destination}','{r.linkfile}')"""
                print(f"{id} ==> insert data id: {r.batchid} filename: {r.batchfile}")
                cur.execute(sql)
                i += 1

            # Save (commit) the changes
            conn.commit()
            return

        print("error load")

    except Exception as e:
        print(e)
        conn.close()


if __name__ == "__main__":
    # main()
    ### after get gedi file
    time.sleep(1)
    read()
    sys.exit(0)
