# -*- coding: utf-8 -*-

import re
from practice.redeal.redeal import Shape


class BaseCondition:
    """ Base class for all condition classes. """

    @property
    def info(self):
        """ Get a description of the condition. """
        raise NotImplementedError("Abstract property.")

    @property
    def is_non_trivial_condition(self):
        return self.condition_count > 0

    @property
    def condition_count(self):
        """ Count the number of simple conditions associated. """
        raise NotImplementedError("Abstract property")

    def accept(self, hand):
        """ Determine if the hand satisfies the condition or not. """
        raise NotImplementedError("Abstract method.")

    def __str__(self):
        return f"{type(self)}: {self.info}"


class SimpleCondition(BaseCondition):
    def __init__(self, accept, info):
        self._accept = accept
        assert info
        self._info = info

    @property
    def info(self):
        """ Get a description of the condition. """
        return self._info

    @property
    def condition_count(self):
        return 1

    def accept(self, hand):
        """ Determine if the hand satisfies the condition or not. """
        return self._accept(hand)


class EvaluationCondition(BaseCondition):
    """ A condition on how good the hand is, by some method of evaluation. """

    def __init__(self, evaluation_method, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum
        self._evaluation_method = evaluation_method

    @property
    def condition_count(self):
        return 1

    @property
    def info(self):
        return (f"Evaluation method: {self._evaluation_method}. Min: "
                f"{self.minimum}. Max: {self.maximum}.")

    def accept(self, hand):
        """If the hand evaluates to within the specified range."""
        evaluation = self._evaluation_method(hand)
        return self.minimum <= evaluation <= self.maximum


class ShapeConditionFactory:
    """ Creates ShapeConditions. """

    _balanced = Shape("(4333)") + Shape("(4432)") + Shape("(5332)")
    _any = Shape("xxxx")
    _unbalanced = _any - _balanced
    general_types = {"balanced": _balanced, "any": _any,
                     "unbalanced": _unbalanced}
    # Use capture groups to ensure we keep this information.
    _binary_operator = re.compile("([-+])")

    @classmethod
    def create_general_shape_condition(cls, type_):
        """ Create a condition based on general shape types. """
        accept = cls.general_types[type_]
        info = f"Shape is {type_}."
        return SimpleCondition(accept, info)

    @classmethod
    def create_shape_condition(cls, shape_string):
        shape_string = "".join(shape_string.split()).lower()
        regex = re.compile(r"^([-+\dx]|[()])+$")
        assert regex.match(shape_string)
        shapes = cls._binary_operator.split(shape_string)
        converted_shapes = [shape if shape in {"+", "-"} else
                            f"Shape('{shape}')" for shape in shapes]
        overall_shape = eval("".join(converted_shapes))
        return SimpleCondition(overall_shape,
                               f"Shape: {' '.join(converted_shapes)}")

    @staticmethod
    def create_suit_length_condition(suit, minimum, maximum):
        def get_accept(suit):

            def accept(hand):
                return minimum <= len(getattr(hand, suit)) <= maximum

            return accept

        return SimpleCondition(get_accept(suit),
                               f"{minimum} <= {suit} <= {maximum}")


class MultiCondition(BaseCondition):
    def __init__(self, conditions=None):
        self.conditions = list(conditions or [])

    @property
    def condition_count(self):
        return sum((condition.condition_count
                    for condition in self.conditions))


class Condition(MultiCondition):
    """ A set of conditions on a hand. """

    def __init__(self, evaluation_conditions, shape_conditions):
        self.evaluation_conditions = list(evaluation_conditions)
        self.shape_conditions = list(shape_conditions)
        super().__init__(self.evaluation_conditions + self.shape_conditions)

    def _conditions(self):
        return self.evaluation_conditions + self.shape_conditions

    def accept(self, hand):
        """
        Returns boolean as to whether the hand satisfies the condition or not.
        """
        for condition in self.conditions:
            if not condition.accept(hand):
                return False

        return True

    @property
    def info(self):
        return (f"{self.evaluation_conditions}"
                f"\n{self.shape_conditions}")


class AndCondition(MultiCondition):
    """
    Collection of conditions which are all required to be true to accept a
    hand.
    """
    @property
    def info(self):
        infos = (condition.info for condition in self.conditions)
        return f"AND ({', '.join(infos)})"

    def accept(self, hand):
        """
        If all conditions are satisfied by the hand or not.
        """
        for condition in self.conditions:
            if not condition.accept(hand):
                return False

        return True


class NotCondition(BaseCondition):
    """ An inverted condition """
    def __init__(self, condition):
        assert condition
        self.condition = condition

    @property
    def condition_count(self):
        return self.condition.condition_count

    def accept(self, hand):
        """ The inverse of self.condition """
        return not self.condition.accept(hand)

    @property
    def info(self):
        return f"NOT ({self.condition.info})"


class OrCondition(MultiCondition):
    """
    Collection of conditions of which at least one is required to be true to
    accept a hand.
    """

    @property
    def info(self):
        infos = (condition.info for condition in self.conditions)
        return f"OR ({', '.join(infos)})"

    def accept(self, hand):
        for condition in self.conditions:
            if condition.accept(hand):
                return True

        return False


# ============================================================================
# 新增条件类 - 支持更精确的规则检查
# ============================================================================

class TopCardsCondition(BaseCondition):
    """检查花色顶部几张是否包含特定牌（如AKQ领头）"""

    def __init__(self, suit, positions, required_cards):
        """
        Args:
            suit: 花色名称 (spades/hearts/diamonds/clubs)
            positions: 检查前几张牌（如3表示检查前3张）
            required_cards: 必需包含的牌（如"AKQ"表示必须有A、K、Q）
        """
        self.suit = suit
        self.positions = positions
        self.required_cards = required_cards

    @property
    def condition_count(self):
        return 1

    @property
    def info(self):
        return f"{self.suit} top {self.positions} cards contain {self.required_cards}"

    def accept(self, hand):
        """检查指定花色的前positions张是否包含所有required_cards"""
        from practice.redeal.global_defs import Rank

        suit_holding = getattr(hand, self.suit)
        if len(suit_holding) < self.positions:
            return False

        # 获取牌并排序（从大到小）
        cards = list(suit_holding)
        cards.sort(reverse=True)  # Rank支持比较操作，从大到小排序
        top_cards = cards[:self.positions]
        top_ranks = {str(card) for card in top_cards}

        # 检查是否包含所有必需的牌
        for card_char in self.required_cards:
            if card_char not in top_ranks:
                return False

        return True


class SideSuitsCondition(BaseCondition):
    """检查边花是否包含/不包含特定牌"""

    def __init__(self, exclude_suit, not_contains=None, contains=None):
        """
        Args:
            exclude_suit: 排除的花色（通常是主套）
            not_contains: 边花不能包含的牌（如"A,K"）
            contains: 边花必须包含的牌
        """
        self.exclude_suit = exclude_suit
        self.not_contains = not_contains or ""
        self.contains = contains or ""

    @property
    def condition_count(self):
        return 1

    @property
    def info(self):
        cards_info = []
        if self.not_contains:
            cards_info.append(f"not contain {self.not_contains}")
        if self.contains:
            cards_info.append(f"contain {self.contains}")
        return f"Side suits (except {self.exclude_suit}): {', '.join(cards_info)}"

    def accept(self, hand):
        """检查边花是否满足条件"""
        suits = ['spades', 'hearts', 'diamonds', 'clubs']
        suits.remove(self.exclude_suit)

        for suit in suits:
            suit_holding = getattr(hand, suit)
            suit_ranks = {str(card) for card in suit_holding}

            # 检查不能包含的牌
            for card_char in self.not_contains.split(','):
                card_char = card_char.strip()
                if card_char and card_char in suit_ranks:
                    return False

            # 检查必须包含的牌
            for card_char in self.contains.split(','):
                card_char = card_char.strip()
                if card_char and card_char not in suit_ranks:
                    return False

        return True


class StopperCondition(BaseCondition):
    """检查某花色是否有止张（A/K/Q为首，或至少2张且有K/Q）"""

    def __init__(self, suit, has_stopper=True):
        """
        Args:
            suit: 花色名称
            has_stopper: True表示必须有止张，False表示必须无止张
        """
        self.suit = suit
        self.has_stopper = has_stopper

    @property
    def condition_count(self):
        return 1

    @property
    def info(self):
        return f"{self.suit} has {'stopper' if self.has_stopper else 'no stopper'}"

    def accept(self, hand):
        """检查是否有止张"""
        suit_holding = getattr(hand, self.suit)

        if len(suit_holding) == 0:
            has_stopper = False
        elif len(suit_holding) >= 2:
            # 2张以上，检查是否有K或Q
            top_two = list(suit_holding)[:2]
            top_ranks = {str(card.rank) for card in top_two}
            has_stopper = bool(top_ranks & {'A', 'K', 'Q'})
        else:
            # 单张，必须是A/K/Q才算有止张
            top_card = list(suit_holding)[0]
            has_stopper = str(top_card.rank) in {'A', 'K', 'Q'}

        return has_stopper == self.has_stopper


class DistributionCondition(BaseCondition):
    """检查牌型分布（单缺、双张等）"""

    def __init__(self, distribution_type, suit=None):
        """
        Args:
            distribution_type: 分布类型 (singleton/void/doubleton)
            suit: 指定花色，若为None则检查任意花色
        """
        self.distribution_type = distribution_type
        self.suit = suit

    @property
    def condition_count(self):
        return 1

    @property
    def info(self):
        suit_info = f" in {self.suit}" if self.suit else ""
        return f"Has {self.distribution_type}{suit_info}"

    def accept(self, hand):
        """检查是否有指定分布"""
        if self.suit:
            suit_holding = getattr(hand, self.suit)
            length = len(suit_holding)
        else:
            # 检查任意花色
            lengths = [len(getattr(hand, s)) for s in ['spades', 'hearts', 'diamonds', 'clubs']]

            if self.distribution_type == 'singleton':
                return 1 in lengths
            elif self.distribution_type == 'void':
                return 0 in lengths
            elif self.distribution_type == 'doubleton':
                return 2 in lengths
            return False

        if self.distribution_type == 'singleton':
            return length == 1
        elif self.distribution_type == 'void':
            return length == 0
        elif self.distribution_type == 'doubleton':
            return length == 2

        return False


class HonorsCondition(BaseCondition):
    """检查某花色是否有足够的大牌（好套检查）"""

    def __init__(self, suit, min_honors, total_in_top):
        """
        Args:
            suit: 花色名称
            min_honors: 前total_in_top张中至少要有多少张大牌
            total_in_top: 检查前几张牌（如5张中的前3张）
        """
        self.suit = suit
        self.min_honors = min_honors
        self.total_in_top = total_in_top

    @property
    def condition_count(self):
        return 1

    @property
    def info(self):
        return f"{self.suit} has {self.min_honors}+ honors in top {self.total_in_top}"

    def accept(self, hand):
        """检查指定花色是否有足够的大牌"""
        from practice.redeal.global_defs import Rank

        suit_holding = getattr(hand, self.suit)
        if len(suit_holding) < self.total_in_top:
            return False

        # 获取前N张牌
        top_cards = list(suit_holding)[:self.total_in_top]

        # 定义大牌
        honors = {Rank['A'], Rank['K'], Rank['Q'], Rank['J']}

        # 统计大牌数量
        honor_count = sum(1 for card in top_cards if card in honors)

        return honor_count >= self.min_honors
