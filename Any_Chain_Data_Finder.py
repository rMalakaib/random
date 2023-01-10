import pandas as pd
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

CONST_DENOM = "usd"
CONST_MARKET = True

def main():
    month = input("Input month you're reporting on here: ")
    start = input("Input starting Timestamp: ") 
    stop = input("Input ending Timestamp: ") 
    chain_id = input("Input the Chains you're looking for seperated by spaces: ").split(" ") 
    keys = input("Input the Keys you are looking for seperated by spaces (don't input timestamp): ").split(" ")
    
    # #TEST VARIABLES
    # month = "nov"
    # start = 1667304000
    # stop = 1669809600
    # chain_id = ["cosmos","osmosis","evmos" , "juno-network", "sifchain", "stargaze", "akash-network", "secret", "kava", "ethereum", "bitcoin"]
    # keys = ["prices","market_caps"]
    
    
    d_csv = 'D_Eco_' + month + '22'  + '.csv'
    s_eco = 'D_Eco_S' + '-' + month + '22' + '.csv'
    
    
    master = parsing(start, stop, chain_id, keys)
    write(master, d_csv, s_eco)


def parsing(start: str, stop: str, chain_id: list[str], keys: list[str]):
    
    # Chain Id is the first for loop because there could be many chain ID's that all have the same Key values
    raw_data = cg.get_coin_market_chart_range_by_id(id= chain_id[0],
                                                    vs_currency= CONST_DENOM,
                                                    from_timestamp= start, 
                                                    to_timestamp= stop, 
                                                    include_market_cap= False)


    # I automatically assume you always want the timestamp so I do that opration here and intilize it to a dict.
    master_dict = {"timestamp":[(raw_data[keys[1]][i][0]) for i in range(len(raw_data["prices"]))]}
    # this is called a composite literal a simpler example of this is this:
    # [letter (for letter in word)] read the for loop first. for letter in word append letter to list
    # more complex example:
    # [letter for letter in word if letter == "a"] read the for loop then the conditional then the append.
    #  for letter in word if letter == "a" then append letter to list
            
    
    for chainID in chain_id:

        raw_data = cg.get_coin_market_chart_range_by_id(id= chainID,
                                                    vs_currency= CONST_DENOM,
                                                    from_timestamp= start, 
                                                    to_timestamp= stop, 
                                                    include_market_cap= CONST_MARKET)
        title_list = []
        
        for key in keys:
                
            
            if len(title_list) < 1:
                title_list.append([(key+"_"+chainID) for key in keys]) 
                # initializing the title list but only once

            local_list = []
            for i in range(len(raw_data["prices"])):
                
                    local_list.append(raw_data[key][i][1])
                    # appending key data to local list
            
            master_dict[title_list[0][keys.index(key)]] = local_list
            # assigning the key value to an array and its key_pair .aka local list
            
            # I removed conjoining the data frames and just appended all the data to a dict with unique key values
            # This makes the code more efficient operationally speaking.
            
    
    smallest_set = 0
    for key in master_dict:
        if len(master_dict[key]) < smallest_set or smallest_set == 0:
            smallest_set = len(master_dict[key])  
    for key_pair in master_dict.items():
        key, pair = key_pair
        master_dict[key] = pair[:smallest_set]
    # in order to create a DataFrame all arrays have to be the same length
    # if you are joining dataframes this is not true but if you are intializing a new one then it is
    # the above code takes the smallest length of a list with in the data set in the first for loop
    # then changes each data set to the smallest length
    
    return pd.DataFrame(master_dict)

def write(master: pd.DataFrame, d_csv: str, s_eco: str):
    
    date = pd.to_datetime(master["timestamp"], unit="ms")
    master["timestamp"] = date
    
    master.to_csv(d_csv)
    master.describe().to_csv(s_eco)
    # I don't understand the metric that you created so I'm gonna stop here.


if __name__ == "__main__":
    main()

