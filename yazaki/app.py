import os


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
        # import os
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
        self.destination = f'exports/{filetype}/{(self.currentdate).strftime("%Y%m%d")}'
        self.linkfile = f"https://{os.getenv('YAZAKI_HOST')}:{os.getenv('YAZAKI_PORT')}/cehttp/servlet/MailboxServlet?operation=DOWNLOAD&mailbox_id={self.mailbox}&batch_num={self.batchid}&data_format=A&batch_id={self.batchfile}"


class Logging:
    def __init__(self, title, content, status):
        # import os
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
        # import os,
        import datetime
        import random
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

        # import os
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

        # import os
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
    def __get_text_file(i, session, objtype, filename, filelink):
        import requests
        from bs4 import BeautifulSoup
        from termcolor import colored

        # import os

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
                            f"{i} download gedi {objtype} file : {(filename).upper()}",
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

            # import os

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

                        if found is True:  ### False =debug,True=prod.
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
        # import os,
        import time

        cookies = self.__login()
        if cookies is False:
            print(f"error login")
            return

        doc = self.__get_link(cookies)
        if len(doc) > 0:
            i = 0
            while i < len(doc):
                r = doc[i]
                txt = self.__get_text_file(
                    i, cookies, r.filetype, r.batchfile, r.linkfile
                )
                if txt != False:
                    ### check destination folder
                    if os.path.exists(r.destination) is False:
                        os.makedirs(r.destination)

                    __filename = os.path.join(r.destination, r.batchfile)
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

                time.sleep(0.1)
                i += 1

        self.__logout(cookies)
        return doc

    @staticmethod
    def __trimtxt(txt):
        return str(txt).lstrip().rstrip()

    @staticmethod
    def __checknamepart(fac, part):
        p = str(part).lstrip().rstrip().replace(".", "")
        partname = p
        if fac == "AW":
            try:
                k = str(p[: p.index(" ")]).strip()
                s = p[len(k) :]
                ss = s.strip()
                sn = str(ss[: ss.index(" ")]).strip()
                ssize = str(ss[: ss.index(" ")])

                if len(sn) > 1:
                    ssize = str(f"{sn[:1]}.{sn[1:]}").strip()

                c = str(p[(len(k) + len(ssize)) + 1 :]).strip()
                partname = f"{k} {ssize} {c}"
            except:
                pass
            finally:
                pass

        return partname

    @staticmethod
    def __restrip(txt):
        return (txt).rstrip().lstrip()

    @staticmethod
    def __repartname(txt):
        return (str(txt).replace("b", "")).replace("'", "")

    @staticmethod
    def __returnutfpono(self, txt):
        return str(self.__repartname(txt)).strip()

    @staticmethod
    def read_receive(self, filename):
        from datetime import datetime
        import uuid

        f = open(filename, "r", encoding="utf-8")
        docs = []
        for i in f:
            fac = filename[filename.find("SPL") - 2 : filename.find("SPL") - 1]
            uuidcode = str(uuid.uuid4())
            plantype = "RECEIVE"
            cd = 20
            unit = "BOX"
            recisstype = "01"
            factory = "INJ"
            if fac != "5":
                factory = "AW"
                plantype = "RECEIVE"
                cd = 10
                unit = "COIL"
                recisstype = "01"

            line = i
            try:
                docs.append(
                    {
                        "factory": factory,
                        "faczone": str(line[4 : (4 + 3)]).lstrip().rstrip(),
                        "receivingkey": str(line[4 : (4 + 12)]).lstrip().rstrip(),
                        "partno": str(line[76 : (76 + 25)]).lstrip().rstrip(),
                        "partname": str(line[101 : (101 + 25)]).lstrip().rstrip(),
                        "vendor": factory,
                        "cd": cd,
                        "unit": unit,
                        "whs": factory,
                        "tagrp": "C",
                        "recisstype": recisstype,
                        "plantype": plantype,
                        "recid": str(line[0:4]).lstrip().rstrip(),
                        "aetono": str(line[4 : (4 + 12)]).lstrip().rstrip(),
                        "aetodt": str(line[16 : (16 + 10)]).lstrip().rstrip(),
                        "aetctn": float(str(line[26 : (26 + 9)]).lstrip().rstrip()),
                        "aetfob": float(str(line[35 : (35 + 9)]).lstrip().rstrip()),
                        "aenewt": float(str(line[44 : (44 + 11)]).lstrip().rstrip()),
                        "aentun": str(line[55 : (55 + 5)]).lstrip().rstrip(),
                        "aegrwt": float(str(line[60 : (60 + 11)]).lstrip().rstrip()),
                        "aegwun": str(line[71 : (71 + 5)]).lstrip().rstrip(),
                        "aeypat": str(line[76 : (76 + 25)]).lstrip().rstrip(),
                        "aeedes": str(
                            self.__checknamepart(
                                factory, self.__repartname(line[101 : (101 + 25)])
                            )
                        ),
                        "aetdes": str(
                            self.__checknamepart(
                                factory, self.__repartname(line[101 : (101 + 25)])
                            )
                        ),
                        "aetarf": float(str(line[151 : (151 + 10)]).lstrip().rstrip()),
                        "aestat": float(str(line[161 : (161 + 10)]).lstrip().rstrip()),
                        "aebrnd": float(str(line[171 : (171 + 10)]).lstrip().rstrip()),
                        "aertnt": float(str(line[181 : (181 + 5)]).lstrip().rstrip()),
                        "aetrty": float(str(line[186 : (186 + 5)]).lstrip().rstrip()),
                        "aesppm": float(str(line[191 : (191 + 5)]).lstrip().rstrip()),
                        "aeqty1": float(str(line[196 : (196 + 9)]).lstrip().rstrip()),
                        "aeqty2": float(str(line[205 : (205 + 9)]).lstrip().rstrip()),
                        "aeuntp": float(str(line[214 : (214 + 9)]).lstrip().rstrip()),
                        "aeamot": float(str(line[223 : (223 + 11)]).lstrip().rstrip()),
                        "plnctn": float(str(line[26 : (26 + 9)]).lstrip().rstrip()),
                        "plnqty": float(str(line[196 : (196 + 9)]).lstrip().rstrip()),
                        "minimum": 0,
                        "maximum": 0,
                        "picshelfbin": "PNON",
                        "stkshelfbin": "SNON",
                        "ovsshelfbin": "ONON",
                        "picshelfbasicqty": 0,
                        "outerpcs": 0,
                        "allocateqty": 0,
                        "sync": False,
                        "uuid": uuidcode,
                        "updatedon": datetime.now(),
                    }
                )
            except Exception as ex:
                print(ex)
                pass

        return docs

    @staticmethod
    def read_orderplan(self, filename):
        from datetime import datetime
        import uuid

        f = open(filename, "r", encoding="utf-8")
        docs = []
        for line in f:
            fac = filename[filename.find("SPL") - 2 : filename.find("SPL") - 1]
            uuidcode = str(uuid.uuid4())
            plantype = "ORDERPLAN"
            cd = 20
            unit = "BOX"
            sortg1 = "PARTTYPE"
            sortg2 = "PARTNO"
            sortg3 = ""
            factory = "INJ"

            if fac != "5":
                factory = "AW"
                plantype = "ORDERPLAN"
                cd = 10
                unit = "COIL"
                sortg1 = "PONO"
                sortg2 = "PARTTYPE"
                sortg3 = "PARTNO"

            oqty = str(self.__trimtxt(line[89 : (89 + 9)]))
            if oqty == "":
                oqty = 0

            try:
                docs.append(
                    {
                        "vendor": factory,
                        "cd": cd,
                        "unit": unit,
                        "whs": factory,
                        "tagrp": "C",
                        "factory": factory,
                        "sortg1": sortg1,
                        "sortg2": sortg2,
                        "sortg3": sortg3,
                        "plantype": plantype,
                        "orderid": str(self.__trimtxt(line[13 : (13 + 15)])),
                        # remove space
                        "pono": str(self.__returnutfpono(self, line[13 : (13 + 15)])),
                        "recid": str(self.__trimtxt(line[0:4])),
                        "biac": str(self.__trimtxt(line[5 : (5 + 8)])),
                        "shiptype": str(self.__trimtxt(line[4 : (4 + 1)])),
                        "etdtap": datetime.strptime(
                            str(self.__trimtxt(line[28 : (28 + 8)])), "%Y%m%d"
                        ),
                        "partno": str(self.__trimtxt(line[36 : (36 + 25)])),
                        "partname": str(
                            self.__checknamepart(
                                factory,
                                self.__returnutfpono(self, line[61 : (61 + 25)]),
                            )
                        ),
                        "pc": str(self.__trimtxt(line[86 : (86 + 1)])),
                        "commercial": str(self.__trimtxt(line[87 : (87 + 1)])),
                        "sampleflg": str(self.__trimtxt(line[88 : (88 + 1)])),
                        "orderorgi": int(oqty),
                        "orderround": int(str(self.__trimtxt(line[98 : (98 + 9)]))),
                        "firmflg": str(self.__trimtxt(line[107 : (107 + 1)])),
                        "shippedflg": str(self.__trimtxt(line[108 : (108 + 1)])),
                        "shippedqty": float(str(self.__trimtxt(line[109 : (109 + 9)]))),
                        "ordermonth": datetime.strptime(
                            str(self.__trimtxt(line[118 : (118 + 8)])), "%Y%m%d"
                        ),
                        "balqty": float(str(self.__trimtxt(line[126 : (126 + 9)]))),
                        "bidrfl": str(self.__trimtxt(line[135 : (135 + 1)])),
                        "deleteflg": str(self.__trimtxt(line[136 : (136 + 1)])),
                        "ordertype": str(self.__trimtxt(line[137 : (137 + 1)])),
                        "reasoncd": str(self.__trimtxt(line[138 : (138 + 3)])),
                        "upddte": datetime.strptime(
                            str(self.__trimtxt(line[141 : (141 + 14)])), "%Y%m%d%H%M%S"
                        ),
                        "updtime": datetime.strptime(
                            str(self.__trimtxt(line[141 : (141 + 14)])), "%Y%m%d%H%M%S"
                        ),
                        "carriercode": str(self.__trimtxt(line[155 : (155 + 4)])),
                        "bioabt": int(str(self.__trimtxt(line[159 : (159 + 1)]))),
                        "bicomd": str(self.__trimtxt(line[160 : (160 + 1)])),
                        "bistdp": float(str(self.__trimtxt(line[165 : (165 + 9)]))),
                        "binewt": float(str(self.__trimtxt(line[174 : (174 + 9)]))),
                        "bigrwt": float(str(self.__trimtxt(line[183 : (183 + 9)]))),
                        "bishpc": str(self.__trimtxt(line[192 : (192 + 8)])),
                        "biivpx": str(self.__trimtxt(line[200 : (200 + 2)])),
                        "bisafn": str(self.__trimtxt(line[202 : (202 + 6)])),
                        "biwidt": float(str(self.__trimtxt(line[212 : (212 + 4)]))),
                        "bihigh": float(str(self.__trimtxt(line[216 : (216 + 4)]))),
                        "bileng": float(str(self.__trimtxt(line[208 : (208 + 4)]))),
                        "lotno": str(self.__trimtxt(line[220 : (220 + 8)])),
                        "minimum": 0,
                        "maximum": 0,
                        "picshelfbin": "PNON",
                        "stkshelfbin": "SNON",
                        "ovsshelfbin": "ONON",
                        "picshelfbasicqty": 0,
                        "outerpcs": 0,
                        "allocateqty": 0,
                        "sync": False,
                        "uuid": uuidcode,
                        "updatedon": datetime.strptime(
                            str(self.__trimtxt(line[141 : (141 + 14)])), "%Y%m%d%H%M%S"
                        ),
                    }
                )
            except Exception as ex:
                print(ex)
                pass

        # print(f"found orderplan: {len(docs)}")
        return docs

    def read_batch_file(self, typename, filetype, filename):
        doc = []
        if typename == "CK":
            if filetype == "RECEIVE":
                doc = self.read_receive(self, filename)

            else:
                doc = self.read_orderplan(self, filename)

        else:
            print("unknow")
        return doc

    def line_notification(self, msg):
        import requests

        # import os

        url = "https://notify-api.line.me/api/notify"
        payload = f"message={msg}"
        headers = {
            "Authorization": f"Bearer {os.getenv('LINE_NOTIFICATION_TOKEN')}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # BugDWScwhYvjVc5EyRi5sa28LmJxE2G5NIJsrs6vEV7

        response = requests.request(
            "POST", url, headers=headers, data=payload.encode("utf-8")
        )

        print(f"line status => {response}")
        if response.status_code == 200:
            return True

        return False
