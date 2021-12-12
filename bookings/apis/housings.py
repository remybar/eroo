from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response

from common.serializers import inline_serializer
from bookings.models import Housing
from bookings.selectors import (
    get_housing,
    get_housing_list,
)
from bookings.services import (
    create_housing,
    update_housing,
    delete_housing,
)

class _HousingInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
    airbnb_url = serializers.URLField()

class _HousingOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Housing
        fields = ('id', 'name', 'airbnb_url', 'website_task_id')

class HousingListApi(APIView):
    def get(self, request):
        housings = get_housing_list()
        return Response(_HousingOutputSerializer(housings, many=True).data)

class HousingCreateApi(APIView):
    def post(self, request):
        serializer = _HousingInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        housing = create_housing(user=request.user, **serializer.validated_data)
        return Response(data=_HousingOutputSerializer(housing).data, status=status.HTTP_201_CREATED)

class HousingDetailApi(APIView):
    def get(self, request, housing_id):
        housing = get_housing(housing_id=housing_id)
        return Response(_HousingOutputSerializer(housing).data)

class HousingUpdateApi(APIView):
    def post(self, request, housing_id):
        serializer = _HousingInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        update_housing(housing_id=housing_id, **serializer.validated_data)
        return Response(status=status.HTTP_200_OK)

class HousingDeleteApi(APIView):
    def post(self, request, housing_id):
        delete_housing(housing_id=housing_id)
        return Response(status=status.HTTP_200_OK)
