from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response

from common.serializers import inline_serializer
from bookings.models import BookingSeason
from bookings.selectors import (
    get_booking_season,
    get_booking_season_list,
)
from bookings.services import (
    create_booking_season,
    update_booking_season,
    delete_booking_season,
)

class _SeasonInputSerializer(serializers.Serializer):
    housing_id = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(max_length=128)
    base_price = serializers.DecimalField(max_digits=7, decimal_places=2)

class _SeasonOutputSerializer(serializers.ModelSerializer):
    housing_id = serializers.PrimaryKeyRelatedField(read_only=True)
    periods = inline_serializer(many=True, fields={
        'id': serializers.IntegerField(),
        'name': serializers.CharField(),
    })

    class Meta:
        model = BookingSeason
        fields = ('housing_id', 'name', 'base_price', 'periods')

class SeasonListApi(APIView):
    def get(self, request):
        seasons = get_booking_season_list()
        return Response(_SeasonOutputSerializer(seasons, many=True).data)

class SeasonCreateApi(APIView):
    def post(self, request):
        serializer = _SeasonInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        create_booking_season(**serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)

class SeasonDetailApi(APIView):
    def get(self, request, season_id):
        season = get_booking_season(season_id=season_id)
        return Response(_SeasonOutputSerializer(season).data)

class SeasonUpdateApi(APIView):
    def post(self, request, season_id):
        serializer = _SeasonInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        update_booking_season(season_id=season_id, **serializer.validated_data)
        return Response(status=status.HTTP_200_OK)

class SeasonDeleteApi(APIView):
    def post(self, request, season_id):
        delete_booking_season(season_id=season_id)
        return Response(status=status.HTTP_200_OK)
