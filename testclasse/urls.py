"""testclasse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from oauth2_provider.views import TokenView, AuthorizationView

from library.views import create_review, book_detail, BookListView, create_book, APILibroList, simpletoken, summary, \
    addlibro, modifylibro

app_name = 'library'

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', book_detail, name='book_detail'),
    path('books/create/', create_book, name='create_book'),
    path('books/<int:pk>/review/create/', create_review, name='review_create'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),

    path('api/token/', TokenView.as_view(), name='token'),
    path('api/simpletoken/', simpletoken, name='simpletoken'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    path('api/', summary, name='summary'),
    path('api/librolist/', APILibroList.as_view(), name='api-list'),
    path('api/libro/add/', addlibro, name='api-add'),
    path('api/libro/<pk>/modify/', modifylibro, name='api-modify'),
]