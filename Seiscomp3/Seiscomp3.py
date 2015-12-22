#!/usr/bin/env python

import xml.etree.ElementTree as ET

class Seiscomp3 (object):
    def __init__(self, agentConfig, checksLogger, rawConfig):
        self.agentConfig = agentConfig
        self.checksLogger = checksLogger
        self.rawConfig = rawConfig

    def run(self):
        data = {}

        file ='/home/seiscomp/.seiscomp3/log/server.xml'

        tree = ET.parse(file)
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
                        data[serviceName + '-' + test.get('name')] = test.get('value')
                for object in service.findall('input/object'):
                    if object.get('name') in objects:
                        data[serviceName + '-input-' + object.get('name')] = object.get('count')
                for object in service.findall('output/object'):
                    if object.get('name') in objects:
                        data[serviceName + '-output-' + object.get('name')] = object.get('count')

        return data

# vim: set ts=4 sw=4 tw=0 et:
