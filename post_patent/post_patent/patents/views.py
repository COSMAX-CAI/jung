from django.shortcuts import render
from rest_framework import viewsets, serializers
from .models import Patent


# Create your views here.


class PatentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patent
        fields = '__all__'

class PatentsViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Patent.objects.all()
    serializer_class = PatentSerializer
    #permission_classes = [IsAccountAdminOrReadOnly]


class SearchViewSet(viewsets.ModelViewSet):
    serializer_class = PatentSerializer
    def get_queryset(self):
        return Patent.objects.filter(keywords__contains=[self.kwargs['keyword_pk']])
    
