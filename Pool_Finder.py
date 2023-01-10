import requests
import pandas as pd
import datetime


link = f'https://api-osmosis.imperator.co/apr/v2/all'

url = requests.get(link)
data = url.json()
CONST_POOLS = [1, 10, 497, 604, 674, 678, 712, 812]
main = []

def main():
    
  format(parsing(data))

def parsing(data) -> list:
    
    master_list = []
    for d in data:
        for i in range(len(CONST_POOLS)):
            if d["pool_id"] == CONST_POOLS[i]:
                master_list.append([d["pool_id"],
                    d["apr_list"][0]["apr_1d"],
                    d["apr_list"][0]["apr_7d"],
                    d["apr_list"][0]["apr_14d"],
                    d["apr_list"][0]["apr_superfluid"]])
                    
    return master_list
                
def format(master: list):
    
    clean = pd.DataFrame(master)
    clean.columns = ['ID', '1D', '7D', '14D', 'SPRFL']
    csvname = "apr-" + datetime.datetime.today().strftime('%Y-%m-%d') + ".csv"
    clean.to_csv(csvname)
    
main()
