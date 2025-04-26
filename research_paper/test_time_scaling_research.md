# Nghiên cứu về Test-Time Scaling cho bài toán toán học

## 1. Tổng quan về Test-Time Scaling

Test-Time Scaling (TTS) là một phương pháp tối ưu hóa tài nguyên tính toán trong quá trình suy luận (inference) của các mô hình ngôn ngữ lớn (LLMs). Thay vì tập trung vào việc tăng kích thước mô hình (train-time scaling), TTS tập trung vào việc tối ưu hóa cách phân bổ tài nguyên tính toán trong quá trình suy luận dựa trên độ phức tạp của nhiệm vụ.

### 1.1. Ý tưởng cốt lõi

Ý tưởng cốt lõi của TTS là:
- Các bài toán đơn giản chỉ cần ít tài nguyên tính toán (Fast Thinking)
- Các bài toán phức tạp cần nhiều tài nguyên tính toán hơn (Slow Thinking)
- Mô hình nên có khả năng tự động xác định mức độ tài nguyên cần thiết dựa trên độ phức tạp của bài toán

### 1.2. Lợi ích của Test-Time Scaling

- **Hiệu quả tài nguyên**: Chỉ sử dụng nhiều tài nguyên khi thực sự cần thiết
- **Thời gian phản hồi tối ưu**: Trả lời nhanh cho các câu hỏi đơn giản, dành thời gian cho các câu hỏi phức tạp
- **Cân bằng giữa hiệu suất và chi phí**: Đạt được hiệu suất tốt nhất với chi phí tính toán hợp lý

## 2. Các phương pháp Test-Time Scaling hiện đại

### 2.1. Thinking-Optimal Scaling (TOPS)

Theo nghiên cứu "Towards Thinking-Optimal Scaling of Test-Time Compute for LLM Reasoning" (Yang et al., 2025), TOPS là một chiến lược cho phép LLMs tự quyết định số lượng token cần thiết để giải quyết một bài toán cụ thể.

#### 2.1.1. Phát hiện chính

- Việc mở rộng quá mức độ dài của Chain of Thought (CoT) có thể gây tác động tiêu cực đến hiệu suất suy luận của LLMs trong một số lĩnh vực
- Tồn tại một phân phối độ dài tối ưu khác nhau cho các lĩnh vực khác nhau
- CoT dài hơn có thể chứa nhiều bước sai sót hơn, ảnh hưởng tiêu cực đến hiệu suất tổng thể

#### 2.1.2. Phương pháp TOPS

1. Sử dụng một tập dữ liệu nhỏ với các phản hồi có độ dài khác nhau để huấn luyện mô hình "tag"
2. Sử dụng mô hình "tag" để tạo ra các phản hồi cho một tập lớn các bài toán toán học với các mức độ nỗ lực suy luận khác nhau
3. Chọn phản hồi ngắn nhất mà vẫn đúng từ tất cả các mức độ nỗ lực suy luận cho cùng một bài toán
4. Sử dụng tập dữ liệu tối ưu này để cải thiện mô hình cơ sở

#### 2.1.3. Kết quả

Mô hình được cải thiện dựa trên Qwen2.5-32B-Instruct đạt hiệu suất tốt hơn các mô hình distillation-based 32B o1-like khác trên nhiều benchmark toán học với các mức độ khó khác nhau, bao gồm GSM8K, MATH500 và AIME2024.

### 2.2. Diverse Verifier Tree Search (DVTS)

DVTS là một phương pháp test-time scaling được đề cập trong bài viết "Test-Time Compute Scaling: How to make an LLM 'think longer' on harder problems" (Kamau, 2024).

#### 2.2.1. Cơ chế hoạt động

- Mô hình tạo ra nhiều bước suy luận trung gian
- Một Process Reward Model (PRM) đánh giá từng bước
- Chiến lược tìm kiếm được điều chỉnh dựa trên phản hồi từ PRM
- Kết quả cuối cùng được chọn dựa trên điểm số cao nhất

#### 2.2.2. Ứng dụng cho bài toán toán học

DVTS đặc biệt hiệu quả cho các bài toán toán học phức tạp vì:
- Cho phép mô hình khám phá nhiều hướng tiếp cận khác nhau
- Có khả năng phát hiện và sửa lỗi trong quá trình suy luận
- Tăng cường khả năng kiểm tra tính nhất quán của kết quả

### 2.3. Adaptive Computation Time (ACT)

ACT là một phương pháp cho phép mô hình tự động điều chỉnh lượng tính toán dựa trên độ phức tạp của đầu vào.

