# from django.http import HttpResponse
from django.shortcuts import render
from .moon import get_moon_phase  # import your function

def home(request):
    moon = None
    selected_date = None

    if 'date' in request.GET:
        selected_date = request.GET.get('date')  # format: 'YYYY-MM-DD'
        year, month, day = map(int, selected_date.split('-'))
        moon = get_moon_phase(year, month, day)

    return render(request, 'home.html', {
        'moon': moon,
        'selected_date': selected_date,
    })

def loading(request):
    return render(request, 'loading.html')
