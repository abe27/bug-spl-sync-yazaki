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

print(env_path)

y = Yazaki()
conn = sqlite3.connect(f"data/{os.getenv('DB_LITE_NAME')}.db")


def read():
    cur = conn.cursor()
    cur.execute("""select * from gedi_files where download=0 order by id""")
    obj = cur.fetchall()
    i = 0
    while i < len(obj):
        try:
            __upsert = False
            r = obj[i]
            doc = y.read_batch_file(r[1], r[11], os.path.join(r[13], r[5]))
            if len(doc) > 0:
                __oracon = cx_Oracle.connect(os.getenv("ORA_STR"))
                __oracur = __oracon.cursor()
                if r[1] == "CK":
                    __list_receive = []
                    plantype = doc[0]["plantype"]
                    if plantype == "RECEIVE":
                        __rec_etd = datetime.datetime.strptime(
                            doc[0]["aetodt"], "%d/%m/%Y"
                        )
                        __rec_no = doc[0]["receivingkey"]
                        __rec_tag = doc[0]["tagrp"]
                        __list_receive.append(
                            {
                                "factory": doc[0]["factory"],
                                "receiveno": __rec_no,
                                "receivedte": __rec_etd,
                                "receivepln": len(doc),
                            }
                        )

                        ## check duplicate header
                        rec_check = __oracur.execute(
                            f"select RECEIVINGKEY from TXP_RECTRANSENT where RECEIVINGKEY='{__rec_no}'"
                        )

                        sql_insert_ent = f"""UPDATE TXP_RECTRANSENT SET RECEIVINGMAX='{len(doc)}',RECPLNCTN=0 WHERE RECEIVINGKEY='{__rec_no}'"""
                        if rec_check.fetchone() is None:
                            sql_insert_ent = f"""INSERT INTO TXP_RECTRANSENT(RECEIVINGKEY, RECEIVINGMAX, RECEIVINGDTE, VENDOR, RECSTATUS, RECISSTYPE, RECPLNCTN,RECENDCTN, UPDDTE, SYSDTE)
                            VALUES('{__rec_no}', {len(doc)}, to_date('{str(__rec_etd)[:10]}', 'YYYY-MM-DD'), '{__rec_tag}', 0, '01', 0,0, current_timestamp, current_timestamp)"""

                        ### excute head
                        __oracur.execute(
                            f"""DELETE FROM SKTSYS.TXP_RECTRANSBODY WHERE RECEIVINGKEY='{__rec_no}' AND RECCTN=0"""
                        )
                        __oracur.execute(sql_insert_ent)

                    if plantype == "RECEIVE":
                        sumpln = 0
                        x = 0
                        while x < len(doc):
                            p = doc[x]
                            ### check part
                            __part_sql = __oracur.execute(
                                f"select partno from txp_part where partno='{p['partno']}'"
                            )
                            if __part_sql.fetchone() is None:
                                __oracur.execute(
                                    f"""insert into txp_part (tagrp,partno,partname,upddte,sysdte)values('C','{p['partno']}','{p['partname']}',sysdate,sysdate)"""
                                )

                            else:
                                __oracur.execute(
                                    f"""update txp_part set  partname='{p['partname']}',upddte=sysdate where partno='{p['partno']}'"""
                                )
                            ### create body
                            __recebody = __oracur.execute(
                                f"""SELECT PARTNO from TXP_RECTRANSBODY WHERE RECEIVINGKEY='{p['receivingkey']}' AND PARTNO='{p['partno']}'"""
                            )
                            if __recebody.fetchone() is None:
                                rvno = __oracur.execute(
                                    f"(select 'BD'|| TO_CHAR(sysdate,'yyMMdd') || replace(to_char(emp_TXP__RCMANGENO_CK2.nextval,'00099'),' ','') as genrunno  from dual)"
                                )
                                rvno = rvno.fetchone()
                                __part_desc = str(p["partname"]).replace("'", "''")
                                __oracur.execute(
                                    f"""INSERT INTO TXP_RECTRANSBODY
                                    (RECEIVINGKEY, RECEIVINGSEQ, PARTNO, PLNQTY, PLNCTN,RECQTY,RECCTN,TAGRP, UNIT, CD, WHS, DESCRI, RVMANAGINGNO,UPDDTE, SYSDTE, CREATEDBY,MODIFIEDBY,OLDERKEY)
                                    VALUES('{__rec_no}', '{(x + 1)}', '{p['partno']}', {p['plnqty']}, {p['plnctn']},0,0,'C', '{p['unit']}','20' , '{__rec_tag}','{__part_desc}', '{rvno[0]}',sysdate, sysdate, 'SKTSYS', 'SKTSYS', '{__rec_no}')"""
                                )

                                print(f"{__rec_no} insert partno: {p['partno']}")

                            sumpln = +int(p["plnctn"])
                            __oracur.execute(
                                f"""UPDATE TXP_RECTRANSENT SET RECEIVINGMAX='{len(doc)}',RECPLNCTN={sumpln} WHERE RECEIVINGKEY='{__rec_no}'"""
                            )
                            x += 1

                        ### notifications
                        if len(__list_receive) > 0:
                            x = 0
                            while x < len(__list_receive):
                                _r = __list_receive[x]
                                recbody = __oracur.execute(
                                    f"select sum(PLNCTN) from TXP_RECTRANSBODY where RECEIVINGKEY='{_r['receiveno']}'"
                                )
                                pln = recbody.fetchone()
                                d = datetime.datetime.now()
                                if pln != None:
                                    msg = f"""FACTORY: {_r['factory']}\nRECEIVENO: {_r['receiveno']}\nITEM: {_r['receivepln']} CTN: {pln[0]}\nAT: {d.strftime('%Y-%m-%d %H:%M:%S')}"""
                                    y.line_notification(msg)

                                x += 1
                        __upsert = True

                    else:
                        x = 0
                        while x < len(doc):
                            ord_id = doc[x]["uuid"]
                            factory = doc[x]["factory"]
                            orderid = doc[x]["orderid"]
                            pono = doc[x]["pono"]
                            biac = doc[x]["biac"]
                            shiptype = doc[x]["shiptype"]
                            etdtap = doc[x]["etdtap"]
                            partno = doc[x]["partno"]
                            partname = str(doc[x]["partname"]).replace("'", "''")
                            pc = doc[x]["pc"]
                            commercial = doc[x]["commercial"]
                            sampleflg = doc[x]["sampleflg"]
                            orderorgi = doc[x]["orderorgi"]
                            orderround = doc[x]["orderround"]
                            firmflg = doc[x]["firmflg"]
                            shippedflg = doc[x]["shippedflg"]
                            shippedqty = doc[x]["shippedqty"]
                            ordermonth = doc[x]["ordermonth"]
                            balqty = doc[x]["balqty"]
                            bidrfl = doc[x]["bidrfl"]
                            deleteflg = doc[x]["deleteflg"]
                            ordertype = doc[x]["ordertype"]
                            reasoncd = doc[x]["reasoncd"]
                            carriercode = doc[x]["carriercode"]
                            bioabt = doc[x]["bioabt"]
                            bicomd = doc[x]["bicomd"]
                            bistdp = doc[x]["bistdp"]
                            binewt = doc[x]["binewt"]
                            bigrwt = doc[x]["bigrwt"]
                            bishpc = doc[x]["bishpc"]
                            biivpx = doc[x]["biivpx"]
                            bisafn = doc[x]["bisafn"]
                            biwidt = doc[x]["biwidt"]
                            bihigh = doc[x]["bihigh"]
                            bileng = doc[x]["bileng"]
                            lotno = doc[x]["lotno"]
                            allocateqty = doc[x]["allocateqty"]

                            sql = f"""INSERT INTO TXP_ORDERPLAN(FACTORY, SHIPTYPE, AFFCODE, PONO, ETDTAP, PARTNO, PARTNAME, ORDERMONTH, ORDERORGI, ORDERROUND, BALQTY, SHIPPEDFLG, SHIPPEDQTY, PC, COMMERCIAL, SAMPFLG, CARRIERCODE, ORDERTYPE, UPDDTE, ALLOCATEQTY, BIDRFL, DELETEFLG, REASONCD, BIOABT, FIRMFLG, BICOMD, BISTDP, BINEWT, BIGRWT, BISHPC, BIIVPX, BISAFN, BILENG, BIWIDT, BIHIGH, CURINV, OLDINV, SYSDTE, POUPDFLAG, UUID, CREATEDBY, MODIFIEDBY, LOTNO, ORDERSTATUS, ORDERID, STATUS, ORDSYNC)
                            VALUES('{factory}', '{shiptype}','{biac}', '{str(pono).strip()}', to_date('{str(etdtap)[:10]}', 'YYYY-MM-DD'), '{partno}', '{partname}', to_date('{str(ordermonth)[:10]}', 'YYYY-MM-DD'), '{orderorgi}', '{orderround}', '{balqty}', '{shippedflg}', '{shippedqty}', '{pc}', '{commercial}', '{sampleflg}', '{carriercode}', '{ordertype}', SYSDATE, '{allocateqty}', '{bidrfl}', '{deleteflg}', '{reasoncd}', '{bioabt}', '{firmflg}', '{bicomd}', '{bistdp}', '{binewt}', '{bigrwt}', '{bishpc}', '{biivpx}', '{bisafn}', '{bileng}', '{biwidt}', '{bihigh}', '', '', SYSDATE, '', '{ord_id}', 'SYS', 'SYS', '{lotno}', 0, '{str(orderid).strip()}', 1, 0)"""
                            __oracur.execute(sql)
                            x += 1

                        __upsert = True

                if __upsert:
                    cur.execute(f"update gedi_files set download='1' where id='{r[0]}'")

                ### commit the transaction
                __oracon.commit()
                print(f"{i} ==> update download file {r[5]} set symc := 1")

        except Exception as ex:
            print(f"error => {ex}")
            ### rollback the transaction
            __oracon.rollback()
            cur.execute(f"update gedi_files set download='0' where id='{r[0]}'")
            pass

        finally:
            if __oracur:
                __oracur.close()

            if __oracon:
                __oracon.close()

            pass

        i += 1

    cur.close()
    conn.commit()
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
    main()
    ### after get gedi file
    time.sleep(1)
    read()
    sys.exit(0)
