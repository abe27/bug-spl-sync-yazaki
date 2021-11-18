import pathlib, os, sys, sqlite3
from yazaki.app import Yazaki

from dotenv import load_dotenv

app_path = f"{pathlib.Path().absolute()}"
env_path = f"{app_path}/.env"
load_dotenv(env_path)

y = Yazaki()
conn = sqlite3.connect(f"data/{os.getenv('DB_LITE_NAME')}.db")


def main():
    doc = y.get_gedi()
    if doc != False:
        cur = conn.cursor()
        # Create table
        cur.execute(
            """create table if not exists gedi_files(objtype,mailbox,batchid,size,batchfile,currentdate,flags,formats,orgname,factory,filetype,download,linkfile)"""
        )
        i = 0
        while i < len(doc):
            # Insert a row of data
            cur.execute(
                "INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)"
            )
            i += 1

        # Save (commit) the changes
        conn.commit()
        conn.close()
        return

    print("error load")


if __name__ == "__main__":
    main()
    sys.exit(0)
