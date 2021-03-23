from confluent_kafka import Producer
import socket
import sys, select


conf = {'bootstrap.servers': "192.168.1.10:9092,192.168.1.11:9092,192.168.1.12:9092" ,'client.id': socket.gethostname()}

producer = Producer(conf)

while True:
  socket_list = [sys.stdin]
  read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
  for sock in read_sockets:
    message = sys.stdin.readline()
    producer.produce("lamth-testing-cluster", key=None, value=message)

#listm = ["cc", "al", "bl", "cl", "dl"]
#
#for i in listm:
#    producer.produce("lamth-testing-cluster", key=None, value=str(i))
#    producer.flush()
