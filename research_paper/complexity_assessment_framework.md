# Khung đánh giá độ phức tạp cho bài toán toán học

## 1. Tổng quan về khung đánh giá

Khung đánh giá độ phức tạp này được thiết kế để tự động xác định mức độ phức tạp của các bài toán toán học, từ đó quyết định chiến lược tư duy phù hợp (Fast Thinking hoặc Slow Thinking) và mức độ tài nguyên tính toán cần thiết. Khung đánh giá này tích hợp nhiều yếu tố khác nhau, từ đặc điểm cú pháp đến yêu cầu về kiến thức toán học và số bước suy luận cần thiết.

### 1.1. Mục tiêu của khung đánh giá

- Phân loại bài toán toán học theo độ phức tạp một cách chính xác và nhất quán
- Xác định chiến lược tư duy phù hợp (Fast Thinking, Slow Thinking, hoặc kết hợp)
- Ước tính mức độ tài nguyên tính toán cần thiết
- Tối ưu hóa cân bằng giữa hiệu suất và hiệu quả tài nguyên

### 1.2. Cấu trúc tổng thể

Khung đánh giá bao gồm ba giai đoạn chính:

1. **Phân tích sơ bộ**: Đánh giá nhanh dựa trên đặc điểm bề mặt của bài toán
2. **Phân tích chuyên sâu**: Đánh giá chi tiết dựa trên nội dung và yêu cầu của bài toán
3. **Tổng hợp và quyết định**: Kết hợp kết quả từ các giai đoạn trước để đưa ra quyết định cuối cùng

## 2. Phân tích sơ bộ (Fast Assessment)

Giai đoạn phân tích sơ bộ được thiết kế để nhanh chóng đánh giá độ phức tạp của bài toán dựa trên các đặc điểm bề mặt, không đòi hỏi phân tích sâu về nội dung toán học.

### 2.1. Đặc điểm cú pháp

#### 2.1.1. Độ dài của bài toán

| Độ dài (số từ) | Điểm phức tạp |
|----------------|---------------|
| 1-10           | 0.1           |
| 11-30          | 0.2           |
| 31-50          | 0.3           |
| 51-100         | 0.4           |
| >100           | 0.5           |

#### 2.1.2. Cấu trúc câu

| Cấu trúc                                | Điểm phức tạp |
|-----------------------------------------|---------------|
| Câu đơn, không có mệnh đề phụ           | 0.1           |
| Câu có 1-2 mệnh đề phụ                  | 0.2           |
| Câu có 3-4 mệnh đề phụ                  | 0.3           |
| Câu có >4 mệnh đề phụ                   | 0.4           |
| Câu có cấu trúc lồng nhau, điều kiện phức tạp | 0.5     |

#### 2.1.3. Số lượng biến số và ràng buộc

| Số lượng biến số và ràng buộc | Điểm phức tạp |
|-------------------------------|---------------|
| 1-2 biến, 0-1 ràng buộc       | 0.1           |
| 3-4 biến, 1-2 ràng buộc       | 0.2           |
| 5-6 biến, 2-3 ràng buộc       | 0.3           |
| 7-8 biến, 3-4 ràng buộc       | 0.4           |
| >8 biến, >4 ràng buộc         | 0.5           |

### 2.2. Từ khóa và thuật ngữ

#### 2.2.1. Phát hiện từ khóa toán học

Bảng điểm phức tạp dựa trên từ khóa toán học:

| Loại từ khóa                                      | Điểm phức tạp |
|---------------------------------------------------|---------------|
| Phép tính cơ bản (+, -, ×, ÷)                     | 0.1           |
| Phương trình, bất phương trình đơn giản           | 0.2           |
| Hàm số, đạo hàm, tích phân cơ bản                 | 0.3           |
| Xác suất, thống kê, tổ hợp                        | 0.4           |
| Tô pô, đại số trừu tượng, lý thuyết số nâng cao   | 0.5           |

