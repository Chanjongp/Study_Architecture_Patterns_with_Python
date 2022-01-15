import pytest
from dataclasses import dataclass
from typing import NamedTuple
from collections import namedtuple


# 50p 예제
@dataclass(frozen=True)
class Name:
    first_name: str
    surname: str


class CurrencyMatchError(Exception):
    pass


class ValueMatchError(Exception):
    pass


class Money(NamedTuple):
    currency: str
    value: int

    def __add__(self, other):
        if not self.currency == other.currency:
            raise CurrencyMatchError

        return Money(self.currency, self.value + other.value)

    def __sub__(self, other):
        if not self.currency == other.currency:
            raise CurrencyMatchError

        return Money(self.currency, self.value - other.value)

    def __mul__(self, other):
        if type(other) == int:
            return Money(self.currency, self.value * other)

        if not self.currency == other.currency:
            raise CurrencyMatchError

        if not self.value == other.value:
            raise ValueMatchError

        return Money(self.currency, self.value * other.value)

    def __truediv__(self, other):
        if not self.currency == other.currency:
            raise CurrencyMatchError

        return Money(self.currency, self.value / other.value)


Line = namedtuple("Line", ["sku", "qty"])

fiver = Money("gbp", 5)
tenner = Money("gbp", 10)


def can_add_money_values_for_the_same_currency():
    assert fiver + fiver == tenner


def can_subtract_money_values():
    assert tenner - fiver == fiver


def adding_different_currencies_fails():
    with pytest.raises(CurrencyMatchError):
        Money("usd", 10) + Money("gbp", 10)


def can_multiply_money_by_a_number():
    assert fiver * 5 == Money("gbp", 25)


def multiplying_two_money_values_is_an_error():
    with pytest.raises(ValueMatchError):
        tenner * fiver
