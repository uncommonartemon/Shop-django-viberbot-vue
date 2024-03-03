from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import TextMessage, KeyboardMessage,  RichMediaMessage
import json
import requests
from urllib.parse import unquote
from transliterate import translit
from django.utils.text import slugify
from django.conf import settings
import sys

from .MENU import *

token = "5114b04a6a67e26d-47b8019b92f46735-b130ed77ec40cc8f"
base_url = 'https://3595-188-163-102-40.ngrok-free.app'
admin_id = 'vhzrKsMox25NmEkEhSf6uw=='

pages = {}
global_category = {}

cart = {} 
cart_page = {} 

last_visit_before_product_card = {}

order_info = {}

bot_configuration = BotConfiguration(
    name="Torry",
    avatar=None,
    auth_token=token,
)
viber_api = Api(bot_configuration)

@csrf_exempt
def webhook(request):
    if request.method == "POST":
        viber = json.loads(request.body.decode('utf-8'))
        if viber['event'] == 'message':
            text = viber['message']['text']
            sender_id = viber['sender']['id']
            
            if sender_id not in cart:
                cart[sender_id] = []
            if sender_id not in cart_page:
                cart_page[sender_id] = 1
            if sender_id not in pages:
                pages[sender_id] = 1
            if sender_id not in global_category:
                global_category[sender_id] = None
            if sender_id not in last_visit_before_product_card:
                last_visit_before_product_card[sender_id] = None

            if text == 'category':
                category_run(sender_id)

            elif text == 'orders' and sender_id == admin_id:
                admin_menu(sender_id)

            elif text.lower() == "меню":
                main_menu(sender_id)
            elif text in category_list():
                products_from_category(text, sender_id)
            elif text == 'page+':
                page_plus(viber, sender_id)
                products_from_category(global_category[sender_id], sender_id)
            elif text == 'page-':
                page_minus(viber , sender_id)
                products_from_category(global_category[sender_id], sender_id)
            elif text.isdigit():
                product_by_id(viber, sender_id)
            elif text == 'back_from_product':
                products_from_category(global_category[sender_id], sender_id)
            elif text == 'cart' or text.lower() == 'корзина' or text == '':
                open_cart(viber, sender_id)
            elif text.startswith("add "):
                article = text[4:]  
                add_to_cart(viber, article , sender_id)
            elif text.startswith("remove "):
                article = text[7:] 
                remove_from_cart(viber, article, sender_id)
            elif text == 'cart_page-':
                cart_page_minus(viber ,sender_id)
            elif text == 'cart_page+':
                cart_page_plus(viber, sender_id)
            elif text == 'search':
                search_id(viber, 'first')
            elif text == 'search_no_message':
                search_id(viber, 'no_message')
            elif text == 'info':
                info(viber)

            elif text == 'checkout':
                if sender_id not in order_info:
                    order_info[sender_id] = {
                        'name' : None,
                        'phone' : None,
                        'address' : None,
                        'dilevery' : None,
                        'pay_method' : None,
                    }
                checkout(viber)
                print(order_info)

            return HttpResponse(status=200)
        if viber['event'] == 'conversation_started':
            main_menu(viber['user']['id'])
            #create_cell_db(viber)
            return HttpResponse(status=200)
        if viber['event'] == 'subscribed':
            print('Подписка subscribed')
            return HttpResponse(status=200)
        if viber['event'] == 'unsubscribed':
            print(viber)
            if viber['user_id'] in order_info:
                del order_info[viber['user_id']]
            if viber['user_id'] in cart:
                del cart[viber['user_id']]  
            if viber['user_id'] in cart_page:
                del cart_page[viber['user_id']]
            if viber['user_id'] in pages:
                del pages[viber['user_id']]
            if viber['user_id'] in global_category:
                del global_category[viber['user_id']]
            if viber['user_id'] in last_visit_before_product_card:
                del last_visit_before_product_card[viber['user_id']]
            return HttpResponse(status=200)
        else:
            print('Нераспознанное событие:', viber['event'])
            return HttpResponse(status=200)
    else:
        print("Метод запроса не является POST")
        return HttpResponse(status=200)

