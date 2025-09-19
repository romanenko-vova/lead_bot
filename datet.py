from datetime import datetime, timedelta

now = datetime.now()
print(now)

future = now + timedelta(seconds=30)

delta = timedelta(seconds=30)
print(now + delta)

print(now - future)