# Web Termux (Flask)

Web app giả lập Termux: upload file `.py`, chạy trực tiếp trên server, gõ lệnh shell
(bao gồm `pip install ...`) ngay trên trình duyệt.

## Chạy thử ở máy local
```bash
pip install -r requirements.txt
python app.py
```
Mở trình duyệt: http://localhost:5000

## Deploy lên Render.com
1. Đẩy toàn bộ thư mục này lên 1 repo GitHub (Render lấy code từ Git).
2. Vào https://dashboard.render.com → **New** → **Web Service** → chọn repo vừa tạo.
3. Render sẽ tự đọc file `render.yaml` (Blueprint). Nếu tạo thủ công thì điền:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
4. Bấm **Create Web Service**, đợi build xong là có link `https://ten-app.onrender.com`.

Python đã có sẵn trong môi trường Render (env: python) nên không cần cài thêm gì —
bạn chỉ cần `pip install <thư-viện>` ngay trong ô lệnh của web nếu file .py cần thư viện ngoài.

## ⚠️ Lưu ý bảo mật quan trọng
App này cho phép **chạy code tùy ý** trên server (file .py bạn upload, và cả lệnh
shell bất kỳ qua ô lệnh). Điều đó rất tiện cho mục đích cá nhân/học tập, nhưng nếu
deploy public (ai cũng vào được link) thì bất kỳ ai biết link cũng có thể chạy lệnh
trên server của bạn. Gợi ý:
- Thêm xác thực (mật khẩu / Basic Auth) trước khi cho public.
- Không lưu thông tin nhạy cảm (API key, mật khẩu) trên server này.
- Đây phù hợp cho sandbox cá nhân, không phù hợp cho nhiều người dùng không tin cậy.