#### 2.2.2. Phát hiện cấp độ toán học

| Cấp độ                                  | Điểm phức tạp |
|-----------------------------------------|---------------|
| Toán tiểu học                           | 0.1           |
| Toán THCS                               | 0.2           |
| Toán THPT                               | 0.3           |
| Toán đại học cơ bản                     | 0.4           |
| Toán đại học nâng cao, nghiên cứu       | 0.5           |

### 2.3. Tính toán điểm phức tạp sơ bộ

Điểm phức tạp sơ bộ được tính bằng trung bình có trọng số của các điểm thành phần:

```
Điểm_sơ_bộ = 0.3 * Điểm_độ_dài + 0.2 * Điểm_cấu_trúc_câu + 0.2 * Điểm_biến_số + 0.15 * Điểm_từ_khóa + 0.15 * Điểm_cấp_độ
```

## 3. Phân tích chuyên sâu (Deep Assessment)

Giai đoạn phân tích chuyên sâu đánh giá chi tiết hơn về nội dung toán học và yêu cầu suy luận của bài toán.

### 3.1. Phân loại lĩnh vực toán học

#### 3.1.1. Xác định lĩnh vực chính

| Lĩnh vực                | Điểm phức tạp cơ sở |
|-------------------------|---------------------|
| Số học cơ bản           | 0.1                 |
| Đại số cơ bản           | 0.2                 |
| Hình học cơ bản         | 0.2                 |
| Đại số tuyến tính       | 0.3                 |
| Giải tích               | 0.3                 |
| Xác suất thống kê       | 0.3                 |
| Tổ hợp đếm              | 0.4                 |
| Lý thuyết số            | 0.4                 |
| Tô pô, đại số trừu tượng| 0.5                 |

#### 3.1.2. Đánh giá sự kết hợp lĩnh vực

| Số lượng lĩnh vực kết hợp | Hệ số nhân |
|---------------------------|------------|
| 1 lĩnh vực                | 1.0        |
| 2 lĩnh vực                | 1.2        |
| 3 lĩnh vực                | 1.4        |
| >3 lĩnh vực               | 1.6        |

### 3.2. Phân tích yêu cầu suy luận

#### 3.2.1. Ước tính số bước suy luận

| Số bước suy luận ước tính | Điểm phức tạp |
|---------------------------|---------------|
| 1 bước                    | 0.1           |
| 2-3 bước                  | 0.2           |
| 4-6 bước                  | 0.3           |
| 7-10 bước                 | 0.4           |
| >10 bước                  | 0.5           |

#### 3.2.2. Loại suy luận yêu cầu

| Loại suy luận                                    | Điểm phức tạp |
|-------------------------------------------------|---------------|
| Áp dụng công thức trực tiếp                     | 0.1           |
| Suy luận quy nạp đơn giản                       | 0.2           |
| Suy luận diễn dịch nhiều bước                   | 0.3           |
| Chứng minh gián tiếp, phản chứng                | 0.4           |
| Suy luận trừu tượng, xây dựng mô hình toán học  | 0.5           |

### 3.3. Đánh giá độ phức tạp tính toán

#### 3.3.1. Loại phép tính

| Loại phép tính                                  | Điểm phức tạp |
|------------------------------------------------|---------------|
| Phép tính số học đơn giản (+, -, ×, ÷)         | 0.1           |
| Phép tính với phân số, căn thức                | 0.2           |
| Phép tính với logarit, lũy thừa, hàm lượng giác| 0.3           |
| Đạo hàm, tích phân                             | 0.4           |
| Phép tính ma trận, vi phân, chuỗi vô hạn       | 0.5           |

#### 3.3.2. Khối lượng tính toán

