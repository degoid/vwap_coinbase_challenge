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

The only thing that needs to be installed before running the code is the following dependencies.
- [websocket-client, kafka, pytest, pytest-cov]

And then, run this command (using python version +3.5) `pip install -r setup/requirements.txt` 


## Running it

There are two different ways of running it locally, 

- The first one and the more straightforward is running this command: `python main.py`
  - You'll need to define an environment variable to indicate the config file that will be used.
    - `export CONFIG_FILE={your current path}/config/{file to select}.json`
  - This way of running the programma will print the vwap for each pair defined in the config file.
    Example file:
    ```
    {
      "coinbase_url": "wss://ws-feed.pro.coinbase.com",
      "max_size": 200,
      "products": ["ETH-BTC", "ETH-USD", "BTC-USD"],
      "brokers": {
        "broker_1:9092": ["ETH-BTC", "ETH-USD"],
        "broker_2:9093": ["BTC-USD"]
      },
      "log_level": "info",
      "kafka_time": 30
    }

    ```
  
- The second and more complete way of running it is using this command: `docker compose up --build --remove-orphans`
  - Will initialize four services
    - a Kafka zookepper to administrate the Kafka cluster
    - 2 brokers to handler messages and replications
    - 1 coinbase listener that will produce the brokers' messages load
  - Each time that the vwap of a pair is  calculated, it will be sent to a topic identified by the pair, for instance: ETC-USD
  - To consume those message you should execute consumer.py indicating the topic that you want to subscribe 
    - ex.: `python consumer.py --topic=ETH-USD`
    
    
## Tests

`python -m pytest --cov-report term-missing --cov=src`

![Alt text](https://user-images.githubusercontent.com/2218173/153129927-ad5edd5a-5f79-4928-97e9-596814a2eaeb.png?raw=true "Title")

