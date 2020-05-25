import json
import unittest
from project.tests.report_tests import app

class RestartModelTest(unittest.TestCase):
    """为恢复实例编写测试案例"""

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_restart_model(self):
        """测试恢复"""
        ret = self.client.post("/record/restartModel/", data={'model_id':3})
        # ret  =self.client.login(account='123@123.com',password='123456')
        # ret是视图返回的响应对象，data属性是响应的数据
        resp = ret.data
        # 因为login驶入返回的是json字符串
        resp = json.loads(resp)
        # print(resp)
        # print('resp:',resp)
        # 拿到返回值后进行断言测试
        self.assertIsNotNone(resp, '实例恢复失败')
        # self.assertIn("code", resp)
        self.assertEqual(resp["code"], 2000)
        # self.assert 'You were logged in' in ret.data

    def test_record_running(self):
        """测试不能恢复的状态"""
        ret = self.client.post("/record/restartModel/", data={'model_id':6})
        # ret是视图返回的响应对象，data属性是响应的数据
        resp = ret.data
        # 因为login驶入返回的是json字符串
        resp = json.loads(resp)
        # 拿到返回值后进行断言测试
        self.assertIsNotNone(resp, '实例已在运行状态')
        # self.assertIn("code", resp)
        self.assertEqual(resp["code"], 2015)

    def test_record_0(self):
        """测试未部署的状态"""
        ret = self.client.post("/record/restartModel/", data={'model_id': 4})
        # ret是视图返回的响应对象，data属性是响应的数据
        resp = ret.data
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