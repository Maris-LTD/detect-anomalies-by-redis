import atexit
from flask import Flask, request, jsonify
import redis
import json
from datetime import datetime
from detect_anomalies import detect_brute_force, detect_cancel_abuse, detect_large_order, detect_sql_injection, detect_anomalous_order

app = Flask(__name__)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def clear_redis_data():
    redis_client.flushdb()
    print("Redis data cleared")

# Đăng ký hàm clear_redis_data để gọi khi ứng dụng dừng lại
atexit.register(clear_redis_data)

@app.route('/track', methods=['POST'])
def track():
    data = request.json
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    action = data.get('action')  # view, purchase, or cancel
    quantity = data.get('quantity', 1)  # default quantity is 1
    timestamp = datetime.now().isoformat()

    # Lưu trữ vào Redis
    redis_key = f"user:{user_id}:actions"
    redis_client.lpush(redis_key, f"{timestamp}:{action}:{product_id}:{quantity}")

    # Lưu trữ vào file text
    action_data = {
        'user_id': user_id,
        'product_id': product_id,
        'action': action,
        'quantity': quantity,
        'timestamp': timestamp
    }
    
    # with open('user_actions.txt', 'a') as file:
    #     file.write(json.dumps(action_data) + '\n')

    # Kiểm tra và ngăn chặn các hành vi độc hại
    if detect_brute_force(user_id):
        return jsonify({"status": "blocked", "reason": "Brute-force attack detected"}), 403
    if action != 'view':
        if detect_cancel_abuse(user_id, product_id):
            return jsonify({"status": "blocked", "reason": "Cancel abuse detected"}), 403
        if detect_large_order(user_id, quantity):
            return jsonify({"status": "blocked", "reason": "Large order quantity detected"}), 403
        if detect_sql_injection(request.data.decode('utf-8')):
            return jsonify({"status": "blocked", "reason": "SQL injection detected"}), 403
        if detect_anomalous_order(user_id, product_id, quantity):
            return jsonify({"status": "blocked", "reason": "Anomalous order detected"}), 403

    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)