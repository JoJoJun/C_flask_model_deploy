import json
import unittest
import project

app = project.create_app()

class LoginTest(unittest.TestCase):
    """为新建项目逻辑编写测试案例"""

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_login(self):
        """测试登录"""
        ret = self.client.post("/account/login/", data={'account':'123@123.com','password':'123456'})
        # ret是视图返回的响应对象，data属性是响应的数据
        resp = ret.data
        # 因为login驶入返回的是json字符串
        resp = json.loads(resp)
        print('resp:',resp)
        # 拿到返回值后进行断言测试
        self.assertIsNotNone(resp, '登录成功')
        self.assertIn("code", resp)
        self.assertEqual(resp["code"], 1000)

    def test_username_password_wrong(self):
        """测试用户名密码不正确"""
        ret = self.client.post("/account/login/", data={'account':'123@123.com','password':'12345678'})
        # ret是视图返回的响应对象，data属性是响应的数据
        resp = ret.data
        # 因为login驶入返回的是json字符串
        resp = json.loads(resp)
        # 拿到返回值后进行断言测试
        self.assertIsNotNone(resp, '密码或用户名有误')
        self.assertIn("code", resp)
        self.assertEqual(resp["code"], 2017)




if __name__ == '__main__':
    unittest.main()
'''
assertEqual     如果两个值相等，则pass
assertNotEqual  如果两个值不相等，则pass
assertTrue      判断bool值为True，则pass
assertFalse     判断bool值为False，则pass
assertIsNone    不存在，则pass
assertIsNotNone 存在，则pass
'''