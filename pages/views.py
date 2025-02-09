from django.shortcuts import render

def index_view(request):
    return render(request, 'pages/index.html')

def booking_view(request):
    return render(request, 'pages/booking.html')

def bookmark_view(request):
    return render(request, 'pages/bookmark.html')