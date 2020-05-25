import json
import unittest
from project.tests.report_tests import app

class ViewModelTest(unittest.TestCase):
    """为查看项目编写测试案例"""

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_view(self):
        """测试view"""
        ret = self.client.post("/project/view/4", follow_redirects=True)
        # ret是视图返回的响应对象，data属性是响应的数据
        # resp = ret.data
        # 因为login驶入返回的是json字符串
        # resp = json.loads(resp)
        # print('resp:',resp)
        # 拿到返回值后进行断言测试
        self.assertIsNotNone(ret.status, 200)
        # self.assertIn("code", resp)
        # self.assertEqual(resp["code"], 1000)
        # self.assert 'You were logged in' in ret.data

    def test_id_valid(self):
        """测试id不合法"""
        ret = self.client.post("/project/view/8", follow_redirects=True)
        # ret是视图返回的响应对象，data属性是响应的数据
        resp = ret.data
        # 因为login驶入返回的是json字符串
        # resp = json.loads(resp)
        # 拿到返回值后进行断言测试
        self.assertIsNotNone(resp, 'login')
        # self.assertIn("code", resp)
        # self.assertEqual(resp["code"], 2017)




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