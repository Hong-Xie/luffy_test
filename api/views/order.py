

from rest_framework.views import APIView

from api.utils.response import BaseResponse
from api.utils.exceptions import CommonException
from api.utils.auth_class import LoginAuth
import datetime
from api.models import *
from  django.http import JsonResponse

class OrderView(APIView):
    authentication_classes = [LoginAuth]

    def post(self,request):
        """
        1 数据校验
         {
			    balance：699，
				bely：1000，
				global_coupon_id:1
				courses_detail:{
				        course_id:{
						      price_policy_id:1,
							  coupon_record_id:2
							}


				    }

			 }
        2 生成订单
        :return:
        """

        bely=request.data.get("bely")
        balance=request.data.get("balance")
        global_coupon_id=request.data.get("global_coupon_id")
        courses_detail=request.data.get("courses_detail")
        response=BaseResponse()
        try:
            #  数据校验
            if bely>request.user.bely:
                raise CommonException("贝里数据有问题！")




            price_list=[]
            now = datetime.datetime.now().date()
            for course_id,course_info in courses_detail.items():

                #   校验课程是否存在
                course_obj=Course.objects.filter(pk=course_id).first()
                if not course_obj:
                    raise CommonException("课程不存在")

                #   校验价格策略是否正确
                price_policy_id=int(course_info.get("price_policy_id"))
                price_policy_set=course_obj.price_policy.all()
                if price_policy_id not in [price_policy.pk for price_policy in price_policy_set]:
                    raise  CommonException("价格策略有问题！")

                #   校验课程优惠券是否有效

                coupon_record_id = int(course_info.get("coupon_record_id"))
                coupon_record_obj=CouponRecord.objects.filter(pk=coupon_record_id,
                                                              user=request.user,
                                                              coupon__valid_begin_date__lt=now,
                                                              coupon__valid_end_date__gt=now,
                                                              ).first()

                if not coupon_record_obj:
                    raise CommonException("优惠券有问题")

                # 校验该优惠券是否属于该课程
                if coupon_record_obj.coupon.object_id!=int(course_id):
                    raise  CommonException("优惠券与课程不匹配")

                #    计算该循环课程经过课程优惠券处理后的价格

                price=PricePolicy.objects.filter(pk=price_policy_id).first().price

                rebate_price=self.account_price(coupon_record_obj,price)

                #    将计算出的价格存放到一个列表中
                price_list.append(rebate_price)



            # 校验通用优惠券
            g_coupon_record_obj = CouponRecord.objects.filter(pk=global_coupon_id,
                                                            user=request.user,
                                                            coupon__valid_begin_date__lt=now,
                                                            coupon__valid_end_date__gt=now,
                                                            ).first()

            if not g_coupon_record_obj:
                raise  CommonException("通用优惠券与问题")


            # 将价格列表求和后再经通用优惠券处理出一个实际价格
            account_price = self.account_price(g_coupon_record_obj, sum(price_list))

            # 校验balance    实际价格-beli/10==balance

            final_price=account_price-bely/10
            if final_price<0:
                final_price=0

            if final_price!=balance:
                raise CommonException("提交价格有问题")

            # 创建订单
                # Order记录（一条）
                # OrderDetail（多条）

            # 跳转支付宝接口

            '''
            alipay = ali()

            # 生成支付的url
            query_params = alipay.direct_pay(
                subject="课程",  # 商品简单描述
                out_trade_no="x2" + str(time.time()),  # 商户订单号
                total_amount=final_price,  # 交易金额(单位: 元 保留俩位小数)
            )

            pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)

            return pay_url

            '''

            return JsonResponse(self.response.dict)

        except CommonException as e:
            self.response.error_msg=e.msg
            self.response.code=2000



    def account_price(self,coupon_record,price):

        coupon_type=coupon_record.coupon.coupon_type
        money_equivalent_value=coupon_record.coupon.money_equivalent_value
        off_percent=coupon_record.coupon.off_percent
        minimum_consume=coupon_record.coupon.minimum_consume
        debate_price=0
        if coupon_type==0:
            if price>money_equivalent_value:
                debate_price=price-money_equivalent_value

        elif coupon_type==1:
            if price>minimum_consume:
                debate_price=price-money_equivalent_value
            else:
                raise CommonException("优惠券无效")

        elif coupon_type==2:
            debate_price=price*(off_percent/100)

        return debate_price



