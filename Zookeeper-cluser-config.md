# Cấu hình Cụm zookeeper

Tiếp tục [bài viết trước](Kafka-install-Centos7.md), bài viết này sẽ là tìm hiểu về cách cấu hình zookeeper theo cụm gồm 3 node, và cấu hình 3 node kafka sử dụng 3 node zookeeper này.

Sau khi cấu hình kafka ở bài trước, chúng ta đã cài đặt cả zookeeper trên cả 3 node.

## Cấu hình zookeeper đơn.

Trên server 1, sửa file cấu hình của zookeeper thành:
```
tickTime=2000
dataDir=/tmp/zookeeper
clientPort=2181
maxClientCnxns=60
```
Giải thích 
`tickTime`: được tính theo mili giây, chỉ định thời gian giữa các heartbeat để kiểm tra trạng thái giữa các Zookeeper.
Ở đây cấu hình đang để thời gian này là 2000 mili giây, đây là thời gian khuyến nghị

`dataDir`: chỉ định thư mục được sử dụng để lưu trữ snapshot của database trong bộ nhớ và log giao dịch. có thể chỉ định thư mục riêng cho log giao dịch
Ở đây đang cấu hình dataDir là /tmp/zookeeper

`clientPort`: Cổng được sử dụng cho các kết nối từ client.
Ở đây đang để clientPort là 2181 cũng là port mặc định.

`maxClientCnxns`: giới hạn số lượng kết nối tối đa của client.
Ở đây đang để  tối đa là 60 client connect, đủ để lab.


Lưu cấu hình. Sau đó khởi động lại zookeeper bằng lệnh:
```
sudo systemctl restart zookeeper
```

Sau khi khởi động lại, kiểm tra zookeeper bằng lệnh:
```
/home/kafka/kafka/bin/zookeeper-shell.sh localhost:2181
```
Nếu xuất hiện `Connected` trong output của câu lệnh trên tức zookeeper đã chạy và sẵn sàng.



## Cấu hình Zookeeper cluster

Phần trước đã cấu hình để có thể chạy một server zookeeper chạy một mình, tiến hành cấu hình tương tự cho các node khác đến bước zookeeper có thể chạy và sẵn sàng.

Để cấu hình các node zookeeper này tham gia vào một cluster, sửa file cấu hình (/home/kafka/kafka/config/zookeeper.properties), bổ xung các cấu hình cho `initLimit` , `syncLimit` và các server trong túc số, ở cuối file. Sửa file cấu hình của zookeeper trên tất cả các server thành:
```
tickTime=2000
dataDir=/tmp/zookeeper/
clientPort=2181
maxClientCnxns=60
initLimit=10
syncLimit=5
server.1=zookeeper1:2888:3888
server.2=zookeeper2:2888:3888
server.3=zookeeper3:2888:3888
```

Giải thích:
- `initLimit`: là thời gian time out dùng để giới hạn độ dài thời gian Zookeeper trong cụm kết nối đến leader.
- 
`syncLimit`: 