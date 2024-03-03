import requests
from viberbot.api.messages import KeyboardMessage
import math

frame = {
    "BorderWidth": 2,
    "BorderColor": "#ffffff",
    "CornerRadius": 10
}

frame_category = {
    "BorderWidth": 1,
    "BorderColor": "#ffffff",
    "CornerRadius": 5
}

def create_main_menu():
    keyboard = {
        "Type": "keyboard",
        "InputFieldState" : "hidden",
        #"BgColor" : '#131621',
        'DefaultHeight' : False,
        "Buttons": [
            {
                "Columns": 3,
                "Rows": 1,
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b>Категории</b></font>",
                "TextSize": "regular",
                "Image": "",
                "TextVAlign": "middle",
                "TextHAlign": "center",
                "ActionBody": "category",
                "Silent": True,        
                'Frame' : frame,
            },
            {
                "Columns": 3,
                "Rows": 1,
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b>Корзина</b></font>",
                "TextSize": "regular",
                "TextVAlign": "middle",
                "TextHAlign": "center",
                 'Frame' : frame,
                "ActionBody": "cart",
                "Silent": True
            },
            {
                "Columns": 3,
                "Rows": 1,
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b>Поиск</b></font>",
                "TextSize": "regular",
                "TextVAlign": "middle",
                "TextHAlign": "center",
                'Frame' : frame,
                "ActionBody": "search",
                "Silent": True
            },
                       {
                "Columns": 3,
                "Rows": 1,
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b>Инфо</b></font>",
                "TextSize": "regular",
                "TextVAlign": "middle",
                "TextHAlign": "center",
                'Frame' : frame,
                "ActionBody": "info",
                "Silent": True
            },
        ]
    }

    return keyboard

def create_categories(categories):
    keyboard_buttons = []
    for cat in categories: 
        button = {
            'Columns': 3,  # Ширина кнопки для фотографии (в данном случае 6)
            'Rows': 2,  # Высота кнопки для фотографии (в данном случае 3)
            'ActionBody': cat['category'],  
            'BgMediaType': 'picture',
            'BgMedia' : cat['image'],
            'Frame' : frame_category,
            'Image': cat['image'],
            'TextPaddings': [5, 10, 5, 10],
            'Silent': True,
            
            #'Text': '<font color="#000000"><b>'+cat['category']+'</b></font>' ,
        }
        button_name = {
            'Columns': 3, 
            'Rows': 2,
            'ActionBody': cat['category'],  
            'Frame' : frame_category,
            'Text': '<font color="#000000"><b>'+cat['category']+'</b></font>' ,
            'TextSize' : 'large',
            'BgColor': '#ffffff'
        }
        keyboard_buttons.append(button)
        keyboard_buttons.append(button_name)
        

    button_back = {
        'Columns': 3,
        'Rows': 2,
        'ActionBody': 'Меню',  
        'Text': '<font color="#000000"><b>Назад</b></font>' ,
        #'BgColor': '#e5e1ff',
        'TextSize': 'large',
        'Frame' : frame_category,
        "Silent" : True,
        'BgColor': '#ffffff'
    }
    keyboard_buttons.append(button_back)

    keyboard = {
        'Type': 'keyboard',
        'Buttons': keyboard_buttons,
        'DefaultHeight': True,
        "InputFieldState" : "hidden",
    }
    
    return keyboard



########## PRODUCTS CAROUESEL 


