from rest_framework import generics, status
from .models import Product, ProductImage, Category, Info, Material, Icon

from .serializers import ProductSerializer, ProductImageSerializer, CategorySerializer, CategoryImageSerializer, InfoSerializer, IconSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.text import slugify
from transliterate import translit
from django.http import JsonResponse
import json
from datetime import datetime
from .models import Order
from django.conf import settings
from django.shortcuts import get_object_or_404

from viberbotapp.views import send_order_to_admin
from django.core.mail import send_mail
from django.core import serializers

ngrok = settings.BASE_URL
base_url = 'http://127.0.0.1:8000/'

class ProductByArticle(APIView):
    def get(self, request, article):
        try:
            product = Product.objects.get(article=article)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer
    def get_queryset(self):
        queryset = Product.objects.all().prefetch_related('productimage_set')
        category = self.request.query_params.get('category')
        article = self.request.query_params.get('article')
        if category:
            if category == 'Байковое постельное':
                # Находим категорию "Постельное белье" с материалом 'Байка'
                bedding_category = get_object_or_404(Category, category="Постельное белье")
                material = get_object_or_404(Material, material="Байка")
                queryset = queryset.filter(category=bedding_category, material=material)
            else:
                queryset = queryset.filter(category__category=category)
        if article:
            queryset = queryset.filter(article=article)
        return queryset

#viber

class ProductListByCategory(generics.ListAPIView):
    serializer_class = ProductSerializer
    def get_queryset(self):
        queryset = Product.objects.all().prefetch_related('productimage_set')
        category = self.kwargs['category']

        category_cyrillic = translit(category, 'ru', reversed=True)
        category_slug = slugify(category_cyrillic)
        print(category_slug)

        queryset = queryset.filter(category__category=category_slug)

        page = self.kwargs['page']
        items_per_page = 6
        offset = (int(page) - 1) * items_per_page
        limit = offset + items_per_page

        queryset = queryset[offset:limit]

        return queryset

#///////

class InfoList(generics.ListAPIView):
    queryset = Info.objects.all()
    serializer_class = InfoSerializer

class BedImageList(generics.ListAPIView):
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()

#cat

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        response_data = super().list(request, *args, **kwargs).data
        result = []
        for item in response_data:
            category_data = {'category': item['category']}
            images = item['images']
            if images:
                category_data['image'] = images[0]['image'] #.get('image', '').split('8000')[1]
            #     print(category_data)
            url = slugify(translit(item['category'], 'ru', reversed=True))
            category_data['url'] = url

            result.append(category_data)
        return Response(result)
        
class IconList(generics.ListAPIView):
    queryset = Icon.objects.all()
    serializer_class = IconSerializer

"""
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def list(self, request, *args, **kwargs):
        response_data = super().list(request, *args, **kwargs).data
        result = []
        for item in response_data:
            category_data = {'category': item['category']}
            images = item['images']
            if images:
                category_data['image'] = images[0]['image']
                category_data['viber_image'] = images[0]['viber_image']
            url = slugify(translit(item['category'], 'ru', reversed=True))
            category_data['url'] = url
            result.append(category_data)
        return Response(result)
"""

#для get токена , затем юзер отправит post с токеном  

from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

def csrf_token_view(request):
    token = get_token(request)
    return JsonResponse({'csrf_token': token})

#Заказ отправленный пользователем на сервер


@csrf_exempt
def submit_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        order_number = datetime.now().strftime("%d%m%Y%H%M%S")
        order = Order(
            order=order_number,
            user_first_name=data['user']['firstName'],
            user_last_name=data['user']['lastName'],
            user_email=data['user']['email'],
            user_phone=data['user']['number'],
            delivery_method=data['user']['delivery'],
            delivery_city=data['user']['city'],
            delivery_department=data['user']['depart'],
            delivery_street=data['user']['street'],
            payment_method=data['user']['pay'],
            comment=data['user']['comment'],
            feedback=data['user']['feedback'],
            feedback_method=data['user']['feedbackMethod'],
            articles=json.dumps(data['articles'])  # Сериализуем список в JSON строку
        )
        order.save() 

        order_json = serializers.serialize('json', [order])

        send_order_to_admin(order_json)

        # Включаем номер заказа в JSON-ответ
        response_data = {
            'status': 'success',
            'data': {
                'orderNumber': order.order
            }
        }
        response = JsonResponse(response_data)
        
        #send_email()

        def send_email():
            subject = order_number
            message = f'Ваш номер заказа: {order.order}'
            from_email = 'torry.clothes@gmail.com' 
            to_email = data['user']['email']  
            send_mail(subject, message, from_email, [to_email])

        return response