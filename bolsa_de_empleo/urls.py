from django.conf.urls import patterns, include, url
from django.contrib import admin
from aplicaciones.index.views import IndexView, RegistroView, ContrasenaView, IngresarView, EmpresaView, AdmonView, UsuarioView, RecuperarView




urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bolsa_de_empleo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^/?$', IndexView.as_view(), name="index_url"),
    url(r'^ingresar/?$', IngresarView.as_view(), name="ingresar_url"),
    url(r'^registrar/?$', RegistroView.as_view(), name="registrar_url"),
    url(r'^contrasena/?$', ContrasenaView.as_view(), name="contrasena_url"),
    url(r'^empresa/?$', EmpresaView.as_view(), name="empresa_url"),
    url(r'^admon/?$', AdmonView.as_view(), name="admon_url"),
    url(r'^usuario/?$', UsuarioView.as_view(), name="usuario_url"),
    url(r'^recuperar/(?P<clave>(.)*)/?$', RecuperarView.as_view(), name="recuperar_url"),
)


