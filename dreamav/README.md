# DreamAV, Anti-virus for detecting malicious documents(PDF, MS Word)

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/kookmin-sw/2019-cap1-2019_8/blob/master/LICENSE)
[![PyPI Version](https://img.shields.io/badge/pypi-v0.2.5-blue.svg)](https://pypi.org/project/dreamav/)
[![Python Versions](https://img.shields.io/badge/python-3.6-blue.svg)](https://pypi.org/project/lightgbm)


## INSTALL

```bash
pip3 install dreamav
```

## HOW TO USE
```bash
# Start dreamav 
dreamav start

# Stop dreamav
dreamav stop

# Predict file
dreamav submit /path/to/file 

# Request scan to VirusTotal(need VirusTotal API key)
dreamav scan /path/to/file
```

## HOW TO INTERLOCK WITH YOUR SERVER
We provide results to json like below, select the results of model you want  
```buildoutcfg
# PDF
{
    "result":{
        "LightGBM": PROB,
        "XGBoost": PROB,
        "DT": PROB,
        "RF": PROB,
    }
}

# MS Word(DOC)
{
    "result":{
        "DL": PROB
    }
}
```
in your server, upload file to engine like below, and set a threshold.
```buildoutcfg
# example/django
req = requests.post("http://localhost:8080/dream_upload", \
                            files={"file": self.request.FILES["file"]})
if req.status_code == 200:
    result = req.json()

# set threshold(recommend=0.5)
th = 0.5    
if float(result["result"]["LightGBM"]) < th:
    ...
```

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

## Contact Us
If you find some false positive or false negative files, please contact us
```buildoutcfg
Email: vmfn0401@gmail.com
slack: dreamav.slack.com
```

## License
This project is licensed under the terms of the MIT license. See [LICENSE](https://github.com/kookmin-sw/2019-cap1-2019_8/blob/master/LICENSE) for additional details.