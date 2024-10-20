from django.shortcuts import render


def htmx_home(request):
    return render(request, "htmx/htmx.html")


def landing_page(request):
    return render(request, "home/home_page.html")
