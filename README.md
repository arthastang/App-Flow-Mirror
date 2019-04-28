![py3.6](https://img.shields.io/badge/python-3.6-blue.svg)
![MIT](https://img.shields.io/github/license/mashape/apistatus.svg)

# APP Flow Mirror
It's a tool to recognize running apps in smartphone and IoT devices in LAN realtime.
## example
![demo video](example/app flow mirror.mp4)
## how to use
- start up your raspberry pi
- plug a Wireless network adapter on raspberry pi
- configure raspberry as an AP
- connect your smartphone and IoT devices to the AP
- start up this tool and use your smartphone
## install
This tool is running on raspberry pi, write in python3, use the flask web framework.
```bash
# install depends
pip3 install flask scapy scapy-http
# download this tool
git clone https://github.com/arthastang/App-Flow-Mirror
cd App-Flow-Mirror
python3 app-flow-mirror.py
```
## usage
- open your browser，and input localhost:5000.
- click *start scan* button
- wait a moment you will get the scan result.
