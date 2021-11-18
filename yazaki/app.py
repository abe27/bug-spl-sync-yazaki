class ObjectLink(object):
    def __init__(
        self,
        objtype,
        mailbox,
        batchid,
        size,
        batchfile,
        currentdate,
        flags,
        formats,
        orgname,
        download=False,
    ):
        import os
        from datetime import datetime

        ordn = None
        bf = 0
        filetype = "RECEIVE"
        factory = "INJ"

        if objtype == "RMW":
            ordn = str(batchfile).strip()
            factory = "RMW"
            filename = ""
            if ordn[:3] == "OES":
                filename = ordn[len("OES.32TE.SPL.") :]
            else:
                filename = ordn[len("NRRIS.32TE.SPL.") :]

            filename = filename[: filename.find(".")].upper()
            if filename == "ISSUELIST":
                filetype = "CONLOT"

            elif filename == "ISSUENO":
                filetype = "KANBAN"

            else:
                filetype = "RECEIVE"

        elif objtype == "CK":
            ordn = str(batchfile[: len("OES.VCBI")]).strip()
            bf = int(str(batchfile[len("OES.VCBI") + 3 :])[1:2].strip())
            filetype = "RECEIVE"
            if ordn == "OES.VCBI":
                filetype = "ORDERPLAN"

            factory = "INJ"
            if bf == 4:
                factory = "AW"

        elif objtype == "J03":
            print("J03")

        elif objtype == "FG":
            print("FG")

        else:
            print("UNKNOW")

        self.objtype = objtype
        self.mailbox = mailbox
        self.batchid = batchid
        self.size = size
        self.batchfile = batchfile
        self.currentdate = datetime.strptime(currentdate, "%b %d, %Y %I:%M %p")
        self.flags = flags
        self.formats = formats
        self.orgname = orgname
        self.factory = factory
        self.filetype = filetype
        self.download = download
        self.linkfile = f"https://{os.getenv('YAZAKI_HOST')}:{os.getenv('YAZAKI_PORT')}/cehttp/servlet/MailboxServlet?operation=DOWNLOAD&mailbox_id={self.mailbox}&batch_num={self.batchid}&data_format=A&batch_id={self.batchfile}"


class Logging:
    def __init__(self, title, content, status):
        import os
        from datetime import datetime

        filename = f'{datetime.now().strftime("%d_%m_%Y")}.log'
        pathname = os.path.join(os.getenv("LOG_DIR"), filename)

        ## check folder log file if exit
        if (os.path.exists(os.getenv("LOG_DIR"))) is False:
            os.mkdir(os.getenv("LOG_DIR"))

        l = 1
        if os.path.exists(pathname):
            lines = open(pathname, mode="r")
            l = len(lines.readlines()) + 1

        f = open(pathname, mode="a+")
        f.writelines(
            f"{str(l).ljust(10)[:6]}   {(str(title).ljust(10))[:8]}{(str(content).ljust(20))[:15]}{str(status).ljust(150)[:100]}{str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')).rjust(20)}\n"
        )
        f.close()


