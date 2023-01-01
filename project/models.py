from dataclasses import dataclass
from datetime import date

from typing import List, Optional

@dataclass
class OrderLine(object):
    """ 주문 라인은 제품(SKU)과 수량을 가진다.
    """
    orderid: str
    sku: str
    qty: int
    

class Batch(object):
    def __init__(
        self, ref: str, sku: str, qty: int, eta: Optional[date]
    ) -> None:
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self.available_quantity = qty
    
    def allocate(self, line: OrderLine) -> None:
        """ 할당함수
        
        Batch에 주문 라인을 할당한다.
        ex.
        20단위의 SMALL-TAGLE로 이루어진 배치
        2단위의 SMALL-TABLE를 요구하는 주문 라인

        """
        self.available_quantity -= line.qty

    def can_allocate(self, line: OrderLine) -> bool:
        """ 할당 가능 여부
        
        Batch에 주문 라인을 할당할 수 있는지 여부를 반환한다.
        """
        return self.sku == line.sku and self.available_quantity >= line.qty