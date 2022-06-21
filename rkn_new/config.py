import os
from datetime import datetime as dt

class Config(object):
    def __init__(self):
        now_date = f'{dt.now().year}{dt.now().month}{dt.now().day}{dt.now().hour}{dt.now().minute}{dt.now().second}'
        self.OPERATOR = '"ООО РогаИКопыта"'
        self.INN = '65451151351'
        self.OGRN = '651651651651'
        self.EMAIL = 'it@rogaikopyta.ru'
        self.WORKDIR = os.path.abspath(os.path.dirname(__file__))
        self.SSLDIR = "%s\\ssl" % self.WORKDIR
        self.OUT_XML = "%s\\req.xml" % self.SSLDIR
        self.OUT_BIN = "%s\\req.xml.sig" % self.SSLDIR
        self.LOGDIR = "%s\\logs" % self.WORKDIR
        self.LogMain = "%s\\rkn.log" % self.LOGDIR
        self.URL_RKN = 'https://vigruzki.rkn.gov.ru/services/OperatorRequest/?wsdl'
        self.TMPDIR = "%s\\tmp" % self.WORKDIR
        self.ZIPDIR = "%s\\zip" % self.WORKDIR
        self.result_zip = f"%s\\result{now_date}.zip" % self.ZIPDIR
        self.CRIPTOPROPATH = 'C:\\Program Files (x86)\\Crypto Pro\\CSP\\csptest.exe'
        # self.DUMP_FILE = "%s\\dump.xml" % self.TMPDIR
        # self.OLD_DUMP_FILE = "%s\\dump_old.xml" % self.TMPDIR
        self.DUMP_FILE = "%s\\register.xml" % self.TMPDIR
        self.OLD_DUMP_FILE = "%s\\register_old.xml" % self.TMPDIR
        self.lasupload = "%s\\lasupload" % self.WORKDIR
        self.getResult = "getResultSocResources"
        