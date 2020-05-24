import json
import unittest
import project

app = project.create_app()

class PauseModelTest(unittest.TestCase):
    """为暂停实例编写测试案例"""

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_pause_model(self):
        """测试暂停"""
        ret = self.client.post("/record/pauseModel/", data={'model_id':6})
        # ret  =self.client.login(account='123@123.com',password='123456')
        # ret是视图返回的响应对象，data属性是响应的数据
        resp = ret.data
        # print(resp)
        resp = json.loads(resp)
        # 拿到返回值后进行断言测试
        self.assertIsNotNone(resp, '实例暂停失败')
        # self.assertIn("code", resp)
        self.assertEqual(resp["code"], 2000)

    def test_record_paused(self):
        """测试不能暂停的状态"""
        ret = self.client.post("/record/pauseModel/", data={'model_id':3})
        # ret是视图返回的响应对象，data属性是响应的数据
        resp = ret.data
        # 因为login驶入返回的是json字符串
        resp = json.loads(resp)
        # 拿到返回值后进行断言测试
        self.assertIsNotNone(resp, '实例已在暂停状态')
        # self.assertIn("code", resp)
        self.assertEqual(resp["code"], 2014)


    def test_record_0(self):
        """测试未部署的状态"""
        ret = self.client.post("/record/pauseModel/", data={'model_id': 4})
        # ret是视图返回的响应对象，data属性是响应的数据
        resp = ret.data
        print(resp)
        # 因为login驶入返回的是json字符串
        resp = json.loads(resp)
        # 拿到返回值后进行断言测试
        self.assertIsNotNone(resp, '服务未启动')
        # self.assertIn("code", resp)
        self.assertEqual(resp["code"], 2012)



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