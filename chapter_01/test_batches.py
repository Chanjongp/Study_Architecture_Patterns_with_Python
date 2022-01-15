from datetime import date
from model import Batch, OrderLine

# 주문 가능한 수량을 줄이는 배치를 할당하는 테스트
def test_allocating_to_a_batch_reduces_the_available_quantity():
    """
    ### Batch 선언
    SMALL-TABLE의 수량을 20개까지 주문이 가능한 주문 관리 클래스

    1. batch 번호
    2. SMALL-TABLE 이라는 SKU 수량 20개 (주문 가능한 수량)
    3. ETA (배송 중이면 할당)


    ### Orderline 선언
    실제 고객이 수량에 맞게 주문한 정보

    1. 주문참조번호 ID 선언
    2. SKU(SMALL-TABLE) 선언
    3. 수량 2개 선언

    ## batch에 Orderline 할당 (allocate)
    1. batch에 2개를 구매하는 주문정보 할당

    ## 주문라인의 갯수(2개)만큼 줄었는지 테스트
    """
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
    line = OrderLine("order-ref", "SMALL-TABLE", 2)

    batch.allocate(line)

    assert batch.available_quantity == 18


# 테스트를 위한 Batch와 OrderLine을 만드는 함수
def make_batch_and_line(sku, batch_qty, line_qty):
    return (
        Batch("batch-001", sku, batch_qty, eta=date.today()),
        OrderLine("order-123", sku, line_qty),
    )


# 필요한 수량보다 더 많은 수량을 가지고 있을 때 할당 가능한지 체크하는 테스트
def test_can_allocate_if_available_greater_than_required():
    large_batch, small_line = make_batch_and_line("ELEGANT-LAMP", 20, 2)
    assert large_batch.can_allocate(small_line)


# 필요한 수량보다 더 적은 수량을 가지고 있을 때 할당 가능한지 체크하는 테스트
def test_cannot_allocate_if_available_smaller_than_required():
    small_batch, large_line = make_batch_and_line("ELEGANT-LAMP", 2, 20)
    assert small_batch.can_allocate(large_line) is False


# 필요한 수량과 같은 수량을 가지고 있을 때 할당 가능한지 체크하는 테스트
def test_can_allocate_if_available_equal_to_required():
    batch, line = make_batch_and_line("ELEGANT-LAMP", 2, 2)
    assert batch.can_allocate(line)


# SKU 이름이 맞지 않을 경우 할당 가능한지 체크하는 테스트
def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch("batch-001", "UNCOMFORTABLE-CHAIR", 100, eta=None)
    different_sku_line = OrderLine("order-123", "EXPENSIVE-TOASTER", 10)
    assert batch.can_allocate(different_sku_line) is False


# 두번을 할당해도 잘 동작하는지 체크하는 테스트
def test_allocation_is_idempotent():
    batch, line = make_batch_and_line("ANGULAR-DESK", 20, 2)
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity == 18


def test_deallocate():
    batch, line = make_batch_and_line("EXPENSIVE-FOOTSTOOL", 20, 2)
    batch.allocate(line)
    batch.deallocate(line)
    assert batch.available_quantity == 20


# 할당된 OrerLine만 deallocate(할당 해제) 할수 있는지 체크하는 테스트
def test_can_only_deallocate_allocated_lines():
    batch, unallocated_line = make_batch_and_line("DECORATIVE-TRINKET", 20, 2)
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 20
