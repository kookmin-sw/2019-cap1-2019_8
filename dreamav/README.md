# DreamAV, Anti-virus for detecting malicious documents(PDF, MS Word)

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/kookmin-sw/2019-cap1-2019_8/blob/master/LICENSE)
[![PyPI Version](https://img.shields.io/badge/pypi-v0.2.3-blue.svg)](https://pypi.org/project/dreamav/)
[![Python Versions](https://img.shields.io/badge/python-3.6%20I%203.7-blue.svg)](https://pypi.org/project/lightgbm)


## INSTALLATION

```bash
pip3 install dreamav
```

## RUN
```bash
# Start dreamav 
dreamav start

# Stop dreamav
dreamav stop

# Update latest classifier
dreamav update

# Predict file
dreamav submit /path/to/file 

# Request scan to VirusTotal(need VirusTotal API key)
dreamav scan /path/to/file
```

## HOW TO INTERLOCK YOUR SERVER 


## REQUIREMENT
```
numpy==1.16.2
lightgbm==2.2.4
uWSGI==2.0.18
Flask==1.0.2
python-magic==0.4.15
Click==7.0
requests==2.21.0
tensorflow==1.13.1
keras==2.2.4
scikit-learn==0.20.0
```
