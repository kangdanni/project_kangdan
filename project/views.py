from django.shortcuts import render
from django.db.models import F,ExpressionWrapper,Q,IntegerField, OuterRef, Subquery
from django.db.models.functions import Coalesce
# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ReadOnlyField

from .models import Category, Product, Coupon


"""
시리얼라이저를 선언한다.
"""
class RequestSerializer(serializers.Serializer):
  cond = serializers.CharField(max_length=100, allow_null=True)
class ResponseProductListSerializer(serializers.Serializer):
  
  name = serializers.CharField(max_length=100)
  description = serializers.CharField(max_length=255)
  price = serializers.IntegerField()
  category_name = serializers.CharField(max_length=100)
  discount_rate = serializers.FloatField(allow_null=True)
  coupon_applicable=serializers.BooleanField()
  
  def to_representation(self, instance):
    res = super().to_representation(instance)
    #할인율이 존재할 경우에만 내보낸다.
    if not res['discount_rate'] or res['discount_rate'] ==0:
      del res['discount_rate']
    return res

class ResponseProductDetailSerializer(serializers.Serializer):
  
  name = serializers.CharField(max_length=100)
  category_name = serializers.CharField(max_length=255)
  coupon_code = serializers.CharField(max_length=255)
  price = serializers.IntegerField()
  final_price = serializers.IntegerField()

class NestedCouponPriceSerizlier(serializers.Serializer):
  final_price = serializers.IntegerField()
  adj_coupon_code = serializers.CharField(max_length=25)

class ResponseCouponPriceSerializer(serializers.Serializer):
  name = serializers.CharField(max_length=100)
  discount_list = NestedCouponPriceSerizlier(many=True)



"""
API VIEW
"""
class ProductListView(APIView):
  def post(self,request):
    """
    사용자는 전체 리스트 조회가 가능하며, 카테고리별로 상품 필터링이 가능하다.
    상품이름. 설명, 가격 카테고리, 할인율(있을 경우), 쿠폰 적용 가능 여부를 포함한다.
    """
    products = Product.objects.values()
    cond = False


    request_serializer = RequestSerializer(data=request.data)
    if not request_serializer.is_valid():
      return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    cond = request_serializer.data['cond']
    if cond:
      obj_model=products.filter(category = cond)
    else:
      obj_model = products
    
    results = obj_model.annotate(category_name=Subquery(
                  Category.objects.filter(
                    id = OuterRef('id')
                  ).values('name')
                )).values('name','description','category_name','price'\
                          ,'discount_rate','coupon_applicable')
    
    serializer = ResponseProductListSerializer(results,many=True)
    

    return Response(serializer.data)

class ProductDetailView(APIView):
  """ 
  특정 상품의 상세정보를 조회한다.
  상세 페이지에서는 할인율을 적용한 할인 가격을 함께 반환한다.

  원래 가격과 할인 가격 모두 표시.
  상품에 쿠폰이 적용된 경우 쿠폰 할인율을 적용한 최종가격도 표시해야한다.

  #한상품에 쿠폰 한개만 적용할 수 있다고 가정...
  #쿠폰별로 쿠폰 적용 할인가 보여줌..
  """
  def post(self,request):
    
    request_serializer = RequestSerializer(data=request.data)

    if not request_serializer.is_valid() :
      return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
  
    cond = request_serializer.data['cond']

    product = Product.objects.filter(
                id  = cond
              ).annotate(category_name=Subquery(
                  Category.objects.filter(
                    id = OuterRef('id')
                  ).values('name')
              )).values()
    
    coupon_list = Coupon.objects.values()
    
    results = []
    
    for coupon in coupon_list:
      result= {}

      product_dc_rate = product[0]['discount_rate'] if product[0]['discount_rate'] else 0
      coupon_code = coupon['code']
      coupon_dc_rate = coupon['discount_rate']

      org_price = product[0]['price']
      product_dc_price = org_price * (1-product_dc_rate)
      final_price = product_dc_price * (1-coupon_dc_rate)

      result['coupon_code'] = coupon_code
      result['price'] = org_price
      result['final_price']= int(final_price)
      result['name'] = product[0]['name']
      result['category_name'] = product[0]['category_name']

      results.append(result)
    
    serializer = ResponseProductDetailSerializer(results,many=True)

    return Response(serializer.data,status=status.HTTP_200_OK)
class CouponPriceView(APIView):
  """
  상품에 적용가능한 쿠폰 목록을 제공한다.
  쿠폰이 적용된 상품은 할인이 추가되어 최종 가격을 계산한다.

  * 할인율은 상품별로 다를 수 있음.
  * 쿠폰이 적용되면 상품의 할인가격에 추가로 쿠폰할인이 적용되어 최종 가격이 결정된다.

  #한상품에 쿠폰 한개만 적용할 수 있다고 가정...
  """
  def post(self,request):
    
    coupon_produts = Product.objects.filter(
                      coupon_applicable=True
                      ).annotate(
                        discounted_price =ExpressionWrapper(
                                        F('price') * (1 - Coalesce(F('discount_rate'),0))
                                        ,output_field=IntegerField())
                      ).values()
    
    coupon_list = Coupon.objects.values()
    coupon_apply_list = []

    for product in coupon_produts:

      item = dict()
      item['name'] = product['name'] 
      item['discount_list'] = []

      for coupon in coupon_list:
        final_price = product['discounted_price'] * (1-coupon['discount_rate'])
        adj_coupon_code = coupon['code']
        nested_item ={}
        nested_item['final_price'] = int(final_price)
        nested_item['adj_coupon_code']=adj_coupon_code

        item['discount_list'].append(nested_item)

      coupon_apply_list.append(item)

    serializer = ResponseCouponPriceSerializer(coupon_apply_list,many=True)
  
    return Response(serializer.data,status=status.HTTP_200_OK)