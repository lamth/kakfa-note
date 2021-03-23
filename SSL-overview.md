# Tổng quan về SSL sử dụng để mã hóa

Mặc định Kafka giao tiếp sử dụng `PLAINTEXT`, tức là tất cả dữ liệu được gửi đi trong dạng văn bản(clear text). Đễ mã hóa giao tiếp, tất cả các thành phần của Kafka cần phải cấu hình để sử dụng SSL.

Secure Socket Layer(SSL ) là tiền nhiệm của Transport Layer Sercure(TLS). Tuy SSL không còn được sử dụng nhưng vì lý do lịch sử  mà Kafka sử dụng thuật ngữ "SSL" thay vì "TLS" cho cấu hình và code. Bài này sẽ chỉ sử dụng thuật ngữ SSL.

SSL bao gồm cả cơ chế mã hóa và xác thực.

Bật mã hóa với SSL có thể làm giảm hiệu năng tổng thể của kafka do quá trình mã hóa.

SSL sử dụng cặp private-key và certificate trong suốt quá trình SSL handshake.

- Mỗi broker cần một cặp private-key và certificate, client sẽ sử dụng certificate để xác thực broker.
- Mỗi client cần một cặp private-ket và certificate, và nếu client authentication bật thì broker sẽ sử dụng certificate để xác thực danh tính client.

Mỗi broker hay client đều cần cấu hình một truststore, mà nó được sử dụng để xác định certificate(của broker hay client) nào mà chúng có thể tin tưởng(xác thực). Có nhiều cách cấu hình truststore. Ví dụ:
- Truststore chứa một hoặc nhiều certificate, broker hoặc client sẽ tin tưởng bất kì certificate nào được liệt kê trong truestore.
- truestore chứa một Certificate Authority(CA): broker và client sẽ tin tưởng bất kì certificate nào được đăng ký bởi CA trong truststore.

Sử dụng phương thức CA sẽ thuận tiện hơn vì khi thêm một broker hoặc client mới sẽ không cần thay đổi truststore.

![](https://i.imgur.com/AasYmH6.png)

Tuy nhiên, với phương thức CA, Kafka không hỗ trợ thuận tiện cho việc chặc xác thực các broker hay client mà trước đây đã được trust sử dụng cơ chế này(các certificate bị revoke sử dụng Certificate Revocation Lists or the Online Certificate Status Protocol), do đó cần can thiệp vào cơ chế Ủy quyền để chặn truy cập của chúng.

Ngược lại thì nếu sử dụng truststore chứa một hoặc nhiều certificate, việc chặn xác thực những client hoặc broker này chỉ đơn giản là xóa certificate của broker hay client này trong truststore.