def category_carousel(products_page):
    carousel = {
        "Type": "rich_media",
        "ButtonsGroupColumns": 6,
        "ButtonsGroupRows": 7,
        "Buttons": [],
        "Sender": {}, 
        "BgColor": "#ae9ef4",
    }

    for product in products_page:
        # Create a block with product information
        name_row = 0
        if product['name'] == None or product['name'] == '':
            name_row = 1
        if len(product['images']) > 0:
            image_block = {
                "Image": product['images'][0]['image'],
                "Rows": 5 + name_row,
                "ActionBody": str(product['article']), 
                "Silent": True,    
                #"Columns": 6,
            }
        else:
            image_block = {
                "Rows": 5 + name_row,
                "ActionBody": str(product['article']), 
                "Silent": True,    
                "TextSize": "large",
                "Text": "<font color='#e5e1ff'><b>Фотография отсуствует</b></font>",
            }

        block = {
            #"Columns": 6,
            "Silent": True,   
            "Rows": 1 - name_row,
            "ActionBody": str(product['article']), 
            "Title": product['name'],
            "TextSize": "medium",
            "TextVAlign": "middle",
            "TextHAlign": "middle",
            "Text": "<font color='#e5e1ff'><b>"+product['name']+"</b></font>",
            "ImageSize": "medium",
            "ImageScaleType": "crop",

        }
        price = {
            "Rows": 1,
            "Silent": True,   
            "Columns": 3,
            "TextVAlign": "center",
            "TextHAlign": "left",
            "Text": "<font color='#e5e1ff'><b>"+str(product['price'])+"₴</b></font>",
            "ActionBody": str(product['id']), 
        }

        end_text = product['size'] if product['size'] is not None else product['brand'] if product['brand'] is not None else "Инфо"
        add = {
            "Rows": 1,
            "Silent": True,   
            "Columns": 2,
            "TextVAlign": "center",
            "TextHAlign": "center",
            'TextSize' : 'small',
            "Text": "<font color='#e5e1ff'><b>добавить</b></font>",
            "ActionBody": "add " + str(product['article']),
            'Frame' : frame,
            
        }
        end = {
            "Rows": 1,
            "Silent": True,   
            "Columns": 3,
            "TextVAlign": "center",
            "TextHAlign": "right",
            "Text": "<font color='#e5e1ff'><b>"+end_text+"</b></font>",
            "ActionBody": str(product['article']), 
        }
        # Add the product block to the carousel
        if product['name'] != None:
            carousel['Buttons'].append(block)
        carousel['Buttons'].append(image_block)
        carousel['Buttons'].append(price)
        #carousel['Buttons'].append(add)
        carousel['Buttons'].append(end)
    return carousel

def create_navigation(page, category):
    navigation = {
        "Type": "keyboard",
        "InputFieldState" : "hidden",
        #"BgColor" : '#131621',
        'DefaultHeight' : False,
        "Buttons": [ 
             {
                "Columns": 2,
                "Rows": 1,
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b><<</b></font>",
                "TextSize": "large",
                "Image": "",
                "TextVAlign": "middle",
                "TextHAlign": "center",
                "ActionBody": "page-",
                "Silent": True,        
                'Frame' : frame,
            },
            {
                "Columns": 2,
                "Rows": 1,
                "BgColor": "#e5e1ff",
                "Text": "<font color='#ae9ef4'><b>"+ str(page) +"</b></font>",
                "TextSize": "large",
                "TextVAlign": "middle",
                "TextHAlign": "center",
                'Frame' : frame,
                "ActionBody": "button2",
                "Silent": True
            },
            {
                "Columns": 2,
                "Rows": 1,
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b>>></b></font>",
                "TextSize": "large",
                "TextVAlign": "middle",
                "TextHAlign": "center",
                'Frame' : frame,
                "ActionBody": "page+",
                "Silent": True
            },
            {
                "Columns": 3,
                "Rows": 1,
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b>В меню</b></font>",
                "TextSize": "small",
                "TextVAlign": "middle",
                "TextHAlign": "center",
                'Frame' : frame,
                'ActionBody': 'Меню',  
                "Silent": True
            },
                        {
                "Columns": 3,
                "Rows": 1,
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b>К категориям</b></font>",
                "TextSize": "small",
                "TextVAlign": "middle",
                "TextHAlign": "center",
                'Frame' : frame,
                'ActionBody': 'category',  
                "Silent": True
            },
        ]
    }
    return navigation


