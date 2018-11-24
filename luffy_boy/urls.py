"""luffy_boy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin


from api.views.course import coursesView,CourseDetailView
from api.views.auth import LoginView
from api.views.shopping_car import ShoppingCarView
from api.views.payment import PaymentView
from api.views.order import OrderView
from api.views.ordersure import OrderEnsureView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', LoginView.as_view()),
    url(r'^courses/', coursesView.as_view()),
    url(r'^coursedetail/(?P<pk>\d+)', CourseDetailView.as_view()),
    url(r'^shopping_car/', ShoppingCarView.as_view()),
    url(r'^payment/', PaymentView.as_view()),
    url(r'^order/', OrderView.as_view()),
    url(r'^order_ensure/', OrderEnsureView.as_view()),
]
