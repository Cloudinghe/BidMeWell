#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代精确叫牌练习系统

基于《现代精确叫牌法》的桥牌叫牌练习工具。

数据来源：
《现代精确叫牌法》（伯科维兹、曼雷著，杨静、于红英译）
人民体育出版社，2002年
ISBN：9787500926795
"""

__version__ = "0.1.0"
__author__ = "Precision Bidding Project"

# 点力计算模块
from .precision_formulas import (
    hcp,
    support_points,
    controls,
    playing_tricks,
    get_shape,
    is_balanced,
    is_unbalanced,
    analyze_hand,
)

__all__ = [
    "hcp",
    "support_points",
    "controls",
    "playing_tricks",
    "get_shape",
    "is_balanced",
    "is_unbalanced",
    "analyze_hand",
]
