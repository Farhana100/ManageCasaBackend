from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('', include('user.urls')),
    path('', include('apartment.urls')),
    path('', include('election.urls')),
    path('', include('serviceProvider.urls')),
    path('', include('poll.urls')),
    path('', include('finance.urls')),
    path('admin/', admin.site.urls),

    # auth token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)