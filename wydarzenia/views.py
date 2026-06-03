from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import Wydarzenie
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Wydarzenie, Zapis
from django.contrib import messages
from .models import Zapis
from django.utils import timezone
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.db.models import Q

def strona_glowna(request):
    return render(request, 'index.html')

def lista_wydarzen(request):
    return render(request, 'wydarzenia.html')

def ekran_logowania(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Sprawdzenie czy konto w ogóle istnieje
        if not User.objects.filter(username=username).exists():
            error_message = "Nie ma takiego konta"
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                error_message = "Nieprawidłowe hasło"
                
    return render(request, 'logowanie.html', {'error_message': error_message})

def ekran_rejestracji(request):
    blad = None 
    
    if request.method == 'POST':
        login = request.POST.get('username')
        haslo = request.POST.get('password')
        powtorz_haslo = request.POST.get('password_confirm')
        
        if haslo != powtorz_haslo:
            blad = "Hasła nie są identyczne!"
        else:
            if User.objects.filter(username=login).exists():
                blad = "Użytkownik o takiej nazwie już istnieje!"
            else:
                User.objects.create_user(username=login, password=haslo)
                return redirect('login')

    return render(request, 'rejestracja.html', {'error': blad})

def moje_wydarzenia(request):
    if not request.user.is_authenticated:
        return redirect('login') 
        
    return render(request, 'moje_wydarzenia.html')

def stworz_wydarzenie(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    return render(request, 'stworz_wydarzenie.html')

def dodaj_wydarzenie(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'stworz_wydarzenie.html')

def dodaj_wydarzenie(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        nazwa = request.POST.get('nazwa')
        miejsce = request.POST.get('miejsce')
        data = request.POST.get('data')
        opis = request.POST.get('opis')

        Wydarzenie.objects.create(
            nazwa=nazwa,
            miejsce=miejsce,
            data=data,
            opis=opis,
            autor=request.user
        )
        return redirect('moje_wydarzenia')         
    return render(request, 'stworz_wydarzenie.html')

def szczegoly_wydarzenia(request, wydarzenie_id):
    wydarzenie = get_object_or_404(Wydarzenie, pk=wydarzenie_id)
    return render(request, 'szczegoly_wydarzenia.html', {'wydarzenie': wydarzenie})

def strona_glowna(request):
    nadchodzace = Wydarzenie.objects.all()[:6] 
    nowe = Wydarzenie.objects.all().order_by('-id')[:2] 
    return render(request, 'index.html', {'nadchodzace': nadchodzace, 'nowe_wydarzenia': nowe})

def moje_wydarzenia(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    moje = Wydarzenie.objects.filter(autor=request.user)
    
    return render(request, 'moje_wydarzenia.html', {'moje_wydarzenia': moje})

def lista_uczestnikow(request, wydarzenie_id):
    wydarzenie = get_object_or_404(Wydarzenie, pk=wydarzenie_id)

    if wydarzenie.autor != request.user:
        return redirect('moje_wydarzenia')
        
    zapisy = Zapis.objects.filter(wydarzenie=wydarzenie)
    return render(request, 'lista_uczestnikow.html', {'wydarzenie': wydarzenie, 'zapisy': zapisy})

@login_required
def usun_wydarzenie(request, wydarzenie_id):
    wydarzenie = get_object_or_404(Wydarzenie, id=wydarzenie_id)

    if wydarzenie.autor == request.user:
        wydarzenie.delete()
        
    return redirect('moje_wydarzenia')

def lista_wydarzen(request):
    wydarzenia = Wydarzenie.objects.all() 
    return render(request, 'wydarzenia.html', {'wydarzenia': wydarzenia})

@login_required
def zapisz_sie(request, wydarzenie_id):
    wydarzenie = get_object_or_404(Wydarzenie, id=wydarzenie_id)

    Zapis.objects.get_or_create(wydarzenie=wydarzenie, uzytkownik=request.user)
    
    return redirect('events')

@login_required
def zapisz_sie(request, wydarzenie_id):
    wydarzenie = get_object_or_404(Wydarzenie, id=wydarzenie_id)
    
    # Sprawdzamy, czy użytkownik już jest zapisany
    if not Zapis.objects.filter(wydarzenie=wydarzenie, uzytkownik=request.user).exists():
        Zapis.objects.create(wydarzenie=wydarzenie, uzytkownik=request.user)
        messages.success(request, f"Pomyślnie zapisano się na wydarzenie: {wydarzenie.nazwa}")
    else:
        messages.info(request, "Już jesteś zapisany na to wydarzenie.")
        
    return redirect('events')

@login_required
def moje_zapisy(request):
        zapisy = Zapis.objects.filter(uzytkownik=request.user)
        return render(request, 'moje_zapisy.html', {'zapisy': zapisy})

def strona_glowna(request):
    nadchodzace = Wydarzenie.objects.filter(data__gte=timezone.now()).order_by('data')[:6]
    
    nowo_dodane = Wydarzenie.objects.all().order_by('-id')[:5] 
    
    return render(request, 'index.html', {
        'nadchodzace': nadchodzace,
        'nowo_dodane': nowo_dodane
})

def wyloguj_view(request):
    logout(request) 
    return redirect('/')

def lista_wydarzen(request):
    query = request.GET.get('q')
    wydarzenia = Wydarzenie.objects.all()
    
    if query:
        wydarzenia = wydarzenia.filter(
            Q(nazwa__icontains=query) | Q(miejsce__icontains=query)
        )
    
    return render(request, 'wydarzenia.html', {'wydarzenia': wydarzenia})