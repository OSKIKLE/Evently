from . import views
from django.contrib import admin
from django.urls import path, include
from wydarzenia import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.strona_glowna, name='home'),
    path('wydarzenia/', views.lista_wydarzen, name='events'),
    path('logowanie/', views.ekran_logowania, name='login'),
    path('rejestracja/', views.ekran_rejestracji, name='register'), 
    path('moje-wydarzenia/', views.moje_wydarzenia, name='moje_wydarzenia'),
    path('stworz-wydarzenie/', views.stworz_wydarzenie, name='stworz_wydarzenie'),
    path('dodaj-wydarzenie/', views.dodaj_wydarzenie, name='dodaj_wydarzenie'),
    path('wydarzenie/<int:wydarzenie_id>/', views.szczegoly_wydarzenia, name='szczegoly_wydarzenia'),
    path('', include('wydarzenia.urls')),
    path('usun-wydarzenie/<int:wydarzenie_id>/', views.usun_wydarzenie, name='usun_wydarzenie'),
    path('zapisz-sie/<int:wydarzenie_id>/', views.zapisz_sie, name='zapisz_sie'),
    path('moje-zapisy/', views.moje_zapisy, name='moje_zapisy'),
    path('wyloguj/', views.wyloguj_view, name='wyloguj'),
]