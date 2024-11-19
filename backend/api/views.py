from django.contrib.auth.models import User
from .models import Csv, Header
from .serializers import UserSerializer, CsvSerializer, CsvListSerializer, HeaderSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .process_csv import process_file
import json


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class CsvListCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        csvs = Csv.objects.filter(author=user)
        serializer = CsvListSerializer(csvs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user

        uploaded_file = request.FILES['csv_file']
        df = process_file(uploaded_file) 

        headers_and_types = df.dtypes 
        headers_and_types_list = [{'name': col, 'type': dtype.name} for col, dtype in headers_and_types.items()]
        
        raw_rows = [[str(element) for element in sublist] for sublist in df.values.tolist()] 
        rows = [{'content': sublist} for sublist in raw_rows]
        
        
        data = {
            'file_name': uploaded_file.name,
            'author': user.id,
            'headers': headers_and_types_list,
            'rows': rows 
        }
        
        serializer = CsvSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CsvDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, csv_id, user):
        try:
            return Csv.objects.get(id=csv_id, author=user)
        except Csv.DoesNotExist:
            return None

    def get(self, request, csv_id, *args, **kwargs):
        csv_instance = self.get_object(csv_id, request.user.id)
        if not csv_instance:
            return Response({"res": "Object with csv id does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CsvSerializer(csv_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, csv_id, *args, **kwargs):
        csv_instance = self.get_object(csv_id, request.user.id)
        if not csv_instance:
            return Response({"res": "Object with csv id does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        csv_instance.delete()
        return Response({"res": "Object deleted!"}, status=status.HTTP_204_NO_CONTENT)

class HeaderDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, header_id, csv_id, user):
        try:
            csv = Csv.objects.get(id=csv_id, author=user)
            return Header.objects.get(id=header_id, csv=csv)
        except Header.DoesNotExist:
            return None

    def put(self, request, header_id, csv_id, *args, **kwargs):
        header_instance = self.get_object(header_id, csv_id, request.user.id)
        if not header_instance:
            return Response({"res": "Object with header id does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            
        data = {'type': request.data.get('type')}
        serializer = HeaderSerializer(instance=header_instance, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
