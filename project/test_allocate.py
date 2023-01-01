from .models import (
    OrderLine, 
    Batch, 
)


def test_배치에_주문_라인을_할당하고_수량을_확인한다():
    batch = Batch("batch-001", "SMALL-TABLE", 20, eta=None)
    order = OrderLine(
        orderid="order-123",
        sku="SMALL-TABLE", 
        qty=2,
    )
    batch.allocate(order)
    
    assert batch.available_quantity == 18