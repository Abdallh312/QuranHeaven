"""
URL configuration for quranheaven project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from quran.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('exchang/', exchange_details, name='exchang'),   
    path("admin/", admin.site.urls),
    path('accounts/', include('quran.urls')),
    path('', home_view, name='home'),  
    path('welcome/',welcome_view,name='welcome'),
    path('profile/<username>', profile, name='profile'),
    path("<series>",series, name="series"),
    path("<series>/<article>", article, name="article"),
    path("<series>/update/", series_update, name="series_update"),
    path("<series>/delete/", series_delete, name="series_delete"),
    path("new_sheik/",new_series, name="series-create"),
    path("new_gategory/", new_post, name="post-create"),
    path("<series>/<article>/update", article_update, name="article_update"),
    path("<series>/<article>/delete", article_delete, name="article_delete"),
    path("newsletter/", newsletter, name="newsletter"),
    path('make-order/', make_order, name='make_order'),
    path('success/', success, name='success'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('fatwas/', fatwa_list, name='fatwa_list'), 
    path('fatwa/<int:fatwa_id>/', fatwa_detail, name='fatwa_detail'),
    path('exchnage/', exchange_details, name='exchange_details'),
    path('plans/', plan_list, name='plan_list'),
    path('plans/payment/', payment, name='payment'),
    path('plans/payment_yearly/', payment_yearly, name='payment_yearly'),
    path('dontae/', donate, name='donate'),
    # path('astmaa/', astmaa, name='astmaa'),
    # path('reads/', reads, name='reads'),
]
urlpatterns += [
    path('submit_fatwa/', submit_fatwa, name='submit_fatwa'),
]
if  settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
