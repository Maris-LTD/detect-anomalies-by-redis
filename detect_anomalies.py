import redis
from datetime import datetime, timedelta

# Kết nối tới Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Phát hiện các cuộc tấn công Brute-force
def detect_brute_force(user_id, max_attempts=5):
    key = f"user:{user_id}:logins"
    failed_attempts = redis_client.lrange(key, 0, -1)
    failed_attempts = [attempt.decode('utf-8') for attempt in failed_attempts if 'false' in attempt]

    recent_failures = [attempt for attempt in failed_attempts if datetime.fromisoformat(attempt.split(':')[0]) > datetime.now() - timedelta(hours=1)]
    
    if len(recent_failures) > max_attempts:
        return True
    return False

# Ngăn chặn hành vi hủy đơn hàng quá 3 lần
def detect_cancel_abuse(user_id, product_id, max_cancellations=3):
    key = f"user:{user_id}:actions"
    actions = redis_client.lrange(key, 0, -1)
    cancellations = [action.decode('utf-8') for action in actions if 'cancel' in action.decode('utf-8') and product_id in action.decode('utf-8')]
    
    if len(cancellations) > max_cancellations:
        return True
    return False

# Ngăn chặn hành vi mua một đơn hàng với số lượng quá lớn
def detect_large_order(user_id, quantity, max_quantity=50):
    if quantity > max_quantity:
        return True
    return False

# Ngăn chặn các request chứa các từ khóa SQL
def detect_sql_injection(request):
    sql_keywords = ['SELECT', 'INSERT', 'DELETE', 'UPDATE', 'DROP']
    for keyword in sql_keywords:
        if keyword in request.upper():
            return True
    return False

# Ngăn chặn các hành vi đặt hàng không bình thường
def detect_anomalous_order(user_id, product_id, quantity, factor=3, default_avg_quantity=5):
    key = f"user:{user_id}:actions"
    actions = redis_client.lrange(key, 0, -1)
    purchases = [action.decode('utf-8') for action in actions if 'purchase' in action.decode('utf-8') and product_id in action.decode('utf-8')]
    
    quantities = []
    for action in purchases:
        try:
            quantities.append(int(action.split(':')[3]))
        except (IndexError, ValueError) as e:
            print(f"Skipping invalid action data: {action} - Error: {e}")
            
    avg_quantity = sum(quantities) / len(quantities) if quantities else default_avg_quantity
    
    if quantity > avg_quantity * factor:  # Giả sử nếu số lượng đặt hàng lớn hơn gấp {factor} lần số lượng trung bình
        return True
    return False