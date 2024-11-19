from django.urls import path
from . import views

urlpatterns = [
    path("csvs/", views.CsvListCreate.as_view(), name="csv-list"),
    path("csvs/<int:csv_id>/", views.CsvDetail.as_view()),
    path("csvs/<int:csv_id>/headers/<int:header_id>/", views.HeaderDetail.as_view()),
]