def product_card(product):
    carousel = {
        "Type": "rich_media",
        "ButtonsGroupColumns": 6,
        "ButtonsGroupRows": 7,
        "Buttons": [],
        "Sender": {}, 
        #"BgColor": "",
        'Frame': {
            'BorderWidth': 1,
            'BorderColor': '#e5e1ff',
            'CornerRadius': 10
            },
    }
    title = {
        "BgColor": "#ae9ef4",
        "Silent": True,  
        "Rows": 1,
        "Columns" : 6,
        "ActionBody": str(product['article']), 
        "Text": "<font color='#e5e1ff'><b> Карточка товара : #"+ str(product["article"]) + "</b></font>",
        'Frame': {
            'BorderWidth': 1,
            'BorderColor': '#e5e1ff',
            'CornerRadius': 10
        },
    }
    name = {
        "BgColor": "#ae9ef4",
        "Silent": True,  
        "Rows": 1,
        "Columns" : 6,
        "ActionBody": str(product['article']), 
        "Text": "<font color='#e5e1ff'><b>"+ str(product["name"]) + "</b></font>",
        'Frame': {
            'BorderWidth': 1,
            'BorderColor': '#e5e1ff',
            'CornerRadius': 10
        },
    }
    if product['brand'] != None:
        brand_name = str(product["brand"])
    else:
        brand_name = 'Не указан'
    brand = {
        "BgColor": "#ae9ef4",
        "Silent": True,  
        "Rows": 1,
        "Columns" : 3,
        "ActionBody": str(product['article']), 
        "TextSize" : 'small',
        "Text": "<font color='#e5e1ff'><b>Бренд: "+ brand_name + "</b></font>",
        'Frame': {
            'BorderWidth': 1,
            'BorderColor': '#e5e1ff',
            'CornerRadius': 10
        },
    }
    if product['material'] != None:
        material_name = product['material']
    else:
        material_name = 'Материал не указан'
    material = {
        "BgColor": "#ae9ef4",
        "Silent": True,  
        "Rows": 1,
        "Columns" : 3,
        "TextSize" : 'small',
        "ActionBody": str(product['article']), 
        "Text": "<font color='#e5e1ff'><b>Материал: "+ material_name + "</b></font>",
        'Frame': {
            'BorderWidth': 1,
            'BorderColor': '#e5e1ff',
            'CornerRadius': 10
        },
    }
    if product['size'] != None:
        size_value = product['size']
    else:
        size_value = 'Отсуствует'
    size = {
        "BgColor": "#ae9ef4",
        "Silent": True,  
        "Rows": 1,
        "Columns" : 6,
        "ActionBody": str(product['article']), 
        "Text": "<font color='#e5e1ff'><b>Общий размер : "+ size_value + "</b></font>",
        'Frame': {
            'BorderWidth': 1,
            'BorderColor': '#e5e1ff',
            'CornerRadius': 10
        },
    }
    sheet_size = duvet_size = pillow_case = "Нет"
    if product['sheet_size'] != None:
        sheet_size = product['sheet_size']
    if product['duvet_size'] != None:
        duvet_size = product['duvet_size']
    if product['pillow_case'] != None:
        pillow_case = product['pillow_case']
    sizes = {
        "BgColor": "#ae9ef4",
        "Silent": True,  
        "Rows": 1,
        "Columns" : 6,
        "TextSize": "small",
        "ActionBody": str(product['article']), 
        "Text": "<font color='#e5e1ff'><b>Размеры: Простынь: "+sheet_size+", Накидка: "+duvet_size+", Наволочка: "+pillow_case+"</b></font>",
        'Frame': {
            'BorderWidth': 1,
            'BorderColor': '#e5e1ff',
            'CornerRadius': 10
        },
    }
    if product['pillow_case'] != None:
        pillow = {
            "BgColor": "#ae9ef4",
            "Silent": True,  
            "Rows": 1,
            "Columns" : 6,
            "TextSize": "small",
            "ActionBody": str(product['article']), 
            "Text": "<font color='#e5e1ff'><b> Размер подушки : "+str(product['pillow_case'])+", Наполнитель : "+str(product['filler'])+"</b></font>",
            'Frame': {
                'BorderWidth': 1,
                'BorderColor': '#e5e1ff',
                'CornerRadius': 10
            },
        }
    if product['robe'] != None:
        robe = {
            "BgColor": "#ae9ef4",
            "Silent": True,  
            "Rows": 1,
            "Columns" : 6,
            "TextSize": "small",
            "ActionBody": str(product['article']), 
            "Text": "<font color='#e5e1ff'><b> Размер одежды: "+str(product['robe'])+", Категория одежды: "+str(product['robe_category'])+"</b></font>",
            'Frame': {
                'BorderWidth': 1,
                'BorderColor': '#e5e1ff',
                'CornerRadius': 10
            },
        }
    if product['towel'] != None:
        towel = {
            "BgColor": "#ae9ef4",
            "Silent": True,  
            "Rows": 1,
            "Columns" : 6,
            "TextSize": "regular",
            "ActionBody": str(product['article']), 
            "Text": "<font color='#e5e1ff'><b>Размер полотенца: "+product['towel']+"</b></font>",
            'Frame': {
                'BorderWidth': 1,
                'BorderColor': '#e5e1ff',
                'CornerRadius': 10
            },
        }
    if product['rug'] != None:
        rug = {
            "BgColor": "#ae9ef4",
            "Silent": True,  
            "Rows": 1,
            "Columns" : 6,
            "TextSize": "regular",
            "ActionBody": str(product['article']), 
            "Text": "<font color='#e5e1ff'><b>Размер Коврика: "+product['rug']+"</b></font>",
            'Frame': {
                'BorderWidth': 1,
                'BorderColor': '#e5e1ff',
                'CornerRadius': 10
            },
        }
    notes_text = "Отсуствует"
    if product['notes'] != None:
        notes_text = product['notes']
    notes = {
        "BgColor": "#ae9ef4",
        "Silent": True,  
        "Rows": 1,
        "Columns" : 6,
        "TextSize": "small",
        "ActionBody": str(product['article']), 
        "Text": "<font color='#e5e1ff'><b>Описание: "+notes_text+"</b></font>",
        'Frame': {
            'BorderWidth': 1,
            'BorderColor': '#e5e1ff',
            'CornerRadius': 10
        },
    }
    price = {
        "BgColor": "#ae9ef4",
        "Silent": True,  
        "Rows": 1,
        "Columns" : 6,
        "TextSize": "regular",
        "ActionBody": str(product['article']), 
        "Text": "<font color='#e5e1ff'><b>Цена: "+str(product['price'])+"₴</b></font>",
        'Frame': {
            'BorderWidth': 1,
            'BorderColor': '#e5e1ff',
            'CornerRadius': 10
        },
    }
    carousel['Buttons'].append(title)
    carousel['Buttons'].append(name)
    carousel['Buttons'].append(brand)
    carousel['Buttons'].append(material)
    carousel['Buttons'].append(size)
    if product['category'] != 'Коврики' or product['category'] != 'Домашняя одежда' or product['category'] != 'Подушки' or product['category'] != 'Полотенца':
        carousel['Buttons'].append(sizes)
    if product['category'] == "Подушки":
        carousel['Buttons'].append(pillow)
    if product['category'] == "Домашнаяя одежда":
        carousel['Buttons'].append(robe)
    if product['category'] == "Полотнеца":
        carousel['Buttons'].append(towel)
    if product['category'] == "Полотнеца":
        carousel['Buttons'].append(rug)
    carousel['Buttons'].append(notes)
    carousel['Buttons'].append(price)
    for image in product['images']:
        image_block = {
            "BgColor": "#ae9ef4",
            "Rows": 7,
            "Columns" : 6,
            "TextSize": "regular",
            "ActionBody": str(image['image']), 
            'Frame': {
                'BorderWidth': 1,
                'BorderColor': '#e5e1ff',
                'CornerRadius': 10
            },
            'BgMediaType': 'picture',
            'BgMedia' : image['image'], 
        }
        carousel['Buttons'].append(image_block)
    return carousel
    
