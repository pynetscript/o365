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
  - Need to add API token provided by "Bots" at `/etc/environment`
  - username: mr-robot
  - icon_url: [icon_url](https://avatars.slack-edge.com/2018-08-14/416017134033_c12382bddd39e3823d99_48.jpg)
- Create a Private channel
  - My private channel is named #o365
- Specify in the script values from your environment:
  - [runner.py line 133](https://github.com/pynetscript/o365/blob/master/runner.py#L133)
  - [runner.py line 147](https://github.com/pynetscript/o365/blob/master/runner.py#L147)
  - channel: #o365
  - username: mr-robot
  - icon_url: [icon_url](https://avatars.slack-edge.com/2018-08-14/416017134033_c12382bddd39e3823d99_48.jpg)

![Imgur](https://i.imgur.com/JZnOz6S.png)

![Imgur](https://i.imgur.com/WicDA0x.png)

![Imgur](https://i.imgur.com/VIAVz6e.png)

![Imgur](https://i.imgur.com/UU31Joh.png)

![Imgur](https://i.imgur.com/8XNWtc5.png)


# runner.py

- If "clientrequestid_latestversion.txt" file exists in the same directory as "runner.py":
  - Fetch clientRequestId and Worldwide latest version.
- Else:
  - Generate clientRequestId with `uuid` module.
  - Set Worldwide latest version to "0000000000".
  - Open/Create "clientrequestid_latestversion.txt" and write the data - [eg](https://pastebin.com/dA1wr5pH).
- Check the Worldwide latest version - [eg](https://endpoints.office.com/version/Worldwide?clientrequestid=fca86b7c-0b6f-4b68-8e82-afa45b65e631).

- If Online version is higher than version in "clientrequestid_latestversion.txt":
  - Print: `New version of Office 365 worldwide commercial service instance endpoints detected`
  - Write the new version number to "clientrequestid_latestversion.txt" - [eg](https://pastebin.com/fiqYZgaq).
  - Download URLs and IPv4 prefixes that their category is either "Allow" or "Optimize" - [eg](https://endpoints.office.com/endpoints/Worldwide?clientrequestid=fca86b7c-0b6f-4b68-8e82-afa45b65e631)
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

- Microsoft suggests that we run the script every hour so we can create a cron job to run the script at fixed times, dates, or intervals.
- Need to give "execute" permission to "runner.py" for cron job to work (`chmod 774 runner.py`).


## Demo (online version > version in "clientrequestid_latestversion.txt")
```
aleks@acorp:~/o365$ ./runner.py
21/08/2018 15:19:28 - New version of Office 365 worldwide commercial service instance endpoints detected.
```

![Imgur](https://i.imgur.com/8lHat61.png)

![Imgur](https://i.imgur.com/3rcwQv2.png)


## Demo (online version <= version in "clientrequestid_latestversion.txt")
```
aleks@acorp:~/o365$ ./runner.py 
21/08/2018 15:40:05 - Office 365 worldwide commercial service instance endpoints are up-to-date.
```

![Imgur](https://i.imgur.com/IOcoHdj.png)
