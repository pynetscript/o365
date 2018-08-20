[![Build Status](https://travis-ci.org/pynetscript/o365.svg?branch=master)](https://travis-ci.org/pynetscript/o365)
[![GitHub release](https://img.shields.io/badge/version-1.0-blue.svg)](https://github.com/pynetscript/reality)

# o365

### Script use
- Get updated with Office 365 IPs and/or URLs changed by Microsoft (via Slack private channel).
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

# .travis.yml

- [Travis CI](https://travis-ci.org/pynetscript/o365)
- What language: **Python**
- What versions: **3.4** , **3.5** , **3.6**
- What to install: **pip install -r requirements.txt**
- What to run: **python runner.py**
- Where to send notifications: **pynetscript:3GF5L6jlBvYl9TA5mrcJ87rq** 
  - Install Travis CI on [Slack](https://pynetscript.slack.com) and at some point it will output a slack channel to use.
  - Replace **pynetscript:3GF5L6jlBvYl9TA5mrcJ87rq** with your own channel.
  - Supports private channels.

