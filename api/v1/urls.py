from django.urls import path, include

app_name = 'v1'
urlpatterns = [
    path('account/', include('api.v1.account.urls', namespace='account')),
]
