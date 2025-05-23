"""
URL configuration for PagoNET project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from nomina.views import home
from nomina.views import registro, cerrar_sesion, iniciar_sesion


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='inicio'),  # URL for the home view # URL for the register view
    path('company/', include('nomina.urls',namespace='nomina')), 
    path('registro/', registro, name='registro'),  # URL for the register view
    path('cerrar_sesion/', cerrar_sesion, name='logout'),  # URL for the logout view
    path('iniciar_sesion/', iniciar_sesion, name='login'),  # URL for the login view
    path('nomina/', include('nomina.urls')),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
