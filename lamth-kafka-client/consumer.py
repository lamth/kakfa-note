from confluent_kafka import Consumer


conf = {'bootstrap.servers': "192.168.1.10:9092,192.168.1.11:9092,192.168.1.12:9092",
        'group.id': "lamth",
        'auto.offset.reset': 'latest'}

consumer = Consumer(conf)

consumer.subscribe(["lamth-testing-cluster"])


while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    print(msg.value().decode('utf-8'))

consumer.close()
