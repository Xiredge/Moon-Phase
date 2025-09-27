# from django.http import HttpResponse
from django.shortcuts import render
from .moon import get_moon_phase  # import your function

def home(request):
    moon = None
    selected_date = None

    displays = ""

    if 'date' in request.GET:
        selected_date = request.GET.get('date')  # format: 'YYYY-MM-DD'
        year, month, day = map(int, selected_date.split('-'))

        if year <= 1899 or year >= 2053:
            displays = "This webpage can only calculate the moon phases between January 1, 1900 and December 31, 2052"
        else:
            moon = get_moon_phase(year, month, day)


    return render(request, 'home.html', {
        'moon': moon,
        'selected_date': selected_date,

        'displays': displays,
    })