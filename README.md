[![Build Status](https://travis-ci.org/pynetscript/o365.svg?branch=master)](https://travis-ci.org/pynetscript/o365)
[![GitHub release](https://img.shields.io/badge/version-1.0-blue.svg)](https://github.com/pynetscript/reality)

# o365

### Script use
- Get updated with Office 365 IPs and URLs changed by Microsoft (via Slack private channel).
- "Almost" completely based on script provided by Microsoft - [Managing Office 365 endpoints](https://support.office.com/en-us/article/managing-office-365-endpoints-99cab9d4-ef59-4207-9f2b-3728eb46bf9a?redirectSourcePath=%252fen-us%252farticle%252fnetwork-connectivity-to-office-365-64b420ef-0218-48f6-8a34-74bb27633b10&ui=en-US&rs=en-US&ad=US)


# Installation

```
sudo apt-get update
sudo apt-get install -y git
sudo apt-get install -y python3-pip
sudo python3 -m pip install -U pip
cd ~ && git clone https://github.com/pynetscript/o365.git && cd o365
sudo python3 -m pip install -r requirements.txt
```

# Prerequisites

- Add Slack application named "Bots"
  - Need to add API token at `/etc/environment`
- Create a Private channel


# runner.py

- If "clientrequestid_latestversion.txt" file exists in the same directory as "runner.py":
  - Fetch clientRequestId and Worldwide latest version.
- Else:
  - Generate clientRequestId with `uuid` module.
  - Set Worldwide latest version to "0000000000".
  - Open/Create "clientrequestid_latestversion.txt" and write the data - [eg](https://pastebin.com/dA1wr5pH).
- Check the Worldwide latest version - [eg](https://endpoints.office.com/version/Worldwide?clientrequestid=39943d70-aa59-40c9-bdcf-69998b415368).

- If Online version is higher than version in "clientrequestid_latestversion.txt":
  - Print: `New version of Office 365 worldwide commercial service instance endpoints detected`
  - Write the new version number to "clientrequestid_latestversion.txt" - [eg](https://pastebin.com/fiqYZgaq).
  - Download URLs and IPv4 prefixes that their category is either "Allow" or "Optimize" - [eg](https://endpoints.office.com/endpoints/Worldwide?clientrequestid=39943d70-aa59-40c9-bdcf-69998b415368)
  - Store all URLs  as a string (each URL separated by comma).
  - Store all IPv4 prefixes in a string (each prefix separated by comma).
  - Send the data via Slack message:
    - Channel: #o365
    - User: mr-robot
    - Icon_url: "icon_url" variable
    - Text: "text" variable
- Else (Online version equal to or lower than version in "clientrequestid_latestversion.txt":
  - Print: `Office 365 worldwide commercial service instance endpoints are up-to-date.`
  - Send a notification via Slack message:
    - Channel: #o365
    - User: mr-robot
    - Icon_url: "icon_url" variable
    - Text: "text" variable


# cron job

- Microsoft suggests that we run this check every hour so I have created a cron job to run the script every 10 minutes.


## Demo
