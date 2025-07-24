"""
Test file để kiểm tra các chức năng của Tích Tích App
"""
import requests
from decimal import Decimal
import json

BASE_URL = "http://localhost:8000"

def test_create_customer():
    """Test tạo khách hàng mới"""
    print("🧪 Testing: Create Customer")
    customer_data = {"phone": "0123456789"}
    response = requests.post(f"{BASE_URL}/customers/", json=customer_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

def test_create_child(parent_id):
    """Test tạo con cái"""
    print("\n🧪 Testing: Create Child")
    child_data = {"parent_id": parent_id, "name": "Nguyễn Văn An"}
    response = requests.post(f"{BASE_URL}/children/", json=child_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

def test_get_wallet(child_id):
    """Test lấy thông tin ví"""
    print(f"\n🧪 Testing: Get Wallet for child {child_id}")
    response = requests.get(f"{BASE_URL}/wallets/{child_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

def test_add_money(child_id, amount, wallet_type):
    """Test thêm tiền vào ví"""
    print(f"\n🧪 Testing: Add {amount} to {wallet_type} wallet")
    response = requests.post(f"{BASE_URL}/wallets/{child_id}/add-money", 
                           params={"amount": amount, "wallet_type": wallet_type})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

def test_spend_money(child_id, amount):
    """Test chi tiêu"""
    print(f"\n🧪 Testing: Spend {amount}")
    response = requests.post(f"{BASE_URL}/wallets/{child_id}/spend", 
                           params={"amount": amount})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

def test_get_customer_with_children(user_id):
    """Test lấy thông tin khách hàng với con cái"""
    print(f"\n🧪 Testing: Get Customer {user_id} with children")
    response = requests.get(f"{BASE_URL}/customers/{user_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, default=str)}")
    return response.json()

def run_full_test():
    """Chạy test đầy đủ"""
    print("🚀 Starting Tích Tích App Tests")
    print("="*50)
    
    try:
        # 1. Tạo khách hàng
        customer = test_create_customer()
        user_id = customer["user_id"]
        
        # 2. Tạo con cái
        child = test_create_child(user_id)
        child_id = child["child_id"]
        
        # 3. Kiểm tra ví (sẽ được tự động tạo bởi trigger)
        wallet = test_get_wallet(child_id)
        
        # 4. Thêm tiền vào các ví
        test_add_money(child_id, 100000, "savings")
        test_add_money(child_id, 20000, "charity") 
        test_add_money(child_id, 50000, "spending")
        
        # 5. Chi tiêu
        test_spend_money(child_id, 15000)
        
        # 6. Kiểm tra lại ví
        test_get_wallet(child_id)
        
        # 7. Lấy thông tin đầy đủ khách hàng
        test_get_customer_with_children(user_id)
        
        print("\n✅ All tests completed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")

if __name__ == "__main__":
    run_full_test()
