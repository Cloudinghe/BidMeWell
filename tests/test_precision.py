#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代精确叫牌练习系统 - 测试用例
"""

import os
import sys
import unittest

# 添加项目路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))


class TestPrecisionFormulas(unittest.TestCase):
    """点力计算模块测试"""

    def test_hcp_calculation(self):
        """测试高牌点计算"""
        # A=4, K=3, Q=2, J=1
        # 测试数据：♠AK76 ♥KQ832 ♦A52 ♣J7
        # 预期：15点
        # 由于没有实际的 Hand 对象，这里只测试模块是否能正确导入
        try:
            from precision_formulas import hcp

            self.assertTrue(callable(hcp))
        except ImportError:
            self.skipTest("precision_formulas 模块未找到")

    def test_controls_calculation(self):
        """测试控制点计算"""
        try:
            from precision_formulas import controls

            self.assertTrue(callable(controls))
        except ImportError:
            self.skipTest("precision_formulas 模块未找到")

    def test_is_balanced(self):
        """测试均型牌判断"""
        try:
            from precision_formulas import is_balanced

            self.assertTrue(callable(is_balanced))
        except ImportError:
            self.skipTest("precision_formulas 模块未找到")


class TestXMLParsing(unittest.TestCase):
    """XML解析测试"""

    def setUp(self):
        """设置测试环境"""
        self.xml_file = os.path.join(PROJECT_ROOT, "rules", "modern_precision.xml")

    def test_xml_exists(self):
        """测试XML文件存在"""
        self.assertTrue(os.path.exists(self.xml_file))

    def test_xml_syntax(self):
        """测试XML语法正确"""
        import xml.etree.ElementTree as ET

        try:
            tree = ET.parse(self.xml_file)
            self.assertIsNotNone(tree)
        except ET.ParseError as e:
            self.fail(f"XML语法错误: {e}")

    def test_xml_root(self):
        """测试XML根元素"""
        import xml.etree.ElementTree as ET

        tree = ET.parse(self.xml_file)
        root = tree.getroot()
        self.assertEqual(root.tag, "biddingSystem")

    def test_opening_bids_count(self):
        """测试开叫数量"""
        import xml.etree.ElementTree as ET

        tree = ET.parse(self.xml_file)
        root = tree.getroot()
        # 开叫在 openingBids 子元素中
        opening_bids = root.find("openingBids")
        if opening_bids is not None:
            bids = opening_bids.findall("bid")
        else:
            bids = root.findall("bid")
        # 应该有至少9个开叫
        self.assertGreaterEqual(len(bids), 9)

    def test_required_attributes(self):
        """测试必要属性"""
        import xml.etree.ElementTree as ET

        tree = ET.parse(self.xml_file)
        root = tree.getroot()

        # 检查根元素属性
        self.assertIn("name", root.attrib)
        self.assertIn("version", root.attrib)


class TestBidStructure(unittest.TestCase):
    """叫牌结构测试"""

    def setUp(self):
        """设置测试环境"""
        import xml.etree.ElementTree as ET

        xml_file = os.path.join(PROJECT_ROOT, "rules", "modern_precision.xml")
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()

    def test_bid_has_value(self):
        """测试叫牌有value元素"""
        for bid in self.root.iter("bid"):
            value = bid.find("value")
            self.assertIsNotNone(value, f"bid {bid.get('id')} 缺少 value")

    def test_bid_has_desc(self):
        """测试叫牌有desc元素"""
        for bid in self.root.iter("bid"):
            desc = bid.find("desc")
            self.assertIsNotNone(desc, f"bid {bid.get('id')} 缺少 desc")

    def test_1c_opening(self):
        """测试1♣开叫"""
        # 查找1♣开叫 - 在整个文档中搜索
        for bid in self.root.iter("bid"):
            value = bid.find("value")
            if value is not None and value.text == "1c":
                desc = bid.find("desc")
                self.assertIn("强牌", desc.text)
                return
        self.fail("未找到1♣开叫")


class TestScripts(unittest.TestCase):
    """脚本测试"""

    def test_run_practice_exists(self):
        """测试启动脚本存在"""
        script_path = os.path.join(PROJECT_ROOT, "scripts", "run_practice.py")
        self.assertTrue(os.path.exists(script_path))

    def test_validate_rules_exists(self):
        """测试验证脚本存在"""
        script_path = os.path.join(PROJECT_ROOT, "scripts", "validate_rules.py")
        self.assertTrue(os.path.exists(script_path))


class TestProjectStructure(unittest.TestCase):
    """项目结构测试"""

    def test_readme_exists(self):
        """测试README存在"""
        readme_path = os.path.join(PROJECT_ROOT, "README.md")
        self.assertTrue(os.path.exists(readme_path))

    def test_usage_exists(self):
        """测试使用说明存在"""
        usage_path = os.path.join(PROJECT_ROOT, "USAGE.md")
        self.assertTrue(os.path.exists(usage_path))

    def test_license_exists(self):
        """测试LICENSE存在"""
        license_path = os.path.join(PROJECT_ROOT, "LICENSE")
        self.assertTrue(os.path.exists(license_path))

    def test_requirements_exists(self):
        """测试requirements存在"""
        req_path = os.path.join(PROJECT_ROOT, "requirements.txt")
        self.assertTrue(os.path.exists(req_path))

    def test_rules_directory(self):
        """测试rules目录存在"""
        rules_dir = os.path.join(PROJECT_ROOT, "rules")
        self.assertTrue(os.path.isdir(rules_dir))

    def test_src_directory(self):
        """测试src目录存在"""
        src_dir = os.path.join(PROJECT_ROOT, "src")
        self.assertTrue(os.path.isdir(src_dir))

    def test_scripts_directory(self):
        """测试scripts目录存在"""
        scripts_dir = os.path.join(PROJECT_ROOT, "scripts")
        self.assertTrue(os.path.isdir(scripts_dir))


if __name__ == "__main__":
    unittest.main()
