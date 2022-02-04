# insert into gedi_files(objtype,mailbox,batchid,size,batchfile,currentdate,flags,formats,orgname,factory,filetype,download,destination,linkfile)
# values('{r.objtype}','{r.mailbox}','{r.batchid}',{r.size},'{r.batchfile}',{timestamp},'{r.flags}','{r.formats}','{r.orgname}','{r.factory}','{r.filetype}',0,'{r.destination}','{r.linkfile}')


# CK|Y32V802|0350381|7050.0|OES.WHAE.32T5.SPL20220202161357.TXT|1643800620|C R|A|Y32TPS1|INJ|RECEIVE|0|exports/RECEIVE/20220202|https://218.225.124.157:9443/cehttp/servlet/MailboxServlet?operation=DOWNLOAD&mailbox_id=Y32V802&batch_num=0350381&data_format=A&batch_id=OES.WHAE.32T5.SPL20220202161357.TXT

import datetime
from locale import AM_STR
import pathlib
from yazaki.app import ObjectLink
from dotenv import load_dotenv

app_path = f"{pathlib.Path().absolute()}"
env_path = f"{app_path}/.env"
load_dotenv(env_path)

def return_sql(r):
    timestamp = datetime.datetime.timestamp(r.currentdate)
    sql = f"""insert into gedi_files(objtype,mailbox,batchid,size,batchfile,currentdate,flags,formats,orgname,factory,filetype,download,destination,linkfile)
        values('{r.objtype}','{r.mailbox}','{r.batchid}',{r.size},'{r.batchfile}',{timestamp},'{r.flags}','{r.formats}','{r.orgname}','{r.factory}','{r.filetype}',0,'{r.destination}','{r.linkfile}')"""

    return sql

data = [{
        "objtype": "CK", 
        "mailbox": "Y32V802", 
        "batchid": "0286877",
        "size":8930,
        "batchfile": "OES.WHAE.32T4.SPL.20220203080228.TXT",
        "currentdate": "Feb 3, 2022 10:11 AM",
        "flags": "C RT", 
        "formats": "A", 
        "orgname": "Y32TPS1"
    },{
        "objtype": "CK", 
        "mailbox": "Y32V802", 
        "batchid": "0383937",
        "size":13395,
        "batchfile": "OES.WHAE.32T5.SPL20220203081906.TXT",
        "currentdate": "Feb 3, 2022 10:22 AM",
        "flags": "C RT", 
        "formats": "A", 
        "orgname": "Y32TPS1"
    },{
        "objtype": "CK", 
        "mailbox": "Y32V802", 
        "batchid": "0068017",
        "size":13630,
        "batchfile": "OES.WHAE.32T5.SPL20220203092509.TXT",
        "currentdate": "Feb 3, 2022 11:28 AM",
        "flags": "C RT", 
        "formats": "A", 
        "orgname": "Y32TPS1"
    },{
        "objtype": "CK", 
        "mailbox": "Y32V802", 
        "batchid": "0020099",
        "size":11985,
        "batchfile": "OES.WHAE.32T4.SPL.20220203100233.TXT",
        "currentdate": "Feb 3, 2022 12:18 PM",
        "flags": "C RT", 
        "formats": "A", 
        "orgname": "Y32TPS1"
    },{
        "objtype": "CK", 
        "mailbox": "Y32V802", 
        "batchid": "0200631",
        "size":9870,
        "batchfile": "OES.WHAE.32T4.SPL.20220203130242.TXT",
        "currentdate": "Feb 3, 2022 3:05 PM",
        "flags": "C RT", 
        "formats": "A", 
        "orgname": "Y32TPS1"
    },{
        "objtype": "CK", 
        "mailbox": "Y32V802", 
        "batchid": "0299411",
        "size":7050,
        "batchfile": "OES.WHAE.32T5.SPL20220203134518.TXT",
        "currentdate": "Feb 3, 2022 3:48 PM",
        "flags": "C RT", 
        "formats": "A", 
        "orgname": "Y32TPS1"
    },{
        "objtype": "CK", 
        "mailbox": "Y32V802", 
        "batchid": "0105854",
        "size":11515,
        "batchfile": "OES.WHAE.32T4.SPL.20220203140200.TXT",
        "currentdate": "Feb 3, 2022 4:50 PM",
        "flags": "C RT", 
        "formats": "A", 
        "orgname": "Y32TPS1"
    },{
        "objtype": "CK", 
        "mailbox": "Y32V802", 
        "batchid": "0318535",
        "size":6345,
        "batchfile": "OES.WHAE.32T5.SPL20220203155232.TXT",
        "currentdate": "Feb 3, 2022 5:56 PM",
        "flags": "C RT", 
        "formats": "A", 
        "orgname": "Y32TPS1"
    },{
        "objtype": "CK", 
        "mailbox": "Y32V802", 
        "batchid": "0063682",
        "size":83980,
        "batchfile": "OES.VCBI.32T5.SPL20220203203000.TXT",
        "currentdate": "Feb 3, 2022 10:34 PM",
        "flags": "C RT", 
        "formats": "A", 
        "orgname": "Y32TPS1"
    },
{
        "objtype": "CK", 
        "mailbox": "Y32V802",
        "batchid": "0153558",
        "size":32747,
        "batchfile": "OES.VCBI.32T4.SPL20220203203000.TXT",
        "currentdate": "Feb 3, 2022 10:35 PM",
        "flags": "C RT", 
        "formats": "A", 
        "orgname": "Y32TPS1"
    },{
        "objtype": "CK", 
        "mailbox": "Y32V802", 
        "batchid": "0292461",
        "size":6815,
        "batchfile": "OES.WHAE.32T5.SPL20220204080448.TXT",
        "currentdate": "Feb 4, 2022 10:08 AM",
        "flags": "C RT", 
        "formats": "A", 
        "orgname": "Y32TPS1"
    },{
        "objtype": "CK", 
        "mailbox": "Y32V802", 
        "batchid": "0360597",
        "size":14570,
        "batchfile": "OES.WHAE.32T4.SPL.20220204080255.TXT",
        "currentdate": "Feb 4, 2022 10:11 AM",
        "flags": "C RT", 
        "formats": "A", 
        "orgname": "Y32TPS1"
    }
]


f = open('sql.txt', 'w')
for i in data:
    r = ObjectLink(i['objtype'],i['mailbox'],i['batchid'],i['size'],i['batchfile'],i['currentdate'],i['flags'],i['formats'],i['orgname'])
    x = return_sql(r)
    f.write(f'{x};\n')
    
f.close()