## INSTALLATION

```bash
pip3 install dreamav
```

## RUN
```bash
# start dreamav with downloading latest model
dreamav start

# if don't need to download latest model
dreamav start --no-download

# Stop dreamav
dreamav stop
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
```