def admin_menu(user_id):
    message = KeyboardMessage(keyboard=create_admin(), min_api_version=6)
    try: 
        viber_api.send_messages(user_id, [message])
    except:
        print('Админ не подписан')

def send_order_to_admin(order):
    message = TextMessage(text=str(order))
    try:
        viber_api.send_messages(admin_id, [message])
    except:
        print('Админ не подписан')

#main menu
def main_menu(user_id):
    if (user_id == admin_id):
        message = KeyboardMessage(keyboard=create_admin(), min_api_version=6)
        viber_api.send_messages(user_id, [message])
    else:
        message = KeyboardMessage(keyboard=create_main_menu(), min_api_version=6)
        viber_api.send_messages(user_id, [message])

def page_plus(viber, sender):
    global pages
    global global_category

    api_path = '/api/'+ global_category[sender] + '/' + str(pages[sender] + 1) + '/'
    api_url = f"{base_url}{api_path}"
    response = requests.get(api_url).json()
    items = len(response)
    if items > 0:
        pages[sender] += 1
    else:
        message = TextMessage(text=str(pages[sender]) + " - последняя страница")
        viber_api.send_messages(viber['sender']['id'], [message])

def page_minus(viber, sender):
    global page
    if pages[sender] > 1:
        pages[sender] -= 1
    else: 
        message = TextMessage(text="Нулевой страницы не существует")
        viber_api.send_messages(viber['sender']['id'], [message])

def clear(sender):
    global pages, global_category
    pages[sender] = 1

#category menu:

def category_json():
    api_path = "/api/categories/"
    api_url = f"{base_url}{api_path}"
    response = requests.get(api_url)
    categories = response.json() 
    return categories
    
def category_list():
    category_list = []
    for cat in category_json():
        category_list.append(cat['category'])
    return category_list

def category_run(user_id):
    message = KeyboardMessage(tracking_data='tracking_data', keyboard=create_categories(category_json()), min_api_version=7)
    viber_api.send_messages(user_id, [message])
    category_list()
    clear(user_id)

#products menu & slider

def products_from_category(category, user_id):
    true_category = category
    if category == 'Байковое постельное':
        category = 'Постельное белье'
        material = 'Байка'
    else:
        material = None

    api_path = '/api/'+ slugify(translit(category, 'ru', reversed=True)) + '/' + str(pages[user_id]) + '/'
    api_url = f"{base_url}{api_path}"
    response = requests.get(api_url)
    print(api_url)
    products_page = response.json() 

    if material:
        products_page = [product for product in products_page if product['material'] == material]

    global global_category, last_visit_before_product_card
    global_category[user_id] = true_category
    last_visit_before_product_card[user_id] = 'products'

    if len(products_page) == 0:
        viber_api.send_messages(user_id, [TextMessage(text='Извините, товары по категории '+category+' - отсутствуют.')])
        category_run(user_id)

    if len(products_page) > 0:
        message = RichMediaMessage(tracking_data='tracking_data', min_api_version=7, rich_media=category_carousel(products_page))
        navigation = KeyboardMessage(tracking_data='tracking_data', keyboard=create_navigation(pages[user_id], category), min_api_version=7)
        viber_api.send_messages(user_id, [TextMessage(text='Товары категории "' + true_category + '", страница '+str(pages[user_id])+':'),message, navigation])

####### PRODUCT CARD ID

def id_json(article):
    api_path = '/api/product/' + str(article) + '/'
    api_url = f"{base_url}{api_path}"
    response = requests.get(api_url)
    product_json = response.json() 
    return product_json

def product_by_id(viber, sender):
    article = int(viber['message']['text'])
    
    try:
        message = RichMediaMessage(tracking_data='tracking_data', min_api_version=7, rich_media=product_card(id_json(article)))
        navigation = KeyboardMessage(tracking_data='tracking_data', keyboard=product_nav(article, id_json(article), last_visit_before_product_card[sender]), min_api_version=7)
        viber_api.send_messages(viber['sender']['id'], [message, navigation])
    except:
        error_message = TextMessage(text='Номер #'+str(article)+' не найден')
        viber_api.send_messages(viber['sender']['id'], [error_message])
        search_id(viber, 'no_message', sender)

