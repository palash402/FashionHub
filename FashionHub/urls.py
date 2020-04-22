"""Fashion_Hub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from shopping.views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',Home,name='home'),
    url(r'^about/$',About,name='about'),
url(r'^login/$',Login,name='login'),
    url(r'^contact/$',Contact,name='contact'),
    url(r'^products/(?P<sub_id>[0-9]+)/$',products,name='products'),
    url(r'^product_details/(?P<p_id>[0-9]+)/$',Product_Details,name='product_detail'),
url(r'^add_to_cart/(?P<pid>[0-9]+)/$',AddToCart,name='cart'),
url(r'^remove_product/(?P<cid>[0-9]+)/$',Delete_product_from_cart,name='remove'),
    url(r'^mycart/$',MyCart,name='mycart'),
url(r'^signup/$',Signup,name='signup'),
url(r'^payment/(?P<pid>[0-9]+)/$',Payment,name='payment'),
url(r'^payment_check/$',Payment_check,name='payment_check'),
url(r'^order_product/(?P<pid>[0-9]+)/$',Order,name='order'),
url(r'^clear_cart/$',Clear_Cart,name='clearcart'),
############### Admin Urls ############
url(r'^admin_panel/$',Admin_home,name='admin_panel'),
url(r'^All_cat/$',AllCategory,name='all_cat'),
url(r'^Add_cat/$',Add_category,name='add_cat'),
url(r'^all_subcat/$',All_subcategory,name='all_subcat'),
url(r'^Add_subcat/$',Add_sub_cat,name='add_subcat'),
url(r'^All_product/$',All_product,name='all_product'),
url(r'^Add_product/$',Add_product,name='add_product'),
url(r'^delete_category/(?P<cid>[0-9]+)/$',Delete_cat,name='delete_cat'),
url(r'^delete_sub_category/(?P<sid>[0-9]+)/$',Delete_subcat,name='delete_subcat'),
url(r'^delete_product/(?P<pid>[0-9]+)/$',Delete_product,name='delete_pro'),
url(r'^All_orders/$',All_order,name='all_order'),
url(r'^user_list/(?P<pid>[0-9]+)/$',Buyer_details,name='user_list'),
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
