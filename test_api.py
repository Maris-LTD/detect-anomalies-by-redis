import requests
import json
import time
import random

# Đường dẫn đến API
url = "http://127.0.0.1:5000/track"

# Đọc dữ liệu từ file text
def read_data_from_file(filename):
    with open(filename, 'r') as file:
        return [json.loads(line) for line in file]

# Gửi yêu cầu POST đến API
def send_post_request(data):
    response = requests.post(url, json=data)
    
    # Kiểm tra mã trạng thái HTTP của phản hồi
    if response.status_code != 200:
        print(f"HTTP Status Code: {response.status_code}")
        print(f"Response Content: {response.content}")

    try:
        return response.json()
    except json.JSONDecodeError:
        print("Error decoding JSON response")
        print(f"Response Content: {response.content}")
        return None

# Kiểm tra dữ liệu test
def test_data():
    # Đọc dữ liệu hành động người dùng
    user_actions = read_data_from_file('user_actions.txt')

    # Gửi từng hành động đến API và in phản hồi
    for action in user_actions:
        response = send_post_request(action)
        print(f"Request: {action}")
        print(f"Response: {response}")
        print()
        
        # Thêm khoảng thời gian chờ ngẫu nhiên giữa các yêu cầu (giả sử từ 0.5 đến 2 giây)
        time.sleep(random.uniform(0.5, 2.0))

if __name__ == "__main__":
    test_data()