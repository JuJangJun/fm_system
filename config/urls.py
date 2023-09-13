from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('visualization/', include('visualization.urls')),
    path('attend/', include('attend.urls')),
    path('access/', include('access.urls')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),  # 수연
    path('', include('login.urls'))
]
