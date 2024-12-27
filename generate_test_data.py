import redis
from faker import Faker
import random
from datetime import datetime, timedelta
import json

# Kết nối tới Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Tạo đối tượng faker
faker = Faker()

def generate_user_actions(user_id, num_actions=100):
    actions = []
    for _ in range(num_actions):
        timestamp = faker.date_time_between(start_date='-1y', end_date='now').isoformat()
        action = random.choice(['view', 'purchase', 'cancel'])
        product_id = faker.uuid4()
        quantity = random.randint(1, 10)

        # Lưu trữ vào Redis
        redis_key = f"user:{user_id}:actions"
        redis_client.lpush(redis_key, f"{timestamp}:{action}:{product_id}:{quantity}")

        # Lưu trữ vào danh sách
        actions.append({
            'user_id': user_id,
            'product_id': product_id,
            'action': action,
            'quantity': quantity,
            'timestamp': timestamp
        })

    # Lưu danh sách vào file text
    with open('user_actions.txt', 'a') as file:
        for action in actions:
            file.write(json.dumps(action) + '\n')

def generate_login_data(user_id, num_logins=50):
    logins = []
    for _ in range(num_logins):
        login_time = faker.date_time_between(start_date='-1y', end_date='now').isoformat()
        success = random.choice([True, False])
        logins.append({
            'user_id': user_id,
            'login_time': login_time,
            'success': success
        })

    # Lưu danh sách vào file text
    with open('user_logins.txt', 'a') as file:
        for login in logins:
            file.write(json.dumps(login) + '\n')

# Tạo dữ liệu cho một số người dùng
def create_test_data(num_users=10):
    for _ in range(num_users):
        user_id = str(faker.uuid4())
        generate_user_actions(user_id)
        generate_login_data(user_id)

create_test_data()