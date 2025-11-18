import pytest

from app import app


def test_index_page_returns_200_and_contains_title():
    client = app.test_client()
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Anonymous Chat' in resp.data
