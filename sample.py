import requests
import json

data = [
    {"student_id": 2, "date": "2025-09-29", "status": "PRESENT"},
    {"student_id": 4, "date": "2025-09-28", "status": "ABSENT"},
    {"student_id": 5, "date": "2025-09-30", "status": "PRESENT"},
    {"student_id": 6, "date": "2025-09-30", "status": "ABSENT"},
    
]

url = "http://127.0.0.1:8000/students/mark-attendance/"

try:
    response = requests.post(url, json=data)
    print("Status Code:", response.status_code)
    try:
        print("Response JSON:", response.json())
    except json.JSONDecodeError:
        print("Response Text:", response.text)
except requests.exceptions.RequestException as e:
    print("Request failed:", e)
