# HƯỚNG DẪN CHẠY DỰ ÁN DSS BUDGET

## 1. Giới thiệu

Dự án **DSS Budget** là hệ thống hỗ trợ ra quyết định trong quản lý chi tiêu cá nhân. Hệ thống cho phép người dùng tải dữ liệu chi tiêu từ file CSV, nhập ngân sách tháng, phân tích tình trạng chi tiêu, xác định nhóm chi tiêu ưu tiên bằng AHP, dự đoán nguy cơ vượt ngân sách bằng Logistic Regression và đưa ra gợi ý điều chỉnh chi tiêu.

---

## 2. Yêu cầu cài đặt

Trước khi chạy dự án, cần cài đặt:

```text
Python >= 3.9
```

Kiểm tra phiên bản Python bằng lệnh:

```bash
python --version
```

Nếu máy không nhận lệnh `python`, thử:

```bash
py --version
```

---

## 3. Cài thư viện

Mở Terminal hoặc PowerShell tại thư mục dự án, sau đó cài các thư viện cần thiết.

### Cách 1: Cài từng thư viện

```bash
pip install streamlit
pip install pandas
pip install numpy
pip install plotly
pip install scikit-learn
pip install pyodbc
```

### Cách 2: Cài bằng file `requirements.txt`

Nếu dự án có file `requirements.txt`, chạy lệnh:

```bash
pip install -r requirements.txt
```

Nếu máy không nhận lệnh `pip`, dùng:

```bash
python -m pip install -r requirements.txt
```

hoặc:

```bash
py -m pip install -r requirements.txt
```

---

## 4. Chạy ứng dụng

Di chuyển vào thư mục project:

```bash
cd dss_budget_student
```

Sau đó chạy ứng dụng:

```bash
streamlit run app.py
```

Sau khi chạy thành công, trình duyệt sẽ mở tại địa chỉ:

```text
http://localhost:8501
```

Nếu trình duyệt không tự mở, hãy copy đường dẫn trên và dán vào trình duyệt.

---

## 5. Từng bước sử dụng hệ thống

### Bước 1: Tải file CSV chi tiêu

Người dùng tải file CSV chứa dữ liệu chi tiêu cá nhân.

File CSV nên có các thông tin cơ bản như:

```text
Ngày chi tiêu
Danh mục chi tiêu
Số tiền
```

Ví dụ:

```csv
expense_date,category,amount
2024-01-05,Ăn uống,50000
2024-01-06,Di chuyển,30000
2024-01-07,Giải trí,120000
```

---

### Bước 2: Hệ thống đọc dữ liệu

Sau khi tải file CSV, hệ thống sẽ đọc dữ liệu, xử lý các khoản chi và gom nhóm chi tiêu theo tháng.

Các nhóm chi tiêu có thể gồm:

```text
Ăn uống
Di chuyển
Học tập
Giải trí
Sức khỏe
Nhà ở
Khác
```

---

### Bước 3: Nhập ngân sách tháng

Người dùng nhập ngân sách tháng cần theo dõi.

Ví dụ:

```text
8000000
```

---

### Bước 4: Phân tích tình trạng chi tiêu

Hệ thống tính các chỉ số:

```text
Tổng chi tiêu
Ngân sách còn lại
Tỷ lệ sử dụng ngân sách
Mức độ vượt hoặc gần vượt ngân sách
```

Công thức tỷ lệ sử dụng ngân sách:

```text
Tỷ lệ sử dụng ngân sách = Tổng chi tiêu / Ngân sách tháng
```

---

### Bước 5: Xác định nhóm chi tiêu ưu tiên bằng AHP

Hệ thống sử dụng phương pháp AHP để xác định mức độ ưu tiên của các nhóm chi tiêu.

Các tiêu chí có thể gồm:

```text
Mức độ cần thiết
Tác động ngân sách
Khả năng cắt giảm
Tần suất phát sinh
Mức độ linh hoạt
```

AHP giúp xác định nhóm chi nào nên được ưu tiên điều chỉnh khi người dùng có nguy cơ vượt ngân sách.

---

### Bước 6: Dự đoán nguy cơ bằng Logistic Regression

Hệ thống sử dụng mô hình Logistic Regression để dự đoán nguy cơ vượt ngân sách.

Đầu vào của mô hình có thể gồm:

```text
Tổng chi tiêu
Ngân sách tháng
Tỷ lệ sử dụng ngân sách
Số lượng khoản chi
Nhóm chi tiêu chính
```

