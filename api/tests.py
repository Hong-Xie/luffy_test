from django.test import TestCase

# Create your tests here.


# import requests
#
#
#
# requests.post("http://127.0.0.1:8000/shopping_car/?token=7a4452a0-3020-4dd6-9999-0880584e276c",
#               data={
#                   "course_id":1,
#                   "price_policy_id":5,
#               }
#
#               )


# class A(object):
#
#     def __init__(self):
#        self.name="a"
#        self.age="100"
#
#     @property
#     def dict(self):
#
#         return self.__dict__
#
# a=A()
# print(a.dict)
#
# d={"name":"alex"}
#
#
# if "name" in d:
#     print("OK")



################################### 测试redis###################################



import redis

r=redis.Redis(host="127.0.0.1",port=6379)
#
# print(r.get("123"))
#
#
# print(r.hgetall("ShoppingCarKey_1_1"))


# r.hmset("k11",{"k22":{"k33":"v3"}})

# 查询k33 对应的值

# print(r.hgetall("k11"))  # 字典
#
# print(r.hget("k11","k22"))
#
# print(r.hget("k11","k22").decode("utf8"))
#
# import json
#
# s=json.dumps(r.hget("k11","k22").decode("utf8"))
#
# json.loads(s)


##############################
import json

# r.hmset("k11",{"k22":json.dumps({"k33":"v3"})})
#
# print(r.hget("k11","k22"))
#
# print(json.loads(r.hget("k11","k22")))

# print(r.hgetall("ShoppingCarKey_1_1"))

# r.delete("ShoppingCarKey_1_1")

# 短路现象

# print(1 and 2)
# print(1 or 2)
# print(0 or 2)
# print(0 and 2)









import hashlib



md5=hashlib.md5()
md5.update(b"alex is dsb ,egon too")

print(md5.hexdigest()) # 704b5b272aa3652d4605ddad5bdb9698