def product_nav(article, product, last_visit_before_product_card):
    back_value = None
    if last_visit_before_product_card == 'cart':
        back_value = 'cart'
    elif last_visit_before_product_card == 'products':
        back_value = product['category']
    elif last_visit_before_product_card == 'search':
        back_value = 'search_no_message'
    navigation = {
        "Type": "keyboard",
        "InputFieldState" : "hidden",
        #"BgColor" : '#131621',
        'DefaultHeight' : False,
        "Buttons": [ 
            {
                "Columns": 3,
                "Rows": 1,
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b>В корзину #"+ str(article) +"</b></font>",
                "TextSize": "regular",
                "Image": "",
                "TextVAlign": "middle",
                "TextHAlign": "center",
                "ActionBody": "add " + str(article),
                "Silent": True,        
                'Frame' : frame,
            },
            {
                "Columns": 3,
                "Rows": 1,
                "BgColor": "#e5e1ff",
                "Text": "<font color='#ae9ef4'><b>Назад</b></font>",
                "TextSize": "regular",
                "TextVAlign": "middle",
                "TextHAlign": "center",
                'Frame' : frame,
                "ActionBody": back_value,
                "Silent": True
            },
        ]
    }
    return navigation


#CART CART CART CART

def rich_cart(cart):
    carousel = {
        "Type": "rich_media",
        "ButtonsGroupColumns": 6,
        "ButtonsGroupRows": 7,
        "Buttons": [],
        "Sender": {}, 
        "BgColor": "#ae9ef4",
        'Frame': {
            'BorderWidth': 1,
            'BorderColor': '#e5e1ff',
            'CornerRadius': 10
            },
    }
    for product in cart:
        upper_block = {
            "Rows": 1,
            "Silent": True,  
            "ActionBody": str(product['article']), 
            "Text": "<font color='#e5e1ff'><b>"+product['name']+"</b></font>",
        }
        image_block = {
            "Image": product['images'][0]['image'],
            "Rows": 5,
            "ActionBody": str(product['article']), 
            "Silent": True,    
            #"Columns": 6,
        }
        price_block = {
            "Rows": 1,
            "Columns" : 3,
            "Silent": True,  
            "ActionBody": str(product['article']), 
            "Text": "<font color='#e5e1ff'><b>"+str(product['price'])+"₴</b></font>",
        }
        remove_block = {
            "Rows": 1,
            "Columns" : 3,
            "Silent": True,  
            "ActionBody": "remove "+str(product['article'])+"", 
            "Text": "<font color='#e5e1ff'><b>удалить</b></font>",
        }
        carousel["Buttons"].append(upper_block)
        carousel["Buttons"].append(image_block)
        carousel["Buttons"].append(price_block)
        carousel["Buttons"].append(remove_block)
    return carousel 

