from django.shortcuts import render
from rest_framework import viewsets, serializers
from .models import Keyword


# Create your views here.


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'

class KeywordsViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    #permission_classes = [IsAccountAdminOrReadOnly]