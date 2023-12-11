import datetime
a = datetime.datetime.now()
b = a + datetime.timedelta(0, 0.5)  # days, seconds, then other fields.
print(a.time())
print(b.time())


print(b > a)
