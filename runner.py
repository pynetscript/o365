#!/usr/bin/python3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Standard library modules
import json
import os
import urllib.request
import uuid
import time
import datetime
import signal
#from slackclient import SlackClient
import slackclient
from os.path import expanduser


signal.signal(signal.SIGPIPE, signal.SIG_DFL)   # IOERror: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)    # KeyboardInterrupt: Ctrl-C


def webApiGet(methodName, instanceName, clientRequestId):
    """
    Helper to call the webservice and parse the response
    """
    ws = "https://endpoints.office.com"
    requestPath = ws + '/' + methodName + '/' + instanceName + '?clientRequestId=' + clientRequestId
    request = urllib.request.Request(requestPath)
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode())


def slack_message(channel, username, icon_url, text):
    """
    Channel:        #channel    (private/public)
    App joined:     Bots        'https://pynetscript.slack.com/apps/A0F7YS25R-bots?next_id=0'
                    Username:   'mr-robot'
                    Image:      'https://avatars.slack-edge.com/2018-08-14/416017134033_c12382bddd39e3823d99_48.jpg'
    """
    BOTS_TOKEN = os.environ.get('BOTS_TOKEN')
    if BOTS_TOKEN is None:
        NOT_FOUND = 'BOTS_TOKEN was not found in environment variable.'
        COMMAND = 'Add a token with the "export BOTS_TOKEN=xoxb-0123456789a0-123456789b01-23456789c0123456789d0123" command.'
        print('\n'
              '{E1} {E2} \n'.format(E1=NOT_FOUND, E2=COMMAND))
        raise SlackBotsAPITokenNotFound()

    sc = SlackClient(BOTS_TOKEN)
    sc.api_call('chat.postMessage', channel=channel, username=username, icon_url=icon_url, text=text)


# slack image
icon_url = "https://avatars.slack-edge.com/2018-08-14/416017134033_c12382bddd39e3823d99_48.jpg"


# path where client ID and latest version number will be stored
home = expanduser("~")
datapath = (home + '/o365/clientrequestid_latestversion.txt')


# fetch clientrequestid and worldwide latest version from "datapath" file if data exists, else
# generate clientrequestid and worldwide latest version, and write to "datapath file.
if os.path.exists(datapath):
    with open(datapath, 'r') as fin:
        clientRequestId = fin.readline().strip()
        latestVersion = fin.readline().strip()
else:
    clientRequestId = str(uuid.uuid4())
    latestVersion = '0000000000'
    with open(datapath, 'w') as fout:
        fout.write(clientRequestId + '\n' + latestVersion)


# call version method to check the latest version, and pull new data if version number is different
# https://endpoints.office.com/version/Worldwide?clientrequestid=39943d70-aa59-40c9-bdcf-69998b415368
version = webApiGet('version', 'Worldwide', clientRequestId)


# If Online version > version in "clientrequestid_latestversion.txt"
if version['latest'] > latestVersion:
    current_timestamp = datetime.datetime.now()
    current_time = current_timestamp.strftime('%d/%m/%Y %H:%M:%S')
    print(current_time, '- New version of Office 365 worldwide commercial service instance endpoints detected.')

    # write the new version number to "datapath"
    with open(datapath, 'w') as fout:
        fout.write(clientRequestId + '\n' + version['latest'])

    # invoke endpoints method to get the new data
    # https://endpoints.office.com/endpoints/Worldwide?clientrequestid=39943d70-aa59-40c9-bdcf-69998b415368
    endpointSets = webApiGet('endpoints', 'Worldwide', clientRequestId)

    # filter results for Allow and Optimize endpoints, and transform these into tuples with port and category
    flatUrls = []
    for endpointSet in endpointSets:
        if endpointSet['category'] in ('Optimize', 'Allow'):
            category = endpointSet['category']
            urls = endpointSet['urls'] if 'urls' in endpointSet else []
            tcpPorts = endpointSet['tcpPorts'] if 'tcpPorts' in endpointSet else ''
            udpPorts = endpointSet['udpPorts'] if 'udpPorts' in endpointSet else ''
            flatUrls.extend([(category, url, tcpPorts, udpPorts) for url in urls])

    flatIps = []
    for endpointSet in endpointSets:
        if endpointSet['category'] in ('Optimize', 'Allow'):
            ips = endpointSet['ips'] if 'ips' in endpointSet else []
            category = endpointSet['category']
            # IPv4 strings have dots while IPv6 strings have colons
            ip4s = [ip for ip in ips if '.' in ip]
            tcpPorts = endpointSet['tcpPorts'] if 'tcpPorts' in endpointSet else ''
            udpPorts = endpointSet['udpPorts'] if 'udpPorts' in endpointSet else ''
            flatIps.extend([(category, ip, tcpPorts, udpPorts) for ip in ip4s])


    o365_ipv4_ips = (','.join(sorted(set([ip for (category, ip, tcpPorts, udpPorts) in flatIps]))))
    o365_urls = (','.join(sorted(set([url for (category, url, tcpPorts, udpPorts) in flatUrls]))))

    latest_version = (version['latest'])

    with open(datapath, 'r') as fin:
        clientRequestId = fin.readline().strip()


    text = ('New version of Office 365 worldwide commercial service instance endpoints detected at\n' +
            'https://endpoints.office.com/version/Worldwide?clientrequestid=' + clientRequestId + '\n\n'
            'Current version: ' + latestVersion + ' (' + datapath + ')' + '\n'
            'Latest version: ' + latest_version + '\n\n\n'
            'IPv4 Address Ranges for Firewall \n\n' +
            o365_ipv4_ips + '\n\n\n'
            'URLs for Firewall \n\n' +
            o365_urls)

    slack_message('#o365', 'mr-robot', icon_url, text)


else:
    current_timestamp = datetime.datetime.now()
    current_time = current_timestamp.strftime('%d/%m/%Y %H:%M:%S')
    print(current_time, '- Office 365 worldwide commercial service instance endpoints are up-to-date.')

    latest_version = (version['latest'])

    text = ('Office 365 worldwide commercial service instance endpoints are up-to-date.'
            '\nCurrent version: ' + latestVersion +
            '\nLatest version: ' + latest_version)

    slack_message('#o365', 'mr-robot', icon_url, text)
