import os
import tempfile
import pytest
from app import app, db, init_db_with_sample, Scooter

@pytest.fixture
def client(tmp_path):
    db_file = tmp_path / "test.db"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_file}"
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.init_app(app)
            db.create_all()
            init_db_with_sample(app)
        yield client

def test_view_available(client):
    rv = client.get('/api/view_all_available')
    assert rv.status_code == 200
    data = rv.get_json()
    assert isinstance(data, list)

def test_reserve_and_end(client):
    # reserve s1
    rv = client.post('/api/reservation/start', json={'id':'s1'})
    assert rv.status_code == 200
    # ending reservation
    rv = client.post('/api/reservation/end', json={'id':'s1','lat':37.0,'lng':-122.0})
    assert rv.status_code == 200
