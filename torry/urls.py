from django.urls import path, re_path
from .views import ProductList, BedImageList, CategoryList, InfoList, ProductListByCategory, ProductByArticle, IconList
from . import views
from django.views.generic import TemplateView
from .views import csrf_token_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('api/products/', ProductList.as_view()),
    path('api/categories/', CategoryList.as_view(), name='category_list'),
    path('api/product/<article>/', ProductByArticle.as_view(), name='product-detail'),
    path('api/icons/', IconList.as_view(), name='icon-list'),
    path('api/<str:category>/<str:page>/', ProductListByCategory.as_view(), name='product-list-by-category'),
    path('submit_order/', views.submit_order, name='submit_order'),
    path('api/info/', InfoList.as_view(), name='info-list'),
    path('csrf_token/', csrf_token_view, name='csrf_token'),
    # Catch-all URL pattern to serve the Vue Router index.html
    path('category-<str:category>/article-<str:article>', TemplateView.as_view(template_name='index.html')),
    path('category-<str:category>', TemplateView.as_view(template_name='index.html')),
    path('product/<str:article>', TemplateView.as_view(template_name='index.html')),
    path('politic', TemplateView.as_view(template_name='index.html')),
    path('checkout', TemplateView.as_view(template_name='index.html')),
    path('return', TemplateView.as_view(template_name='index.html')),
    # Catch-all URL pattern to serve the Vue Router index.html
    path('', TemplateView.as_view(template_name='index.html')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)