

from rest_framework.views import APIView
from django.shortcuts import HttpResponse

from api.utils.auth_class import LoginAuth
from api.models import *

from django.core.exceptions import ObjectDoesNotExist

from api.utils.response import BaseResponse
import json

from rest_framework.response import Response
from django.http import JsonResponse

from api.utils.exceptions import PriceException

from django_redis import get_redis_connection

class ShoppingCarView(APIView):

    authentication_classes = [LoginAuth,]
    response=BaseResponse()
    conn=get_redis_connection("default")

    def post(self,request):
        """
        购物车的添加课程请求
        :param request:
        :return:
        """
        print(request.user,request.auth)

        print("request.data",request.data) # {'course_id': 1, 'price_policy_id': 1}
        # 获取数据

        course_id=request.data.get("course_id")
        price_policy_id=request.data.get("price_policy_id")

        # 校验数据是否合法


        try:
            # (1) 校验课程是否存在
            course_obj=Course.objects.get(pk=course_id)

            # 查找课程关联的所有的价格策略

            price_policy_list=course_obj.price_policy.all()

            price_policy_dict={}
            for price_policy_item in price_policy_list:
                price_policy_dict[price_policy_item.pk]={
                          "price":price_policy_item.price,
                          "valid_period":price_policy_item.valid_period,
                          "valid_period_text":price_policy_item.get_valid_period_display()
                }

            print(price_policy_dict)

            '''
            price_policy_dict= {
                           1:{
                              "price":100,
                              "valid_period":7,
                              "valid_period_text":"一周"
                              }，

                            2 :{
                              "price":200,
                              "valid_period":14,
                              "valid_period_text":"两周"
                              }

                        }



            '''

            if price_policy_id not in price_policy_dict:
                raise PriceException()


            # shopping_car的key
            from django.conf import settings
            shopping_car_key=settings.LUFFY_SHOPPING_CAR

            user_id=request.user.pk
            shopping_car_key=shopping_car_key%(user_id,course_id)
            print(shopping_car_key)

            val={
                "course_name":course_obj.name,
                "course_img_src":course_obj.course_img,
                "price_policys":json.dumps(price_policy_dict),
                "default_prcie_policy_id":price_policy_id
            }

            self.conn.hmset(shopping_car_key,val)
            self.response.data = "success"


        except PriceException as e:
            self.response.code = "3000"
            self.response.error_msg = e.msg

        except ObjectDoesNotExist as e:
            print("该课程不存在！")
            self.response.code="2000"
            self.response.error_msg="该课程不存在！"

        return JsonResponse(self.response.dict)

    def get(self,request):
        """
        查看购物车列表请求
        :param request:
        :return:
        """
        pass