from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from graphene_file_upload.django import FileUploadGraphQLView
from graphql_jwt.decorators import jwt_cookie

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql', csrf_exempt(jwt_cookie(FileUploadGraphQLView.as_view(graphiql=True)))),
    path('payment/', include('payment.urls')),
    path('authentication/', include('authentication.urls')),
    path('class_payment/', include('class_payment.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
