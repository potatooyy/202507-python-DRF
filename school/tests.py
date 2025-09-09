# school/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from datetime import datetime
from .models import Teacher, Student, Title, Role

class BaseTestCase(APITestCase):
    """基礎測試類，設置常用的測試數據和認證"""
    
    def setUp(self):
        # 建立超級使用者
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        
        # 建立一般使用者
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # 建立測試教師
        self.teacher1 = Teacher.objects.create(
            teacher_name="test_teacher1",
            staff_id="T001",
            title=Title.PROFESSOR,
            department_id="CS"
        )
        
        self.teacher2 = Teacher.objects.create(
            teacher_name="test_teacher2",
            staff_id="T002", 
            title=Title.ASSISTANT_PROFESSOR,
            department_id="EE"
        )
        
        # 建立測試學生
        self.student1 = Student.objects.create(
            student_name="test_student1",
            student_id="S001",
            role=Role.STUDENT,
            department_id="CS",
            enroll_year=2022,
            class_id="CS101",
            mentor=self.teacher1,
            advisor=self.teacher2
        )

class TeacherViewSetTest(BaseTestCase):
    """測試 TeacherViewSet"""
    
    def test_list_teachers_unauthenticated(self):
        """測試未認證用戶是否能取得教師列表"""
        url = reverse('teacher-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_list_teachers_authenticated(self):
        """測試已認證用戶取得教師列表"""
        self.client.force_authenticate(user=self.user)
        url = reverse('teacher-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_list_teachers_superuser(self):
        """測試管理員取得教師列表"""
        self.client.force_authenticate(user=self.superuser)
        url = reverse('teacher-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_retrieve_teacher(self):
        """測試取得單一教師詳情"""
        url = reverse('teacher-detail', kwargs={'pk': self.teacher1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['teacher_name'], 'test_teacher1')
        self.assertEqual(response.data['staff_id'], 'T001')
        self.assertEqual(len(response.data['mentees']), 1)
        self.assertEqual(len(response.data['advisees']), 0)
    
    def test_create_single_teacher(self):
        """測試建立單一教師"""
        url = reverse('teacher-list')
        data = {
            'teacher_name': '新教師',
            'staff_id': 'T003',
            'title': Title.LECTURER,
            'department_id': 'MATH'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Teacher.objects.count(), 3)
        
        # 驗證建立的教師資料
        new_teacher = Teacher.objects.get(staff_id='T003')
        self.assertEqual(new_teacher.teacher_name, '新教師')
        self.assertEqual(new_teacher.title, Title.LECTURER)
    
    def test_create_multiple_teachers(self):
        """測試批量建立教師"""
        url = reverse('teacher-list')
        data = [
            {
                'teacher_name': '教師A',
                'staff_id': 'TA01',
                'title': Title.PROFESSOR,
                'department_id': 'PHYSICS'
            },
            {
                'teacher_name': '教師B',
                'staff_id': 'TB01',
                'title': Title.ASSOCIATE_PROFESSOR,
                'department_id': 'CHEMISTRY'
            }
        ]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Teacher.objects.count(), 4)
        
        # 驗證資料
        self.assertTrue(Teacher.objects.filter(staff_id='TA01').exists())
        self.assertTrue(Teacher.objects.filter(staff_id='TB01').exists())
    
    def test_create_teacher_invalid_data(self):
        """測試用無效資料建立教師"""
        url = reverse('teacher-list')
        data = {
            'teacher_name': '',  # 空的名字
            'staff_id': 'T001',  # 重複的 staff_id
            'title': 'invalid_title',  # 無效的職稱
            'department_id': 'CS'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_teacher(self):
        """測試更新教師資料"""
        url = reverse('teacher-detail', kwargs={'pk': self.teacher1.pk})
        data = {
            'teacher_name': 'test_teacher1更新',
            'staff_id': 'T001',
            'title': Title.ASSOCIATE_PROFESSOR,
            'department_id': 'CS'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 驗證更新
        self.teacher1.refresh_from_db()
        self.assertEqual(self.teacher1.teacher_name, 'test_teacher1更新')
        self.assertEqual(self.teacher1.title, Title.ASSOCIATE_PROFESSOR)
    
    def test_partial_update_teacher(self):
        """測試部分更新教師資料"""
        url = reverse('teacher-detail', kwargs={'pk': self.teacher1.pk})
        data = {'teacher_name': 'test_teacher1部分更新'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 驗證更新
        self.teacher1.refresh_from_db()
        self.assertEqual(self.teacher1.teacher_name, 'test_teacher1部分更新')
        self.assertEqual(self.teacher1.staff_id, 'T001')  # 其他欄位保持不變
    
    def test_delete_teacher(self):
        """測試刪除教師"""
        teacher_count_before = Teacher.objects.count()
        url = reverse('teacher-detail', kwargs={'pk': self.teacher2.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Teacher.objects.count(), teacher_count_before - 1)
        self.assertFalse(Teacher.objects.filter(pk=self.teacher2.pk).exists())

class StudentViewSetTest(BaseTestCase):
    """測試 StudentViewSet"""
    
    def test_list_students(self):
        """測試取得學生列表"""
        url = reverse('student-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_retrieve_student(self):
        """測試取得單一學生詳情"""
        url = reverse('student-detail', kwargs={'pk': self.student1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['student_name'], 'test_student1')
        self.assertEqual(response.data['student_id'], 'S001')
        self.assertEqual(response.data['mentor']['teacher_name'], 'test_teacher1')
        self.assertEqual(response.data['advisor']['teacher_name'], 'test_teacher2')
    
    def test_student_grade_calculation(self):
        """測試學生年級計算"""
        # 測試 2022 年入學的學生在不同時間點的年級
        url = reverse('student-detail', kwargs={'pk': self.student1.pk})
        response = self.client.get(url)
        
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        if current_month >= 8:
            expected_grade = current_year - 2022 + 1
        else:
            expected_grade = current_year - 2022
            
        # 確保年級至少為 1
        expected_grade = max(expected_grade, 1)
        
        self.assertEqual(response.data['grade'], expected_grade)
    
    def test_create_single_student(self):
        """測試建立單一學生"""
        url = reverse('student-list')
        data = {
            'student_name': '新學生',
            'student_id': 'S002',
            'role': Role.STUDENT,
            'department_id': 'EE',
            'enroll_year': 2023,
            'class_id': 'EE101',
            'mentor_id': self.teacher1.pk,
            'advisor_id': self.teacher2.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 2)
        
        # 驗證建立的學生資料
        new_student = Student.objects.get(student_id='S002')
        self.assertEqual(new_student.student_name, '新學生')
        self.assertEqual(new_student.mentor, self.teacher1)
        self.assertEqual(new_student.advisor, self.teacher2)
    
    def test_create_multiple_students(self):
        """測試批量建立學生"""
        url = reverse('student-list')
        data = [
            {
                'student_name': '學生A',
                'student_id': 'SA01',
                'role': Role.CLASS_PRESIDENT,
                'department_id': 'CS',
                'enroll_year': 2023,
                'class_id': 'CS201',
                'mentor_id': self.teacher1.pk,
                'advisor_id': self.teacher2.pk
            },
            {
                'student_name': '學生B',
                'student_id': 'SB01',
                'role': Role.CLASS_OFFICER,
                'department_id': 'EE',
                'enroll_year': 2023,
                'class_id': 'EE201',
                'mentor_id': self.teacher2.pk,
                'advisor_id': self.teacher1.pk
            }
        ]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 3)
        
        # 驗證資料
        student_a = Student.objects.get(student_id='SA01')
        student_b = Student.objects.get(student_id='SB01')
        self.assertEqual(student_a.role, Role.CLASS_PRESIDENT)
        self.assertEqual(student_b.role, Role.CLASS_OFFICER)
    
    def test_create_student_without_mentor(self):
        """測試建立沒有導師的學生"""
        url = reverse('student-list')
        data = {
            'student_name': '無導師學生',
            'student_id': 'S_NO_MENTOR',
            'role': Role.STUDENT,
            'department_id': 'MATH',
            'enroll_year': 2023,
            'class_id': 'MATH101',
            # 'mentor_id': None,
            # 'advisor_id': None
        }
        response = self.client.post(url, data, format='json')
        print(f"Response status: {response.status_code}")  # 調試用
        if response.status_code != 201:
            print(f"Response data: {response.data}")  # 調試用
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        new_student = Student.objects.get(student_id='S_NO_MENTOR')
        self.assertIsNone(new_student.mentor)
        self.assertIsNone(new_student.advisor)
    
    def test_create_student_invalid_mentor(self):
        """測試用不存在的導師 ID 建立學生"""
        url = reverse('student-list')
        data = {
            'student_name': '測試學生',
            'student_id': 'S_INVALID',
            'role': Role.STUDENT,
            'department_id': 'CS',
            'enroll_year': 2023,
            'class_id': 'CS101',
            'mentor_id': 999,  # 不存在的 ID
            'advisor_id': 999   # 不存在的 ID
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_student(self):
        """測試更新學生資料"""
        url = reverse('student-detail', kwargs={'pk': self.student1.pk})
        data = {
            'student_name': 'test_student1更新',
            'student_id': 'S001',
            'role': Role.CLASS_PRESIDENT,
            'department_id': 'CS',
            'enroll_year': 2022,
            'class_id': 'CS102',
            'mentor_id': self.teacher2.pk,
            'advisor_id': self.teacher1.pk
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 驗證更新
        self.student1.refresh_from_db()
        self.assertEqual(self.student1.student_name, 'test_student1更新')
        self.assertEqual(self.student1.role, Role.CLASS_PRESIDENT)
        self.assertEqual(self.student1.mentor, self.teacher2)
        self.assertEqual(self.student1.advisor, self.teacher1)
    
    def test_delete_student(self):
        """測試刪除學生"""
        student_count_before = Student.objects.count()
        url = reverse('student-detail', kwargs={'pk': self.student1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Student.objects.count(), student_count_before - 1)

class AuthenticationTest(BaseTestCase):
    """測試認證相關功能"""
    
    def test_admin_login_required_for_admin_panel(self):
        """測試管理後台需要登入"""
        admin_url = reverse('admin:index')
        response = self.client.get(admin_url)
        # 應該重導向到登入頁面
        self.assertEqual(response.status_code, 302)
    
    def test_superuser_can_access_admin(self):
        """測試超級用戶可以存取管理後台"""
        self.client.force_authenticate(user=self.superuser)
        # 或使用 login 方式
        # self.client.login(username='admin', password='admin123')
        
        admin_url = reverse('admin:index')
        # 注意：這裡可能需要使用 Django 的 Client 而非 APIClient
        from django.test import Client
        client = Client()
        client.login(username='admin', password='admin123')
        response = client.get(admin_url)
        self.assertEqual(response.status_code, 200)

class ModelTest(TestCase):
    """測試模型方法和屬性"""
    
    def setUp(self):
        self.teacher = Teacher.objects.create(
            teacher_name="測試教師",
            staff_id="T999",
            title=Title.PROFESSOR,
            department_id="TEST"
        )
        
        self.student = Student.objects.create(
            student_name="測試學生",
            student_id="S999",
            role=Role.STUDENT,
            department_id="TEST",
            enroll_year=2020,
            class_id="TEST101",
            mentor=self.teacher
        )
    
    def test_teacher_str_method(self):
        """測試 Teacher 的 __str__ 方法"""
        expected = "T999 測試教師 professor"
        self.assertEqual(str(self.teacher), expected)
    
    def test_student_str_method(self):
        """測試 Student 的 __str__ 方法"""
        expected = "S999 測試學生"
        self.assertEqual(str(self.student), expected)
    
    def test_student_grade_property_past_august(self):
        """測試學生年級計算（8月後）"""
        # 假設現在是 2024 年 9 月，學生 2020 年入學
        with self.settings(USE_TZ=False):
            # 這裡可以使用 freezegun 來模擬時間，或者直接測試邏輯
            grade = self.student.grade
            self.assertIsInstance(grade, int)
            self.assertGreaterEqual(grade, 1)
    
    def test_choices_values(self):
        """測試選擇欄位的值"""
        # 測試 Title 選擇
        self.assertEqual(Title.PROFESSOR, 'professor')
        self.assertEqual(Title.LECTURER, 'lecturer')
        
        # 測試 Role 選擇
        self.assertEqual(Role.STUDENT, 'student')
        self.assertEqual(Role.CLASS_PRESIDENT, 'class_president')

class SerializerTest(TestCase):
    """測試序列化器"""
    
    def setUp(self):
        self.teacher = Teacher.objects.create(
            teacher_name="序列化測試教師",
            staff_id="SER001",
            title=Title.ASSISTANT_PROFESSOR,
            department_id="SER"
        )
    
    def test_teacher_serializer_validation(self):
        """測試 TeacherSerializer 驗證"""
        from .serializers import TeacherSerializer
        
        # 有效資料
        valid_data = {
            'teacher_name': '新教師',
            'staff_id': 'NEW001',
            'title': Title.LECTURER,
            'department_id': 'NEW'
        }
        serializer = TeacherSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        
        # 無效資料 - 重複的 staff_id
        invalid_data = {
            'teacher_name': '重複教師',
            'staff_id': 'SER001',  # 已存在
            'title': Title.LECTURER,
            'department_id': 'NEW'
        }
        serializer = TeacherSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
    
    def test_student_serializer_with_relations(self):
        """測試 StudentSerializer 的關聯欄位"""
        from .serializers import StudentSerializer
        
        data = {
            'student_name': '關聯測試學生',
            'student_id': 'REL001',
            'role': Role.STUDENT,
            'department_id': 'REL',
            'enroll_year': 2023,
            'class_id': 'REL101',
            'mentor_id': self.teacher.pk
        }
        serializer = StudentSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        student = serializer.save()
        self.assertEqual(student.mentor, self.teacher)

class PermissionTest(BaseTestCase):
    """測試權限相關功能（如果有設置權限的話）"""
    
    def test_unauthenticated_user_permissions(self):
        """測試未認證用戶的權限"""
        # 根據你的權限設置來調整這些測試
        url = reverse('teacher-list')
        response = self.client.get(url)
        # 假設允許未認證用戶查看列表
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_authenticated_user_permissions(self):
        """測試已認證用戶的權限"""
        self.client.force_authenticate(user=self.user)
        url = reverse('teacher-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class EdgeCaseTest(BaseTestCase):
    """測試邊界情況和異常處理"""
    
    def test_nonexistent_teacher_detail(self):
        """測試查詢不存在的教師"""
        url = reverse('teacher-detail', kwargs={'pk': 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_nonexistent_student_detail(self):
        """測試查詢不存在的學生"""
        url = reverse('student-detail', kwargs={'pk': 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_teacher_with_students(self):
        """測試刪除有學生的教師（測試 SET_NULL 行為）"""
        # 確保有學生關聯到這個教師
        self.assertEqual(self.student1.mentor, self.teacher1)
        
        url = reverse('teacher-detail', kwargs={'pk': self.teacher1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # 驗證學生的 mentor 被設為 NULL
        self.student1.refresh_from_db()
        self.assertIsNone(self.student1.mentor)
    
    def test_invalid_json_format(self):
        """測試無效的 JSON 格式"""
        url = reverse('teacher-list')
        response = self.client.post(
            url, 
            data='invalid json', 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

