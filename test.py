import requests

BASE= "http://127.0.0.1:5000/"

data = [
        {"likes": 78, "name":"Joe", "views":100000},
        {"likes": 100000, "name":"How to make Rest API", "views":800000},
        {"likes": 24, "name":"Tim", "views":20000}]


for i in range(len(data)):
    response=requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())

response= requests.delete(BASE + "video/0")
input()

response= requests.get(BASE + "video/2")
print(response.json())