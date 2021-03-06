# Tất cả những gì bạn cần biết về Kafka

Bài này như một bản tóm tắt lấy nội dung chủ yếu từ bài viết của anh Quang Vũ: https://vsudo.net/blog/kafka-la-gi.html

![](https://i.imgur.com/IhhQPwT.png)

Hầu như các công ty lớn trên thế giới đều sử dụng kafka trong nền tảng hạ tầng của mình. Vậy Kafka là gì và sức ảnh hưởng của nó ra sao.

## Kafka là gì?
Kafka:
- Nền tảng streaming phân tán
- Sản phẩm mã nguồn mở
- Có khả năng mở rộng, chịu tải cao
- Có độ trễ thấp khi xử lý
- Có khả năng lưu trữ message


## Kafka hoạt động như thế nào?
Kafka được xây dựng trên mô hình **Pub/Sub**.
Trong đó, các ứng dụng(**producers**) tạo ra các message(**records**) và gửi đến kafka node(**broker**) nơi mà các message được lấy bới các ứng dụng muốn nhận(**consumers**) message.
Các messages được gửi tới kafka node sẽ được lưu trong các **topics**, khi consumer đăng ký vào topic để nhận các tin nhắn mà producer gửi vào topic đó.
**Message** là các byte dữ liệu với kafka nên nó có thể là bất cứ loại dữ liệu gì.

![](https://i.imgur.com/RSLT3Ne.png)

Topic như là một danh mục để đẩy các message vào.

### Partition
Topics trong Kafka có thể có kích thước rất lớn. Do đó topic có thể được chia ra làm nhiều **partition** đặt trên các broker khác nhau để giúp bảo toàn dữ liệu đồng thời tăng hiệu năng xử lý dữ liệu.
Khi chia topic thành các partition, các consumer có thể đồng thời lấy dữ liệu của topic bằng cách lắng nghe trên các partition khác nhau cùng lúc.

Để tăng tính khả dụng, partition cũng có gí trị replica riêng của nó. Ví dụ với 3 broker:

![](https://i.imgur.com/BvZWepL.png)

Tất cá các message gửi đến một topic sẽ được gửi đến partition leader tương ứng, từ partition leader sẽ phối hợp để cập nhật dữ liệu mới lên các partition replicas. Nếu partition leader hỏng thì một trong các partition replica sẽ đảm nhận vai trò leader.

![](https://i.imgur.com/op9tk5e.png)

Vì điều này, các producer và Consumer nếu muốn ghi hoặc nghe thì phải biết đâu là partition leader. Thông tin về partition leader được lưu trữ dạng metadata trong dịch vụ là **Zookeeper**. 

## Cấu trúc dữ liệu log trong Kafka
**log** là một chìa khóa chính dẫn tới khả năng mở rộng và hiệu năng cao của Kafka. Ở đây là nói đến **Cấu trúc dữ liệu log**.

Dạng cấu trúc dữ liệu log có thứ tự nhất quán cho các record, chỉ hỗ trợ nối(append) thêm chứ không cho sửa hay xóa các record.

![](https://i.imgur.com/Qkt714z.png)

Mỗi nguồn dữ liệu sẽ ghi message vào log. Một hoặc nhiều consumer sẽ đọc message từ log tại thời điểm họ lựa chọn(có thể đọc tất cả message trong log, hoặc chỉ đọc các message sau thời điểm mà consumer nghe vào topic,...)

Mỗi entry trong log được định danh vởi một con số gọi là offset (nó gần như là số thứ tự vậy)

Vì offset chỉ có thể duy trì trên từ node/broker, do dó kafka chỉ đảm bảo dữ liệu được sắp xếp theo thứ tự trong mỗi partition.

## Parsistence data trong Kafka
Kafka lưu trữ dữ liệu trên disk(không hề lưu trên ram), và vì dữ liệu được sắp xếp có thứ tự trong cấu trúc log, cho phép kafka tận dụng tối đa khả năng đọc và ghi lên disk một cách tuần tự.

Một vài lý do sau đây chỉ ra vì sao mà lưu trữ trên disk nhưng kafka vẫn có hiệu năng cao:
1. Kafka có một giao thức để nhóm các message lại với nhau - **Batch**. Khi nhóm các message lại với nhau trong một lần ghi hoặc đọc, thay vì đọc, ghi từng message, Kafka có thể sử lý chúng cùng một lúc, giảm thiểu chi phí sử dụng tài nguyên mạng, server. Nhưng lưu ý cơ chế này vì tổng thể là hiệu năng tăng nhưng một số message có thể chậm hơn thông thường.
2. Kafka phụ thuộc khá nhiều vào pagecache của hệ điều hành cho việc lưu trữ dữ liệu và sử dụng ram trên một máy tính hiệu quả.
3. Kafka lưu trữ dữ liệu dưới dạng nhị phân trong xuyên suốt quá trình(producer> broker > consumer) làm cho nó có thể tận dụng cơ chế zero-copy. Nghĩa là khi hệ điều hành copy dữ liệu từ pagecache trực tiếp sang socket mà không cần qua xử lý trung dam là Kafka.
4. Khả năng đọc ghi dữ liệu tuyến tính. Vấn đề làm cho lưu trữ trên disk chậm chủ yếu hiện nay là do việc tìm kiếm dữ liệu nhiều lần trên disk. Kafka với khả năng đọc ghi dữ liệu tuyến tính có thể tận dụng tối đa hiệu xuất trên disk.

## Consumer và Consumer Group

Comsumer đọc messages từ bất cứ partition nào cho phép bạn mở dộng lượng message được sử dụng tương tự như các các producer cung cấp message.

Các consumer cũng được tổ chức thành các consumer groups cho một topics cụ thể - mỗi partition tại một thời điểm chỉ có thể được đọc từ tối đa 1 comsumer trong 1 consumer group. Từ đó tránh việc trong cùng consumer group lại có hai comsumer cùng đọc tin nhắn trên một partition và sử lý dữ liệu tương tự.
- Nếu bạn có số consumer > số partition, khi đó một số consumer sẽ ở chế độ rảnh rỗi bởi vì chúng không có partition nào để xử lý.
- Nếu bạn có số partition > số consumer, khi đó consumer sẽ nhận các message từ nhiều partition.
- Nếu bạn có số consumer = số partition, mỗi consumer sẽ đọc message theo thứ tự từ 1 partition.

![](https://i.imgur.com/SzpsFZj.png)

Như ví dụ ở ảnh trên, Kafka cluster này có 2 broker/server, server 1 có partition 0 và 3, server 2 có partition 1 và 2. Có hai consumer group là A có 2 consumer và consumer group B có 4 consumers. Để cho hợp lý nhất thì vì consumer group A có 2 consumer vậy mỗi consumer trong group A nên đọc từ 2 partition, consumer group B có 4 consumer -bằng số lượng partition vậy mỗi consumer trong group B nên nghe một partition.

Kafka không lưu thông tin về hành vi của consumer, nó không biết consumer đã đọc những record nào. Do đó Kafka sẽ lưu trữ message theo một khoảng thời gian được cấu hình từ trước. Việc lấy message nào là do consumer quyết định, khi muốn đọc message từ kafka, consumer sẽ thăm dò xem Kafka có message mới không và cho Kafka biết nó muốn lấy message nào. Việc lưu lại message trong một khoản thời gian cũng giúp Consumer có thể đọc lại các message cũ trong trường hợp gặp gián đoạn hoặc lỗi.

Ví dụ: nếu Kafka được cấu hình để giữ các messages tồn tại trong một ngày và consumer bị down lâu hơn 1 ngày, khi đó consumer sẽ mất message. Tuy nhiên, nếu consumer chỉ bị down trong khoảng 1 giờ đồng hồ, khi đó nó hoàn toàn có thể bắt đầu đọc lại message từ offset mới nhất.


## Zookeeper và vai trò của nó

Zookeeper đóng vai trò là nơi lưu trữ dữ liệu phân tán dạng key-value. Nó được tối ưu hóa cho tác vụ đọc nhanh nhưng ghi chậm. Kafka sử dụng Zookeeper để thực hiện việc bầu chọn leader của broker và partition. Zookeeper được thiết kế cho khả năng chịu lỗi cao, do đó Kafka phụ thuộc khá nhiều vào nó.

Zookeeper cũng được sử dụng để lưu trữ tất cả các metadata như:
- Offset cho mỗi partition của consumer group
- ACL(Access Controll List) - được sử dụng để kiểm soát quyền truy cập/ủy quyền vào các tài nguyên trong Kafka
- Quota của consumer/producer -số lượng message tối đa mỗi giây mà consumer/producer có thể đọc, ghi.
- Thông tin partition leader và trạng thái của chúng.


Producer và consumer không tương tác trực tiếp với Zookeeper để biết partition leader hay những metadata khác mà chúng truy vấn thông qua Kafka, Kafka sẽ tương tác trực tiếp với Zookeeper để lấy metadata và trả về cho chúng.


## Kết luận.

Kafka đang nhanh chóng trở thành trụ cột của đường ống dữ liệu đối với bất kỳ tổ chức nào. Kafka cho phép bạn có một lượng lớn các messages đi qua một phương tiện tập trung và lưu trữ chúng mà không cần phải lo lắng gì về những vấn đề như hiệu suất hay mất mát dữ liệu. Kafka có thể là thành phần trung tâm trong mô hình kiến trúc hướng sự kiện (event-driven) và cho phép bạn phân tách giữa ứng dụng này với ứng dụng khác.