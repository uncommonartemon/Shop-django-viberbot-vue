from rest_framework import serializers
from .models import Product, ProductImage, Category, CategoryImage, Info, Icon
from django.conf import settings

base_url = settings.BASE_URL

class ProductImageSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    class Meta:
        model = ProductImage
        fields = ('image', 'product')

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.CharField(source='category.category')
    color = serializers.CharField(source='color.color', allow_null=True)
    brand = serializers.CharField(source='brand.brand', allow_null=True)
    size = serializers.CharField(source='size.size', allow_null=True)
    material = serializers.CharField(source='material.material', allow_null=True)
    pillow_case = serializers.CharField(source='pillow_case.pillow_case', allow_null=True)
    duvet_size = serializers.CharField(source='duvet_size.duvet_size', allow_null=True)
    sheet_size = serializers.CharField(source='sheet_size.sheet_size', allow_null=True)
    filler = serializers.CharField(source='filler.filler', allow_null=True)
    towel = serializers.CharField(source='towel.towel', allow_null=True)
    rug = serializers.CharField(source='rug.rug_size', allow_null=True)
    robe = serializers.CharField(source='robe.cloth', allow_null=True)
    robe_category = serializers.CharField(source='robe_category.clothCategory', allow_null=True)
    class Meta:
        model = Product
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        images = ProductImageSerializer(instance.productimage_set.all(), many=True).data
        for image in images:
            image['image'] = base_url + image['image'] #раскоментировать при viber
        representation['images'] = images 
        return representation
              
    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES
        bed = Product.objects.create(**validated_data)
        bed.productimage_set.all().delete() # удалить все связанные изображения
        for image_data in images_data.values():
            ProductImage.objects.create(product=bed, image=image_data)
        return bed

    def update(self, instance, validated_data):
        images_data = self.context.get('view').request.FILES
        instance = super().update(instance, validated_data)
        for image_data in images_data.values():
            ProductImage.objects.create(product=instance, image=image_data)
        return instance
    

class CategoryImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    viber_image = serializers.ImageField(read_only=True)  # Add the viber_image field

    class Meta:
        model = CategoryImage
        fields = ('category', 'image', 'viber_image')
        
class CategorySerializer(serializers.ModelSerializer):
    images = CategoryImageSerializer(source='categoryimage_set', many=True)
    class Meta:
        model = Category
        fields = ('category', 'images')

class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = ['id', 'name', 'url']

class IconSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    def get_filename(self, obj):
        return obj.image.name.split('/')[-1].split('.')[0]

    def get_image(self, obj):
        return f"{base_url}{obj.image.url}"

    class Meta:
        model = Icon
        fields = ('filename', 'image')

#VIBER

