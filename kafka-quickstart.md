    # Tìm hiểu qua về Kafka		
￼
Tài liệu tiếng Anh: https://kafka.apache.org/quickstart		
Phiên bản cài đặt: kafka_2.13-2.7.0
Hệ điều hành: Ubuntu 18.04		
￼
## Bước 1: Lấy Kafka		
[Tải] Kafka:		
Vì bài viết này cài phiên bản 2.13-2.7.0, nên có thể tải sử dụng lệnh sau:		
```		
sudo apt install wget -y		
wget https://mirror.downloadvn.com/apache/kafka/2.7.0/kafka_2.13-2.7.0.tgz		
```		
Giải nén:		
```		
tar -xzf kafka_2.13-2.7.0.tgz		
cd kafka_2.13-2.7.0		
```		


## Bước 2: Bắt đàu môi trường Kafka		
*NOTE: Môi trường của bạn phải có Java 8+ đã được cài đặt.*		
￼
<details><summary>Cài đặt Java </summary>		
- Update cache apt:		
```		
sudo apt update		
``		
Kiểm tra xem đã có java chưa:		
```		
java -version		
```		
Nếu không có java, output sẽ hiển thị tương tự như sau:		
```sh	
Output		
Command 'java' not found, but can be installed with:		
apt install default-jre		
apt install openjdk-11-jre-headless		
apt install openjdk-8-jre-headless		
```		
Chạy lệnh sau để cài đặt Java Runtime Environment mặc định mà sẽ cài Java từ OpenJDK 11:		
```		
sudo apt install default-jre		
```		
JRE sẽ cho phép chạy hầu hết các ứng dụng Java.		
Kiểm tra cài đặt hoàn tất với lệnh:		
```		
java --version		
```		
</details>		

<details><summary>Bonus: Cài đặt Java trên CentOS 7 </summary>		

Update yum		
```sh
yum update # sợ vl		
```		

Cài đặt jdk 11		
```sh	
sudo yum install java-11-openjdk-devel		
```		
```sh	
sudo yum install java-11-openjdk		
```		
</details>		

Chạy các lệnh sau theo thứ tự để đảm bảo tất cả các dịch vụ hoạt động đúng thứ tự		
```sh
# Start the ZooKeeper service		
# Note: Soon, ZooKeeper will no longer be required by Apache Kafka.		
bin/zookeeper-server-start.sh config/zookeeper.properties		
```		
Tiếp theo, mở một cửa sổ terminal nữa và chạy lệnh sau(nhớ cd vào thư mục kafka vừa giải nén):		
```sh
# Start the Kafka broker service		
bin/kafka-server-start.sh config/server.properties		
```		

Sau khi chạy xong các lệnh này thì một môi trường Kafka cơ bản được chạy và sẵn sàng sử dụng.		

## Bước 3. Tạo một topic để chứa các event		
Kafka là một nền tảng phát trực tiếp các event mà cho phép đọc viết, lưu trữ và xử lý **event**(hay còn gọi là các bản ghi, hay tin nhắn-message) trên nhiều máy.	

Event có thể là thông tin thanh toán, vị trí địa lý của thiết bị điện thoại, thông số đo đạc được từ các cảm biết trên các thiết bị IOT,... Những event này được ổ chức và lưu trữ trong các **topic.** Có thể coi một topic là một thư mục trên hệ thống và event là các file trong thư mục đó.		

Vì thế, trước khi tạo được event đầu tiên thì phải tạo một topic. Mở một cửa sổ terminal nữa và cd đến thư mục chứa kafka, chạy lệnh sau để tạo topic:		
```		
bin/kafka-topics.sh --create --topic quickstart-events --bootstrap-server localhost:9092		
```		

Để hiện thị tất cả các tùy chọn khi chạy các script của kafka, chạy script đó và không điền bất cứ tùy chọn nào.		
```		
bin/kafka-topics.sh		
```

## Bước 4: Viết Event vào Topic


