# README

## System requirements
- mongodb server at 127.0.0.1:27017
- quantz_repo

## Installation
```bash
git clone git@github.com:zhangyuz/quantz_repo.git
cd quantz_repo
pip install .
cd -
git clone git@github.com:zhangyuz/quantz_server.git
cd quantz_server
pip install .
cd -
# extra dependend on a customized graphene-mongo
git clone git@github.com:zhangyuz/graphene-mongo.git
cd graphene-mongo
pip install .
cd -
```

## Running
```bash
python app.py
```