def create_nav_cart(cart_page, len_cart):
    navigation = {
        "Type": "keyboard",
        "InputFieldState" : "hidden",
        #"BgColor" : '#131621',
        'DefaultHeight' : False,
        "Buttons": []
    }
    if len_cart > 6:
        navigation["Buttons"].append({
            "Columns": 2,
            "Rows": 1,
            "BgColor": "#ae9ef4",
            "Text": "<font color='#e5e1ff'><b><<</b></font>",
            "TextSize": "large",
            "Image": "",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            "ActionBody": "cart_page-",
            "Silent": True,
            'Frame' : frame,
        })
        navigation["Buttons"].append({
            "Columns": 2,
            "Rows": 1,
            "BgColor": "#e5e1ff",
            "Text": "<font color='#ae9ef4'><b>"+ str(cart_page)+'/'+ str(math.ceil(len_cart / 6)) +"</b></font>",
            "TextSize": "large",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            'Frame' : frame,
            "ActionBody": "button2",
            "Silent": True
        })
        navigation["Buttons"].append({
            "Columns": 2,
            "Rows": 1,
            "BgColor": "#ae9ef4",
            "Text": "<font color='#e5e1ff'><b>>></b></font>",
            "TextSize": "large",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            'Frame' : frame,
            "ActionBody": "cart_page+",
            "Silent": True
        })
    button_back = {
        "Columns": 3,
        "Rows": 1,
        "BgColor": "#ae9ef4",
        "Text": "<font color='#e5e1ff'><b>Вернуться</b></font>",
        "TextSize": "regular",
        "TextVAlign": "middle",
        "TextHAlign": "center",
        'Frame' : frame,
        "ActionBody": "меню",
        "Silent": True
    }
    button_check_out = {
        "Columns": 3,
        "Rows": 1,
        "BgColor": "#ae9ef4",
        "Text": "<font color='#e5e1ff'><b>Оформить заказ</b></font>",
        "TextSize": "regular",
        "TextVAlign": "middle",
        "TextHAlign": "center",
        'Frame' : frame,
        "ActionBody": "checkout",
        "Silent": True
    }
    navigation['Buttons'].append(button_back)
    navigation['Buttons'].append(button_check_out)

    return navigation

