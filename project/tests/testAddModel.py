import json
import unittest
from project.tests.report_tests import app

class AddProTest(unittest.TestCase):
    """为导入模型逻辑编写测试案例"""

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_wrong_param(self):
        """测试输入错误的参数"""
        ret = self.client.post("/model/addModel/21", data={'name':'测试项目1','url':'url','description':'des'})
        # ret是视图返回的响应对象，data属性是响应的数据
        resp = ret.data
        # 因为login驶入返回的是json字符串
        resp = json.loads(resp)
        # 拿到返回值后进行断言测试
        self.assertIsNotNone(resp, '我获取到数据')
        self.assertIn("code", resp)
        self.assertEqual(resp["code"], 2000)

    def test_lack_param(self):
        """测试输入不全的参数"""
        ret = self.client.post("/model/addModel/21", data={'name':'测试项目1模型','type':'','description':'des','version':'','file':''})
        # ret是视图返回的响应对象，data属性是响应的数据
        resp = ret.data
        # 因为login驶入返回的是json字符串
        resp = json.loads(resp)
        # 拿到返回值后进行断言测试
        self.assertIsNotNone(resp, '我获取到数据')
        self.assertIn("code", resp)
        self.assertEqual(resp["code"], 2000)


    def test_lack_file(self):
        """测试输入不全的文件"""
        ret = self.client.post("/model/addModel/21", data={'name':'测试项目1模型','type':'H5','description':'des','version':'1','file':''})
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
