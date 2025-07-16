from django.shortcuts import render
from rest_framework import generics
from .models import MyModel
from .serializers import MyModelSerializer


# Create your views here.
class BookListCreateApiView(generics.ListCreateAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
