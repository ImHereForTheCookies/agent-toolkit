import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client(tmp_path):
    return TestClient(create_app(tmp_path / "test.db"))


def make_item(client, name="rice", quantity=2, unit="kg"):
    resp = client.post("/items", json={"name": name, "quantity": quantity, "unit": unit})
    assert resp.status_code == 201, resp.text
    return resp.json()


def test_health_returns_ok(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_create_item_returns_it_with_an_id(client):
    item = make_item(client)
    assert item["id"] == 1
    assert (item["name"], item["quantity"], item["unit"]) == ("rice", 2, "kg")
    assert item["updated_at"]


def test_list_items_returns_created_items_in_order(client):
    make_item(client, "rice")
    make_item(client, "eggs", 12, "pcs")
    assert [i["name"] for i in client.get("/items").json()] == ["rice", "eggs"]


def test_list_items_is_empty_on_fresh_db(client):
    assert client.get("/items").json() == []


def test_get_item_by_id(client):
    item = make_item(client)
    assert client.get(f"/items/{item['id']}").json() == item


def test_get_missing_item_returns_404(client):
    assert client.get("/items/999").status_code == 404


def test_create_rejects_empty_name(client):
    resp = client.post("/items", json={"name": "   ", "quantity": 1})
    assert resp.status_code == 422


def test_create_rejects_negative_quantity(client):
    resp = client.post("/items", json={"name": "rice", "quantity": -1})
    assert resp.status_code == 422


def test_patch_updates_quantity(client):
    item = make_item(client, quantity=2)
    resp = client.patch(f"/items/{item['id']}", json={"quantity": 5})
    assert resp.status_code == 200
    assert resp.json()["quantity"] == 5
    assert client.get(f"/items/{item['id']}").json()["quantity"] == 5


def test_patch_updates_name_and_leaves_other_fields(client):
    item = make_item(client, "rice", 2, "kg")
    body = client.patch(f"/items/{item['id']}", json={"name": "basmati"}).json()
    assert (body["name"], body["quantity"], body["unit"]) == ("basmati", 2, "kg")


def test_patch_rejects_empty_name(client):
    item = make_item(client)
    assert client.patch(f"/items/{item['id']}", json={"name": ""}).status_code == 422


def test_quantity_cannot_go_negative(client):
    item = make_item(client, quantity=2)
    resp = client.patch(f"/items/{item['id']}", json={"quantity": -1})
    assert resp.status_code == 422
    assert client.get(f"/items/{item['id']}").json()["quantity"] == 2


def test_patch_missing_item_returns_404(client):
    assert client.patch("/items/999", json={"quantity": 1}).status_code == 404


def test_delete_item_removes_it(client):
    item = make_item(client)
    assert client.delete(f"/items/{item['id']}").status_code == 204
    assert client.get(f"/items/{item['id']}").status_code == 404


def test_delete_missing_item_returns_404(client):
    assert client.delete("/items/999").status_code == 404
