# 使用 Django Rest framework 製作師生資料庫 CRUD API
## 圖片若無法查看請至hackmd查看 (https://hackmd.io/@CeeEHezuSRKMy_RGkLpNdw/Skw-qbEUlg)
### 1. 資料庫設計
學生 table 的「導師(mentor)」和「指導老師(advisor)」為外鍵，關聯到老師 table 的主鍵(id)。

![image](https://hackmd.io/_uploads/S10LKRjLgl.png)

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

- teacher table

| 欄位名稱   | 資料型別   | 約束條件     | 說明  |
| -------- | ----- | --------- | -------- |
| id    | integer   | PRIMARY KEY      | 老師的唯一識別碼 |
| teacher\_name  | varchar   | NOT NULL   | 老師姓名   |
| staff\_id | varchar | NOT NULL, UNIQUE | 教職員編號  |
| title   | varchar   |   -       | 職稱    |
| department\_id | varchar   |   -    | 所屬系所 ID  |
| created\_at | timestamp | DEFAULT `now()`| 建立時間 |

- student table

| 欄位名稱  | 資料型別      | 約束條件   | 說明         |
| --- | --------- | -------- | ---------- |
| id   | integer   | PRIMARY KEY   | 學生的唯一識別碼   |
| student\_name  | varchar   | NOT NULL  | 學生姓名|
| student\_id    | varchar   | NOT NULL, UNIQUE | 學號 |
| role  | varchar   |   -   | 角色（一般學生/班級幹部）   |
| department\_id | varchar   |    -       | 所屬系所 ID |
| enroll\_year   | integer   |    -    | 入學年度       |
| class\_id      | varchar   |     -     | 班級 ID      |
| mentor  | integer   | FOREIGN KEY → teachers.id | 導師（對應老師）  |
| advisor | integer   | FOREIGN KEY → teachers.id | 指導教授（對應老師） |
| created\_at | timestamp | DEFAULT `now()`  | 建立時間|


### 2. 建立專案、專案結構及 GitHub repo
#### 2.1. 使用 `uv` 建立專案資料夾並啟用虛擬環境、安裝 Django
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
### 3. 資料庫遷移、伺服器執行及API功能測試
#### 3.1. makemigrations 和 migrate
```bash=
uv run python manage.py makemigrations
uv run python manage.py migrate
```
#### 3.2. 建立 superuser
```bash=
uv run python manage.py createsuperuser
```
依序輸入使用者名稱、電子郵件、密碼
#### 3.3. runserver
```bash=
uv run python manage.py runserver
```
#### 3.4. 至瀏覽器以`http://127.0.0.1:8000/api` 即可對 tabels 進行 CRUD
![image](https://hackmd.io/_uploads/rJBikAjIxe.png)
- `http://127.0.0.1:8000/api/teachers`: teachers GET、POST
![image](https://hackmd.io/_uploads/Skz610oLgl.png)
![image](https://hackmd.io/_uploads/Hy1xgRi8xg.png)

- `http://127.0.0.1:8000/api/teachers/{id}`: teachers PUT、DELETE
![image](https://hackmd.io/_uploads/ByX3ZRjIxe.png)
![image](https://hackmd.io/_uploads/SyZpZCiUxx.png)

- `http://127.0.0.1:8000/api/students`: students GET、POST
![image](https://hackmd.io/_uploads/B1KzxRi8ex.png)
![image](https://hackmd.io/_uploads/HkqXe0i8lg.png)

- `http://127.0.0.1:8000/api/students/{id}`: students PUT、DELETE
![image](https://hackmd.io/_uploads/SkNGGAsIex.png)
![image](https://hackmd.io/_uploads/By7c4RsIel.png)



#### 3.5. 至瀏覽器以`http://127.0.0.1:8000/admin` 即可以superuser 身分登入對 tabels 進行 CRUD
![image](https://hackmd.io/_uploads/SJkYRasIxg.png)
![image](https://hackmd.io/_uploads/H1Y5ApsUxg.png)
![image](https://hackmd.io/_uploads/r1tR0TsLxg.png)
![image](https://hackmd.io/_uploads/rkBlk0sIxl.png)
![image](https://hackmd.io/_uploads/B1DJyCo8el.png)
![image](https://hackmd.io/_uploads/BJyG1CsLge.png)
![image](https://hackmd.io/_uploads/Hknf1Ri8le.png)
![image](https://hackmd.io/_uploads/BJYX10iIgx.png)
### 4. API list
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

### 5. postman 測試 CRUD
- GET teachers
![image](https://hackmd.io/_uploads/HJggsjiLlx.png)
- GET teachers {id}
![image](https://hackmd.io/_uploads/BJ6A3ssLgx.png)
- POST teachers
![image](https://hackmd.io/_uploads/S1lmC3sUxg.png)
- PUT teachers {id}
![image](https://hackmd.io/_uploads/B1SEeTs8ee.png)
- DELETE teachers {id}
![image](https://hackmd.io/_uploads/HJzblToLgx.png)
![image](https://hackmd.io/_uploads/rkGsx6oLxl.png)

- GET students
![image](https://hackmd.io/_uploads/ryaPGajUgg.png)
- GET students {id}
![image](https://hackmd.io/_uploads/ryI6G6jLgg.png)

- POST students
![image](https://hackmd.io/_uploads/BkvGr2oUxe.png)

- PUT students {id}
![image](https://hackmd.io/_uploads/Hy3g8ni8gx.png)
- DELETE student {id}
![image](https://hackmd.io/_uploads/rJGVQaoLll.png)
![image](https://hackmd.io/_uploads/Hyp2X6oIxe.png)
