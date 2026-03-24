#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代精确叫牌练习系统 - 启动脚本

用法:
    python scripts/run_practice.py                    # 交互模式
    python scripts/run_practice.py --auto --boards 10 # 自动模式
    python scripts/run_practice.py --help             # 显示帮助

集成:
    - redeal: 发牌引擎
    - practice: 规则解析和叫牌判断
"""

import os
import sys
import argparse
import random

# 添加项目路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))

# 默认规则文件路径
DEFAULT_RULES = os.path.join(PROJECT_ROOT, "rules", "modern_precision.xml")


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="现代精确叫牌练习系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                          交互模式练习
  %(prog)s --auto --boards 10       自动模式练习10副牌
  %(prog)s -r custom.xml            使用自定义规则文件
  %(prog)s --seed 42                固定随机种子
        """,
    )

    parser.add_argument(
        "-r",
        "--rules",
        default=DEFAULT_RULES,
        help=f"规则文件路径 (默认: rules/modern_precision.xml)",
    )

    parser.add_argument(
        "-a", "--auto", action="store_true", help="自动模式（程序自动叫牌）"
    )

    parser.add_argument(
        "-b", "--boards", type=int, default=0, help="练习副数 (默认: 无限，0表示无限)"
    )

    parser.add_argument("-v", "--verbose", action="store_true", help="显示详细信息")

    parser.add_argument(
        "-s", "--seed", type=int, default=None, help="随机种子，用于复现牌局"
    )

    return parser.parse_args()


def print_banner():
    """打印欢迎信息"""
    print("=" * 60)
    print("        现代精确叫牌练习系统 v0.2.0")
    print("=" * 60)
    print()
    print("数据来源：《现代精确叫牌法》")
    print("点力系统：Milton Work (A=4, K=3, Q=2, J=1)")
    print("发牌引擎：redeal")
    print()
    print("-" * 60)


def format_hand(hand) -> dict:
    """格式化手牌信息"""
    # 获取各花色的牌
    spades = sorted([str(c) for c in hand.spades], reverse=True)
    hearts = sorted([str(c) for c in hand.hearts], reverse=True)
    diamonds = sorted([str(c) for c in hand.diamonds], reverse=True)
    clubs = sorted([str(c) for c in hand.clubs], reverse=True)

    # 计算点力
    hcp = hand.hcp
    shape = hand.shape
    shape_str = f"{shape[0]}-{shape[1]}-{shape[2]}-{shape[3]}"

    # 计算控制点 (A=2, K=1)
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
        "shape_str": shape_str,
        "hand_obj": hand,
    }


def print_hand(hand_info: dict):
    """打印手牌信息"""
    print()
    print("你的持牌：")
    print(f"  ♠: {hand_info['spades']}")
    print(f"  ♥: {hand_info['hearts']}")
    print(f"  ♦: {hand_info['diamonds']}")
    print(f"  ♣: {hand_info['clubs']}")
    print()
    print("点力分析：")
    print(f"  高牌点(HCP): {hand_info['hcp']}")
    print(f"  控制点: {hand_info['controls']}")
    print(f"  牌型: {hand_info['shape_str']}")

    # 判断是否均型
    shape = hand_info["shape"]
    if max(shape) <= 5 and min(shape) >= 2:
        if max(shape) == 5 and (shape[0] == 5 or shape[1] == 5):
            print(f"  牌型分类: 不均型（高花5张）")
        else:
            print(f"  牌型分类: 均型")
    else:
        print(f"  牌型分类: 不均型")
    print()


def get_valid_opening_bids(bids: dict, hand) -> list:
    """获取当前手牌可以开叫的叫品"""
    valid_bids = []
    for bid_value, bid_obj in bids.items():
        if bid_obj.accept(hand):
            valid_bids.append((bid_value, bid_obj.description))
    return valid_bids


