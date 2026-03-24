#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代精确叫牌规则验证脚本

验证XML规则文件的正确性和完整性
"""

import os
import sys
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple

# 项目路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_RULES = os.path.join(PROJECT_ROOT, "rules", "modern_precision.xml")


def validate_xml_syntax(xml_file: str) -> Tuple[bool, str]:
    """验证XML语法"""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        return True, "XML语法正确"
    except ET.ParseError as e:
        return False, f"XML语法错误: {e}"
    except Exception as e:
        return False, f"解析错误: {e}"


def count_bids(root) -> Dict[str, int]:
    """统计叫牌规则数量"""
    stats = {
        "opening_bids": 0,  # 开叫
        "responses": 0,  # 应叫
        "rebid": 0,  # 再叫
        "total": 0,  # 总计
    }

    def count_recursive(element, depth=0):
        bids = element.findall("bid")
        for bid in bids:
            stats["total"] += 1
            if depth == 0:
                stats["opening_bids"] += 1
            elif depth == 1:
                stats["responses"] += 1
            else:
                stats["rebid"] += 1
            count_recursive(bid, depth + 1)

    count_recursive(root)
    return stats


def validate_bid_structure(bid_element) -> List[str]:
    """验证单个叫牌的结构"""
    errors = []

    # 检查必要元素
    value = bid_element.find("value")
    desc = bid_element.find("desc")

    if value is None:
        errors.append(f"缺少 <value> 元素")
    elif value.text is None or value.text.strip() == "":
        errors.append(f"<value> 元素为空")

    if desc is None:
        errors.append(f"缺少 <desc> 元素")
    elif desc.text is None or desc.text.strip() == "":
        errors.append(f"<desc> 元素为空")

    return errors


def validate_all_bids(root) -> Tuple[int, List[str]]:
    """验证所有叫牌"""
    total_checked = 0
    all_errors = []

    def check_bid(bid_element, path=""):
        nonlocal total_checked
        total_checked += 1

        bid_id = bid_element.get("id", "unknown")
        current_path = f"{path}/{bid_id}" if path else bid_id

        errors = validate_bid_structure(bid_element)
        for error in errors:
            all_errors.append(f"[{current_path}] {error}")

        # 递归检查子叫牌
        for child in bid_element.findall("bid"):
            check_bid(child, current_path)

    for opening_bid in root.findall("bid"):
        check_bid(opening_bid)

    return total_checked, all_errors


def print_validation_report(xml_file: str):
    """打印验证报告"""
    print("=" * 60)
    print("现代精确叫牌规则验证报告")
    print("=" * 60)
    print()
    print(f"规则文件: {xml_file}")
    print()

    # 1. 验证XML语法
    print("【1】XML语法验证")
    syntax_ok, syntax_msg = validate_xml_syntax(xml_file)
    print(f"    {'✓' if syntax_ok else '✗'} {syntax_msg}")

    if not syntax_ok:
        print()
        print("验证失败，请修复XML语法错误后重试。")
        return False

    # 解析XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 2. 统计规则数量
    print()
    print("【2】规则统计")
    stats = count_bids(root)
    print(f"    开叫规则: {stats['opening_bids']} 条")
    print(f"    应叫规则: {stats['responses']} 条")
    print(f"    再叫规则: {stats['rebid']} 条")
    print(f"    总计: {stats['total']} 条")

    # 3. 验证叫牌结构
    print()
    print("【3】叫牌结构验证")
    total_checked, errors = validate_all_bids(root)
    print(f"    已检查: {total_checked} 条")

    if errors:
        print(f"    发现错误: {len(errors)} 个")
        print()
        for error in errors[:10]:  # 只显示前10个错误
            print(f"    ✗ {error}")
        if len(errors) > 10:
            print(f"    ... 还有 {len(errors) - 10} 个错误")
    else:
        print(f"    ✓ 所有叫牌结构正确")

    # 4. 检查必要属性
    print()
    print("【4】根元素属性检查")
    hcp_attr = root.get("hcp", "未设置")
    shape_attr = root.get("shape", "未设置")
    formulas_attr = root.get("formulas", "未设置")

    print(f"    点力系统(hcp): {hcp_attr}")
    print(f"    牌型系统(shape): {shape_attr}")
    print(f"    公式模块(formulas): {formulas_attr}")

    # 5. 列出所有开叫
    print()
    print("【5】开叫列表")
    for i, bid in enumerate(root.findall("bid"), 1):
        value = bid.find("value")
        desc = bid.find("desc")
        value_text = value.text if value is not None else "?"
        desc_text = desc.text if desc is not None else "?"
        print(f"    {i}. {value_text} - {desc_text[:30]}...")

    # 6. 总结
    print()
    print("=" * 60)
    print("验证结果:")
    if syntax_ok and not errors:
        print("  ✓ 规则文件验证通过")
        print(f"  ✓ 共 {stats['total']} 条规则")
        return True
    else:
        print("  ✗ 规则文件存在问题，请修复后重试")
        return False


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="验证现代精确叫牌规则文件")
    parser.add_argument("-r", "--rules", default=DEFAULT_RULES, help="规则文件路径")
    parser.add_argument("-v", "--verbose", action="store_true", help="显示详细信息")

    args = parser.parse_args()

    if not os.path.exists(args.rules):
        print(f"错误：规则文件不存在: {args.rules}")
        sys.exit(1)

    success = print_validation_report(args.rules)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
