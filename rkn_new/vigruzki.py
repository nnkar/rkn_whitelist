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


from config import Config
from utils import StartRequest as sr
from utils import WorkingWithFiles


cfg = Config()
wwf = WorkingWithFiles()
domainlist = []
ipsublist = []

if __name__ == '__main__':

    dir = os.path.abspath(os.curdir)
    
    logging.basicConfig(filename=cfg.LogMain, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

   
    while True: 
        logging.info(f"Script start")
        if sr.checklastDumpDateUrgently():
            #if True:
            logging.info(f"New date")
            new_xml = sr.createXML(cfg.OUT_XML)
            if new_xml:
                logging.info(f"XML create")
                print(f"XML create")
                new_sig = sr.createSIG()
                if new_sig:
                    logging.info(f"SIG create")
                    print(f"SIG create")
                    time.sleep(20)
                    code = sr.sendRequest(cfg.OUT_XML, cfg.OUT_BIN, cfg.URL_RKN)
                    print("Code ----- %s" % code)
                    if code: 
                        wwf.createoldDump()
                        now_date = f'{datetime.now().year}{datetime.now().month}{datetime.now().day}{datetime.now().hour}{datetime.now().minute}{datetime.now().second}'   
                        zip_data = sr.get_result(code, cfg.URL_RKN)
                        zip_path = f'{cfg.ZIPDIR}\\result_{now_date}.zip'
                        print(cfg.result_zip)
                        
                        new_zip = sr.create_zip(zip_data, zip_path)
                        if zip_data:
                            print(f'Zip file created: {zip_path}')
                            logging.info(f"Zip file created: {zip_path}")            
                            wwf.func_unzip(zip_path, 'register.xml')
                            # парсинг xml и вывод в файл
                            try:
                                tree = ET.parse(cfg.DUMP_FILE)
                            except IOError as Err:
                                print('Ошибка открытия register.xml : %s' % Err)
                                exit(Err)
                            # получаем дерево xml
                            root = tree.getroot()
                            for record in root:
                                domain = record.find('domain')
                                if domain is not None:
                                    domain = domain.text
                                    # print("Domain ----- %s" % domain)
                                    domainlist.append(domain)
                                ipSubnets = record.findall('ipSubnet')
                                if ipSubnets is not None:
                                    for ipSubnet in ipSubnets:
                                        ipsub = ipSubnet.text
                                        # print("ipSubnet ----- %s" % ipsub)
                                        ipsublist.append(ipsub)
                            # print("Domainbs %s" % domainlist)
                            # print("IPs %s" % ipsublist)
                            wwf.write_in_file("domain.txt", domainlist)
                            wwf.write_in_file("iplists.txt", ipsublist)

                        else:
                            print(f'Error zip file not created')
                            logging.error(f"Zip file not created")
                else:
                    logging.error(f"SIG create error")
            else:
                logging.error(f"XML create error")
        else:
            print(f'{datetime.now()}: New date not')
            logging.info(f"New date not")
            time.sleep(3600)
        domainlist = []
        ipsublist = []