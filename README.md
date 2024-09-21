# Overview
The goal is to automate the process of finding arbitrage opportunities in sports betting. Currently, the repository scrapes half a dozen sports betting platforms for nfl game odds. The repository stores the scraping results in a psql database and queries the database to find arbitrage opportunities. 

# Dependencies
You will need to install a chromedriver (needed for selenium): https://googlechromelabs.github.io/chrome-for-testing/ \
You will need to setup a psql database either on your machine or from a hosting service and put the credentials in a .env file.\
You will need to have Python 3, I have only tested with 3.12.5 \
# Installing
```
git clone https://github.com/keeganasmith/arbitrage.git
cd arbitrage
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
# Running
```
python3 main.py
```
