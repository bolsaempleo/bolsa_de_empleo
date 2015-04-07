from django.shortcuts import render, render_to_response
from django.views.generic import base
from django.template import RequestContext
from models import *
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives


# Create your views here.
class IndexView(base.View):

    def get(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return: retorna un html de la pagina principal
        """

        return render_to_response("index/index.html",
                                  {"mensaje": ""},
                                  context_instance=RequestContext(request))


class IngresarView(base.View):

    def get(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return: retorna un html de la pagina principal
        """
        usuario = request.user
        print usuario
        if usuario.is_authenticated():
            loginELement = Login.objects.get(pk=usuario.id)
            cuenta = loginELement.id_user
            return render_to_response("index/ingresar.html",
                                      {
                                          "mensaje": "",
                                          "cuenta": cuenta
                                      },
                                      context_instance=RequestContext(request))
        else:
            return render_to_response("index/ingresar.html",
                                      {"mensaje": ""},
                                      context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        """

        :param request: username y un password
        :param args:
        :param kwargs:
        :return:
        """
        datos = request.POST
        print datos
        username = datos['username']
        password = datos['password']
        usuario = authenticate(username = username, password = password)
        print type(usuario)
        if usuario is not None and usuario.is_active:
            login(request,usuario)
            print usuario.id
            loginELement = Login.objects.get(pk=usuario.id)
            cuenta = loginELement.id_user
            return render(request,
                          "index/ingresar.html",
                          {
                              "mensaje": "",
                              "cuenta": cuenta
                          })
        else:
            return render_to_response(request,
                                      "index/index.html",
                                      {"mensaje": "usuario o contrasena incorrecta"})



class RegistroView(base.View):

    def get(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return: retorna un html de la pagina principal
        """
        return render_to_response("index/registrar.html", {"mensaje": ""}, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        """
        :param request:
            tipo_documento; ,
            documento: ,
            contrasena: ,
            correo_electronico: ,
            nombre_completo: ,
            fecha_nacimiento: ,
        :param args:
        :param kwargs:
        :return:
        """
        datos = request.POST
        print datos
        cuenta = Cuentas(nombreusuario= datos['documento'], contrase_a =datos['password'],
                         e_mail=datos['correo_electronico'], fechanacimiento= datos['fecha_nacimiento'],
                         nombreyapellido= datos['nombre_completo'], estado="en espera")
        cuenta.save()
        login = Login.objects.create_user(username=datos['documento'],password=datos['password'])
        login.contrase_a = login.password
        login.id_user =cuenta
        login.email = datos['correo_electronico']
        login.save()
        return render_to_response("index/registrar.html",
                                  {"mensaje": "se ha creado  la cuenta correctamente, porfavor espere a que sea aceptada"},
                                  context_instance=RequestContext(request))



class ContrasenaView(base.View):

    def get(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return: retorna un html de la pagina principal
        """
        return render_to_response("index/contrasena.html", {"mensaje": ""}, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return: retorna un html de la pagina principal
        """
        a = request.POST
        contenido = "este es un mensaje enviado desde django"
        mensaje = EmailMultiAlternatives("Correo, de password olvidado",
                                         contenido,
                                         "notificaciones.bolsadeempleo@gmail.com",
                                         [a['username']])
        mensaje.attach_alternative(contenido,"text/html")
        mensaje.send()
        return render_to_response("index/contrasena.html", {"mensaje": ""}, context_instance=RequestContext(request))

class AdmonView(base.View):

    def get(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return: retorna un html de la pagina principal
        """
        return render_to_response("index/admon.html", {"mensaje": ""}, context_instance=RequestContext(request))


class EmpresaView(base.View):

    def get(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return: retorna un html de la pagina principal
        """
        return render_to_response("index/empresa.html", {"mensaje": ""},context_instance=RequestContext(request))