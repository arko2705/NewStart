from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name='index'),
    path('Features/',views.features,name="features"),
    path('How To Use/',views.HTU,name="HTU"),
    path('Get Started/',views.gs,name="gs"),
    path('About/',views.ab,name="ab"),
    path('query/',views.q,name="q"),
    path('your data is loading...',views.loading,name='loading'),
    path('YourData',views.data,name="data"),
    path('idk',views.yes,name="idk")
]