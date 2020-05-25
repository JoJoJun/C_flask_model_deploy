import json
import unittest
from project.tests.report_tests import app

class AddProTest(unittest.TestCase):
    """为导入模型逻辑编写测试案例"""

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_lack_param(self):
        """测试参数缺失"""
        ret = self.client.post("/record/startModel/", data={'model_id':''})
        # ret是视图返回的响应对象，data属性是响应的数据
        resp = ret.data
        # 因为login驶入返回的是json字符串
        resp = json.loads(resp)
        # 拿到返回值后进行断言测试
        self.assertIsNotNone(resp, '我获取到数据')
        self.assertIn("code", resp)
        self.assertEqual(resp["code"], 1005)

    def test_wrong_param(self):
        """测试错误的参数"""
        ret = self.client.post("/record/startModel/", data={'model_id':'hhh'})
        # ret是视图返回的响应对象，data属性是响应的数据
        resp = ret.data
        # 因为login驶入返回的是json字符串
        resp = json.loads(resp)
        # 拿到返回值后进行断言测试
        self.assertIsNotNone(resp, '我获取到数据')
        self.assertIn("code", resp)
        self.assertEqual(resp["code"], 2000)


    def test_started(self):
        """测试实例正在运行"""
        ret = self.client.post("/record/startModel/", data={'model_id':'61'})
        # ret是视图返回的响应对象，data属性是响应的数据
        resp = ret.data
        # 因为login驶入返回的是json字符串
        resp = json.loads(resp)
        # 拿到返回值后进行断言测试
        self.assertIsNotNone(resp, '我获取到数据')
        self.assertIn("code", resp)
        self.assertEqual(resp["code"], 2015)

    def test_wrong_envir(self):
        """测试错误的运行环境"""
        ret = self.client.post("/record/startModel/", data={'model_id': '111'})
        # ret是视图返回的响应对象，data属性是响应的数据
        resp = ret.data
        # 因为login驶入返回的是json字符串
        resp = json.loads(resp)
        # 拿到返回值后进行断言测试
        self.assertIsNotNone(resp, '我获取到数据')
        self.assertIn("code", resp)
        self.assertEqual(resp["code"], 2000)

if __name__ == '__main__':
    unittest.main()
