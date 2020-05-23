import json
import unittest
import project

app = project.create_app()

class AddProTest(unittest.TestCase):
    """为导入模型逻辑编写测试案例"""

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_wrong_param(self):
        """测试输入错误的参数"""
        ret = self.client.post("/model/editParam/57", data={'input':'node1','output':'node2','mem':'true'})
        # ret是视图返回的响应对象，data属性是响应的数据
        resp = ret.data
        # 因为login驶入返回的是json字符串
        resp = json.loads(resp)
        # 拿到返回值后进行断言测试
        self.assertIsNotNone(resp, '我获取到数据')
        self.assertIn("code", resp)
        self.assertEqual(resp["code"], 2000)

    def test_deployed(self):
        """测试已经部署的模型"""
        ret = self.client.post("/model/editParam/81", data={'input':'node1','output':'node2','mem':'true'})
        # ret是视图返回的响应对象，data属性是响应的数据
        resp = ret.data
        # 因为login驶入返回的是json字符串
        resp = json.loads(resp)
        # 拿到返回值后进行断言测试
        self.assertIsNotNone(resp, '我获取到数据')
        self.assertIn("code", resp)
        self.assertEqual(resp["code"], 2019)

    def test_wrong_path(self):
        """测试已经部署的模型"""
        ret = self.client.post("/model/editParam/79", data={'input':'node1','output':'node2','mem':'true'})
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
