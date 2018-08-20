[![Build Status](https://travis-ci.org/pynetscript/o365.svg?branch=master)](https://travis-ci.org/pynetscript/o365)
[![GitHub release](https://img.shields.io/badge/version-1.0-blue.svg)](https://github.com/pynetscript/reality)

# o365

### Script use
- 

### Script output
- Cisco IOS command output
- Errors in screen
- Progress bar
- Statistics
- Log success/erros in `runner.log`
- Travis CI build notification to Slack private channel

# Installation

```
sudo apt-get update
sudo apt-get install -y git
sudo apt-get install -y python-pip
sudo apt-get install -y python3-pip
sudo python -m pip install -U pip
sudo python3 -m pip install -U pip
cd ~ && git clone https://github.com/pynetscript/o365.git && cd o365
sudo python -m pip install -r requirements.txt
sudo python3 -m pip install -r requirements.txt
```

# .travis.yml

- [Travis CI](https://travis-ci.org/pynetscript/o365)
- What language: **Python**
- What versions: **2.7** , **3.4** , **3.5** , **3.6**
- What to install: **pip install -r requirements.txt**
- What to run: **python runner.py**
- Where to send notifications: **pynetscript:3GF5L6jlBvYl9TA5mrcJ87rq** 
  - Install Travis CI on [Slack](https://pynetscript.slack.com) and at some point it will output a slack channel to use.
  - Replace **pynetscript:3GF5L6jlBvYl9TA5mrcJ87rq** with your own channel.
  - Supports private channels.