def search_keyboard(viber):
    navigation = {
        "Type": "keyboard",
        "InputFieldState" : "regular",
        #"BgColor" : '#131621',
        'DefaultHeight' : False,
        "Buttons": [
        {
            "Columns": 6,
            "Rows": 1,
            "BgColor": "#ae9ef4",
            "Text": "<font color='#e5e1ff'><b>Вернуться</b></font>",
            "TextSize": "large",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            'Frame' : frame,
            "ActionBody": "меню",
            "Silent": True
        }
        ]
    }
    return navigation


### INFO 

def info_slider(info):
    slider = {
        "Type": "rich_media",
        "ButtonsGroupColumns": 6,
        "ButtonsGroupRows": 2,
        "Buttons": [],
        "Sender": {}, 
        #"BgColor": "#ae9ef4",
        "Frame" : frame,
    }
    site = {
        'Rows': 2,
        "Silent": True,
        "ActionType": "open-url",
        "OpenURLType": "external",
        "ActionBody": "https://torry.od.ua/",
        "Text": "<font color='#ffffff'><b>Наш web-сайт</b></font>",
        "Frame" : frame,
        'BgColor': '#212624',
        "TextSize" : 'large',
    }
    for info_item in reversed(info):
        print(info_item)
        if info_item['name'].lower() == 'instagram':
            button = {
                'Rows': 2,
                "Silent": True,
                "ActionType": "open-url",
                "OpenURLType": "external",
                "ActionBody": info_item['url'],
                "Text": "<font color='#ffffff'><b>"+info_item['name']+"</b></font>",
                "Frame" : frame,
                'BgColor': '#212624',
                "TextSize" : 'large',
                'Image': 'https://i0.wp.com/www.csscodelab.com/wp-content/uploads/2020/03/instagram-style-background-gradient-css.png?w=1135&ssl=1',
            }
            slider['Buttons'].append(button)
        if info_item['name'].lower() == 'viber':
            button = {
                'Rows': 2,
                "Silent": True,
                "ActionType": "open-url",
                "OpenURLType": "external",
                "ActionBody": info_item['url'],
                "Text": "<font color='#e5e1ff'><b>Наша группа "+info_item['name']+"</b></font>",
                "Frame" : frame,
                'BgColor': '#7360f2',
                "TextSize" : 'large',
                #'Image': '',
            }
            slider['Buttons'].append(button)
    slider['Buttons'].append(site)
    return slider


def create_admin():
    keyboard = {
        "Type": "keyboard",
        "InputFieldState" : "minimized",
        #"BgColor" : '#131621',
        'DefaultHeight' : False,
        "Buttons": [
            {
                "Columns": 3,
                "Rows": 1,
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b>Категории</b></font>",
                "TextSize": "regular",
                "Image": "",
                "TextVAlign": "middle",
                "TextHAlign": "center",
                "ActionBody": "category",
                "Silent": True,        
                'Frame' : frame,
            },
            {
                "Columns": 3,
                "Rows": 1,
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b>Корзина</b></font>",
                "TextSize": "regular",
                "TextVAlign": "middle",
                "TextHAlign": "center",
                 'Frame' : frame,
                "ActionBody": "cart",
                "Silent": True
            },
            {
                "Columns": 3,
                "Rows": 1,
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b>Поиск</b></font>",
                "TextSize": "regular",
                "TextVAlign": "middle",
                "TextHAlign": "center",
                'Frame' : frame,
                "ActionBody": "search",
                "Silent": True
            },
            {
                "Columns": 3,
                "Rows": 1,
                "BgColor": "#ae9ef4",
                "Text": "<font color='#e5e1ff'><b>Заказы</b></font>",
                "TextSize": "regular",
                "TextVAlign": "middle",
                "TextHAlign": "center",
                'Frame' : frame,
                "ActionBody": "orders",
                "Silent": True
            }
        ]
    }

    return keyboard