Đầu ra của mô hình:

```text
Mức nguy cơ
Điểm rủi ro
Khả năng vượt ngân sách
```

---

### Bước 7: Đưa ra phương án DSS

Sau khi phân tích, hệ thống đưa ra gợi ý điều chỉnh chi tiêu.

Ví dụ:

```text
Nên giảm chi tiêu nhóm Giải trí vì nhóm này có khả năng cắt giảm cao.
Nên kiểm soát nhóm Ăn uống vì tần suất phát sinh thường xuyên.
Không nên giảm mạnh nhóm Nhà ở hoặc Sức khỏe vì đây là nhóm thiết yếu.
```

---

## 6. Luồng xử lý tổng quát

```text
Tải file CSV
      ↓
Đọc và xử lý dữ liệu chi tiêu
      ↓
Gom nhóm chi tiêu theo tháng
      ↓
Nhập ngân sách tháng
      ↓
Tính tổng chi, phần còn lại và tỷ lệ sử dụng ngân sách
      ↓
AHP xác định nhóm chi tiêu ưu tiên
      ↓
Logistic Regression dự đoán nguy cơ vượt ngân sách
      ↓
DSS đề xuất phương án điều chỉnh
```

---

## 7. Code SQL Server

Chạy đoạn SQL sau trong SQL Server Management Studio để tạo database và các bảng cần thiết.

```sql
IF DB_ID('DSS_BUDGET') IS NULL
BEGIN
    CREATE DATABASE DSS_BUDGET;
END
GO

USE DSS_BUDGET;
GO

IF OBJECT_ID('users', 'U') IS NOT NULL DROP TABLE users;
IF OBJECT_ID('budgets', 'U') IS NOT NULL DROP TABLE budgets;
IF OBJECT_ID('expenses', 'U') IS NOT NULL DROP TABLE expenses;
IF OBJECT_ID('predictions', 'U') IS NOT NULL DROP TABLE predictions;
GO

CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    full_name NVARCHAR(100) NOT NULL,
    email NVARCHAR(100) NOT NULL UNIQUE,
    password_hash NVARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT GETDATE()
);
GO

CREATE TABLE budgets (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    budget_month CHAR(7) NOT NULL,
    monthly_budget FLOAT NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
GO

CREATE TABLE expenses (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    expense_date DATE NOT NULL,
    category NVARCHAR(100) NOT NULL,
    expense_group NVARCHAR(100) NOT NULL,
    amount FLOAT NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
GO

CREATE TABLE predictions (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    budget_month CHAR(7) NOT NULL,
    total_expense FLOAT NOT NULL,
    monthly_budget FLOAT NOT NULL,
    risk_label NVARCHAR(20) NOT NULL,
    risk_score FLOAT NOT NULL,
    selected_plan NVARCHAR(200) NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
GO
```

---

## 8. Một số lỗi thường gặp

### Lỗi: `python is not recognized`

Nguyên nhân là Python chưa được cài hoặc chưa thêm vào PATH.

Cách xử lý:

```bash
py --version
```

Nếu `py` chạy được thì dùng `py` thay cho `python`.

---

### Lỗi: `pip is not recognized`

Cách xử lý:

```bash
python -m pip install -r requirements.txt
```

hoặc:

```bash
py -m pip install -r requirements.txt
```

---

### Lỗi: Không chạy được `streamlit`

Cài lại Streamlit:

```bash
pip install streamlit
```

hoặc:

```bash
python -m pip install streamlit
```

Sau đó chạy lại:

```bash
streamlit run app.py
```

---

### Lỗi: Không kết nối được SQL Server

Kiểm tra lại:

```text
Tên server SQL Server
Tên database DSS_BUDGET
Username/password nếu dùng SQL Authentication
Driver ODBC đã cài trên máy
Chuỗi kết nối trong code
```

Nếu thiếu driver SQL Server, cần cài **ODBC Driver for SQL Server**.

---

## 9. Lệnh chạy nhanh

```bash
cd dss_budget_student
pip install -r requirements.txt
streamlit run app.py
```

Mở trình duyệt tại:

```text
http://localhost:8501
```

---

## 10. Ghi chú

Nếu thay đổi code, hãy dừng ứng dụng bằng:

```text
Ctrl + C
```

Sau đó chạy lại:

```bash
streamlit run app.py
```