#### 2.3.1. Nguyên lý hoạt động

- Mô hình dự đoán một "halting probability" sau mỗi bước tính toán
- Nếu halting probability vượt quá ngưỡng, mô hình dừng tính toán và đưa ra kết quả
- Nếu không, mô hình tiếp tục thực hiện thêm các bước tính toán

#### 2.3.2. Ứng dụng cho bài toán toán học

- Các phép tính đơn giản như "1+1=2" sẽ có halting probability cao ngay từ đầu
- Các bài toán phức tạp sẽ có halting probability thấp, dẫn đến nhiều bước tính toán hơn

## 3. Đánh giá độ phức tạp của bài toán toán học

### 3.1. Các yếu tố ảnh hưởng đến độ phức tạp

#### 3.1.1. Yếu tố cú pháp

- **Độ dài của bài toán**: Bài toán dài thường phức tạp hơn
- **Số lượng biến số**: Nhiều biến số thường đòi hỏi nhiều bước tính toán hơn
- **Cấu trúc câu**: Câu phức tạp, nhiều mệnh đề phụ thường khó hiểu hơn

#### 3.1.2. Yếu tố ngữ nghĩa

- **Khái niệm toán học**: Các khái niệm trừu tượng, nâng cao thường phức tạp hơn
- **Mối quan hệ giữa các đại lượng**: Quan hệ phức tạp, phi tuyến thường khó hơn
- **Yêu cầu kiến thức nền tảng**: Bài toán đòi hỏi nhiều kiến thức nền tảng thường phức tạp hơn

#### 3.1.3. Yếu tố giải pháp

- **Số bước suy luận**: Nhiều bước suy luận thường chỉ ra bài toán phức tạp
- **Độ phức tạp của các phép tính**: Phép tính phức tạp (đạo hàm, tích phân) thường khó hơn
- **Số lượng phương pháp cần kết hợp**: Bài toán đòi hỏi kết hợp nhiều phương pháp thường phức tạp hơn

### 3.2. Phương pháp đánh giá độ phức tạp

#### 3.2.1. Phương pháp dựa trên đặc trưng

- Trích xuất các đặc trưng từ bài toán (độ dài, số lượng biến số, từ khóa toán học, v.v.)
- Sử dụng một mô hình ML đơn giản để dự đoán độ phức tạp dựa trên các đặc trưng này

#### 3.2.2. Phương pháp dựa trên mô hình nhỏ

- Sử dụng một mô hình LLM nhỏ để nhanh chóng đánh giá độ phức tạp của bài toán
- Dựa trên độ tin cậy của mô hình nhỏ để quyết định có cần sử dụng mô hình lớn hơn hay không

#### 3.2.3. Phương pháp meta-reasoning

- Mô hình tự đánh giá độ phức tạp của bài toán trong quá trình reasoning
- Dựa trên các dấu hiệu như sự không chắc chắn, số lượng bước dự kiến, v.v.

## 4. Cơ chế chuyển đổi giữa Fast và Slow Thinking

### 4.1. Mô hình hai giai đoạn

#### 4.1.1. Giai đoạn đánh giá (Fast Thinking)

- Sử dụng Fast Thinking để nhanh chóng đánh giá độ phức tạp của bài toán
- Quyết định xem có cần chuyển sang Slow Thinking hay không
- Nếu bài toán đủ đơn giản, trả lời ngay bằng Fast Thinking

#### 4.1.2. Giai đoạn suy luận chi tiết (Slow Thinking)

- Chỉ được kích hoạt nếu bài toán được đánh giá là phức tạp
- Thực hiện suy luận từng bước, có thể sử dụng nhiều tài nguyên tính toán hơn
- Có thể sử dụng các kỹ thuật như DVTS để tối ưu hóa quá trình suy luận

### 4.2. Cơ chế chuyển đổi động

#### 4.2.1. Ngưỡng độ phức tạp

- Thiết lập một ngưỡng độ phức tạp để quyết định chuyển đổi
- Nếu độ phức tạp < ngưỡng: sử dụng Fast Thinking
- Nếu độ phức tạp >= ngưỡng: chuyển sang Slow Thinking

#### 4.2.2. Chuyển đổi dựa trên độ tin cậy

- Bắt đầu với Fast Thinking cho mọi bài toán
- Nếu độ tin cậy của kết quả < ngưỡng: chuyển sang Slow Thinking
- Nếu độ tin cậy của kết quả >= ngưỡng: giữ nguyên kết quả từ Fast Thinking

