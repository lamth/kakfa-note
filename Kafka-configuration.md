# Một số cấu hình trong kafka

Chú thích về các kiểu dữ liệu
- string: chuỗi
- int: số tự nhiên
- boolean: giá trị là true hoặc false

`zookeeper.connect`
  Danh sách các host zookeeper mà broker này sẽ đăng ký vào. Nên cấu hình chỏ đến tất cả các hosts trong Zookeeper cluster.
  - Kiểu dữ liệu: string
  - Độ quan trọng: cao

`broker.id`
  Số dùng để định danh broker. Trong một Kafka cluster, các broker không thể có broker.id giống nhau.
  - Kiểu dữ liệu: int
  - Độ quan trọng: cao

`log.dirs`
  Thư mục mà dữ liệu log của Kafka được đặt vào.
  - Kiểu dữ liệu: string
  - Mặc định: “/tmp/kafka-logs” 
  - Độ quan trọng: high

`listeners`
  Danh sách các URI(địa chỉ bao gồm giao thức) được phân cách bằng dấu phẩy mà 
  - Kiểu dữ liệu: string
  - Mặc định: `PLAINTEXT://host.name:port`
  - Độ quan trọng: cao

`advertised.listeners`
  Các listeners được gửi đến zookeeper để cho người dùng sử dụng, nó có thể sẽ cần khác so với interface mà broker bind ra.
  - Kiểu dữ liệu: string
  - Mặc định: `listeners`
  - Độ quan trọng: cao

`num.partitions`
  Số lượng partition mặc định cho một topic được tạo tự động.
  - Kiểu dữ liệu: int
  - Mặc định: 1
  - Độ quan trọng: bình thường

#### Một số cấu hình liên quan đến nhân bản(replication config).

`default.replication.factor`
  Số nhân bản mặc định cho một topic được áp dụng cho topic mà được tạo tự động. Nên thiết lập ít nhất là 2.
  - Kiểu dữ liệu: int 
  - Độ quan trọng: bình thường

`min.insync.replicas`
  Số lượng replica nhỏ nhất trong ISR(in sync replica) cần để thực hiện một yêu cầu sản xuất với `required.acks=-1`.
  - Kiểu dữ liệu: int
  - Mặc định: 1
  - Độ quan trọng: trung bình

`unclear.leader.election.enable`
  Cho biết liệu có nên cho phép các bản sao(replica) mà không có trong IRS được bật chọn làm leader, ngay cả khi nó có thể dẫn tới việc mất dữ liệu.
  - Kiểu dữ liệu: boolean
  - Mặc định: false
  - Mức độ quan trọng: trung bình.


## Ví dụ về file cấu hình cho mô hình Kafka cluster gồm 3 Kafka broker và một Zookeeper.
#### Mô hình

![](https://i.imgur.com/ts4Wh6n.png)

#### Các file cấu hình
`File /etc/hosts trên tất cả các server`
```
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6

192.168.50.10 kafka1
192.168.50.11 zookeeper kafka2
192.168.50.12 kafka3
```


`Cấu hình cho Kafka thứ nhất`
```conf
broker.id=1
port=9092
advertised.listeners=PLAINTEXT://kafka1:9092
zookeeper.connect=zookeeper:2181
log.dirs=/tmp/kafka-logs
```

`Cấu hình cho Kafka thứ hai`
```conf
broker.id=2
port=9092
advertised.listeners=PLAINTEXT://kafka2:9092
zookeeper.connect=zookeeper:2181
log.dirs=/tmp/kafka-logs
```


`Cấu hình cho Kafka thứ ba`
```conf
broker.id=3
port=9092
advertised.listeners=PLAINTEXT://kafka3:9092
zookeeper.connect=zookeeper:2181
log.dirs=/tmp/kafka-logs
```

`Cấu hình cho zookeeper`
```conf
dataDir=/tmp/zookeeper
clientPort=2181
maxClientCnxns=0
admin.enableServer=false
```