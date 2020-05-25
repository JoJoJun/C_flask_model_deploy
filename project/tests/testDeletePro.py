import json
import unittest
import project

app = project.create_app()

class DeleteProTest(unittest.TestCase):
    """为删除项目逻辑编写测试案例"""

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_delete_empty_project(self):
        """测试删除一个空项目"""
        ret = self.client.post("/project/deletePro/", data={'id':36})
        # ret是视图返回的响应对象，data属性是响应的数据
        resp = ret.data
        # 因为login驶入返回的是json字符串
        resp = json.loads(resp)
        # 拿到返回值后进行断言测试
        self.assertIsNotNone(resp, '删除成功')
        self.assertIn("code", resp)
        self.assertEqual(resp["code"], 1000)
    def test_delete_model_project(self):
        """测试删除有模型的项目"""
        ret = self.client.post("/project/deletePro/", data={'id': 37})
        # ret是视图返回的响应对象，data属性是响应的数据
        resp = ret.data
        # 因为login驶入返回的是json字符串
        resp = json.loads(resp)
        # 拿到返回值后进行断言测试
        self.assertIsNotNone(resp, '删除成功')
        self.assertIn("code", resp)
        self.assertEqual(resp["code"], 1000)



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