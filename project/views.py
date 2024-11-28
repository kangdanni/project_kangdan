from django.shortcuts import render
from django.db.models import Sum, IntegerField
from django.db.models import F,ExpressionWrapper

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ReadOnlyField

from .models import Category, Product, Coupon



class CategorySerializer(serializers.Serializer):
  name = serializers.CharField(max_length=100)

class ProductsSerializer(serializers.Serializer):
  
  name = serializers.CharField(max_length=100)
  description = serializers.CharField()
  price = serializers.IntegerField()
  category = serializers.StringRelatedField()
  discount_rate = serializers.FloatField()
  coupon_applicable=serializers.BooleanField()


class TestView(APIView):
  def post(self,request):
    """
    사용자는 전체 리스트 조회가 가능하며, 카테고리별로 상품 필터링이 가능하다.

    상품이름. 설명, 가격 카테고리, 할인율(있을 경우), 쿠폰 적용 가능 여부를 포함한다.

    """
    categorys = Category.objects.values()
    
    serializer= TestSerializer(categorys,many=True)

    return Response(serializer.data)

class ProductDetailView(APIView):
  """ 
  특정 상품의 상세정보를 조회한다.
  상세 페이지에서는 할인율을 적용한 할인 가격을 함께 반환한다.

  원래 가격과 할인 가격 모두 표시.
  상품에 쿠폰이 적용된 경우 쿠폰 할인율을 적용한 최종가격도 표시해야한다.
  """
  def post(self,request):
    Product.objects.filter()

    return  

class TestProductView(APIView):
  """
  상품에 적용가능한 쿠폰 목록을 제공한다.
  쿠폰이 적용된 상품은 할인이 추가되어 최종 가격을 계산한다.

  * 할인율은 상품별로 다를 수 있음.
  * 쿠폰이 적용되면 상품의 할인가격에 추가로 쿠폰할인이 적용되어 최종 가격이 결정된다.
  """
  def post(self,request):

    products  = Product.objects.values()

    for i in products:
      print(i)
    serializer= ProductsSerializer(products,many=True)

    return Response(serializer.data)
  
class CouponPriceView(APIView):
  def post(self,request):
    
    coupon_produts = Product.objects.filter(
                      coupon_applicable=True
                      ).annotate(
                        discounted_price =ExpressionWrapper(F('price') *(1 - F('discount_rate')),output_field=IntegerField())
                      ).values()
    
    coupon_list = Coupon.objects.values()

    coupon_apply_list = []
    for product in coupon_produts:
      print(product)
      item = dict()
      item['name'] = product['name'] 
      item['discount_list'] = []

      for coupon in coupon_list:
        print(coupon, 'cc')
        final_price = product['discounted_price'] * (1-coupon['discount_rate'])
        adj_coupon_code = coupon['code']
        
        item['final_price'] = final_price
        item['adj_coupon_code']=adj_coupon_code
        item['discount_list'].append(item)

      coupon_apply_list.append(item)
    print(coupon_apply_list)
    return Response({'msg':'ok'})