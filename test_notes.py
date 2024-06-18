import pytest
from flask import Flask, session, request
from flask.testing import FlaskClient
from main import app, User, Note
from models import Base, engine

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            Base.metadata.create_all(engine)
        yield client
        with app.app_context():
            Base.metadata.drop_all(engine)

def test_registration(client):
    rv = client.post('/register', data=dict(
        email='test@example.com',
        password='TestPassword1'
    ), follow_redirects=True)
    assert rv.status_code == 200

def test_login(client):
    client.post('/register', data=dict(
        email='test@example.com',
        password='TestPassword1'
    ))

    rv = client.post('/login', data=dict(
        email='test@example.com',
        password='TestPassword1'
    ), follow_redirects=True)
    assert rv.status_code == 200 

def test_add_note(client):
    client.post('/register', data=dict(
        email='test@example.com',
        password='TestPassword1'
    ))

    client.post('/login', data=dict(
        email='test@example.com',
        password='TestPassword1'
    ))

    rv = client.post('/add_note', data=dict(
        title='Test Note',
        text='This is a test note.'
    ), follow_redirects=True)
    assert rv.status_code == 200

