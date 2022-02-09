# Volume Weighted Average Price - CoinBase WebSocket

## Description

The goal of this project is to create a real-time VWAP (volume-weighted average price) calculation engine. You
will use the coinbase websocket feed to stream in trade executions and update the VWAP for each trading pair
as updates become available.

Retrieve a data feed from the coinbase websocket and subscribe to the matches channel. Pull data for
the following three trading pairs:
- BTC-USD
- ETH-USD
- ETH-BTC

Calculate the VWAP per trading pair using a sliding window of 200 data points.

### Architecture design

TODO

### Future work

TODO

## Setup

The only thing that needs to be installed before running the code are the following dependencies 
- [websocket-client, kafka, pytest, pytest-cov]

Run this command (using python version +3.5) `pip install -r setup/requirements.txt` 


## Running it

There are 2 different ways of running it locally, 

- The first one and the simplier is running this command: `python main.py`
  - You'll need to define a environment variable to indicate the config file that will be used
    - `export CONFIG_FILE={your current path}/config/{file to select}.json`
  - This way of running the programma will print the vwap for each pair definiend in the config file
  
- The second and more complete way of running it is using this command: `docker compose up --build --remove-orphans`
  - Will initialize 4 services
    - a Kafka zookepper to administrate the Kafka cluster
    - 2 brokers to handler messages and replications
    - 1 coinbase listener that will produce the brokers messages load
  - Every time that the vwap of a pair will be calculated it will be sent to a topic identified by the pair
  - To consume those message you should execute consumer.py indicating the topic that you want to subscribe 
    - ex.: `python consumer.py --topic=ETH-USD`
    
    
## Tests

`python -m pytest --cov-report term-missing --cov=src`

![Alt text](https://user-images.githubusercontent.com/2218173/153129927-ad5edd5a-5f79-4928-97e9-596814a2eaeb.png?raw=true "Title")