#### 4.2.3. Chuyển đổi dựa trên phản hồi

- Bắt đầu với Fast Thinking
- Nếu phát hiện mâu thuẫn hoặc lỗi trong quá trình suy luận: chuyển sang Slow Thinking
- Nếu quá trình suy luận suôn sẻ: tiếp tục với Fast Thinking

### 4.3. Tích hợp với test-time scaling

#### 4.3.1. Phân bổ tài nguyên động

- Phân bổ ít tài nguyên cho Fast Thinking (ít token, ít bước suy luận)
- Phân bổ nhiều tài nguyên hơn cho Slow Thinking (nhiều token, nhiều bước suy luận)
- Điều chỉnh mức độ phân bổ dựa trên độ phức tạp của bài toán

#### 4.3.2. Kết hợp với TOPS

- Sử dụng TOPS để xác định mức độ nỗ lực suy luận tối ưu cho từng bài toán
- Áp dụng Fast Thinking cho các bài toán cần ít nỗ lực suy luận
- Áp dụng Slow Thinking cho các bài toán cần nhiều nỗ lực suy luận hơn

#### 4.3.3. Kết hợp với DVTS

- Sử dụng Fast Thinking để tạo ra giải pháp ban đầu
- Nếu cần, sử dụng DVTS trong Slow Thinking để khám phá nhiều hướng tiếp cận khác nhau
- Chọn giải pháp tốt nhất dựa trên điểm số từ Process Reward Model

## 5. Ứng dụng cụ thể cho môn toán

### 5.1. Phân loại bài toán toán học

#### 5.1.1. Phép tính đơn giản (Fast Thinking)

- Phép cộng, trừ, nhân, chia đơn giản
- Chuyển đổi đơn vị đơn giản
- Tính toán phần trăm cơ bản
- Ví dụ: 1+1=2, 25×4=100, 50% của 200 là 100

#### 5.1.2. Bài toán trung bình (Fast-then-Slow)

- Phương trình bậc nhất, bậc hai đơn giản
- Bài toán hình học cơ bản
- Bài toán xác suất đơn giản
- Ví dụ: Giải phương trình 2x+3=7, tính diện tích hình tròn bán kính 5cm

#### 5.1.3. Bài toán phức tạp (Slow Thinking)

- Phương trình bậc cao, hệ phương trình
- Bài toán tối ưu hóa
- Bài toán đòi hỏi nhiều bước suy luận
- Ví dụ: Bài toán AIME, IMO, các bài toán trong GSM8K khó

### 5.2. Chiến lược xử lý theo loại bài toán

#### 5.2.1. Chiến lược cho phép tính đơn giản

- Sử dụng Fast Thinking
- Trả lời trực tiếp, không cần suy luận từng bước
- Tối ưu hóa thời gian phản hồi

#### 5.2.2. Chiến lược cho bài toán trung bình

- Bắt đầu với Fast Thinking để phân tích bài toán
- Chuyển sang Slow Thinking nếu cần
- Sử dụng suy luận từng bước nhưng giới hạn số lượng bước

#### 5.2.3. Chiến lược cho bài toán phức tạp

- Sử dụng Slow Thinking ngay từ đầu
- Áp dụng các kỹ thuật như DVTS để khám phá nhiều hướng tiếp cận
- Không giới hạn số lượng bước suy luận
- Kiểm tra kết quả kỹ lưỡng

## 6. Kết luận và hướng tiếp theo

### 6.1. Tổng kết các phát hiện chính

- Test-Time Scaling là một phương pháp hiệu quả để tối ưu hóa tài nguyên tính toán trong quá trình suy luận
- Việc đánh giá độ phức tạp của bài toán là yếu tố quan trọng để quyết định chiến lược tư duy phù hợp
- Cơ chế chuyển đổi giữa Fast và Slow Thinking cần được thiết kế linh hoạt và hiệu quả
- Các phương pháp như TOPS và DVTS có thể được kết hợp để tạo ra một hệ thống tối ưu

### 6.2. Hướng tiếp theo

- Thiết kế một khung đánh giá độ phức tạp chi tiết cho các bài toán toán học
- Phát triển cơ chế chuyển đổi Fast-Slow Thinking dựa trên đánh giá độ phức tạp
- Xây dựng phương pháp huấn luyện để mô hình học cách tự động chuyển đổi giữa các chế độ tư duy
- Đề xuất chiến lược triển khai và đánh giá hiệu quả của hệ thống
