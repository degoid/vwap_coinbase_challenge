import argparse

from kafka import KafkaConsumer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic', default='BTC-USD', help='Topic to consume: {product}. Ex.: BTC-USD')
    args = parser.parse_args()

    consumer = KafkaConsumer(
        args.topic,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group-1',
        bootstrap_servers=['localhost:29092', 'localhost:39093']
    )

    for message in consumer:
        print(f"{message.topic} -> {str(message.value.decode('utf-8') )}")


if __name__ == "__main__":
    main()
