import atexit
from flask import Flask, request, jsonify
import redis
import json
from datetime import datetime
from detect_anomalies import detect_brute_force, detect_cancel_abuse, detect_large_order, detect_sql_injection, detect_large_value_order, detect_unusual_purchase_time, is_in_blacklist

app = Flask(__name__)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def process_message(data):
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    action = data.get('event_type')  # view, purchase, or cancel
    price = data.get('price', 0)
    timestamp = data.get('event_time')

    # Kiểm tra xem user_id có nằm trong blackList hay không
    if is_in_blacklist(user_id):
        print(f"Blocked: User {user_id} is in blacklist")
        return

    # Lưu trữ vào Redis
    redis_key = f"user:{user_id}:actions"
    redis_client.lpush(redis_key, f"{timestamp}:{action}:{product_id}:{price}")

    # Lưu trữ vào file text
    action_data = {
        'user_id': user_id,
        'product_id': product_id,
        'action': action,
        'price': price,
        'timestamp': timestamp
    }
    
    # with open('user_actions.txt', 'a') as file:
    #     file.write(json.dumps(action_data) + '\n')

    # Kiểm tra và ngăn chặn các hành vi độc hại
    if detect_brute_force(user_id):
        print(f"Blocked: Brute-force attack detected for user {user_id}")
        return
    if action == 'purchase':
        if detect_cancel_abuse(user_id, product_id):
            print(f"Blocked: Cancel abuse detected for user {user_id} and product {product_id}")
            return
        if detect_large_order(user_id, product_id, max_quantity=10, time_window_minutes=60):
            print(f"Blocked: Large order quantity detected for user {user_id} and product {product_id}")
            return
        if detect_sql_injection(json.dumps(data)):
            print(f"Blocked: SQL injection detected in data {data}")
            return
        if detect_large_value_order(user_id, price, threshold=1000):
            print(f"Warning: Large value order detected for user {user_id} with price {price}")
        if detect_unusual_purchase_time(user_id, timestamp, start_hour=0, end_hour=6):
            print(f"Warning: Unusual purchase time detected for user {user_id} at {timestamp}")

    print(f"Processed: {data}")

@app.route('/track', methods=['POST'])
def track():
    data = request.json
    process_message(data)
    return jsonify({"status": "success"}), 200

def clear_redis_data():
    redis_client.flushdb()
    print("Redis data cleared")

# Đăng ký hàm clear_redis_data để gọi khi ứng dụng dừng lại
atexit.register(clear_redis_data)

if __name__ == '__main__':
    app.run(debug=True)