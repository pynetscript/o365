#!/usr/bin/python3

###############################################################################
# Written by:           Aleks Lambreca
# Creation date:        19/08/2018
# Last modified date:   22/08/2018
# Version:              v1.0
###############################################################################


# Standard library modules
import json
import os
import urllib.request
import uuid
import requests
import time
import datetime
import signal
from slackclient import SlackClient


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
    class SlackBotsAPITokenNotFound(Exception):
        pass
    
    BOTS_TOKEN = os.environ.get('BOTS_TOKEN')
    if BOTS_TOKEN is None:
        NOT_FOUND = 'BOTS_TOKEN was not found in environment variable "/etc/environment".'
        COMMAND = 'Add token with BOTS_TOKEN="xoxb-0123456789a0-123456789b01-23456789c0123456789d0123" format.'
        print('\n'
              '{E1} {E2} \n'.format(E1=NOT_FOUND, E2=COMMAND))
        raise SlackBotsAPITokenNotFound()

    sc = SlackClient(BOTS_TOKEN)
    sc.api_call('chat.postMessage', channel=channel, username=username, icon_url=icon_url, text=text)


def slack_upload(channels, initial_comment, title, filename, filetype, file):
    """
    Upload file to slack
    """
    class SlackBotsAPITokenNotFound(Exception):
        pass
    
    BOTS_TOKEN = os.environ.get('BOTS_TOKEN')
    if BOTS_TOKEN is None:
        NOT_FOUND = 'BOTS_TOKEN was not found in environment variable "/etc/environment".'
        COMMAND = 'Add token with BOTS_TOKEN="xoxb-0123456789a0-123456789b01-23456789c0123456789d0123" format.'
        print('\n'
              '{E1} {E2} \n'.format(E1=NOT_FOUND, E2=COMMAND))
        raise SlackBotsAPITokenNotFound()

    sc = SlackClient(BOTS_TOKEN)
    sc.api_call('files.upload', channels=channels, initial_comment=initial_comment, title=title, filename=filename, 
                filetype=filetype, file=file)

    
# slack image
icon_url = "https://avatars.slack-edge.com/2018-08-14/416017134033_c12382bddd39e3823d99_48.jpg"


# path where client ID and latest version number will be stored
path = os.path.dirname(os.path.abspath(__file__))
datapath = (path + '/clientrequestid_latestversion.txt')


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
latest_version = (version['latest'])

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
            ip4s = [ip for ip in ips if '.' in ip]
            tcpPorts = endpointSet['tcpPorts'] if 'tcpPorts' in endpointSet else ''
            udpPorts = endpointSet['udpPorts'] if 'udpPorts' in endpointSet else ''
            flatIps.extend([(category, ip, tcpPorts, udpPorts) for ip in ip4s])


    o365_ipv4 = (','.join(sorted(set([ip for (category, ip, tcpPorts, udpPorts) in flatIps]))))
    o365_urls = (','.join(sorted(set([url for (category, url, tcpPorts, udpPorts) in flatUrls]))))

    o365_tcp = (','.join(sorted(set([tcpPorts for (category, ip, tcpPorts, udpPorts) in flatIps]))))
    o365_udp = (','.join(sorted(set([udpPorts for (category, ip, tcpPorts, udpPorts) in flatIps]))))
    o365_udp_fix = o365_udp.lstrip(',')

    with open(datapath, 'r') as fin:
        clientRequestId = fin.readline().strip()

    path_o365_ipv4 = os.path.dirname(os.path.abspath(__file__))
    data_o365_ipv4 = (path_o365_ipv4 + '/o365_ipv4.csv')
    with open(data_o365_ipv4, 'w') as data_o365_ipv4_out:
        data_o365_ipv4_out.write(o365_ipv4)

    path_o365_url = os.path.dirname(os.path.abspath(__file__))
    data_o365_url = (path_o365_url + '/o365_url.csv')
    with open(data_o365_url, 'w') as data_o365_url_out:
        data_o365_url_out.write(o365_urls)


    text0 = ('*New version of Office 365 worldwide commercial service instance endpoints detected at:*\n' +
            'https://endpoints.office.com/version/Worldwide?clientrequestid=' + clientRequestId + '\n\n'
            'Current version: ' + '`' + latestVersion + '`' + ' (' + datapath + ')' + '\n'
            'Latest version: ' + '`' + latest_version + '`' + '\n\n\n')
    slack_message('#o365', 'mr-robot', icon_url, text0)

    slack_upload('#o365',
                 '*IPv4 Address Ranges for Firewall*',
                 'o365_ipv4.csv',
                 'o365_ipv4.csv',
                 'csv',
                 (data_o365_ipv4, open(data_o365_ipv4, 'rb'), 'csv'))

    slack_upload('#o365',
                 '*URLs for Firewall*',
                 'o365_url.csv',
                 'o365_url.csv',
                 'csv',
                 (data_o365_url, open(data_o365_url, 'rb'), 'csv'))

    text1 = ('*IPv4 Address Ranges & URLs TCP/UDP ports* \n\n' +
             'TCP: ' + '```' + o365_tcp + '```' + '\n' +
             'UDP: ' + '```' + o365_udp_fix + '```')
    slack_message('#o365', 'mr-robot', icon_url, text1)


else:
    current_timestamp = datetime.datetime.now()
    current_time = current_timestamp.strftime('%d/%m/%Y %H:%M:%S')
    print(current_time, '- Office 365 worldwide commercial service instance endpoints are up-to-date.')

    text = ('*Office 365 worldwide commercial service instance endpoints are up-to-date.*'
            '\nCurrent version: ' + '`' + latestVersion + '`' +
            '\nLatest version: ' + '`' + latest_version + '`' )

    slack_message('#o365', 'mr-robot', icon_url, text)