| Khối lượng tính toán                            | Điểm phức tạp |
|------------------------------------------------|---------------|
| Ít phép tính, kết quả đơn giản                 | 0.1           |
| Vài phép tính, kết quả có thể phức tạp         | 0.2           |
| Nhiều phép tính, cần theo dõi các bước trung gian | 0.3        |
| Tính toán lặp lại, đệ quy đơn giản             | 0.4           |
| Tính toán đệ quy phức tạp, nhiều trường hợp    | 0.5           |

### 3.4. Tính toán điểm phức tạp chuyên sâu

Điểm phức tạp chuyên sâu được tính như sau:

```
Điểm_lĩnh_vực = Điểm_lĩnh_vực_chính * Hệ_số_kết_hợp
Điểm_chuyên_sâu = 0.25 * Điểm_lĩnh_vực + 0.3 * Điểm_số_bước + 0.25 * Điểm_loại_suy_luận + 0.1 * Điểm_loại_phép_tính + 0.1 * Điểm_khối_lượng
```

## 4. Tổng hợp và quyết định

### 4.1. Tính toán điểm phức tạp tổng thể

Điểm phức tạp tổng thể là sự kết hợp có trọng số của điểm phức tạp sơ bộ và điểm phức tạp chuyên sâu:

```
Điểm_tổng_thể = 0.4 * Điểm_sơ_bộ + 0.6 * Điểm_chuyên_sâu
```

### 4.2. Phân loại độ phức tạp

Dựa trên điểm phức tạp tổng thể, bài toán được phân loại như sau:

| Điểm phức tạp tổng thể | Phân loại độ phức tạp |
|------------------------|------------------------|
| 0.0 - 0.2              | Đơn giản               |
| 0.2 - 0.4              | Trung bình             |
| 0.4 - 0.6              | Phức tạp               |
| 0.6 - 0.8              | Rất phức tạp           |
| 0.8 - 1.0              | Cực kỳ phức tạp        |

### 4.3. Quyết định chiến lược tư duy

Dựa trên phân loại độ phức tạp, hệ thống quyết định chiến lược tư duy phù hợp:

| Phân loại độ phức tạp | Chiến lược tư duy      | Mức độ tài nguyên |
|-----------------------|------------------------|-------------------|
| Đơn giản              | Fast Thinking          | Thấp (10%)        |
| Trung bình            | Fast-then-Slow         | Trung bình (30%)  |
| Phức tạp              | Slow Thinking          | Cao (60%)         |
| Rất phức tạp          | Slow Thinking + DVTS   | Rất cao (80%)     |
| Cực kỳ phức tạp       | Slow Thinking + DVTS   | Tối đa (100%)     |

## 5. Triển khai trong quá trình reasoning

### 5.1. Quy trình đánh giá trong thời gian thực

Quy trình đánh giá độ phức tạp trong thời gian thực bao gồm các bước sau:

1. **Phân tích sơ bộ ban đầu**: Thực hiện ngay khi nhận được bài toán
2. **Quyết định sơ bộ**: Nếu bài toán rõ ràng là đơn giản (điểm sơ bộ < 0.15), sử dụng Fast Thinking ngay
3. **Phân tích chuyên sâu**: Nếu cần, thực hiện phân tích chuyên sâu
4. **Quyết định cuối cùng**: Xác định chiến lược tư duy dựa trên điểm phức tạp tổng thể
5. **Điều chỉnh động**: Có thể điều chỉnh chiến lược trong quá trình suy luận nếu phát hiện bài toán phức tạp hơn hoặc đơn giản hơn dự kiến

### 5.2. Mã giả cho quy trình đánh giá

