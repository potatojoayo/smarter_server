from django.shortcuts import render


def address(request):
    return render(request, 'address.html',)
