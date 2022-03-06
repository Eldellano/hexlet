from django.urls import path
from hello_django.calc.views import CalcView, CalcDefView, CalcHistory

urlpatterns = [
    path('', CalcDefView.as_view()),
    path('history/', CalcHistory.as_view()),
    path('<int:a>/<int:b>/', CalcView.as_view(), name='calc')
]