```python
def assess_complexity(math_problem):
    # Phân tích sơ bộ
    preliminary_score = assess_preliminary(math_problem)
    
    # Quyết định nhanh cho bài toán đơn giản
    if preliminary_score < 0.15:
        return {
            "complexity_score": preliminary_score,
            "complexity_level": "Simple",
            "thinking_strategy": "Fast Thinking",
            "resource_level": "Low"
        }
    
    # Phân tích chuyên sâu
    deep_score = assess_deep(math_problem)
    
    # Tính điểm tổng thể
    overall_score = 0.4 * preliminary_score + 0.6 * deep_score
    
    # Xác định phân loại và chiến lược
    if overall_score < 0.2:
        return {
            "complexity_score": overall_score,
            "complexity_level": "Simple",
            "thinking_strategy": "Fast Thinking",
            "resource_level": "Low"
        }
    elif overall_score < 0.4:
        return {
            "complexity_score": overall_score,
            "complexity_level": "Medium",
            "thinking_strategy": "Fast-then-Slow",
            "resource_level": "Medium"
        }
    elif overall_score < 0.6:
        return {
            "complexity_score": overall_score,
            "complexity_level": "Complex",
            "thinking_strategy": "Slow Thinking",
            "resource_level": "High"
        }
    elif overall_score < 0.8:
        return {
            "complexity_score": overall_score,
            "complexity_level": "Very Complex",
            "thinking_strategy": "Slow Thinking + DVTS",
            "resource_level": "Very High"
        }
    else:
        return {
            "complexity_score": overall_score,
            "complexity_level": "Extremely Complex",
            "thinking_strategy": "Slow Thinking + DVTS",
            "resource_level": "Maximum"
        }
```

### 5.3. Tích hợp với test-time scaling

Kết quả đánh giá độ phức tạp được sử dụng để điều chỉnh mức độ tài nguyên tính toán:

```python
def allocate_resources(complexity_assessment, max_resources):
    resource_levels = {
        "Low": 0.1,
        "Medium": 0.3,
        "High": 0.6,
        "Very High": 0.8,
        "Maximum": 1.0
    }
    
    resource_percentage = resource_levels[complexity_assessment["resource_level"]]
    allocated_resources = max_resources * resource_percentage
    
    return {
        "tokens": int(allocated_resources["max_tokens"] * resource_percentage),
        "thinking_steps": int(allocated_resources["max_thinking_steps"] * resource_percentage),
        "search_breadth": int(allocated_resources["max_search_breadth"] * resource_percentage),
        "search_depth": int(allocated_resources["max_search_depth"] * resource_percentage)
    }
```

## 6. Ví dụ áp dụng

### 6.1. Ví dụ 1: Bài toán đơn giản

**Bài toán**: Tính 25 × 4

**Phân tích sơ bộ**:
- Độ dài: 3 từ → 0.1
- Cấu trúc câu: Câu đơn → 0.1
- Số biến số: 2 biến, 0 ràng buộc → 0.1
- Từ khóa: Phép tính cơ bản → 0.1
- Cấp độ: Toán tiểu học → 0.1

**Điểm sơ bộ**: 0.1

**Quyết định**: Đơn giản → Fast Thinking

### 6.2. Ví dụ 2: Bài toán trung bình

**Bài toán**: Giải phương trình 2x² + 5x - 3 = 0

**Phân tích sơ bộ**:
- Độ dài: 7 từ → 0.1
- Cấu trúc câu: Câu đơn → 0.1
- Số biến số: 1 biến, 1 ràng buộc → 0.1
- Từ khóa: Phương trình → 0.2
- Cấp độ: Toán THCS → 0.2

**Điểm sơ bộ**: 0.14

**Phân tích chuyên sâu**:
- Lĩnh vực: Đại số cơ bản → 0.2 × 1.0 = 0.2
- Số bước suy luận: 2-3 bước → 0.2
- Loại suy luận: Áp dụng công thức → 0.1
- Loại phép tính: Phép tính với căn thức → 0.2
- Khối lượng tính toán: Vài phép tính → 0.2

**Điểm chuyên sâu**: 0.18

**Điểm tổng thể**: 0.4 × 0.14 + 0.6 × 0.18 = 0.164

**Quyết định**: Đơn giản → Fast Thinking

### 6.3. Ví dụ 3: Bài toán phức tạp

