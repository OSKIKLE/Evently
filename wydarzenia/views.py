from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone

from .models import Wydarzenie, Zapis


# -----------------------------
# STRONA GŁÓWNA
# -----------------------------
def strona_glowna(request):
    nadchodzace = Wydarzenie.objects.filter(data__gte=timezone.now()).order_by('data')[:6]
    nowo_dodane = Wydarzenie.objects.all().order_by('-id')[:5]

    return render(request, 'index.html', {
        'nadchodzace': nadchodzace,
        'nowo_dodane': nowo_dodane
    })


# -----------------------------
# LOGOWANIE / REJESTRACJA
# -----------------------------
def ekran_logowania(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            error_message = "Nie ma takiego konta"
        else:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')
            else:
                error_message = "Nieprawidłowe hasło"

    return render(request, 'logowanie.html', {'error_message': error_message})


def ekran_rejestracji(request):
    blad = None

    if request.method == 'POST':
        login_u = request.POST.get('username')
        haslo = request.POST.get('password')
        powtorz = request.POST.get('password_confirm')

        if haslo != powtorz:
            blad = "Hasła nie są identyczne!"
        elif User.objects.filter(username=login_u).exists():
            blad = "Użytkownik o takiej nazwie już istnieje!"
        else:
            User.objects.create_user(username=login_u, password=haslo)
            return redirect('login')

    return render(request, 'rejestracja.html', {'error': blad})


def wyloguj_view(request):
    logout(request)
    return redirect('/')


# -----------------------------
# LISTA WYDARZEŃ (z filtrowaniem + ukrywanie starych)
# -----------------------------
def lista_wydarzen(request):
    query = request.GET.get('q')

    wydarzenia = Wydarzenie.objects.filter(data__gte=timezone.now()).order_by('data')

    if query:
        wydarzenia = wydarzenia.filter(
            Q(nazwa__icontains=query) | Q(miejsce__icontains=query)
        )

    return render(request, 'wydarzenia.html', {'wydarzenia': wydarzenia})


# -----------------------------
# SZCZEGÓŁY WYDARZENIA
# -----------------------------
def szczegoly_wydarzenia(request, wydarzenie_id):
    wydarzenie = get_object_or_404(Wydarzenie, pk=wydarzenie_id)
    return render(request, 'szczegoly_wydarzenia.html', {'wydarzenie': wydarzenie})


# -----------------------------
# TWORZENIE WYDARZENIA
# -----------------------------
@login_required
def stworz_wydarzenie(request):
    return render(request, 'stworz_wydarzenie.html')


@login_required
def dodaj_wydarzenie(request):
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


# -----------------------------
# MOJE WYDARZENIA
# -----------------------------
@login_required
def moje_wydarzenia(request):
    moje = Wydarzenie.objects.filter(autor=request.user)
    return render(request, 'moje_wydarzenia.html', {'moje_wydarzenia': moje})


# -----------------------------
# LISTA UCZESTNIKÓW
# -----------------------------
@login_required
def lista_uczestnikow(request, wydarzenie_id):
    wydarzenie = get_object_or_404(Wydarzenie, pk=wydarzenie_id)

    if wydarzenie.autor != request.user:
        return redirect('moje_wydarzenia')

    zapisy = Zapis.objects.filter(wydarzenie=wydarzenie)
    return render(request, 'lista_uczestnikow.html', {'wydarzenie': wydarzenie, 'zapisy': zapisy})


# -----------------------------
# USUWANIE WYDARZENIA
# -----------------------------
@login_required
def usun_wydarzenie(request, wydarzenie_id):
    wydarzenie = get_object_or_404(Wydarzenie, id=wydarzenie_id)

    if wydarzenie.autor == request.user:
        wydarzenie.delete()

    return redirect('moje_wydarzenia')


# -----------------------------
# ZAPISYWANIE SIĘ NA WYDARZENIE
# -----------------------------
@login_required
def zapisz_sie(request, wydarzenie_id):
    wydarzenie = get_object_or_404(Wydarzenie, id=wydarzenie_id)

    if not Zapis.objects.filter(wydarzenie=wydarzenie, uzytkownik=request.user).exists():
        Zapis.objects.create(wydarzenie=wydarzenie, uzytkownik=request.user)
        messages.success(request, f"Pomyślnie zapisano się na wydarzenie: {wydarzenie.nazwa}")
    else:
        messages.info(request, "Już jesteś zapisany na to wydarzenie.")

    return redirect('events')


# -----------------------------
# MOJE ZAPISY
# -----------------------------
@login_required
def moje_zapisy(request):
    zapisy = Zapis.objects.filter(uzytkownik=request.user)
    return render(request, 'moje_zapisy.html', {'zapisy': zapisy})
