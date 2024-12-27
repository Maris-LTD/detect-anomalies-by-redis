# from kafka import KafkaConsumer
# import json

# def consume_messages(topic_name):
#     # Tạo Kafka consumer
#     consumer = KafkaConsumer(
#         topic_name,
#         bootstrap_servers='localhost:9092',  
#         value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # Deserialize dữ liệu JSON
#         auto_offset_reset='earliest',  # Bắt đầu từ thông điệp đầu tiên
#         enable_auto_commit=True
#     )

#     print(f"Listening to topic: {topic_name}")
#     for message in consumer:
#         print(f"Received: {message.value}")  # Hiển thị nội dung thông điệp

# if __name__ == "__main__":
#     topic_name = "ecommerce-topic"  # Tên Kafka topic
#     consume_messages(topic_name)




# from kafka import KafkaConsumer
# import json

# def consume_messages(topic_name):
#     # Tạo Kafka consumer
#     consumer = KafkaConsumer(
#         topic_name,
#         bootstrap_servers='localhost:9092',  # Địa chỉ Kafka broker
#         value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # Giải mã JSON từ dữ liệu nhị phân
#         auto_offset_reset='earliest',  # Bắt đầu đọc từ thông điệp đầu tiên
#         enable_auto_commit=True  # Tự động commit offset
#     )

#     print(f"Listening to topic: {topic_name}")
#     for message in consumer:
#         # Hiển thị nội dung của thông điệp nhận được
#         print(f"Received: {message.value}")

# if __name__ == "__main__":
#     topic_name = "ecommerce-topic"  # Tên Kafka topic cần lắng nghe
#     consume_messages(topic_name)




from kafka import KafkaConsumer
import json

def consume_messages(topic_name):
    # Tạo Kafka consumer
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers='localhost:9092',  # Địa chỉ Kafka broker
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # Giải mã JSON từ dữ liệu nhị phân
        auto_offset_reset='earliest',  # Bắt đầu đọc từ thông điệp đầu tiên
        enable_auto_commit=True  # Tự động commit offset
    )

    print(f"[Consumer] Listening to topic: {topic_name}")
    try:
        for message in consumer:
            # Kiểm tra thông điệp trước khi giải mã JSON
            if message.value:
                print(f"[Consumer] Received: {message.value}")
                print(f"    Partition: {message.partition}, Offset: {message.offset}")
            else:
                print("[Consumer] Received an empty message")
    except json.JSONDecodeError as e:
        print(f"[Consumer] Error decoding JSON: {e}")
    except Exception as e:
        print(f"[Consumer] Error while consuming messages: {e}")
    finally:
            consumer.close()

if __name__ == "__main__":
    topic_name = "ecommerce-topic"  # Tên Kafka topic cần lắng nghe
    consume_messages(topic_name)
