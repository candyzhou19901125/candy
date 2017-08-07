from django.test import TestCase
from sign.models import Event, Guest
from django.contrib.auth.models import User


# Create your tests here.
class ModelTest(TestCase):
    def setUp(self):
        Event.objects.create(id=1, name="oneplus 3 event", status=True, limit=2000,
                             address="shenzhen", start_time="2017-9-20 02:18:22")
        Guest.objects.create(id=1, event_id=1, realname="allen", phone="13928093625",
                             email="allen@gmail.com", sign=False)

    def test_event_models(self):
        result = Event.objects.get(name="oneplus 3 event")
        self.assertEqual(result.address, "shenzhen")
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone="13928093625")
        self.assertEqual(result.realname, "allen")
        self.assertFalse(result.sign)


# 测试Index视图
class IndexPageTest(TestCase):
    def test_index_page_renders_index_template(self):
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class LoginActionTest(TestCase):
    """测试登录动作"""
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')

    def test_add_admin(self):
        """测试添加用户"""
        user = User.objects.get(username="admin")
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.email, "admin@mail.com")

    def test_login_action_username_password_null(self):
        """用户名密码为空"""
        test_data = {'username': '', 'password': ''}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or  password null!", response.content)

    def test_login_action_username_password_error(self):
        """用户名密码错误"""
        test_data ={'username': 'abc', 'password': '123'}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or  password error!", response.content)

    def test_login_action_success(self):
        """登录成功"""
        test_data = {'username': 'admin', 'password': 'admin123456'}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 302)


class EventManageTest(TestCase):
    """发布会管理"""
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(name='sweetwatch', limit=1500, address='beijing', status=1,
                             start_time='2017-9-15 12:30:00')
        login_user = {'username': 'admin', 'password': 'admin123456'}
        self.client.post('/login_action/', data=login_user)  # 预先登录

    def test_add_event(self):
        """测试添加event """
        event = Event.objects.get(name="sweetwatch")
        self.assertIn(event.name, "sweetwatch")
        self.assertIn(event.address, "beijing")

    def test_event_manage_success(self):
        """测试发布会：sweetwatch"""
        response = self.client.get('/event_manage/')
        self.assertEqual(response.status_code, 200)
        # print(response.content)
        self.assertIn(b"sweetwatch", response.content)
        self.assertIn(b"beijing",  response.content)

    def test_event_manage_search_success(self):
        """测试发布会搜索"""
        response = self.client.get('/search_name/', {'name': 'sweetwatch'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"sweetwatch", response.content)
        self.assertIn(b"beijing", response.content)


class GuestManageTest(TestCase):
    """测试嘉宾管理"""
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(id=1, name="smartwatch", limit=2000, address="beijing", status=1,
                             start_time='2017-10-6 14:00:00')
        Guest.objects.create(realname="allen", phone="15170461073", email="allen@163.com", sign=0, event_id=1)
        login_user = {'username': 'admin', 'password': 'admin123456'}
        self.client.post("/login_action/", data=login_user)  # 预先登录

    def test_add_guest(self):
        """测试添加event """
        guest = Guest.objects.get(realname="allen")
        self.assertIn(guest.realname, "allen")
        self.assertIn(guest.phone, "15170461073")
        self.assertFalse(guest.sign)

    def test_guest_manage_success(self):
        """测试发布会：sweetwatch"""
        response = self.client.get('/guest_manage/')
        print(response.status_code)
        self.assertEqual(response.status_code, 200)
        # print(response.content)
        self.assertIn(b"allen", response.content)
        self.assertIn(b"15170461073",  response.content)

    def test_event_manage_search_success(self):
        """测试发布会搜索"""
        response = self.client.get('/search_phone/', {'phone': '15170461073'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"allen", response.content)
        self.assertIn(b"allen@163.com", response.content)


class SignIndexActionTest(TestCase):
    """发布会签到"""
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(id=1, name="smartwatch", limit=2000, address="beijing", status=1,
                             start_time='2017-10-6 14:00:00')
        Event.objects.create(id=2, name="sweetwatch", limit=2000, address="shenzhen", status=1,
                             start_time='2017-10-9 14:00:00')
        Guest.objects.create(realname="allen", phone=15170461073, email="allen@163.com", sign=0, event_id=1)
        Guest.objects.create(realname="lisi", phone=17456238925, email="lisi@163.com", sign=1, event_id=2)
        login_user = {'username': 'admin', 'password': 'admin123456'}
        self.client.post("/login_action/", data=login_user)

    def test_sign_index_action_phone_null(self):
        """手机号为空"""
        response = self.client.post('/sign_index_action/1/', {"phone": ""})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"phone error.", response.content)

    def test_sign_index_action_phone_or_event_id_error(self):
        """手机号或发布会id错误"""
        response = self.client.post('/sign_index_action/2/', {"phone": 15170461073})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"event id or phone error.", response.content)

    def test_sign_index_action_user_sign_has(self):
        """用户已签到"""
        response = self.client.post('/sign_index_action/2/', {"phone": 17456238925})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"user has sign in.", response.content)

    def test_sign_index_action_sign_success(self):
        """签到成功"""
        response = self.client.post('/sign_index_action/1/', {"phone": 15170461073})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"sign in success!", response.content)













