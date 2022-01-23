# pylint: disable=protected-access
import model
import repository


def test_repository_can_save_a_batch(session):
    batch = model.Batch("batch1", "RUSTY-SOAPDISH", 100, eta=None)

    repo = repository.SqlAlchemyRepository(session)
    repo.add(batch)
    session.commit()

    rows = session.execute(
        'SELECT reference, sku, _purchased_quantity, eta FROM "batches"'
    )
    assert list(rows) == [("batch1", "RUSTY-SOAPDISH", 100, None)]


def insert_order_line(session):
    session.execute(
        "INSERT INTO order_lines (orderid, sku, qty)"
        ' VALUES ("order1", "GENERIC-SOFA", 12)'
    )
    [[orderline_id]] = session.execute(
        "SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku",
        dict(orderid="order1", sku="GENERIC-SOFA"),
    )
    return orderline_id


def insert_batch(session, batch_id):
    session.execute(
        "INSERT INTO batches (reference, sku, _purchased_quantity, eta)"
        ' VALUES (:batch_id, "GENERIC-SOFA", 100, null)',
        dict(batch_id=batch_id),
    )
    [[batch_id]] = session.execute(
        'SELECT id FROM batches WHERE reference=:batch_id AND sku="GENERIC-SOFA"',
        dict(batch_id=batch_id),
    )
    return batch_id


def insert_allocation(session, orderline_id, batch_id):
    session.execute(
        "INSERT INTO allocations (orderline_id, batch_id)"
        " VALUES (:orderline_id, :batch_id)",
        dict(orderline_id=orderline_id, batch_id=batch_id),
    )


def test_repository_can_retrieve_a_batch_with_allocations(session):
    # 1. orderline DB에 INSERT 후 id 가져오기
    orderline_id = insert_order_line(session)

    # 2. batch1 DB에 INSERT 후 id 가져오기 (batch2는 INSERT만)
    batch1_id = insert_batch(session, "batch1")
    insert_batch(session, "batch2")

    # 3. batch1에 orderline 할당하기
    insert_allocation(session, orderline_id, batch1_id)

    # 4. 스키마와 Domain Model이 매핑된 session을 Repository에 적용
    repo = repository.SqlAlchemyRepository(session)
    # 5. batch1라는 reference를 가지고 있는 데이터를 도메인 모델의 객체로 가져오기
    retrieved = repo.get("batch1")

    # 6. batch1라는 refernece를 가진 도메인 모델인 Batch의 객체를 expected에 할당
    expected = model.Batch("batch1", "GENERIC-SOFA", 100, eta=None)

    # 7. 5번(Repository Pattern), 6번(도메인 모델에 바로 객체선언)으로 가져온 도메인 모델이 동일한지 체크
    assert retrieved == expected  # Batch.__eq__ ocomparesnly  reference
    assert retrieved.sku == expected.sku
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {
        model.OrderLine("order1", "GENERIC-SOFA", 12),
    }