class Yazaki:
    def __init__(self):
        import os, datetime, random
        from sty import fg, ef, rs
        from sty import RgbFg, Style

        d = datetime.datetime.now()
        fg.orange = Style(RgbFg(255, 150, 50))

        __color = [fg.red, fg(201), fg.orange, fg(122, 255, 51), fg(249, 238, 238)]

        print(str(" ").ljust(80))
        print(
            f"{ef.italic}{__color[random.randint(0, len(__color)) - 1]}         ,(#####################################/,*###################*       "
        )
        print(
            "     .####,.%##############      (#############.*####.      ####.####.        "
        )
        print(
            "    *###,(###                                .###/*###*    #### ####          "
        )
        print(
            "     *####.(#########.         ################(.####*   ,###(.####           "
        )
        print(
            "         *#########.####     ,####,##############*      (###*/###/            "
        )
        print(
            "  ###############(.(###/    /###//###/                 ####.################( "
        )
        print(
            ",##################(       ####.(###,                 #####################,  "
        )
        print(
            f"((**,#,(#(./* ,/((./*,#**#*.(,//( *, #.(#,/#.(/.#.#***,/* (,*(.#   ( ,#.#/,   {fg.rs}{rs.italic}",
            sep="\n",
        )
        print(str(" ").ljust(80))

        __txt_credit = fg(249, 238, 238)
        print(
            f"{__txt_credit}\n**********************************************************{fg.rs}"
        )
        print("\n")
        print(
            f"{__txt_credit}Copyright © {d.strftime('%Y')}. {fg.rs}{fg.orange}Taweechai Yuenyang, {fg.rs}{__txt_credit}All rights reserved.{fg.rs}"
        )
        print(
            f"{__txt_credit}Contact Email:{fg.rs} {fg.orange}krumii.it@gmail.com{fg.rs}"
        )
        print(
            f"{__txt_credit}Source:{fg.rs} {fg.orange}https://github.com/abe27{fg.rs}"
        )
        print(
            f"{__txt_credit}AT:{fg.rs} {fg.orange}{d.strftime('%Y-%m-%d %H:%M')}{fg.rs}"
        )
        print("\n")
        print(f"{fg.red}{'แพ็คเก็จนี้ใช้สำหรับงานของ SPL':^58}{fg.rs}")
        print(
            f"{__txt_credit}**********************************************************\n{fg.rs}"
        )

    @staticmethod
    def __login():
        import sys
        import os
        import urllib
        import urllib3
        import requests
        from bs4 import BeautifulSoup

        # from yazaki_packages.logs import Logging

        resp = False
        try:
            # login yazaki website.
            url = f"https://{os.getenv('YAZAKI_HOST')}:{os.getenv('YAZAKI_PORT')}/cehttp/servlet/MailboxServlet"
            passwd = urllib.parse.quote(os.getenv("YAZAKI_PASSWD"))
            payload = (
                f"operation=LOGON&remote={os.getenv('YAZAKI_USER')}&password={passwd}"
            )
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            urllib3.disable_warnings()
            resp = requests.request(
                "POST", url, data=payload, headers=headers, verify=False, timeout=3
            )

            txt = None
            docs = BeautifulSoup(resp.text, "html.parser")
            for i in docs.find_all("hr"):
                txt = (i.previous).replace("\n", "")

            _txt_status = "success"
            if txt.find("751") >= 0:
                _txt_status = "error"
                Logging(os.getenv("YAZAKI_USER"), f"login", f"{_txt_status}: {txt}")
                return False

            Logging(os.getenv("YAZAKI_USER"), f"login", f"{_txt_status}: {txt}")

        except Exception as msg:
            Logging(
                os.getenv("YAZAKI_USER"), "login", "error: " + str(msg),
            )
            sys.exit(0)

        return resp

    @staticmethod
    def __logout(session):
        import requests
        import os
        from bs4 import BeautifulSoup

        url = f"https://{os.getenv('YAZAKI_HOST')}:{os.getenv('YAZAKI_PORT')}/cehttp/servlet/MailboxServlet?operation=LOGOFF"
        headers = {}
        pyload = {}
        rq = requests.request(
            "POST",
            url,
            data=pyload,
            headers=headers,
            verify=False,
            timeout=3,
            cookies=session.cookies,
        )

        docs = BeautifulSoup(rq.text, "html.parser")
        for i in docs.find_all("hr"):
            txt = (i.previous).replace("\n", "")

        _txt_status = "success"
        if txt.find("751") >= 0:
            _txt_status = "error"
            Logging(os.getenv("YAZAKI_USER"), f"logout", f"{_txt_status}: {txt}")
            return False

        Logging(os.getenv("YAZAKI_USER"), f"logout", f"{_txt_status}: {txt}")

        return True

    @staticmethod
    def __get_text_file(session, objtype, filename, filelink):
        import requests
        from bs4 import BeautifulSoup
        from termcolor import colored
        import os

        docs = False
        try:
            if session is not None:
                if session.status_code == 200:
                    # download file
                    rq = requests.get(
                        filelink,
                        stream=True,
                        verify=False,
                        cookies=session.cookies,
                        allow_redirects=True,
                    )
                    docs = BeautifulSoup(rq.content, "lxml")
                    print(
                        colored(
                            f"download gedi {objtype} file : {(filename).upper()}",
                            "blue",
                        )
                    )
                    Logging(
                        os.getenv("YAZAKI_USER"),
                        f"download",
                        f"success: {(filename).upper()}.",
                    )
                    # logout

        except Exception as ex:
            Logging(
                os.getenv("YAZAKI_USER"),
                f"download",
                f"error: {(filename).upper()} is {str(ex)}.",
            )
            pass

        return docs

    @staticmethod
    def __get_link(session):
        obj = []
        try:
            import datetime
            from datetime import timedelta
            import requests
            from bs4 import BeautifulSoup
            from termcolor import colored
            import os

            etd = str((datetime.datetime.now() - timedelta(days=7)).strftime("%Y%m%d"))

            # get cookies after login.
            if session.status_code == 200:
                # get html page
                url = f"https://{os.getenv('YAZAKI_HOST')}:{os.getenv('YAZAKI_PORT')}/cehttp/servlet/MailboxServlet"
                headers = {"Content-Type": "application/x-www-form-urlencoded"}
                pyload = f"operation=DIRECTORY&fromdate={etd}&Submit=Receive"
                r = requests.request(
                    "POST",
                    url,
                    data=pyload,
                    headers=headers,
                    verify=False,
                    timeout=3,
                    cookies=session.cookies,
                )
                # print(type(r))
                soup = BeautifulSoup(r.text, "html.parser")
                for tr in soup.find_all("tr"):
                    found = False
                    i = 0
                    docs = []
                    for td in tr.find_all("td"):
                        txt = (td.text).rstrip().lstrip()
                        docs.append(txt)
                        if td.find("a") != None:
                            found = True

                        if found is False:
                            if len(docs) >= 9:
                                l = ObjectLink(
                                    os.getenv("SERVICE_TYPE"),
                                    docs[0],
                                    docs[1],
                                    str(docs[2]).replace(",", "").strip(),
                                    docs[3],
                                    f"{docs[4]} {docs[5]}",
                                    docs[6],
                                    docs[7],
                                    docs[8],
                                    found,
                                )
                                obj.append(l)

                        i += 1

                print(colored(f"found new link => {len(obj)}", "green"))
                Logging(
                    os.getenv("YAZAKI_USER"),
                    f"get data",
                    f"success: found new link {len(obj)}.",
                )

        except Exception as ex:
            Logging(os.getenv("YAZAKI_USER"), f"get data", "error: " + str(ex))
            pass

        return obj

    def get_gedi(self):
        import os, time

        cookies = self.__login()
        if cookies is False:
            print(f"error login")
            return

        doc = self.__get_link(cookies)
        if len(doc) > 0:
            i = 0
            while i < len(doc):
                r = doc[i]
                txt = self.__get_text_file(cookies, r.filetype, r.batchfile, r.linkfile)
                if txt != False:
                    ### check destination folder
                    __destination = (
                        f'exports/{r.filetype}/{(r.currentdate).strftime("%Y%m%d")}'
                    )
                    if os.path.exists(__destination) is False:
                        os.makedirs(__destination)

                    __filename = os.path.join(__destination, r.batchfile)
                    ### check duplicate file gedi. remove when exits.
                    if os.path.exists(__filename) == True:
                        os.remove(__filename)

                    try:
                        f = open(__filename, mode="a", encoding="ascii", newline="\r\n")
                        for p in txt:
                            f.write(p.text)
                        f.close()
                    except:
                        pass

                time.sleep(1.5)
                i += 1

        self.__logout(cookies)
