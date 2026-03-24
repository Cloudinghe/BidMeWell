#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代精确叫牌练习系统 - 应叫练习脚本

练习同伴开叫后的应叫能力。

用法:
    python scripts/run_practice2.py              # 交互模式
    python scripts/run_practice2.py --auto       # 自动模式
    python scripts/run_practice2.py --seed 42    # 固定随机种子
"""

import os
import sys
import argparse
import random
from random import choice

# 添加项目路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))

# 默认规则文件路径
DEFAULT_RULES = os.path.join(PROJECT_ROOT, "rules", "modern_precision.xml")


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="应叫练习系统 - 练习同伴开叫后的应叫",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-r", "--rules", default=DEFAULT_RULES, help="规则文件路径"
    )
    parser.add_argument("-a", "--auto", action="store_true", help="自动模式")
    parser.add_argument("-b", "--boards", type=int, default=0, help="练习副数")
    parser.add_argument("-s", "--seed", type=int, default=None, help="随机种子")
    parser.add_argument("-v", "--verbose", action="store_true", help="详细信息")
    return parser.parse_args()


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
        "hand_obj": hand,
    }


def print_hand(hand_info: dict, title: str = "持牌"):
    """打印手牌信息"""
    print(f"{title}：")
    print(f"  ♠: {hand_info['spades']}")
    print(f"  ♥: {hand_info['hearts']}")
    print(f"  ♦: {hand_info['diamonds']}")
    print(f"  ♣: {hand_info['clubs']}")
    print()
    print("点力分析：")
    print(f"  高牌点(HCP): {hand_info['hcp']}")
    print(f"  控制点: {hand_info['controls']}")
    print(f"  牌型: {hand_info['shape_str']}")

    # 牌型分类
    shape = hand_info["shape"]
    if max(shape) <= 5 and min(shape) >= 2:
        if max(shape) == 5 and (shape[0] == 5 or shape[1] == 5):
            print(f"  牌型分类: 不均型（高花5张）")
        else:
            print(f"  牌型分类: 均型")
    else:
        print(f"  牌型分类: 不均型")
    print()


def get_valid_bids(bids_dict, hand, parent_bid_obj=None):
    """获取当前手牌可以使用的叫品

    Returns:
        list of tuples: [(bid_value, description, bid_obj), ...]
    """
    if parent_bid_obj is None:
        # 开叫
        potential_bids = bids_dict
    else:
        # 应叫
        potential_bids = parent_bid_obj.children if hasattr(parent_bid_obj, 'children') else {}

    valid_bids = []
    for bid_value, bid_obj in potential_bids.items():
        try:
            if bid_obj.accept(hand):
                valid_bids.append((bid_value, bid_obj.description, bid_obj))
        except:
            pass
    return valid_bids


def simulate_partner_bid(bids, north_hand):
    """模拟同伴（北家）的开叫

    Returns:
        tuple: (bid_value, description, bid_obj) or None
    """
    valid_bids = get_valid_bids(bids, north_hand)
    if valid_bids:
        return choice(valid_bids)
    return None


def simulate_opponent_bid(bids, east_hand, partner_bid_obj):
    """模拟对手（东家）的应叫

    Returns:
        tuple: (bid_value, description) or None
    """
    if partner_bid_obj is None:
        return None

    # 获取同伴开叫后的应叫规则
    valid_bids = get_valid_bids(bids, east_hand, partner_bid_obj)

    # 东家有一定概率应叫
    if valid_bids and random.random() > 0.7:  # 30%概率应叫
        chosen = choice(valid_bids)
        return (chosen[0], chosen[1])

    # 大部分情况Pass
    return ("pass", "Pass")


def print_banner():
    """打印欢迎信息"""
    print("=" * 60)
    print("        现代精确叫牌练习系统 - 应叫练习")
    print("=" * 60)
    print()
    print("练习内容：同伴开叫后，你的应叫")
    print("数据来源：《现代精确叫牌法》")
    print("点力系统：Milton Work (A=4, K=3, Q=2, J=1)")
    print()


def run_interactive_mode(rules_file: str, seed=None, verbose=False):
    """运行交互模式"""
    print_banner()

    # 检查规则文件
    if not os.path.exists(rules_file):
        print(f"错误：规则文件不存在: {rules_file}")
        sys.exit(1)

    print(f"规则文件: {rules_file}")
    print()

    # 设置随机种子
    if seed is not None:
        random.seed(seed)

    # 加载规则和发牌引擎
    try:
        from practice.xml_parsing.xml_parser import XmlReaderForFile
        from practice.redeal import Deal

        print("正在加载规则...")
        reader = XmlReaderForFile(rules_file)
        bids = reader.get_bids_from_xml()
        print(f"规则加载成功！共 {len(bids)} 个开叫定义")

        dealer = Deal.prepare({})
        print("发牌引擎就绪")

    except ImportError as e:
        print(f"错误：无法加载必要模块: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"加载失败: {e}")
        sys.exit(1)

    print()
    print("提示：输入 'quit' 或 'exit' 退出程序")
    print("      输入 'partner' 查看同伴持牌")
    print("      输入 'hint' 查看推荐应叫")
    print()

    # 主循环
    board_count = 0
    while True:
        board_count += 1
        print("-" * 60)
        print(f"第 {board_count} 副牌")
        print("-" * 60)

        # 发四方牌
        deal = dealer()
        north_hand = deal.north  # 同伴
        east_hand = deal.east    # 对手
        south_hand = deal.south  # 用户
        west_hand = deal.west   # 对手

        # 格式化手牌
        north_info = format_hand(north_hand)
        south_info = format_hand(south_hand)

        # 模拟同伴开叫
        partner_bid = simulate_partner_bid(bids, north_hand)

        if partner_bid is None:
            # 同伴无法开叫，重新发牌
            print("同伴无法开叫，重新发牌...")
            continue

        # 模拟对手应叫
        opponent_bid = simulate_opponent_bid(bids, east_hand, partner_bid)

        # 显示叫牌进程
        print()
        print("叫牌进程：")
        north_bid_str = partner_bid[0].upper() if partner_bid[0] != 'pass' else 'Pass'
        east_bid_str = opponent_bid[0].upper() if opponent_bid and opponent_bid[0] != 'pass' else 'Pass'
        print(f"  北家(同伴): {north_bid_str} - {partner_bid[1]}")
        print(f"  东家(对手): {east_bid_str}")
        print()

        # 显示用户手牌
        print("你的持牌（南家）：")
        print_hand(south_info)

        # 获取用户可用的应叫选项
        # 根据叫牌进程，用户是第3家（北家开叫，东家应叫，南家表态）
        user_valid_bids = []

        if opponent_bid and opponent_bid[0] != 'pass':
            # 对手应叫了，获取相应的应叫规则
            # 这里简化为获取所有可能的应叫
            for bid_value, bid_obj in bids.items():
                try:
                    if bid_obj.accept(south_hand):
                        user_valid_bids.append((bid_value, bid_obj.description, bid_obj))
                except:
                    pass
        else:
            # 对手Pass，获取同伴开叫后的应叫规则
            # partner_bid is (bid_value, description, bid_obj)
            partner_bid_obj = partner_bid[2] if partner_bid else None
            if partner_bid_obj and hasattr(partner_bid_obj, 'children'):
                for bid_value, bid_obj in partner_bid_obj.children.items():
                    try:
                        if bid_obj.accept(south_hand):
                            user_valid_bids.append((bid_value, bid_obj.description, bid_obj))
                    except:
                        pass

        if not user_valid_bids:
            user_valid_bids = [("pass", "无法应叫", None)]

        # 显示可用叫品
        print("请选择你的应叫:")
        for bid_value, desc, _ in user_valid_bids:
            print(f"  {bid_value:4s} - {desc[:40]}")
        print()

        # 获取用户输入
        try:
            user_input = input("你的应叫 > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        # 处理命令
        if user_input in ["quit", "exit", "q"]:
            print("再见！")
            break
        elif user_input == "partner":
            print()
            print("同伴（北家）持牌：")
            print_hand(north_info)
            continue
        elif user_input == "hint":
            if user_valid_bids:
                best_bid = user_valid_bids[0]
                print(f"\n推荐应叫: {best_bid[0]} - {best_bid[1]}")
            print()
            continue
        elif user_input == "help":
            print("\n可用命令:")
            print("  quit/exit - 退出程序")
            print("  partner   - 查看同伴持牌")
            print("  hint      - 显示推荐应叫")
            print("  skip      - 跳到下一副牌")
            print()
            continue
        elif user_input == "skip":
            continue

        # 验证叫牌
        valid_bid_values = [b[0] for b in user_valid_bids]

        if user_input in valid_bid_values:
            for bid_value, desc, _ in user_valid_bids:
                if bid_value == user_input:
                    print(f"\n✓ 正确！")
                    print(f"你的应叫: {bid_value.upper()} - {desc}")
                    break
        elif user_input == "pass":
            if "pass" in valid_bid_values or not user_valid_bids:
                print(f"\n✓ 你选择 Pass")
            else:
                print(f"\n⚠ 你选择 Pass，但这手牌可以应叫")
                if user_valid_bids:
                    print(f"推荐应叫: {user_valid_bids[0][0]} - {user_valid_bids[0][1]}")
        else:
            print(f"\n✗ 无效的叫牌: {user_input}")
            if user_valid_bids:
                print(f"可用的叫牌: {', '.join([b[0] for b in user_valid_bids])}")

        print()


def run_auto_mode(rules_file: str, boards: int, seed=None, verbose=False):
    """运行自动模式"""
    print_banner()
    print("自动模式")
    print(f"规则文件: {rules_file}")
    print(f"练习副数: {boards if boards > 0 else '无限'}")

    if seed is not None:
        random.seed(seed)

    try:
        from practice.xml_parsing.xml_parser import XmlReaderForFile
        from practice.redeal import Deal

        reader = XmlReaderForFile(rules_file)
        bids = reader.get_bids_from_xml()
        dealer = Deal.prepare({})

    except Exception as e:
        print(f"加载失败: {e}")
        sys.exit(1)

    print("-" * 60)

    max_boards = boards if boards > 0 else 10
    stats = {"correct": 0, "total": 0}

    for i in range(max_boards):
        deal = dealer()
        north_hand = deal.north
        south_hand = deal.south

        partner_bid = simulate_partner_bid(bids, north_hand)
        if partner_bid is None:
            continue

        south_info = format_hand(south_hand)

        # 获取应叫选项 - partner_bid is (bid_value, description, bid_obj)
        partner_bid_obj = partner_bid[2] if partner_bid else None
        user_valid_bids = []
        if partner_bid_obj and hasattr(partner_bid_obj, 'children'):
            for bid_value, bid_obj in partner_bid_obj.children.items():
                try:
                    if bid_obj.accept(south_hand):
                        user_valid_bids.append((bid_value, bid_obj.description))
                except:
                    pass

        if not user_valid_bids:
            user_valid_bids = [("pass", "无法应叫")]

        # 随机选择应叫
        correct_bid = choice(user_valid_bids)

        print(f"\n第 {i + 1} 副牌")
        print(f"  同伴: {partner_bid[0].upper()} - {partner_bid[1]}")
        print(f"  你的牌: {south_info['hcp']} HCP, {south_info['shape_str']}")
        print(f"  应叫: {correct_bid[0].upper()} - {correct_bid[1][:30]}")

        stats["total"] += 1

    print()
    print("-" * 60)
    print(f"自动完成 {stats['total']} 副牌")


def main():
    """主函数"""
    args = parse_args()

    if args.auto:
        run_auto_mode(
            rules_file=args.rules,
            boards=args.boards,
            seed=args.seed,
            verbose=args.verbose,
        )
    else:
        run_interactive_mode(
            rules_file=args.rules,
            seed=args.seed,
            verbose=args.verbose,
        )


if __name__ == "__main__":
    main()
