from django.shortcuts import render, redirect
from .models import Stock
from .form import StockForm
from django.contrib import messages
# Create your views here.

# pk_bc567b4d46eb417489a87da4a11fd0d6


def home(request):
    import requests
    import json

    if request.method == "POST":
        ticker = request.POST["ticker"]
        api_request = requests.get(
            "https://cloud-sse.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_bc567b4d46eb417489a87da4a11fd0d6")

        try:
            api = json.loads(api_request.content)
        except:
            api = 'Error...'
        return render(request, 'home.html', {'api': api})
    else:
        return render(request, 'home.html', {'ticker': 'Please enter ticker Symbol...'})


def about(request):
    return render(request, 'about.html', {})


def addStock(request):
    import requests
    import json

    if request.method == "POST":
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock Added Successfully"))
            return redirect('addStock')

    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            api_request = requests.get(
                "https://cloud-sse.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_bc567b4d46eb417489a87da4a11fd0d6")

            try:
                api = json.loads(api_request.content)
                output.append(api)
            except:
                api = 'Error...'
        return render(request, 'addStock.html', {'ticker': ticker, 'output': output})


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock Has been deleted successfully"))
    return redirect('addStock')