def search_id(viber, state, sender):
    global last_visit_before_product_card
    last_visit_before_product_card[sender] = 'search'

    message = TextMessage(text='Введите номер товара')
    serach_keyboard = KeyboardMessage(tracking_data='tracking_data', keyboard=search_keyboard(viber), min_api_version=7)
    if state == 'first':
        viber_api.send_messages(viber['sender']['id'], [message ,serach_keyboard])
    elif state == 'no_message':
        viber_api.send_messages(viber['sender']['id'], [serach_keyboard])

####### CARt & DB

def add_to_cart(viber, article, sender):
    global cart 
    
    #if article in cart:
        #viber_api.send_messages(viber['sender']['id'], [TextMessage(text='Товар с номером #'+str(article)+' уже есть в корзине')])
        #products_from_category(global_category, viber['sender']['id'])
    #else:
    cart[sender].append(int(article))
    viber_api.send_messages(viber['sender']['id'], [TextMessage(text='Товар под номером #'+str(article)+' добавлен в корзину, возвращаем вас к каталогу')])
    products_from_category(global_category[sender], viber['sender']['id'])

def remove_from_cart(viber, article, sender):
    global cart
    cart[sender].remove(int(article))
    viber_api.send_messages(viber['sender']['id'], [TextMessage(text='Товар под номером #'+str(article)+' удален из корзины')])
    open_cart(viber)

def get_cart_products(cart_page, sender):
    items_per_page = 6
    start_index = (cart_page - 1) * items_per_page
    end_index = start_index + items_per_page
    cart_articles = cart[sender][start_index:end_index]
    cart_products = []
    for article in cart_articles:
        cart_products.append(id_json(article))
    for product in cart_products:
        product['count'] = 1
    return cart_products

def total_price_cart(sender):
    total = 0
    product = None
    for article in cart[sender]:
        product = id_json(article)
        total += int(product['price'])
    return total
        
def open_cart(viber, sender): #1
    if len(cart[sender]) == 0:
        viber_api.send_messages(viber['sender']['id'], [TextMessage(text='Ваша корзина пуста')])
        main_menu(viber['sender']['id'])
    else:
        total = total_price_cart(sender)
        cart_message = RichMediaMessage(tracking_data='tracking_data', min_api_version=7, rich_media=rich_cart(get_cart_products(cart_page[sender], sender)))
        nav_keyboard = KeyboardMessage(tracking_data='tracking_data', keyboard=create_nav_cart(cart_page[sender], len(cart[sender])),min_api_version=7)
        viber_api.send_messages(viber['sender']['id'], [
            TextMessage(text='Ваша корзина (кол-во товаров: '+str(len(cart[sender]))+', общая стоимость '+str(total)+' грн., страница '+str(cart_page[sender])+'):'), 
            cart_message, 
            nav_keyboard
        ])
        global last_visit_before_product_card 
        last_visit_before_product_card[sender] = 'cart'

def cart_page_plus(viber, sender):
    global cart_page
    page_items = get_cart_products(cart_page[sender] + 1, sender)
    if len(page_items) > 0:
        cart_page[sender] += 1
        open_cart(viber, sender)
    
def cart_page_minus(viber, sender):
    global cart_page
    if cart_page[sender] > 1: 
        cart_page[sender] -= 1
        open_cart(viber, sender)

##### INFO

def get_info():
    api_path = '/api/info/'
    api_url = f"{base_url}{api_path}"
    response = requests.get(api_url)
    info_json = response.json()
    return info_json

def info(viber):
    info_message = RichMediaMessage(tracking_data='tracking_data', min_api_version=7, rich_media=info_slider(get_info()))
    viber_api.send_messages(viber['sender']['id'], [info_message])
    try:
        main_menu(viber['sender']['id'])
    except:
        main_menu(viber['user']['id'])


def checkout(viber):
    status = None
    #for o in order_info[viber['sender']['id']]:
        #print(o)
    #checkout_menu = KeyboardMessage(tracking_data='tracking_data', keyboard=checkout_menu(), min_api_version=7)