**Bài toán**: Tìm tất cả các giá trị của tham số m để phương trình x⁴ - mx² + m - 3 = 0 có đúng hai nghiệm phân biệt.

**Phân tích sơ bộ**:
- Độ dài: 20 từ → 0.2
- Cấu trúc câu: Câu có 1 mệnh đề phụ → 0.2
- Số biến số: 2 biến, 1 ràng buộc → 0.1
- Từ khóa: Phương trình → 0.2
- Cấp độ: Toán THPT → 0.3

**Điểm sơ bộ**: 0.2

**Phân tích chuyên sâu**:
- Lĩnh vực: Đại số cơ bản + Giải tích → 0.3 × 1.2 = 0.36
- Số bước suy luận: 7-10 bước → 0.4
- Loại suy luận: Suy luận diễn dịch nhiều bước → 0.3
- Loại phép tính: Phép tính với logarit, lũy thừa → 0.3
- Khối lượng tính toán: Nhiều phép tính → 0.3

**Điểm chuyên sâu**: 0.35

**Điểm tổng thể**: 0.4 × 0.2 + 0.6 × 0.35 = 0.29

**Quyết định**: Trung bình → Fast-then-Slow

## 7. Đánh giá và cải tiến

### 7.1. Phương pháp đánh giá hiệu quả

Để đánh giá hiệu quả của khung đánh giá độ phức tạp, có thể sử dụng các phương pháp sau:

1. **So sánh với đánh giá của chuyên gia**: So sánh kết quả phân loại của khung đánh giá với đánh giá của các chuyên gia toán học
2. **Đánh giá hiệu suất**: Đo lường hiệu suất của mô hình khi sử dụng chiến lược tư duy được đề xuất
3. **Đánh giá hiệu quả tài nguyên**: Đo lường mức độ tiết kiệm tài nguyên tính toán so với việc sử dụng Slow Thinking cho tất cả các bài toán
4. **Phân tích lỗi**: Xác định các trường hợp khung đánh giá phân loại sai và nguyên nhân

### 7.2. Hướng cải tiến

Một số hướng cải tiến tiềm năng cho khung đánh giá:

1. **Học từ dữ liệu**: Sử dụng kỹ thuật học máy để tinh chỉnh các trọng số và ngưỡng dựa trên dữ liệu thực tế
2. **Tích hợp phản hồi**: Điều chỉnh đánh giá dựa trên phản hồi từ quá trình suy luận
3. **Mở rộng các yếu tố đánh giá**: Bổ sung thêm các yếu tố đánh giá như độ quen thuộc của mô hình với loại bài toán
4. **Cá nhân hóa**: Điều chỉnh khung đánh giá dựa trên hiệu suất của mô hình cụ thể

## 8. Kết luận

Khung đánh giá độ phức tạp cho bài toán toán học này cung cấp một phương pháp có hệ thống để xác định mức độ phức tạp của bài toán và chiến lược tư duy phù hợp. Bằng cách kết hợp phân tích sơ bộ và phân tích chuyên sâu, khung đánh giá có thể xử lý nhiều loại bài toán toán học khác nhau, từ phép tính đơn giản đến các bài toán phức tạp đòi hỏi nhiều bước suy luận.

Việc tích hợp khung đánh giá này với test-time scaling sẽ giúp tối ưu hóa việc sử dụng tài nguyên tính toán, chỉ sử dụng nhiều tài nguyên khi thực sự cần thiết. Điều này đặc biệt quan trọng trong bối cảnh người dùng quan tâm đến việc tránh lãng phí tài nguyên khi áp dụng Slow Thinking cho các bài toán đơn giản như "1 + 1 = 2".

Khung đánh giá này có thể được tiếp tục cải tiến thông qua việc học từ dữ liệu và phản hồi, cũng như mở rộng để áp dụng cho các lĩnh vực khác ngoài toán học.