def run_interactive_mode(rules_file: str, seed=None, verbose=False):
    """运行交互模式"""
    print_banner()

    # 检查规则文件
    if not os.path.exists(rules_file):
        print(f"错误：规则文件不存在: {rules_file}")
        print(f"请确保文件存在，或使用 -r 参数指定正确的路径")
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

        # 创建发牌器
        dealer = Deal.prepare({})
        print("发牌引擎就绪")

    except ImportError as e:
        print(f"错误：无法加载必要模块: {e}")
        print("请确保已安装所有依赖：pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"加载失败: {e}")
        sys.exit(1)

    print()
    print("提示：输入 'quit' 或 'exit' 退出程序")
    print("      输入 'help' 查看帮助")
    print("      输入 'hint' 查看推荐叫牌")
    print()

    # 主循环
    board_count = 0
    while True:
        board_count += 1
        print("-" * 60)
        print(f"第 {board_count} 副牌")
        print("-" * 60)

        # 发牌
        deal = dealer()
        hand = deal.south  # 玩家坐南家

        # 格式化手牌信息
        hand_info = format_hand(hand)
        print_hand(hand_info)

        # 获取可以开叫的叫品
        valid_bids = get_valid_opening_bids(bids, hand)

        if not valid_bids:
            print("此牌无法开叫，请选择 pass")
            valid_bids = [("pass", "无法开叫")]

        # 显示可用叫品
        print("请选择你的开叫:")
        for bid_value, desc in valid_bids:
            print(f"  {bid_value:4s} - {desc[:40]}")
        print()

        # 获取用户输入
        try:
            user_input = input("你的叫牌 > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        # 处理命令
        if user_input in ["quit", "exit", "q"]:
            print("再见！")
            break
        elif user_input == "help":
            print("\n可用命令:")
            print("  quit/exit - 退出程序")
            print("  help      - 显示帮助")
            print("  skip      - 跳到下一副牌")
            print("  hint      - 显示推荐叫牌")
            print("  info      - 查看当前牌详情")
            print()
            continue
        elif user_input == "skip":
            continue
        elif user_input == "info":
            print_hand(hand_info)
            continue
        elif user_input == "hint":
            if valid_bids:
                best_bid = valid_bids[0]
                print(f"\n推荐叫牌: {best_bid[0]} - {best_bid[1]}")
            print()
            continue

        # 验证叫牌
        valid_bid_values = [b[0] for b in valid_bids]

        if user_input in valid_bid_values:
            # 找到对应的叫牌描述
            for bid_value, desc in valid_bids:
                if bid_value == user_input:
                    print(f"\n✓ 正确！")
                    print(f"你的叫牌: {bid_value.upper()} - {desc}")
                    break
        elif user_input == "pass":
            if "pass" in valid_bid_values or not valid_bids:
                print(f"\n✓ 你选择 Pass")
            else:
                print(f"\n⚠ 你选择 Pass，但这手牌可以开叫")
                print(f"推荐叫牌: {valid_bids[0][0]} - {valid_bids[0][1]}")
        else:
            print(f"\n✗ 无效的叫牌: {user_input}")
            if valid_bids:
                print(f"可用的叫牌: {', '.join([b[0] for b in valid_bids])}")

        print()


def run_auto_mode(rules_file: str, boards: int, seed=None, verbose=False):
    """运行自动模式"""
    print_banner()
    print("自动模式")
    print(f"规则文件: {rules_file}")
    print(f"练习副数: {boards if boards > 0 else '无限'}")
    if seed:
        print(f"随机种子: {seed}")
    print()

    # 设置随机种子
    if seed is not None:
        random.seed(seed)

    # 加载规则和发牌引擎
    try:
        from practice.xml_parsing.xml_parser import XmlReaderForFile
        from practice.redeal import Deal

        reader = XmlReaderForFile(rules_file)
        bids = reader.get_bids_from_xml()
        dealer = Deal.prepare({})

    except ImportError as e:
        print(f"错误：无法加载必要模块: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"加载失败: {e}")
        sys.exit(1)

    print("-" * 60)

    max_boards = boards if boards > 0 else 10  # 默认演示10副
    stats = {"passed": 0, "opened": 0, "total": 0}

    for i in range(max_boards):
        # 发牌
        deal = dealer()
        hand = deal.south
        hand_info = format_hand(hand)

        print(f"\n第 {i + 1} 副牌")
        print(
            f"  持牌: ♠{hand_info['spades']} ♥{hand_info['hearts']} "
            f"♦{hand_info['diamonds']} ♣{hand_info['clubs']}"
        )
        print(f"  点力: {hand_info['hcp']} HCP, 牌型: {hand_info['shape_str']}")

        # 获取可以开叫的叫品
        valid_bids = get_valid_opening_bids(bids, hand)

        if valid_bids:
            stats["opened"] += 1
            bid_value, desc = valid_bids[0]
            print(f"  开叫: {bid_value.upper()} - {desc[:30]}")
        else:
            stats["passed"] += 1
            print(f"  开叫: Pass (无法开叫)")

        stats["total"] += 1

    print()
    print("-" * 60)
    print("统计:")
    print(f"  总副数: {stats['total']}")
    print(f"  开叫: {stats['opened']} ({stats['opened'] / stats['total'] * 100:.0f}%)")
    print(f"  Pass: {stats['passed']} ({stats['passed'] / stats['total'] * 100:.0f}%)")


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
            rules_file=args.rules, seed=args.seed, verbose=args.verbose
        )


if __name__ == "__main__":
    main()
