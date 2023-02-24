"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

import blog
from blog import views

extra_patterns = [
        path('2/', views.test2),
        path('3/', views.test3)
]


# extra_patterns = ([
#         path('2/', views.test2),
#         path('3/', views.test3),
#     ], 'blog')

urlpatterns = [
    path('admin/', admin.site.urls),

    # TODO include用法
    path('api1/', include('blog.urls')),
    # path('api1/1/', include('blog.urls')),
    # path('api2/', include(extra_patterns), {'foo': 'bar'}),
    # path('api3/', include((extra_patterns, 'blog'))),
]
