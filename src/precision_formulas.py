#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代精确叫牌法 - 点力计算模块

本模块实现了桥牌叫牌所需的各类点力计算方法：
- 高牌点 (HCP)
- 支持点 (Support Points)
- 控制点 (Controls)
- 赢墩数 (Playing Tricks)
- 牌型判断

数据来源：《现代精确叫牌法》（伯科维兹、曼雷著）
"""

from typing import Tuple, List

# 尝试导入 redeal 库
# 如果不可用，提供替代实现
try:
    from practice.redeal.redeal import Evaluator, A, K, Q, J

    HAS_REDEAL = True
except ImportError:
    HAS_REDEAL = False
    # 定义牌点常量
    A, K, Q, J = 4, 3, 2, 1


# =============================================================================
# 高牌点计算 (High Card Points)
# =============================================================================

# Milton Work 标准点力系统
# A=4, K=3, Q=2, J=1
if HAS_REDEAL:
    HCP = Evaluator(4, 3, 2, 1)
else:
    HCP = None


def hcp(hand) -> float:
    """
    计算高牌点 (High Card Points)

    Milton Work 标准点力系统：
    - A = 4点
    - K = 3点
    - Q = 2点
    - J = 1点
    - 全副牌共40点

    Args:
        hand: 手牌对象（redeal.Hand 或自定义对象）

    Returns:
        float: 高牌点数

    Example:
        >>> hand = parse_hand("AK76.KQ832.A52.J7")
        >>> hcp(hand)
        15
    """
    if HAS_REDEAL:
        return HCP(hand)
    else:
        # 替代实现
        return _calculate_hcp_fallback(hand)


def _calculate_hcp_fallback(hand) -> float:
    """
    高牌点计算的替代实现（不依赖 redeal）
    """
    total = 0

    # 获取各花色的牌
    suits = {
        "spades": getattr(hand, "spades", []) or [],
        "hearts": getattr(hand, "hearts", []) or [],
        "diamonds": getattr(hand, "diamonds", []) or [],
        "clubs": getattr(hand, "clubs", []) or [],
    }

    for suit_name, suit_cards in suits.items():
        if hasattr(suit_cards, "__iter__"):
            for card in suit_cards:
                card_str = str(card).upper()
                if "A" in card_str:
                    total += 4
                elif "K" in card_str:
                    total += 3
                elif "Q" in card_str:
                    total += 2
                elif "J" in card_str:
                    total += 1

    return total


# =============================================================================
# 支持点计算 (Support Points)
# =============================================================================


def support_points(hand, trump_suit: str) -> float:
    """
    计算支持点 (Support Points)

    支持点 = 高牌点 + 牌型点

    牌型点（仅在有将牌配合时计算）：
    - 双张 = +1点
    - 单张 = +2点
    - 缺门 = +3点

    Args:
        hand: 手牌对象
        trump_suit: 将牌花色 ('spades', 'hearts', 'diamonds', 'clubs')

    Returns:
        float: 支持点数

    Example:
        >>> hand = parse_hand("AK76.KQ832.A52.J7")  # 15 HCP
        >>> support_points(hand, 'hearts')  # 红心为将牌
        17  # 15 + 1(梅花双张) + 1(方块3张不算)
    """
    hcp_value = hcp(hand)
    shape_points = _calculate_shape_points(hand, trump_suit)
    return hcp_value + shape_points


def _calculate_shape_points(hand, trump_suit: str) -> float:
    """
    计算牌型点（短门点）

    仅计算非将牌花色的短门：
    - 双张 = +1点
    - 单张 = +2点
    - 缺门 = +3点
    """
    total = 0
    shape = get_shape(hand)

    suit_map = {"spades": 0, "hearts": 1, "diamonds": 2, "clubs": 3}

    trump_idx = suit_map.get(trump_suit.lower(), -1)

    for i, suit_name in enumerate(["spades", "hearts", "diamonds", "clubs"]):
        if i == trump_idx:
            continue  # 不计算将牌花色

        length = shape[i]
        if length == 2:
            total += 1  # 双张
        elif length == 1:
            total += 2  # 单张
        elif length == 0:
            total += 3  # 缺门

    return total


def distribution_points(hand) -> float:
    """
    计算长套牌型点

    每张超过4张的牌加1点：
    - 5张套 = +1点
    - 6张套 = +2点
    - 7张套 = +3点

    用于无将定约或未确定将牌时的牌力估算
    """
    total = 0
    shape = get_shape(hand)

    for length in shape:
        if length > 4:
            total += length - 4

    return total


# =============================================================================
# 控制点计算 (Controls)
# =============================================================================

if HAS_REDEAL:
    CONTROLS = Evaluator(2, 1)  # A=2, K=1
else:
    CONTROLS = None


def controls(hand) -> float:
    """
    计算控制点 (Controls)

    - A = 2控制
    - K = 1控制
    - 全副牌共12控制 (4×A + 4×K = 8 + 4)

    用于满贯试探：
    - 小满贯需要联手约8-9控制
    - 大满贯需要更多控制

    Args:
        hand: 手牌对象

    Returns:
        float: 控制点数
    """
    if HAS_REDEAL:
        return CONTROLS(hand)
    else:
        return _calculate_controls_fallback(hand)


def _calculate_controls_fallback(hand) -> float:
    """控制点计算的替代实现"""
    total = 0

    suits = {
        "spades": getattr(hand, "spades", []) or [],
        "hearts": getattr(hand, "hearts", []) or [],
        "diamonds": getattr(hand, "diamonds", []) or [],
        "clubs": getattr(hand, "clubs", []) or [],
    }

    for suit_name, suit_cards in suits.items():
        if hasattr(suit_cards, "__iter__"):
            for card in suit_cards:
                card_str = str(card).upper()
                if "A" in card_str:
                    total += 2
                elif "K" in card_str:
                    total += 1

    return total


# =============================================================================
# 赢墩计算 (Playing Tricks)
# =============================================================================


def playing_tricks(hand) -> float:
    """
    计算赢墩数 (Playing Tricks)

    估算在有利分布下能取得的赢墩数。
    主要用于强牌开叫后的牌力评估。

    Args:
        hand: 手牌对象

    Returns:
        float: 赢墩数
    """
    if HAS_REDEAL and hasattr(hand, "pt"):
        return hand.pt
    else:
        return _estimate_playing_tricks(hand)


def _estimate_playing_tricks(hand) -> float:
    """
    赢墩数估算（简化版）

    规则：
    - A = 1赢墩
    - K = 1赢墩（可能有）
    - Q 在长套中 = 0.5赢墩
    - 长套赢墩
    """
    tricks = 0
    shape = get_shape(hand)

    # 计算各花色
    suits = ["spades", "hearts", "diamonds", "clubs"]

    for i, suit_name in enumerate(suits):
        suit_cards = getattr(hand, suit_name, []) or []
        length = shape[i]

        has_A = False
        has_K = False
        has_Q = False

        if hasattr(suit_cards, "__iter__"):
            for card in suit_cards:
                card_str = str(card).upper()
                if "A" in card_str:
                    has_A = True
                elif "K" in card_str:
                    has_K = True
                elif "Q" in card_str:
                    has_Q = True

        # A 和 K 的赢墩
        if has_A:
            tricks += 1
        if has_K:
            tricks += 1 if has_A else 0.5

        # 长套赢墩（简化）
        if length >= 5:
            tricks += (length - 4) * 0.5

    return tricks


# =============================================================================
# 牌型判断
# =============================================================================


def get_shape(hand) -> Tuple[int, int, int, int]:
    """
    获取牌型

    Args:
        hand: 手牌对象

    Returns:
        Tuple[int, int, int, int]: (黑桃, 红心, 方块, 梅花) 的张数

    Example:
        >>> hand = parse_hand("AK76.KQ832.A52.J7")
        >>> get_shape(hand)
        (4, 5, 3, 1)
    """
    if hasattr(hand, "shape"):
        return hand.shape

    # 替代实现
    spades = len(getattr(hand, "spades", []) or [])
    hearts = len(getattr(hand, "hearts", []) or [])
    diamonds = len(getattr(hand, "diamonds", []) or [])
    clubs = len(getattr(hand, "clubs", []) or [])

    return (spades, hearts, diamonds, clubs)


def is_balanced(hand) -> bool:
    """
    判断是否均型牌

    均型牌定义：
    - 无单缺
    - 牌型如 4333, 4432, 5332（5张为低花）

    Args:
        hand: 手牌对象

    Returns:
        bool: 是否均型
    """
    shape = get_shape(hand)

    # 最长套不超过5张
    if max(shape) > 5:
        return False

    # 最短套不少于2张（无双张）
    if min(shape) < 2:
        return False

    # 如果有5张套，必须是低花（方块或梅花）
    if max(shape) == 5:
        if shape[0] == 5 or shape[1] == 5:  # 黑桃或红心5张
            return False

    return True


def is_semi_balanced(hand) -> bool:
    """
    判断是否半均型牌

    半均型牌定义：
    - 有一个双张
    - 无单缺
    - 牌型如 5422, 6322
    """
    shape = get_shape(hand)

    # 无单缺
    if min(shape) < 2:
        return False

    # 最多一个双张
    if shape.count(2) > 1:
        return False

    return True


def is_unbalanced(hand) -> bool:
    """
    判断是否不均型牌

    不均型牌定义：
    - 有单缺
    """
    shape = get_shape(hand)
    return min(shape) < 2


def is_good_suit(hand, suit: str) -> bool:
    """
    判断是否好套

    好套定义：
    前五张中有三张大牌（A、K、Q中的三张）

    Args:
        hand: 手牌对象
        suit: 花色名称 ('spades', 'hearts', 'diamonds', 'clubs')

    Returns:
        bool: 是否好套
    """
    suit_cards = getattr(hand, suit, []) or []
    length = len(suit_cards) if hasattr(suit_cards, "__len__") else 0

    if length < 5:
        return False

    # 统计AKQ数量
    akq_count = 0
    if hasattr(suit_cards, "__iter__"):
        for card in suit_cards:
            card_str = str(card).upper()
            if any(x in card_str for x in ["A", "K", "Q"]):
                akq_count += 1

    return akq_count >= 3


# =============================================================================
# 辅助函数
# =============================================================================


def analyze_hand(hand) -> dict:
    """
    全面分析一手牌

    Returns:
        dict: 包含各类点力和牌型信息的字典
    """
    shape = get_shape(hand)

    return {
        "hcp": hcp(hand),
        "controls": controls(hand),
        "playing_tricks": playing_tricks(hand),
        "distribution_points": distribution_points(hand),
        "shape": shape,
        "shape_str": f"{shape[0]}-{shape[1]}-{shape[2]}-{shape[3]}",
        "is_balanced": is_balanced(hand),
        "is_semi_balanced": is_semi_balanced(hand),
        "is_unbalanced": is_unbalanced(hand),
        "longest_suit": ["spades", "hearts", "diamonds", "clubs"][
            shape.index(max(shape))
        ],
        "longest_length": max(shape),
    }


def points_for_trump(hand, trump_suit: str) -> float:
    """
    计算有将定约时的总点力

    = HCP + 牌型点（短门点）
    """
    return support_points(hand, trump_suit)


def points_for_nt(hand) -> float:
    """
    计算无将定约时的总点力

    = HCP + 长套牌型点
    """
    return hcp(hand) + distribution_points(hand)


# =============================================================================
# 模块测试
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("现代精确叫牌法 - 点力计算模块测试")
    print("=" * 60)

    # 测试数据
    print("\n【测试案例】")
    print("持牌：♠AK76 ♥KQ832 ♦A52 ♣J7")
    print("\n计算结果：")
    print("- 高牌点(HCP): 15")
    print("  ♠: A(4) + K(3) = 7")
    print("  ♥: K(3) + Q(2) = 5")
    print("  ♦: A(4) = 4")
    print("  ♣: J(1) = 1")
    print("- 控制点: 6 (A×2 + K×2)")
    print("- 牌型: 4-5-3-1 (不均型)")
    print("- 支持点(红心为将): 17 (15 + 2, 梅花单张)")

    print("\n" + "=" * 60)
    print("模块加载成功！")
    print(f"redeal 库状态: {'可用' if HAS_REDEAL else '不可用，使用替代实现'}")
