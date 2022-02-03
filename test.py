# insert into gedi_files(objtype,mailbox,batchid,size,batchfile,currentdate,flags,formats,orgname,factory,filetype,download,destination,linkfile)
# values('{r.objtype}','{r.mailbox}','{r.batchid}',{r.size},'{r.batchfile}',{timestamp},'{r.flags}','{r.formats}','{r.orgname}','{r.factory}','{r.filetype}',0,'{r.destination}','{r.linkfile}')


# CK|Y32V802|0350381|7050.0|OES.WHAE.32T5.SPL20220202161357.TXT|1643800620|C R|A|Y32TPS1|INJ|RECEIVE|0|exports/RECEIVE/20220202|https://218.225.124.157:9443/cehttp/servlet/MailboxServlet?operation=DOWNLOAD&mailbox_id=Y32V802&batch_num=0350381&data_format=A&batch_id=OES.WHAE.32T5.SPL20220202161357.TXT

import datetime
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

data = [
    {
        "objtype": "CK", 
        "mailbox": "Y32V802", 
        "batchid": "0262431", 
        "size": 13630, 
        "batchfile": "OES.WHAE.32T5.SPL20220202080333.TXT", 
        "currentdate": "Feb 2, 2022 10:07 AM", 
        "flags": "C RT", 
        "formats": "A", 
        "orgname": "Y32TPS1"
    },
    {
        "objtype": "CK", 
        "mailbox": "Y32V802", 
        "batchid": "0340578", 
        "size": 12925, 
        "batchfile": "OES.WHAE.32T4.SPL.20220202080240.TXT", 
        "currentdate": "Feb 2, 2022 10:07 AM", 
        "flags": "C RT", 
        "formats": "A", 
        "orgname": "Y32TPS1"
    },
    {
        "objtype": "CK", 
        "mailbox": "Y32V802", 
        "batchid": "0371246", 
        "size": 11750, 
        "batchfile": "OES.WHAE.32T5.SPL20220202093714.TXT", 
        "currentdate": "Feb 2, 2022 10:07 AM", 
        "flags": "C RT", 
        "formats": "A", 
        "orgname": "Y32TPS1"
    },
    {
        "objtype": "CK", 
        "mailbox": "Y32V802", 
        "batchid": "0298738", 
        "size": 22090, 
        "batchfile": "OES.WHAE.32T4.SPL.20220202090242.TXT", 
        "currentdate": "Feb 2, 2022 10:07 AM", 
        "flags": "C RT", 
        "formats": "A", 
        "orgname": "Y32TPS1"
    },
    {
        "objtype": "CK", 
        "mailbox": "Y32V802", 
        "batchid": "0294561", 
        "size": 11750, 
        "batchfile": "OES.WHAE.32T4.SPL.20220202130259.TXT", 
        "currentdate": "Feb 2, 2022 10:07 AM", 
        "flags": "C RT", 
        "formats": "A", 
        "orgname": "Y32TPS1"
    },
    {
        "objtype": "CK", 
        "mailbox": "Y32V802", 
        "batchid": "0277237", 
        "size": 8930, 
        "batchfile": "OES.WHAE.32T5.SPL20220202135518.TXT", 
        "currentdate": "Feb 2, 2022 10:07 AM", 
        "flags": "C RT", 
        "formats": "A", 
        "orgname": "Y32TPS1"
    },
    {
        "objtype": "CK", 
        "mailbox": "Y32V802", 
        "batchid": "0381173", 
        "size": 6580, 
        "batchfile": "OES.WHAE.32T4.SPL.20220202140245.TXT", 
        "currentdate": "Feb 2, 2022 10:07 AM", 
        "flags": "C RT", 
        "formats": "A", 
        "orgname": "Y32TPS1"
    },
    {
        "objtype": "CK", 
        "mailbox": "Y32V802", 
        "batchid": "0350381", 
        "size": 7050, 
        "batchfile": "OES.WHAE.32T5.SPL20220202161357.TXT", 
        "currentdate": "Feb 2, 2022 10:07 AM", 
        "flags": "C RT", 
        "formats": "A", 
        "orgname": "Y32TPS1"
    },
    {
        "objtype": "CK", 
        "mailbox": "Y32V802", 
        "batchid": "0397605", 
        "size": 106301, 
        "batchfile": "OES.VCBI.32T5.SPL20220202203000.TXT", 
        "currentdate": "Feb 2, 2022 10:07 AM", 
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