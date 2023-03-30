from django.contrib import admin
from django.urls import include, path
from . import views
from .middlewares.auth import  auth_middleware


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage,name="homepage"),
    path('pro_desc', views.pro_desc,name="pro_desc"),
    path('product_quantity', views.product_quantity,name="product_quantity"),
    path('signup', views.signup),
    path('login', views.login,name="login"),
    path('logout', views.logout),
    path('cart', auth_middleware(views.cart), name='cart'),
    path('checkout', auth_middleware(views.CheckOut), name='checkout'),
    path('updateprofile', auth_middleware(views.updateprofile), name='updateprofile'),
    path('orderdetail', auth_middleware(views.orderdetail), name='orderdetail'),
    path('store', views.store , name='store'),
    path('sell', auth_middleware(views.sell) , name='sell'),
    path('sellproductlist', auth_middleware(views.sellproductlist) , name='sellproductlist'),
    # path('orders', views.orders,name="orders"),
    path('orders', auth_middleware(views.orders), name='orders'),

]


from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)