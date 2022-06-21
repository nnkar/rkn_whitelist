from unittest import result
from urllib import request

import os
import sys
import base64

import xml.etree.ElementTree as ET
from suds.client import Client
from datetime import datetime
import dateutil.parser
import quote
import logging
import time
import zipfile
import subprocess
import xml.etree.ElementTree as ET
import dateutil.parser

from config import Config
cfg = Config()

#logging.basicConfig(filename=cfg.LogMain, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

class StartRequest:

    def checklastDumpDateUrgently():
        def getLastDumpDate():
            client = Client(cfg.URL_RKN)
            result = client.service.getLastDumpDateEx() 
            print("222222222 - %s " % result) 
            #print("11111111 - %s" % client.service.lastDumpDateSocResources())    
            # result = client.service.lastDumpDateSocResources()      
            #value = result.lastDumpDateUrgently / 1000  
            value = result.lastDumpDateSocResources / 1000         
            print("33333333 - %s" % value) 
            return value
   
        value = getLastDumpDate()        
        f = open(cfg.lasupload, 'r')
        string = f.readlines()        
        f.close()
    
        if(float(value) > float(string[0])):
            fu = open(cfg.lasupload, 'w')
            fu.write(str(int(value)))
            fu.close()
            return True
        else:
            return False

        

    def createXML(filename):
        dt = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        request_xml = '<?xml version="1.0" encoding="windows-1251"?>\n'
        request_xml += '<request>\n'
        request_xml += '<requestTime>' + dt + '.000+04:00</requestTime>\n'
        request_xml += '<operatorName>' + cfg.OPERATOR + '</operatorName>\n'
        request_xml += '<inn>' + cfg.INN + '</inn>\n'
        request_xml += '<ogrn>' + cfg.OGRN + '</ogrn>\n'
        request_xml += '<email>' + cfg.EMAIL + '</email>\n'
        request_xml += '</request>'
        with open(filename, 'wb') as f:
            f.write(request_xml.encode(encoding='cp1251'))
        return True
    
    def createSIG():
        #"C:\Program Files (x86)\Crypto Pro\CSP\csptest.exe" -sfsign -sign -detached -add -in %myreq% -out %mysig% -my %mysigemail%

        subprocess.Popen([cfg.CRIPTOPROPATH, '-sfsign', '-sign', '-detached', '-add', '-in', cfg.OUT_XML, '-out', cfg.OUT_BIN, '-my', cfg.EMAIL])
        return True

    def sendRequest(xmlfile, signfile, URL_RKN):
        try:            
            f = open(xmlfile, "rb")    
            data = f.read()
            f.close()       
            xml = base64.b64encode(data)        
            f = open(signfile, 'rb')
            data = f.read()
            f.close()
            sign = base64.b64encode(data)
            client = Client(URL_RKN)
            xml = str(xml)[2:-1]
            sign = str(sign)[2:-1]
            dfv = '2.4'
                        
            result = client.service.sendRequest(xml, sign, dfv)

            if result['result']:
                logging.info(f"Comment: {result['resultComment']}")
                print(f"Comment: {result['resultComment']}")
                logging.info(f"Code: {result['code']}")
                print(f"Code: {result['code']}")
                logging.info("Sending a request: Done")
                print("Sending a request: Done")
                code = result['code']
                return code
            else:
                logging.info(f"Comment: {result['resultComment']}")
                print(f"Comment: {result['resultComment']}")
                logging.error("Sending a request: Fuilt")
                print("Sending a request: Fuilt")
                return False
        except Exception as e:
            logging.error(f"Sending a request: {e}")
            print("Sending a request: Fuilt, information in logs")

    def get_result(code, URL_RKN):
        time_slip = 60
        minuts = 60
        for time_step in range(minuts):            

            logging.info(f"Code {code} sent")
            print(f"Code {code} sent")
            logging.info(f'Attempted code review request: {time_step+1}')
            print(f'Attempted code review request: {time_step+1}')

            client = Client(URL_RKN)
            # result = client.service.getResult(code)
            result = client.service.getResultSocResources(code)
            print("Result --- %s" % result['result'])
            if result['result']:
                # print(f"Comment: {result['resultComment']}")
                break
            else:                
                logging.info(f"Comment: {result['resultComment']}")
                print(f"Comment: {result['resultComment']}")               
                if result['resultCode'] != 0:                    
                    logging.error(f"Comment: {result['resultComment']}")
                    print(f"Comment: {result['resultComment']}")
                    break
                else:
                    logging.info(f"Retry request after {time_slip} seconds")
                    print(f"Retry request after {time_slip} seconds")                    
                    time.sleep(time_slip)

        return result['registerZipArchive']
        
    def create_zip(data, path):
        try:
            f = open(path, "wb")
            f.write(base64.b64decode(data))
            f.close()
            return True
        except:
            return False

class WorkingWithFiles():
    def __init__(self):
        
        pass


    def write_in_file(self, file_name, data, path=cfg.TMPDIR):
        """ Write data to spec file """
        with open(path + "/" + file_name, 'w') as f:
            data = sorted(set(data))
            for item in data:
                f.write("%s\n" % item)
        return 0

    def func_unzip(self, infile, outfile):
        try:
            logging.info(f"File unpacking")
            print(f"File unpacking")     
            zip_file = zipfile.ZipFile(infile, 'r')
            zip_file.extract(outfile, cfg.TMPDIR)
            zip_file.close()
            return True
        except Exception as e:
            logging.error(f"File file is not unpacked {e}")
            print(f"File file is not unpacked {e}")     
            return False

    
    def createoldDump(self):
        try:
            f = open(cfg.DUMP_FILE, "r")    
            data = f.read()
            f.close() 
            
            f = open(cfg.OLD_DUMP_FILE, "wb")
            f.write(data.encode(encoding='cp1251'))
            f.close()
            logging.info(f"Old Dump create")
            print(f"Old Dump create")
        except Exception as e:
            logging.error(f"Old Dump not create {e}")
            print(f"Old Dump not create {e}") 

    def ipSearch():
        old_ips = []
        new_ips = []
        tree = ET.parse(cfg.DUMP_FILE)
        root = tree.getroot()
        for i, record in enumerate(root):
            ips = record.findall('ip')
            if ips is not None:
                for ip in ips:
                    ip_ts = ip.get('ts')
                    ip = ip.text
                    new_ips.append(ip)


