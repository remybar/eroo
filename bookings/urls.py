from django.urls import path, include

from bookings.apis.seasons import (
    SeasonCreateApi,
    SeasonUpdateApi,
    SeasonListApi,
    SeasonDetailApi,
    SeasonDeleteApi,
)
from bookings.apis.housings import (
    HousingCreateApi,
    HousingUpdateApi,
    HousingListApi,
    HousingDetailApi,
    HousingDeleteApi,
)

season_patterns = [
    path('', SeasonListApi.as_view(), name='list'),
    path('detail/<int:season_id>/', SeasonDetailApi.as_view(), name='detail'),
    path('create/', SeasonCreateApi.as_view(), name='create'),
    path('update/<int:season_id>/', SeasonUpdateApi.as_view(), name='update'),
    path('delete/<int:season_id>/', SeasonDeleteApi.as_view(), name='delete'),
]

housing_patterns = [
    path('', HousingListApi.as_view(), name='list'),
    path('detail/<int:housing_id>/', HousingDetailApi.as_view(), name='detail'),
    path('create/', HousingCreateApi.as_view(), name='create'),
    path('update/<int:housing_id>/', HousingUpdateApi.as_view(), name='update'),
    path('delete/<int:housing_id>/', HousingDeleteApi.as_view(), name='delete'),
]

app_name = 'bookings'
urlpatterns = [
    path('api/v1/seasons/', include((season_patterns, 'seasons'))),
    path('api/v1/housings/', include((housing_patterns, 'housings'))),
]
