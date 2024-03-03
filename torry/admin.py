from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.forms import Select
import os
import random
from django.db.models import F
from django.core.validators import RegexValidator
from dal import autocomplete
# Register your models here.

from .models import (Order, Category, CategoryImage ,Product, Brand, ProductImage, Material, Sheet_size,
 Duvet_size, Pillow_case, Size, Color, Filler, RugSize, ClothSize, TowelSize, ClothCategory, Info, Icon)

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('order', 'user_first_name', 'user_last_name', 'user_email', 'user_phone', 'delivery_method',
        'delivery_city', 'delivery_department', 'delivery_street', 'payment_method', 'comment',
        'feedback', 'feedback_method', 'time', 'articles')
    list_display = ('order', 'user_first_name', 'user_last_name', 'user_phone', 'delivery_city', 'articles' ,'time', 'processed')
    list_filter = ('processed', 'time')
    actions = ['mark_as_processed', 'mark_as_unprocessed']

    def mark_as_processed(self, request, queryset):
        queryset.update(processed=True)

    def mark_as_unprocessed(self, request, queryset):
        queryset.update(processed=False)

    mark_as_processed.short_description = "Mark selected orders as processed"
    mark_as_unprocessed.short_description = "Mark selected orders as unprocessed"
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(is_processed=F('processed'))  # Добавляем временное поле "is_processed" с значением поля "processed"
        queryset = queryset.order_by('is_processed', '-time')  # Сортируем сначала по "is_processed" (False, True), затем по убывающему "time"
        return queryset

admin.site.register(Order, OrderAdmin)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fields = ['image_preview', 'image']
    readonly_fields = ['image_preview']
    can_delete = True
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100px" />', obj.image.url)
        else:
            return '(No image)'
    def get_extra(self, request, obj=None, **kwargs):
        count = self.model.objects.filter(product=obj).count()
        if count == 0:
            return 2
        else:
            return 0
    image_preview.short_description = 'Превью'
    class Meta:
        ordering = ['id']
        verbose_name = 'Изображение продукта'
        verbose_name_plural = 'Изображения продукта'

class ArticleGeneratorWidget(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        if not value:
            value = random.randint(1000, 9999)
        return super().render(name, value, attrs, renderer)

class ProductColorChoiceField(forms.ModelChoiceField):
    widget = autocomplete.Select2(attrs={'class': 'autocomplete-select'})

class ProductAdminForm(forms.ModelForm):
    article = forms.IntegerField(
        label='Номер/Артикул',
        required=False,  # Поле становится необязательным
        widget=ArticleGeneratorWidget,  # Используем свой виджет
        validators=[RegexValidator(r'^-?\d{1,30}$', 'ID должен содержать только цифры и знак минуса.')]
    )
    color = forms.ModelChoiceField(
        queryset=Color.objects.all(),
        label='Цвет',
        widget=autocomplete.Select2(attrs={'class': 'autocomplete-select'}),
    )

    def clean_article(self):
        article = self.cleaned_data.get('article')
        if self.instance.pk is None and Product.objects.filter(article=article).exists():
            raise forms.ValidationError('Такой артикул уже существует.')
        return article

    class Meta:
        model = Product
        fields = '__all__'


class BedAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('article', 'created_at' , 'name', 'category', 'price', 'discount', 
    'brand', 'color', 'material' , 'size', 'sheet_size', 'duvet_size', 'pillow_case'
    ,'filler', 'towel', 'robe', 'rug'
    )
    list_filter = ['article', 'name', 'price']
    search_fields = ['article']
    form = ProductAdminForm 

class SizeAdmin(admin.ModelAdmin):
    size = ('Общий размер')

class CategoryImageInline(admin.TabularInline):
    model = CategoryImage
    extra = 1
    max_num = 1

class CategoryAdmin(admin.ModelAdmin):
    category_display = ('Категория')
    inlines = [CategoryImageInline]

class ClothCategoryAdmin(admin.ModelAdmin):
    clothCategory = ('Категория одежды')

class BrandAdmin(admin.ModelAdmin):
    brand_display = ('Бренд')

class MeterialAdmin(admin.ModelAdmin):
    material = ('Материал')

class FillerAdmin(admin.ModelAdmin):
    material = ('Наполнитель')

class ClothSizeAdmin(admin.ModelAdmin):
    material = ('Размер одежды')

class TowelSizeAdmin(admin.ModelAdmin):
    material = ('Размер полотенца')

class RugSizeAdmin(admin.ModelAdmin):
    material = ('Размер коврика')

class Sheet_Size_Admin(admin.ModelAdmin):
    sheet_size = ('Размер простыни')

class Duvet_Size_Admin(admin.ModelAdmin):
    duvet_size = ('Размер пододеяльника')

class Pillow_Size_Admin(admin.ModelAdmin):
    pillow_case = ('Размер наволочки')

class Color_Admin(admin.ModelAdmin):
    list_display = ['color_buttons', 'color', 'color_translation']

    def color_buttons(self, obj):
        return format_html(
            '<div style="display: flex; justify-content: center; align-items: center; height: 100%;">'
            '<button type="button" style="background-color:{};margin: 0;"></button>',
            obj.color
        )
    color_buttons.short_description = "Цвет"

admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, BedAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(ProductImage)
admin.site.register(Material, MeterialAdmin)
admin.site.register(Sheet_size, Sheet_Size_Admin)
admin.site.register(Duvet_size, Duvet_Size_Admin)
admin.site.register(Pillow_case, Pillow_Size_Admin)
admin.site.register(Color, Color_Admin)
admin.site.register(Filler, FillerAdmin)
admin.site.register(RugSize, RugSizeAdmin)
admin.site.register(TowelSize, TowelSizeAdmin)
admin.site.register(ClothSize, ClothSizeAdmin)
admin.site.register(ClothCategory, ClothCategoryAdmin)
admin.site.register(Info)
admin.site.register(Icon)
