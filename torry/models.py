from django.db import models
from django.core.validators import RegexValidator
from django_cleanup import cleanup
import json
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your models here.

class Category(models.Model):
    category = models.CharField(max_length=50, verbose_name="Категория")
    def __str__(self):
        return self.category
    class Meta:
        verbose_name="Категория"
        verbose_name_plural="Категории"

class CategoryImage(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='category_images/')
    viber_image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        super(CategoryImage, self).save(*args, **kwargs)

        if self.image and not self.viber_image:  
            img = Image.open(self.image)
            img.thumbnail((400, 400))  

            output = BytesIO()
            format = self.image.name.split('.')[-1].lower()  

            if format == 'png':
                img.save(output, format='PNG') 
                viber_image_extension = 'png'
            elif format == 'jpeg' or format == 'jpg':
                img.save(output, format='JPEG')  
                viber_image_extension = 'jpg'
            else:
                return 
            output.seek(0)

            viber_image = InMemoryUploadedFile(
                output,
                'ImageField',
                f'{self.image.name.split(".")[0]}_viber.{viber_image_extension}',
                f'image/{viber_image_extension}',
                output.tell(),
                None
            )

            self.viber_image = viber_image
            super(CategoryImage, self).save(*args, **kwargs)

class Icon(models.Model):
    image = models.ImageField(upload_to='icons/')

class Brand(models.Model):
    brand = models.CharField(max_length=50, verbose_name="Бренд")
    def __str__(self):
        return self.brand
    class Meta:
        verbose_name="Бренд"
        verbose_name_plural="Бренды"

class Pillow_case(models.Model):
    pillow_case = models.CharField(max_length=20, verbose_name="Размер наволочек")
    def __str__(self):
        return self.pillow_case
    class Meta:
        verbose_name="Размер наволочки"
        verbose_name_plural="Размеры наволочок"

class Material(models.Model):
    material = models.CharField(max_length=30, verbose_name="Материал")
    def __str__(self):
        return self.material
    class Meta:
        verbose_name="Материал"
        verbose_name_plural="Материалы"

class Sheet_size(models.Model):
    sheet_size = models.CharField(max_length=20, verbose_name="Размер простыни")
    def __str__(self):
        return self.sheet_size
    class Meta:
        verbose_name="Размер простыни"
        verbose_name_plural="Размеры простыни"

class Duvet_size(models.Model):
    duvet_size = models.CharField(max_length=20, verbose_name="Размер пододеяльника")
    def __str__(self):
        return self.duvet_size
    class Meta:
        verbose_name="Размер пододеяльника"
        verbose_name_plural="Размеры пододеяльника"

class Size(models.Model):
    size = models.CharField(max_length=20, verbose_name="Общий размер")
    def __str__(self):
        return self.size
    class Meta:
        verbose_name="Общий размер"
        verbose_name_plural="Общие размеры"

class Color(models.Model):
    color = models.CharField(max_length=40, verbose_name="Color css")
    color_translation = models.CharField(max_length=40, verbose_name="Название цвета") 
    def __str__(self):
        return self.color_translation
    class Meta:
        verbose_name="Цвет"
        verbose_name_plural="Цвета"

class Filler(models.Model):
    filler = models.CharField(max_length=25, verbose_name="Наполнитель")
    def __str__(self):
        return self.filler
    class Meta:
        verbose_name="Наполнитель"
        verbose_name_plural="Наполнители"

class RugSize(models.Model):
    rug_size = models.CharField(max_length=25, verbose_name="Размер Коврика")
    def __str__(self):
        return self.rug_size
    class Meta:
        verbose_name="Размер коврика"
        verbose_name_plural="Размер ковриков"

class ClothSize(models.Model):
    cloth = models.CharField(max_length=25, verbose_name="Размер одежды")
    def __str__(self):
        return self.cloth
    class Meta:
        verbose_name="Размер одежды"
        verbose_name_plural="Размеры одежды"

class TowelSize(models.Model):
    towel = models.CharField(max_length=25, verbose_name="Полотенца")
    def __str__(self):
        return self.towel
    class Meta:
        verbose_name="Размер полотенца"
        verbose_name_plural="Размеры полотенц"

class ClothCategory(models.Model):
    clothCategory = models.CharField(max_length=25, verbose_name="Категория домашней одежды")
    def __str__(self):
        return self.clothCategory
    class Meta:
        verbose_name="Категория домашней одежды"
        verbose_name_plural="Категории домашней одежды"

