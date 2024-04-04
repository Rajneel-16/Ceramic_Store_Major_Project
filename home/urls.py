from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name="home"
urlpatterns = [
    path("",views.home,name="home"),
    path("login-page/", views.login_page, name="login"),
    path("register/", views.register, name="register"),
    path("logout",views.logout_user,name="logout"),
    path("detaile",views.detaile,name="detaile"),
    path("home",views.home),

    path("cart",views.cart,name="cartpage"),
    path("addtocart/<int:id>",views.addtocart,name="add"),
    path("del/<int:id>",views.deleteitem,name="delete"),

    path('download/<str:filename>/',views.download, name='download'),
    path("filter/",views.filter,name="filter"),
    path("menu/",views.filter_sidebar,name="sidebar"),
    path("detaile/<str:num>",views.detaile,name="detaile"),
    path("buy",views.purchase,name="purchase"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)