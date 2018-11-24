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

from api.models import *

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings


class PaymentView(APIView):

    authentication_classes = [LoginAuth,]
    response=BaseResponse()
    conn=get_redis_connection("default")

    def post(self,request):
        """
        结算课程的保存
        :param request:
        :return:
        """
        print(request.user,request.auth)
        print("request.data",request.data) #      {course_id_list:[course_id, ....]}
        course_id_list=request.data.get("course_id_list")
        try:
            payment_key=settings.LUFFY_PAYMENT%(request.user.pk)
            payment_dict={}
            for course_id in course_id_list:
                # 校验课程是否存在购物车中
                course_dict={}

                shopping_car_key = settings.LUFFY_SHOPPING_CAR
                shopping_car_key=shopping_car_key%(request.user.pk,course_id)

                if not  self.conn.exists(shopping_car_key):
                    self.response.error_msg = "购物城中不存在该课程"
                    self.response.code = 2000
                    raise Exception


                # 获取循环的该课程的详细信息字典

                course_detail=self.conn.hgetall(shopping_car_key)
                print("course_detail",course_detail)
                print("ok123")

                course_detail_dict={}
                for key,val in course_detail.items():

                    key=key.decode("utf8")
                    val=val.decode("utf8")
                    if key=="price_policys":
                        print(val)
                        val=json.loads(val)
                        print(type(val))

                    course_detail_dict[key]=val

                print("----->",course_detail_dict)


                # 查询登录用户所有有效优惠券
                import datetime
                now=datetime.datetime.now().date()

                coupon_record_list=CouponRecord.objects.filter(user=request.user,status=0,coupon__valid_begin_date__lt=now,coupon__valid_end_date__gt=now)

                #  构建数据结构，保存到redis中：
                course_coupons_dict = {}
                global_coupons_dict = {}
                for coupon_record  in coupon_record_list:
                    temp={
                        "name":coupon_record.coupon.name,
                        "coupon_type": coupon_record.coupon.coupon_type,
                        "money_equivalent_value": coupon_record.coupon.money_equivalent_value or "",
                        "off_percent": coupon_record.coupon.off_percent or "",
                        "minimum_consume": coupon_record.coupon.minimum_consume or "",
                        "object_id":coupon_record.coupon.object_id or ""

                    }

                    # 判断该优惠券对象是通用优惠券还是课程优惠券
                    if coupon_record.coupon.object_id:
                        # 课程优惠券
                        course_coupons_dict[coupon_record.pk]=json.dumps(temp)
                    else:
                        # 通用优惠券
                        global_coupons_dict[coupon_record.pk]=json.dumps(temp)

                course_dict["course_detail"]=json.dumps(course_detail_dict)
                course_dict["coupons"]=json.dumps(course_coupons_dict)

                payment_dict[course_id]=course_dict

            self.conn.hmset(payment_key,payment_dict)
            self.response.data="success"

        except Exception as e :
            print(e)


        return JsonResponse(self.response.dict)

    def get(self,request):
        """
        :param request:
        :return:
        """
        pass