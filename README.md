# 使用Django Rest framework 製作師生CRUD API

## 完整含圖片版請至hackmd查看 (https://hackmd.io/@CeeEHezuSRKMy_RGkLpNdw/Skw-qbEUlg)
### 1. 規劃老師及學生的table
學生 table 的「導師(mentor)」和「指導老師(advisor)」為外鍵，關聯到老師 table 的主鍵(id)。

```sql=
-- https://dbdiagram.io/

Table teachers {
  id integer [primary key]
  teacher_name varchar [not null]
  staff_id varchar [not null, unique]
  title varchar
  department_id varchar
  created_at timestamp [default: `now()`]
}

Table students {
  id integer [primary key]
  student_name varchar [not null]
  student_id varchar [not null, unique]
  role varchar
  department_id varchar
  enroll_year integer
  class_id varchar
  mentor integer [ref: > teachers.id]
  advisor integer [ref: > teachers.id]
  created_at timestamp [default: `now()`]
}
```



### 2. 專案結構
#### 2.1. 建立專案資料夾並啟用虛擬環境，安裝Django
```bash=
uv init
uv add Django djangorestframework django-cors-headers
```
#### 2.2. 在專案中新增Django project: mysite
```bash=
uv run django-admin startproject mysite
```
#### 2.3. 在專案中新增 app: school

```bash=
uv run django-admin startapp app-name
```
#### 專案結構如下：
```bash=
.
├── db.sqlite3
├── main.py
├── manage.py
├── mysite
│   ├── asgi.py
│   ├── __init__.py
│   ├── __pycache__/...
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── school
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations/...
│   ├── models.py
│   ├── __pycache__/...
│   ├── serializers.py
│   ├── tests.py
│   └── views.py
├── pyproject.toml
├── README.md
└── uv.lock
```
#### GitHub repo
https://github.com/potatooyy/202507-python

#### 2.4. makemigrations 和 migrate
```bash=
uv run python manage.py makemigrations
uv run python manage.py migrate
```
#### 2.5. 建立 superuser
```bash=
uv run python manage.py createsuperuser
```
依序輸入使用者名稱、電子郵件、密碼
#### 2.6. runserver
```bash=
uv run python manage.py runserver
```
#### 2.6.1. 至瀏覽器以`http://127.0.0.1:8000/api` 即可對 tabels 進行 CRUD
`http://127.0.0.1:8000/api/teachers`: teachers GET、POST
`http://127.0.0.1:8000/api/teachers/{id}`: teachers PUT、DELETE

`http://127.0.0.1:8000/api/students`: students GET、POST
`http://127.0.0.1:8000/api/students/{id}`: students PUT、DELETE


#### 2.6.2. 至瀏覽器以`http://127.0.0.1:8000/admin` 即可以superuser 身分登入對 tabels 進行 CRUD

### 3. API list
| 資源 (Resource) | 方法 (Method) | 路徑 (Path) | 功能 (Description) |
| ------------- | ----------- | --------- | ---------------- |
| teachers | GET    | `/api/teachers/`      | 列出所有老師 |
| teachers | POST   | `/api/teachers/`      | 新增老師   |
| teachers | GET    | `/api/teachers/{id}/` | 查詢單一老師 |
| teachers | PUT    | `/api/teachers/{id}/` | 更新老師   |
| teachers | DELETE | `/api/teachers/{id}/` | 刪除老師   |
| students | GET    | `/api/students/`      | 列出所有學生 |
| students | POST   | `/api/students/`      | 新增學生   |
| students | GET    | `/api/students/{id}/` | 查詢單一學生 |
| students | PUT    | `/api/students/{id}/` | 更新學生   |
| students | DELETE | `/api/students/{id}/` | 刪除學生   |

### 4. postman 測試 CRUD
