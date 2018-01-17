from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Greeting
from django.views.decorators.csrf import csrf_exempt

import truther

@csrf_exempt
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def input(request):
    if request.method == 'GET':
        evaluation = ''
        statement = ''
        if request.GET.get("myInput"):
            statement = request.GET.get("myInput")
        if statement:
            output = truther.truthme(statement)
            print output
            if output:
                evaluation = "That's probably true!"
            else:
                evaluation = "That's likely to be false."
        return render(request, 'input.html', {'evaluation' : evaluation, 'statement' : statement})
    elif request.method == 'POST':
        input_data = request.POST.get("myInput")
        return render(request, 'input.html', {'output': 'test'})
        #truther.truthme(input_data)})
        #return Response(truther.truthme(input_data), status=200)