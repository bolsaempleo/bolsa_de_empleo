from django.shortcuts import render, render_to_response
from django.views.generic import base
from django.template import RequestContext
from models import *
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives
import hashlib
from bolsa_de_empleo.settings import HOST


def generar_codigo(usuario):
    """
    :param usuario:
    :return:
    """
    manejador = hashlib.md5()
    manejador.update(usuario.nombreusuario)
    mensaje = manejador.hexdigest()
    return mensaje


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
            return HttpResponseRedirect('/usuario')
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
            login(request, usuario)
            print usuario.id
            loginELement = Login.objects.get(pk=usuario.id)
            cuenta = loginELement.id_user
            return HttpResponseRedirect('/usuario')
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
        cuenta = Cuentas(nombreusuario=datos['documento'], contrase_a =datos['password'],
                         e_mail=datos['correo_electronico'], fechanacimiento= datos['fecha_nacimiento'],
                         nombreyapellido=datos['nombre_completo'], estado="en espera")
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
        login_element = Login.objects.get(email=a['username'])
        usuario = login_element.id_user
        codigo = generar_codigo(usuario)
        codigo_cambio = CodigoDeCambio.objects.get_or_create(login_id = login_element)[0]
        codigo_cambio.codigo = codigo
        codigo_cambio.save()
        contenido = "Hemos recibido una solicitud de recuperacion de clave, porfavor<br>" \
                    "accede al siguiente link: <a href='"+HOST+"/recuperar/"+codigo+"'>Recuperar clave.</a>"
        print contenido
        mensaje = EmailMultiAlternatives("Correo de clave olvidado",
                                         contenido,
                                         "notificaciones.bolsadeempleo@gmail.com",
                                         [a['username']])
        mensaje.attach_alternative(contenido, "text/html")
        mensaje.send()
        return render_to_response("index/contrasena.html", {"mensaje": "Se ah enviado un mensaje al correo suministado"},
                                  context_instance=RequestContext(request))


class AdmonView(base.View):

    def get(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return: retorna un html de la pagina principal
        """
        if request.user.is_authenticated():
            usuarios = Cuentas.objects.exclude(pk=request.user.id).exclude(pk__in = Perfiles.objects.all().values('id_user'))
            return render_to_response("index/admon.html", {"mensaje": "", "usuarios": usuarios}, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect("/")

    def post(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        usuario = Cuentas.objects.get(pk=request.POST['id_user'])
        if request.POST['aceptacion'] == "aprobado":
            usuario.deleted = False
        elif request.POST['aceptacion'] == "rechazado":
            usuario.deleted = True
        perfil = request.POST['perfil']
        nuevoPerfil= Perfiles.objects.get_or_create(id_user=usuario, perfil=perfil)[0]
        nuevoPerfil.save()
        return HttpResponse("success")


class EmpresaView(base.View):

    def get(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return: retorna un html de la pagina principal
        """
        return render_to_response("index/empresa.html", {"mensaje": ""},context_instance=RequestContext(request))


class UsuarioView(base.View):

    def get(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return: retorna un html de la pagina principal
        """
        return render_to_response("index/usuario.html", {"mensaje": ""}, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return: retorna un html de la pagina principal
        """
        datos = request.POST
        print datos
        if datos['modulo'] == 'empresa':
            return HttpResponseRedirect('/empresa')
        elif datos['modulo'] =='ciudadano':
            return HttpResponseRedirect('/ciudadano')
        elif datos['modulo'] =='funcionario':
            return HttpResponseRedirect('/empresa')
        elif datos['modulo'] == 'admon':
            return HttpResponseRedirect('/admon')
        else:
            return HttpResponseRedirect('/')


class RecuperarView(base.View):

    def get(self, request, clave=None, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return: retorna un html de la pagina principal
        """
        print("clave")
        print(clave)
        return render_to_response("index/recuperar.html", {"mensaje": ""}, context_instance=RequestContext(request))

    def post(self, request, clave=None, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return: retorna un html de la pagina principal
        """
        datos = request.POST
        mensaje = None
        error = None
        password_1 = datos['password_1']
        password_2 = datos['password_2']
        if password_1 != password_2:
            error = True
            mensaje = "Las dos claves son distintas porfavor escriba dos claves iguales"
        else:
            codigo_dcambio = CodigoDeCambio.objects.get(codigo=clave)
            login_element = codigo_dcambio.login_id
            login_element.set_password(password_1)
            login_element.save()
            contenido = "Se ha cambiado tu clave con exito"
            mensaje = EmailMultiAlternatives("Clave cambiada",
                                             contenido,
                                             "notificaciones.bolsadeempleo@gmail.com",
                                             [login_element.email])
            mensaje.attach_alternative(contenido, "text/html")
            mensaje.send()
            mensaje = "Se ha cambiado laa clave con exito"
        return render_to_response("index/recuperar.html", {"mensaje": mensaje, "error": error}, context_instance=RequestContext(request))