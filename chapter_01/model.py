from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional, List


class OutOfStock(Exception):
    pass


def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {line.sku}")


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref  # 주문 참조 번호(Order Reference)
        self.sku = sku  # 제품 (Stock Keeping Unit)
        self.eta = eta  # 현재 배송중이면 시간정보, 창고 재고면 None
        self._purchased_quantity = qty  # 구매 수량
        self._allocations = set()  # 주문 라인(Order Line)  type: Set[OrderLine]

    def __repr__(self):
        return f"<Batch {self.reference}>"

    def __eq__(self, other):
        """
        EQ : equal를 체크하는 함수
        """
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other):
        """
        1. 이 엔티티의 eta가 없을 경우 -> False
        2. 비교할 대상의 엔티티의 eta가 없을 경우 -> True (내)
        """
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def allocated_orderline(self) -> Optional[set[OrderLine]]:
        return self._allocations

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty
