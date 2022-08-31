import json
import pytest
from app import app
client = app.test_client()

def testRegister():
    response = client.post(
        "/api/register", json={
            "email": "vinaysingh8866@gmail.com",
            "upassword": "123456789",
            "uname": "vinaysingh"})
    assert response.status_code == 200
    print("Testing Passed")


def testLogin():
    response = client.post(
        "/api/login", json={
            "email": "vinaysingh8866@gmail.com",
            "upassword": "123456789"})
    assert response.status_code == 200
    print("Testing Passed")

def testAddAsset():
    login = client.post(
        "/api/login", json={
            "email": "vinaysingh8866@gmail.com",
            "upassword": "123456789"})
    token = login.json['token']
    response = client.post(
        "/api/add_stock", headers={"Authorization": "Bearer " + token}, json={
            "name": "amatic",
            "balance": "0.012"})
    assert response.status_code == 200
    print("Testing Passed")

testRegister()
testLogin()
testAddAsset()