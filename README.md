
# Introduction

Dự án này là một dự án ứng dụng web. chủ yếu phục vụ cho các môn đồ án ở trường đại học.  
phù hợp cho sinh viên chuyên về các khoa sau:  
- Khoa học dư liệu.
- Trí tuệ nhân tạo.  

# Công nghệ sử dụng
- front-end: thuần chay html, css, js.
- back-end: django.
- database: mySQL hoặc bất cứ loại SQL nào (hiện đang dùng SQLite vì lý do chi phí và hiệu xuất cho demo).
- xây dựng và huấn luyện model: tensorflow, sklearn, nltk.
# các chức năng
- Chuẩn đoán bệnh, chức năng này được phân thành 2 chức năng nhỏ:
  - chuẩn đoán bằng chatBOT: người dùng sẽ chat với bot để chuẩn đoán.
  - chuẩn đoán bằng lựa chọn triệu chứng: người dùng sẽ lựa chọn các triệu chứng có sẵn để chuẩn đoán bệnh.
- tìm thuốc bằng hình ảnh: người dùng cung cấp hình ảnh của thuốc để hệ thống nhận diện và tìm kiếm trong cơ sở dữ liệu.
- tra cứu tài liệu: admin có thể viết các bài viết về các căn bệnh. người dùng có thể tìm kiếm và đọc bài viết này (thực chất thì nó là POST).
# Giải thích cách trình bày mã nguồn
- chatBOTService: xử lý chức năng chat, cung cấp các API để giao tiếp thông qua HTTP.
- front_end: cung cấp giao diện người dùng.
- medicineService: xử lý các công việc liên quan đến tìm kiếm thuốc bằng hình ảnh giao tiếp qua API hoặc helper.
- predictService: xử lý các chức năng của chuẩn đoán bệnh. Giao tiếp thông qua API hoặc helper.
- sqlService: làm việc với cơ sở dữ liệu. Giao tiếp thông qua helper.
- static: thư mục chứa file tĩnh như html, css, js, json, ảnh...
- utilities: chứa tool xử lý ảnh đầu vào.
# Cách cài đặt và sử dụng
- yêu cầu hệ thống: tốt nhất là có GPU (không thì lag điên vì đây là dự án deep learning xử lý ảnh), hệ điều hành window 10 trở lên.

- cài đặt python phiên bản 3.11 (3.13 lỗi vì một số thư viện không hỗ trợ phiên bản này)
- cài đặt các thư viện yêu cầu theo các bước sau:
  - tạo môi trường ảo: python -m venv env
  - tải các thư viện: pip install -r requirements.txt
  - nễu lỗi thì dùng: python pip install -r requirements.txt

- khởi chạy dự án: python manager.py runserver
  
