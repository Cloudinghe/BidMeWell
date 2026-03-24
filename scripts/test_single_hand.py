#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代精确叫牌练习系统 - 单牌测试脚本

用法:
    python scripts/test_single_hand.py           # 随机发牌测试
    python scripts/test_single_hand.py --detail  # 详细规则匹配过程
    python scripts/test_single_hand.py --find    # 寻找可开叫的牌
"""

import os
import sys
import argparse

# 添加项目路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))

from practice.redeal import Deal
from practice.xml_parsing.xml_parser import XmlReaderForFile

# 默认规则文件路径
DEFAULT_RULES = os.path.join(PROJECT_ROOT, "rules", "modern_precision.xml")

# 规则条件说明
RULE_CONDITIONS = {
    "1c": "16+ HCP 强牌约定叫",
    "1d": "11-15 HCP, 2张以上方块, 无5张高花",
    "1h": "11-15 HCP, 5张以上红心",
    "1s": "11-15 HCP, 5张以上黑桃",
    "1n": "13-15 HCP 均型牌",
    "2c": "11-15 HCP, 6张以上梅花",
    "2d": "特殊约定叫",
    "2h": "弱二红心, 5-10 HCP, 6张红心",
    "2s": "弱二黑桃, 5-10 HCP, 6张黑桃",
    "2n": "22-24 HCP 均型牌",
}


def format_hand(hand) -> dict:
    """格式化手牌信息"""
    spades = sorted([str(c) for c in hand.spades], reverse=True)
    hearts = sorted([str(c) for c in hand.hearts], reverse=True)
    diamonds = sorted([str(c) for c in hand.diamonds], reverse=True)
    clubs = sorted([str(c) for c in hand.clubs], reverse=True)

    hcp = hand.hcp
    shape = hand.shape

    # 计算控制点
    controls = 0
    for suit in [hand.spades, hand.hearts, hand.diamonds, hand.clubs]:
        for c in suit:
            card_str = str(c).upper()
            if card_str.startswith("A"):
                controls += 2
            elif card_str.startswith("K"):
                controls += 1

    return {
        "spades": " ".join(spades) if spades else "-",
        "hearts": " ".join(hearts) if hearts else "-",
        "diamonds": " ".join(diamonds) if diamonds else "-",
        "clubs": " ".join(clubs) if clubs else "-",
        "hcp": hcp,
        "controls": controls,
        "shape": shape,
        "shape_str": f"{shape[0]}-{shape[1]}-{shape[2]}-{shape[3]}",
    }


def print_hand(hand_info: dict):
    """打印手牌信息"""
    print()
    print("你的持牌：")
    print("-" * 40)
    print(f"  ♠: {hand_info['spades']}")
    print(f"  ♥: {hand_info['hearts']}")
    print(f"  ♦: {hand_info['diamonds']}")
    print(f"  ♣: {hand_info['clubs']}")
    print()
    print("点力分析：")
    print(f"  高牌点(HCP): {hand_info['hcp']}")
    print(f"  控制点: {hand_info['controls']}")
    print(f"  牌型: {hand_info['shape_str']}")
    print(f"  黑桃: {hand_info['shape'][0]}张, 红心: {hand_info['shape'][1]}张")
    print(f"  方块: {hand_info['shape'][2]}张, 梅花: {hand_info['shape'][3]}张")
    print()


def analyze_unmatched_reason(
    bid_value: str, condition: str, hcp: int, shape: tuple
) -> list:
    """分析规则不匹配的原因"""
    reasons = []

    if "16+" in condition and hcp < 16:
        reasons.append(f"HCP={hcp} < 16")
    if "11-15" in condition and (hcp < 11 or hcp > 15):
        reasons.append(f"HCP={hcp} 不在 11-15 范围")
    if "13-15" in condition and (hcp < 13 or hcp > 15):
        reasons.append(f"HCP={hcp} 不在 13-15 范围")
    if "5-10" in condition and (hcp < 5 or hcp > 10):
        reasons.append(f"HCP={hcp} 不在 5-10 范围")
    if "22-24" in condition and (hcp < 22 or hcp > 24):
        reasons.append(f"HCP={hcp} 不在 22-24 范围")
    if "5+红心" in condition and shape[1] < 5:
        reasons.append(f"红心={shape[1]}张 < 5张")
    if "5+黑桃" in condition and shape[0] < 5:
        reasons.append(f"黑桃={shape[0]}张 < 5张")
    if "6+红心" in condition and shape[1] < 6:
        reasons.append(f"红心={shape[1]}张 < 6张")
    if "6+黑桃" in condition and shape[0] < 6:
        reasons.append(f"黑桃={shape[0]}张 < 6张")
    if "6+梅花" in condition and shape[3] < 6:
        reasons.append(f"梅花={shape[3]}张 < 6张")
    if "均型" in condition:
        if max(shape) > 5 or min(shape) < 2:
            reasons.append(f"牌型{shape[0]}-{shape[1]}-{shape[2]}-{shape[3]}不是均型")
    if "无5张高花" in condition:
        if shape[0] >= 5:
            reasons.append(f"黑桃={shape[0]}张 >= 5张")
        if shape[1] >= 5:
            reasons.append(f"红心={shape[1]}张 >= 5张")

    return reasons


def find_valid_bid(bids: dict, hand) -> tuple:
    """找到第一个匹配的叫品"""
    for bid_value, bid_obj in bids.items():
        if bid_obj.accept(hand):
            return (bid_value, bid_obj.description)
    return None


def run_test(rules_file: str, find_openable: bool = False, detail: bool = False):
    """运行单牌测试"""

    print("=" * 60)
    print("现代精确叫牌练习系统 - 单牌测试")
    print("=" * 60)
    print()

    # 1. 加载规则
    print(f"【步骤1】加载规则文件")
    print(f"  文件: {rules_file}")
    reader = XmlReaderForFile(rules_file)
    bids = reader.get_bids_from_xml()
    print(f"  已加载 {len(bids)} 个开叫规则")
    print()

    # 2. 发牌
    print("【步骤2】随机发牌")
    dealer = Deal.prepare({})

    if find_openable:
        # 寻找可开叫的牌
        for attempt in range(1, 100):
            deal = dealer()
            hand = deal.south
            if find_valid_bid(bids, hand):
                print(f"  第 {attempt} 次发牌找到可开叫的牌")
                break
        else:
            print("  100次发牌都未找到可开叫的牌，使用最后一次结果")
    else:
        deal = dealer()
        hand = deal.south
        print("  随机发牌完成")

    # 3. 显示手牌
    hand_info = format_hand(hand)
    print_hand(hand_info)

    # 4. 规则判断
    print("【步骤3】规则判断")
    print("-" * 60)

    if detail:
        # 详细模式：显示每个规则的判断过程
        print()
        valid_bid = None
        for bid_value, bid_obj in bids.items():
            result = bid_obj.accept(hand)
            condition = RULE_CONDITIONS.get(bid_value, "")

            print(f"\n规则: {bid_value.upper()}")
            print(f"  条件: {condition}")
            print(f"  结果: {'✅ 匹配' if result else '❌ 不匹配'}")

            if not result:
                reasons = analyze_unmatched_reason(
                    bid_value, condition, hand_info["hcp"], hand_info["shape"]
                )
                if reasons:
                    print(f"  原因: {', '.join(reasons)}")
            else:
                valid_bid = (bid_value, bid_obj.description)
                print(f"  ✓ 所有条件满足！")
        print()
    else:
        # 简洁模式：只显示结果
        print()
        print(f"检查 {len(bids)} 个开叫规则：")
        print()

        valid_bids = []
        for bid_value, bid_obj in bids.items():
            result = bid_obj.accept(hand)
            status = "✅" if result else "❌"
            print(
                f"  {status} {bid_value.upper():4s} - {RULE_CONDITIONS.get(bid_value, '')[:30]}"
            )
            if result:
                valid_bids.append((bid_value, bid_obj.description))
        print()

    # 5. 最终结论
    print("-" * 60)
    print("【最终结论】")
    print("-" * 60)

    valid_bid = find_valid_bid(bids, hand)

    if valid_bid:
        bid_value, desc = valid_bid
        print()
        print(f"  开叫: {bid_value.upper()}")
        print(f"  规则: {desc}")
        print()
        print("  匹配条件:")
        print(f"    - 高牌点: {hand_info['hcp']} HCP")
        shape = hand_info["shape"]
        if shape[0] >= 5:
            print(f"    - 黑桃: {shape[0]} 张")
        if shape[1] >= 5:
            print(f"    - 红心: {shape[1]} 张")
        if shape[2] >= 5:
            print(f"    - 方块: {shape[2]} 张")
        if shape[3] >= 5:
            print(f"    - 梅花: {shape[3]} 张")
    else:
        print()
        print("  开叫: PASS")
        print("  原因: 不符合任何开叫规则")
        print()
        print("  开叫最低要求:")
        print("    - 1♦/1♥/1♠: 需要 11-15 HCP")
        print("    - 1NT: 需要 13-15 HCP 均型")
        print("    - 1♣: 需要 16+ HCP")

    print()


def main():
    parser = argparse.ArgumentParser(description="单牌测试 - 展示规则匹配过程")
    parser.add_argument("-r", "--rules", default=DEFAULT_RULES, help="规则文件路径")
    parser.add_argument("-f", "--find", action="store_true", help="寻找可开叫的牌")
    parser.add_argument(
        "-d", "--detail", action="store_true", help="显示详细规则匹配过程"
    )

    args = parser.parse_args()

    run_test(rules_file=args.rules, find_openable=args.find, detail=args.detail)


if __name__ == "__main__":
    main()
