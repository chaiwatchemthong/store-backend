# StoreFront — Backend

Django REST Framework backend สำหรับระบบ StoreFront Management System

---

## Tech Stack

| ส่วน | เทคโนโลยี |
|------|-----------|
| Framework | Django 5.2 + Django REST Framework |
| Authentication | JWT (djangorestframework-simplejwt) |
| Database | SQLite (POC) |
| CORS | django-cors-headers |

---

## โครงสร้างโปรเจกต์

```
storefront-backend/
  config/
    settings.py     # Django settings
    urls.py         # root URL config
  users/
    models.py       # Custom User model (email + role)
    serializers.py  # RegisterSerializer, UserSerializer
    views.py        # register, login, me
    urls.py         # /api/auth/* routes
    tests.py        # 24 unit tests
  products/
    models.py       # Product model (owner FK, name, price, stock, image)
    serializers.py  # ProductSerializer
    views.py        # list, create, my-products, detail/edit/delete
    urls.py         # /api/products/* routes
  manage.py
  requirements.txt
  .env.example
```

---

## การติดตั้งและรัน

### 1. สร้าง Virtual Environment

```bash
# สร้าง venv
python -m venv venv

# เปิดใช้งาน — macOS / Linux
source venv/bin/activate

# เปิดใช้งาน — Windows
venv\Scripts\activate
```

> ทุกครั้งที่เปิด terminal ใหม่ต้อง activate venv ก่อนเสมอ  
> สังเกตว่า prompt จะขึ้นต้นด้วย `(venv)` เมื่อ active อยู่

### 2. ติดตั้ง dependencies

```bash
pip install -r requirements.txt
```

### 3. ตั้งค่า environment (ไม่บังคับสำหรับ dev)

```bash
cp .env.example .env
```

ค่าใน `.env.example`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
```

> สำหรับ POC นี้ Django ใช้ค่า default ใน `settings.py` ได้เลย ไม่จำเป็นต้องสร้าง `.env`

### 4. รัน database migrations

```bash
python manage.py migrate
```

### 5. (ไม่บังคับ) สร้าง test users

```bash
python manage.py shell -c "
from users.models import User
User.objects.create_user(email='seller@test.com', password='pass1234', first_name='Test', last_name='Seller', role='seller')
User.objects.create_user(email='buyer@test.com',  password='pass1234', first_name='Test', last_name='Buyer',  role='buyer')
print('done')
"
```

### 6. รัน development server

```bash
python manage.py runserver
```

Server ทำงานที่ `http://localhost:8000`

---

## API Endpoints

Base URL: `http://localhost:8000/api`

### Authentication

#### Register
```
POST /api/auth/register/
```

Request body:
```json
{
  "email": "user@example.com",
  "password": "pass1234",
  "first_name": "สมชาย",
  "last_name": "ใจดี",
  "role": "buyer"
}
```

> `role` รับค่า `"buyer"` หรือ `"seller"` เท่านั้น

Response `201 Created`:
```json
{
  "access": "<JWT access token>",
  "refresh": "<JWT refresh token>",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "สมชาย",
    "last_name": "ใจดี",
    "role": "buyer"
  }
}
```

---

#### Login
```
POST /api/auth/login/
```

Request body:
```json
{
  "email": "user@example.com",
  "password": "pass1234"
}
```

Response `200 OK`:
```json
{
  "access": "<JWT access token>",
  "refresh": "<JWT refresh token>",
  "user": { ... }
}
```

Response `401 Unauthorized` (รหัสผ่านผิด หรือไม่พบ email):
```json
{
  "detail": "อีเมลหรือรหัสผ่านไม่ถูกต้อง"
}
```

---

#### Get current user
```
GET /api/auth/me/
Authorization: Bearer <access_token>
```

