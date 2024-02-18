with open("test.txt", "w+", encoding="utf-8") as file:
    file.write("Hello World!")

from datetime import datetime
now = datetime.now()
current_time = now.strftime("%Y-%m-%d %H:%M:%S")

print("="*60)
print(f"Current time: {current_time}")
print("test complete.")
print("="*60)