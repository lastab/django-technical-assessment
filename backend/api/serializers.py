from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Csv, Header, Row
from django.db import transaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class HeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Header
        fields = ["id", "name", "type"]


class RowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Row
        fields = ["id", "content"]

class CsvListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Csv
        fields = ["id", "file_name", "author", "created_at"]

class CsvSerializer(serializers.ModelSerializer):
    headers = HeaderSerializer(many=True)
    rows = RowSerializer(many=True)

    class Meta:
        model = Csv
        fields = ["id", "file_name", "headers", "rows", "author", "created_at"]

    def create(self, validated_data):
        headers_data = validated_data.pop('headers')
        rows_data = validated_data.pop('rows')
        with transaction.atomic():
            csv = Csv.objects.create(**validated_data)
            for header_data in headers_data:
                Header.objects.create(csv= csv, **header_data)
            for row_data in rows_data:
                Row.objects.create(csv=csv, **row_data)

        return csv
