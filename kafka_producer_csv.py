from kafka import KafkaProducer
import csv
import json

def produce_messages(topic_name, csv_file):
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize data to JSON
    )

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)  # Read CSV file as dictionary
        for row in reader:
            producer.send(topic_name, value=row)
            # producer.send(topic_name, value=json.dumps({"key": "value"}).encode('utf-8'))
            print(f"Sent: {row}")

    producer.flush()
    producer.close()

if __name__ == "__main__":
    topic_name = 'ecommerce-topic'
    csv_file = 'user_actions.csv'
    produce_messages(topic_name, csv_file)





# from kafka import KafkaProducer
# import csv
# import json

# def produce_messages(topic_name, csv_file):
#     # Tạo KafkaProducer với value_serializer để serialize dữ liệu sang JSON
#     producer = KafkaProducer(
#         bootstrap_servers='localhost:9092',
#         value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize data to JSON
#     )

#     # Mở file CSV và đọc dữ liệu
#     with open(csv_file, 'r', encoding='utf-8') as file:
#         reader = csv.DictReader(file)  # Đọc CSV theo dạng dictionary
#         for row in reader:
#             try:
#                 # Gửi từng dòng dữ liệu tới Kafka topic
#                 producer.send(topic_name, value=row)  # Gửi trực tiếp dictionary
#                 print(f"Sent: {row}")  # Log dữ liệu đã gửi
#             except Exception as e:
#                 print(f"Failed to send message: {row}, error: {e}")

#     # Đảm bảo dữ liệu đã được gửi hết
#     producer.flush()
#     producer.close()

# if __name__ == "__main__":
#     topic_name = 'ecommerce-topic'
#     csv_file = 'D:\\Workspace\\Project\\Big_Data\\data\\eCommerce behavior data.csv'
#     produce_messages(topic_name, csv_file)





# from kafka import KafkaProducer
# import csv
# import json

# def produce_messages(topic_name, csv_file):
#     # Tạo KafkaProducer với value_serializer để serialize dữ liệu sang JSON
#     producer = KafkaProducer(
#         bootstrap_servers='localhost:9092',
#         value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize data sang JSON
#     )

#     # Mở file CSV và đọc dữ liệu
#     try:
#         with open(csv_file, 'r', encoding='utf-8') as file:
#             reader = csv.DictReader(file)  # Đọc file CSV dạng dictionary
#             for row in reader:
#                 if row:  # Kiểm tra dữ liệu không rỗng
#                     try:
#                         # Gửi từng dòng dữ liệu tới Kafka topic
#                         producer.send(topic_name, value=row)
#                         print(f"[Producer] Sent: {row}")
#                     except Exception as e:
#                         print(f"[Producer] Failed to send message: {row}, error: {e}")
#                 else:
#                     print("[Producer] Skipped empty row")
#     except FileNotFoundError:
#         print(f"[Producer] File not found: {csv_file}")
#     except Exception as e:
#         print(f"[Producer] Error reading file: {e}")

#     # Đảm bảo dữ liệu đã được gửi hết
#     producer.flush()
#     producer.close()

# if __name__ == "__main__":
#     topic_name = 'ecommerce-topic'
#     csv_file = 'D:\\Workspace\\Project\\Big_Data\\data\\eCommerce behavior data.csv'
#     produce_messages(topic_name, csv_file)
