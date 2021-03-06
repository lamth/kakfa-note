# Cài đặt kafka

### Tạo người dùng kafka

```
sudo useradd kafka -m
echo 'kafkalab'| sudo passwd kafka --stdin
sudo usermod -aG wheel kafka
su -l kafka
```

### Tải và giải nén


Trong home folder của user kafka
Tải và giải nén kafka:
Tạo thư mục để tải file nén về
```
mkdir ~/Downloads
```
Tải về
```
curl "https://mirror.downloadvn.com/apache/kafka/2.7.0/kafka_2.13-2.7.0.tgz" -o ~/Downloads/kafka_2.13-2.7.0.tgz
```

Tạo thư mục ~/kafka và giải nén kafka vào thư mục này:
```
mkdir ~/kafka && cd ~/kafka
tar -xvzf ~/Downloads/kafka_2.13-2.7.0.tgz --strip 1
```


### Cài đặt java
Update yum		
```sh
sudo yum update # sợ vl
```		

Cài đặt jdk 11		
```sh	
sudo yum install java-11-openjdk-devel -y
sudo yum install java-11-openjdk -y	
```		
### Cấu hình Kafka server
Chỉnh sửa cấu hình của kafka server bằng cách chỉnh sửa file sau
```
~/kafka/config/server.properties
```
Ví dụ cấu hình cho phép xóa topic: Thêm dòng sau vào cuối file:
```
delete.topic.enable = true
```

### Tạo service cho zookeeper và kafka để quản lý với systemd
Trên Terminal của user kafka:
Tạo file service cho zookeeper, chạy lệnh sau:
```
sudo tee /etc/systemd/system/zookeeper.service << EOF
[Unit]
Requires=network.target remote-fs.target
After=network.target remote-fs.target

[Service]
Type=simple
User=kafka
ExecStart=/home/kafka/kafka/bin/zookeeper-server-start.sh /home/kafka/kafka/config/zookeeper.properties
ExecStop=/home/kafka/kafka/bin/zookeeper-server-stop.sh
Restart=on-abnormal

[Install]
WantedBy=multi-user.target
EOF
```

Tạo file service cho kafka:
```
sudo tee /etc/systemd/system/kafka.service << EOF
[Unit]
Requires=zookeeper.service
After=zookeeper.service

[Service]
Type=simple
User=kafka
ExecStart=/bin/sh -c '/home/kafka/kafka/bin/kafka-server-start.sh /home/kafka/kafka/config/server.properties > /home/kafka/kafka/kafka.log 2>&1'
ExecStop=/home/kafka/kafka/bin/kafka-server-stop.sh
Restart=on-abnormal

[Install]
WantedBy=multi-user.target
EOF
```

sudo systemctl start kafka



## Kiểm tra

Kiểm tra Kafka bằng cách gửi và nhận message qua nó bằng:
- Producer: được sử dụng để gửi bản ghi và dữ liệu vào topic
- Consumer: được sử dụng để đọc tin nhắn, bản ghi từ topic.


Đầu tiên, Tạo một topic sử dụng script `kafka-topics.sh`, phải truyền vào địa chỉ của zookeeper:
```
cd /home/kafka
./kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic TutorialTopic
```

Có thể tạo một producer sử dụng command line sử dụng `kafka-console-producer.sh`:
```
cd /home/kafka
echo "Hello Kafka!" | ./kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic TutorialTopic > /dev/null
```

Tiếp theo tạo một consumer, sử dụng script `kafka-console-consumer.sh`:
```
cd /home/kafka
./kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic TutorialTopic --from-beginning
```
Chú ý rằng tùy chọn `--from-beginning` là để consumer lấy tất cả message của topic từ đầu.
Nếu không có lỗi thì rõ ràng nó sẽ hiện dòng này rồi:)
```
Hello Kafka!
```

Ở cả hai câu lệnh trên, Producer và Consumer sẽ tiếp tục hoạt động, producer vẫn nhận input và consumer vẫn đọc và in ra output. Bạn có thể tiếp tục test bằng cách nhập thêm tin nhắn vào producer và kiểm tra nhận tin nhắn trên consumer. Khi test xong ấn `Ctrl + C` để tắt hai chương trình này.

## Càì KafkaT

tool để xem kafka tổng quan hơn.

Cài đặt một số gói yêu cầu:
```
sudo yum install ruby ruby-devel make gcc patch
```
Cài đặt Kafka bằng lệnh gem:
```
sudo gem install kafkat
```
Tạo file config:
```
vi ~/.kafkatcfg
```




## Tạo một cụm nhiều node

Nếu mà tạo một cluster với nhiều node/broker. sử dụng nhiều máy Centos 7 và thực hiện lại các bước ở phía trên cho từng máy chủ. Thêm vào đó, phải thay đổi  một số thông tin trong file *server.properties* ở các dòng sau đây:
- giá trị của *broker.id*. Giá trị này cần là duy nhất cho từng node trong một cluster. Nó dùng để xác định các node trong một cluster ví dụ `server1`, `server2`,...
- giá trị *zookeeper.connect* nên thay đổi để tất các các node trỏ về cùng một Zookeeper. theo dạng <HOSTNAME/IP_ADDRESS>:<PORT>




