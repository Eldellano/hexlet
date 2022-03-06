from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic.base import TemplateView
from hello_django.calc.models import History
# Create your views here.

# def index(request):
#     return HttpResponse('calc')


class CalcView(TemplateView):

    # def get(self, request, a, b):
    #     return HttpResponse(a + b)

    template_name = 'calc/calc.html'

    def get_context_data(self, a, b, **kwargs):
        context = super().get_context_data()
        context['first'] = a
        context['second'] = b
        result = a + b
        context['sum'] = result
        History(value=result).save()
        return context


class CalcDefView(CalcView):

    def get(self, *args):
        return redirect('calc', a=40, b=2)

class CalcHistory(TemplateView):
    template_name = 'calc/history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['hist'] = History.objects.all().order_by("-timestamp")[:11]
        # for h in History.objects.all():
        #     print(h.timestamp, h.value)
        return context
