from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from .models import Wydarzenie, Zapis


# -----------------------------
# STRONA GŁÓWNA
# -----------------------------
def strona_glowna(request):
    nadchodzace = Wydarzenie.objects.filter(data__gte=timezone.now()).order_by('data')[:6]
    nowe = Wydarzenie.objects.all().order_by('-id')[:2]
    return render(request, 'index.html', {'nadchodzace': nadchodzace, 'nowe_wydarzenia': nowe})


# -----------------------------
# LISTA WYDARZEŃ
# -----------------------------
def lista_wydarzen(request):
    wydarzenia = Wydarzenie.objects.filter(data__gte=timezone.now()).order_by('data')
    return render(request, 'wydarzenia.html', {'wydarzenia': wydarzenia})


# -----------------------------
# LOGOWANIE / REJESTRACJA / WYLOGOWANIE
# -----------------------------
def ekran_logowania(request):
    if request.method == 'POST':
        login_user = request.POST.get('username')
        haslo_user = request.POST.get('password')
        user = authenticate(request, username=login_user, password=haslo_user)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Nieprawidłowe dane logowania.")
    return render(request, 'logowanie.html')


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
    return redirect('home')


# -----------------------------
# MOJE WYDARZENIA
# -----------------------------
def moje_wydarzenia(request):
    if not request.user.is_authenticated:
        return redirect('login')
    moje = Wydarzenie.objects.filter(autor=request.user)
    return render(request, 'moje_wydarzenia.html', {'moje_wydarzenia': moje})


# -----------------------------
# TWORZENIE WYDARZENIA
# -----------------------------
def stworz_wydarzenie(request):
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


# -----------------------------
# SZCZEGÓŁY WYDARZENIA
# -----------------------------
def szczegoly_wydarzenia(request, wydarzenie_id):
    wydarzenie = get_object_or_404(Wydarzenie, pk=wydarzenie_id)
    return render(request, 'szczegoly_wydarzenia.html', {'wydarzenie': wydarzenie})


# -----------------------------
# ZAPISYWANIE SIĘ NA WYDARZENIE
# -----------------------------
def zapisz_sie(request, wydarzenie_id):
    if not request.user.is_authenticated:
        # zamiast przekierowania — popup w HTML
        messages.warning(request, "Musisz być zalogowany, aby zapisać się na wydarzenie.")
        return redirect('events')

    wydarzenie = get_object_or_404(Wydarzenie, id=wydarzenie_id)

    if not Zapis.objects.filter(wydarzenie=wydarzenie, uzytkownik=request.user).exists():
        Zapis.objects.create(wydarzenie=wydarzenie, uzytkownik=request.user)
        messages.success(request, f"Pomyślnie zapisano się na wydarzenie: {wydarzenie.nazwa}")
    else:
        messages.info(request, "Już jesteś zapisany na to wydarzenie.")

    return redirect('events')