class Product(models.Model): 
    article = models.IntegerField(
        verbose_name='Номер/Артикль',
        validators = [RegexValidator(r'^-?\d{1,30}$', 'ID должен содержать только цифры и знак минуса.')], 
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=30, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория", default=1 )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="Бренд", null=True, blank=True)
    price = models.IntegerField(verbose_name="Цена (или скидка)")
    discount = models.IntegerField(verbose_name="Цена до скидки", blank=True, null=True)
    size = models.ForeignKey(Size,on_delete=models.CASCADE, verbose_name="Общий размер", null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name="Цвет", null=True, blank=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, blank=True, verbose_name="Материал", null=True)
    counter = models.IntegerField(verbose_name='Количество', null=True, blank=True)
    notes = models.TextField(verbose_name='Описание', null=True, blank=True)
    #Постель + подушка + покрывала и тд
    pillow_case = models.ForeignKey(Pillow_case, on_delete=models.CASCADE, verbose_name="Размер подушки", blank=True, null=True)
    sheet_size = models.ForeignKey(Sheet_size, on_delete=models.CASCADE, verbose_name="Размер простыни", blank=True, null=True)
    duvet_size = models.ForeignKey(Duvet_size, on_delete=models.CASCADE, verbose_name="Размер пододеяльника", blank=True, null=True)
    #Подушка и покрывало
    filler = models.ForeignKey(Filler, on_delete=models.CASCADE, blank=True, verbose_name="Наполнитель", null=True)
    #Коврик
    rug = models.ForeignKey(RugSize, on_delete=models.CASCADE, blank=True, verbose_name="Размер коврика", null=True)
    #халат 
    robe = models.ForeignKey(ClothSize, on_delete=models.CASCADE, verbose_name="Размер одежды", blank=True, null=True)
    robe_category = models.ForeignKey(ClothCategory, on_delete=models.CASCADE, verbose_name="Категория домашней одежды", blank=True, null=True)
    #Полотенце
    towel = models.ForeignKey(TowelSize, on_delete=models.CASCADE, verbose_name="Размер полотенца", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    class Meta:
        verbose_name="Товар"
        verbose_name_plural="Товар"
        ordering = ['-created_at']

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='bed_images/', verbose_name="Изображение")
    def __str__(self):
        return self.image.name
    class Meta:
        verbose_name="Изображения выбранного продукта"
        verbose_name_plural="Изображения выбранного продукта"
    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

class Order(models.Model):
    order = models.CharField(max_length=25, verbose_name="Номер заказа")
    user_first_name = models.CharField(max_length=25, null=True, verbose_name="Имя")
    user_last_name = models.CharField(max_length=25, null=True, verbose_name="Фамилия")
    user_email = models.EmailField(null=True, verbose_name="Email заказчика")
    user_phone = models.CharField(max_length=20,null=True, verbose_name="Номер телефона")
    delivery_method = models.CharField(max_length=50,null=True, verbose_name="Способ доставки")
    delivery_city = models.CharField(max_length=255,null=True, verbose_name="Город Доставки")
    delivery_department = models.CharField(max_length=255,null=True, verbose_name="Отделение Новой Почты")
    delivery_street = models.CharField(max_length=255,null=True, verbose_name="Адрес доставки курьером")
    payment_method = models.CharField(max_length=50,null=True, verbose_name="Способ оплаты")
    comment = models.TextField(blank=True, null=True, verbose_name="комментарий")
    feedback = models.BooleanField(default=False, verbose_name="Хочет ли заказчик обратной связи")
    feedback_method = models.CharField(max_length=50, blank=True, null=True, verbose_name="Способ обратной связи")
    time = models.DateTimeField(auto_now_add=True, verbose_name="Время (Когда сервер принял заказ)")
    articles = models.TextField(null=True, verbose_name="Артикли заказанных товаров")
    processed = models.BooleanField(default=False, verbose_name="Заказ обработан?")
    class Meta:
        verbose_name="Заказ"
        verbose_name_plural="Заказы"
        ordering = ['processed', '-time']



class Info(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название соц-сети')
    url = models.URLField(verbose_name='Ссылка на соц-сеть')
    def __str__(self):
        return self.name
    class Meta: 
        verbose_name='Соц-сеть + ссылка'
        verbose_name='Ссылки на соц-сети'