Response `200 OK`:
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "สมชาย",
  "last_name": "ใจดี",
  "role": "buyer"
}
```

Response `401 Unauthorized` (ไม่มี token หรือ token หมดอายุ):
```json
{
  "detail": "Given token not valid for any token type"
}
```

---

### Products

> **หมายเหตุ POC:** products app อยู่ระหว่างพัฒนา — โครงสร้าง model และ endpoint ออกแบบไว้แล้ว รอ integrate เข้า project หลัก

#### List all products (ทุกคนดูได้)
```
GET /api/products/
GET /api/products/?search=keyword
```

Response `200 OK`:
```json
[
  {
    "id": 1,
    "seller_id": 2,
    "seller_name": "seller@test.com",
    "name": "Wireless Headphones",
    "description": "...",
    "price": "1290.00",
    "stock": 48,
    "image": "/media/products/headphones.jpg",
    "created_at": "2025-05-29T10:00:00Z"
  }
]
```

---

#### Create product (Seller เท่านั้น)
```
POST /api/products/
Authorization: Bearer <seller_token>
Content-Type: multipart/form-data
```

Request fields:
| Field | Type | Required |
|-------|------|----------|
| name | string | ✅ |
| description | string | |
| price | decimal | ✅ |
| stock | integer | ✅ |
| image | file (JPG/PNG) | |

Response `201 Created`: Product object

Response `403 Forbidden` (user เป็น buyer):
```json
{ "detail": "เฉพาะ Seller เท่านั้นที่สร้างสินค้าได้" }
```

---

#### Get / Edit / Delete product
```
GET    /api/products/:id/                         → ทุกคน
PATCH  /api/products/:id/  Authorization: Bearer  → เจ้าของเท่านั้น
DELETE /api/products/:id/  Authorization: Bearer  → เจ้าของเท่านั้น
```

Response `403 Forbidden` (ไม่ใช่เจ้าของ):
```json
{ "detail": "คุณไม่ใช่เจ้าของสินค้านี้" }
```

---

#### My products (Seller ดูสินค้าตัวเอง)
```
GET /api/products/my/
Authorization: Bearer <seller_token>
```

Response: รายการ Product ของ Seller คนนั้นเท่านั้น

---

## JWT Token

- **Access token** หมดอายุใน **8 ชั่วโมง**
- **Refresh token** หมดอายุใน **7 วัน**
- ส่ง access token ใน header: `Authorization: Bearer <token>`

---

## Unit Tests

### รัน tests ทั้งหมด

```bash
python manage.py test users
```

### รันพร้อม verbose output

```bash
python manage.py test users --verbosity=2
```

### ผลลัพธ์ที่ควรได้

```
Ran 24 tests in ~23s

OK
```

### รายละเอียด tests

| Class | จำนวน | ครอบคลุม |
|-------|--------|----------|
| `RegisterTests` | 9 | register สำเร็จ, duplicate email, password สั้นเกิน, email ผิดรูปแบบ, token ครบ, password ไม่รั่ว |
| `LoginTests` | 6 | login สำเร็จ, รหัสผ่านผิด, email ไม่มีในระบบ, ไม่ส่ง credentials |
| `MeTests` | 5 | มี token ถูกต้อง, ไม่มี token, token ปลอม, ข้อมูล user ถูกต้อง, password ไม่รั่ว |
| `UserModelTests` | 4 | hash password, default role, USERNAME_FIELD, `__str__` |

> tests ใช้ in-memory SQLite แยกต่างหาก ไม่กระทบ `db.sqlite3` จริง

---

## Environment Variables

| ตัวแปร | ค่าตัวอย่าง | คำอธิบาย |
|--------|------------|----------|
| `SECRET_KEY` | `your-secret-key` | Django secret key — **ต้องเปลี่ยนใน production** |
| `DEBUG` | `True` | ปิดใน production |

---

## Architectural Decisions

**Custom User model** — ใช้ email เป็น username แทน username field มาตรฐาน เพราะ assignment กำหนดให้ login ด้วย email ถ้าเปลี่ยนทีหลังจะ migrate ยาก จึงกำหนดตั้งแต่แรก

**`AbstractBaseUser` แทน `AbstractUser`** — ควบคุม field ได้เต็มที่ ไม่มี field ที่ไม่จำเป็นเช่น `username`, `is_staff`, `is_superuser` ติดมา

**Function-based views (auth) + Generic views (products)** — auth ใช้ `@api_view` เพราะ logic ไม่ซับซ้อน ส่วน products ใช้ `ListCreateAPIView` และ `RetrieveUpdateDestroyAPIView` เพื่อลด boilerplate

**Role check ใน view layer** — ตรวจ `request.user.role` ก่อน perform_create แทนที่จะใช้ custom Permission class เพราะ POC — ถ้า scale ขึ้นควรแยกเป็น `IsSeller` permission class

**CORS allow all origins** — POC เท่านั้น ใน production ควรกำหนด `CORS_ALLOWED_ORIGINS` เป็น URL ของ frontend จริง
