#!/usr/bin/env python

import iso8601
import xml.etree.ElementTree as ET

class Seiscomp3 (object):
    def __init__(self, agentConfig, checksLogger, rawConfig):
        self.agentConfig = agentConfig
        self.checksLogger = checksLogger
        self.rawConfig = rawConfig

        # File to read SC3 SoH information from
        self.file = self.rawConfig['Seiscomp3']\
            .get('file', '/home/seiscomp/.seiscomp3/log/server.xml')

        self.updates = {}

    def run(self):
        data = {}
        
        tree = ET.parse(self.file)
        root = tree.getroot()

        tests = ['uptime','cpuusage','clientmemoryusage']
        services = ['scamp','scautoloc','scautopick','scevent','scevtlog','scevtspool','evtspool2','scmag','screloc','_MASTER_','rsamtrig']
        objects = ['record','origin','pick','event','amplitude','magnitude']

        for service in root:
            if service.get('name') in services:
                serviceName = service.get('name')
                source = service.get('host')
                for test in service.findall('test'):
                    if test.get('name') in tests:
                        time = iso8601.parse_date(test.get('updateTime')).utctimetuple()
                        key = serviceName + '-' + test.get('name')
                        last = self.updates.get(key,0)
                        if time != last:
                            data[key] = test.get('value')
                            self.updates[key] = time
                for object in service.findall('input/object'):
                    if object.get('name') in objects:
                        time = iso8601.parse_date(test.get('updateTime')).utctimetuple()
                        key = serviceName + '-input-' + object.get('name') 
                        last = self.updates.get(key,0)
                        if time != last:
                            data[key] = object.get('count')
                            self.updates[key] = time
                for object in service.findall('output/object'):
                    if object.get('name') in objects:
                        time = iso8601.parse_date(test.get('updateTime')).utctimetuple()
                        key = serviceName + '-output-' + object.get('name') 
                        last = self.updates.get(key,0)
                        if time != last:
                            data[key] = object.get('count')
                            self.updates[key] = time

        return data

    

if __name__ == '__main__':
    """Standalone test
    """

    import json
    import logging
    import sys
    import time

    raw_agent_config = {
        'Seiscomp3': {
        }
    }
    if sys.argv[1]:
        raw_agent_config['Seiscomp3']['file'] = sys.argv[1]

    main_checks_logger = logging.getLogger('Seiscomp3')
    main_checks_logger.setLevel(logging.DEBUG)
    main_checks_logger.addHandler(logging.StreamHandler(sys.stdout))
    sc3_check = Seiscomp3({}, main_checks_logger, raw_agent_config)

    while True:
        try:
            print json.dumps(sc3_check.run(), indent=4, sort_keys=True)
        except:
            main_checks_logger.exception("Unhandled exception")
        finally:
            time.sleep(60)

# vim: set ts=4 sw=4 tw=0 et:
