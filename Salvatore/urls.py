"""Salvatore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# from django.conf.urls import url
# # from django.contrib import admin
#
# urlpatterns = [
#     # url(r'^admin/', admin.site.urls),
# ]
from django.conf.urls import url
from django.http import HttpResponse
from django.shortcuts import redirect
favicon=lambda request:redirect('/static/upload/favicon.ico')
def addressroute(request,**kwargs):
    app =  kwargs.get('app',None)
    function = kwargs.get('function',None)
    if app and function:
        try:
            appObj = __import__("%s.views" %app)
            viewObj = getattr(appObj, 'views')
            funcObj = getattr(viewObj, function)
        except:
            return HttpResponse('404 Not Found1')
        else:
            return funcObj(request)
    elif app:
        try:
            appObj = __import__("silas.views")
            viewObj = getattr(appObj, 'views')
            funcObj = getattr(viewObj, app)
        except:
            return HttpResponse('404 Not Found2')
        else:
            return funcObj(request)
    else:
        try:
            appObj = __import__("silas.views")
            viewObj = getattr(appObj, 'views')
            funcObj = getattr(viewObj, 'index')
        except:
            return HttpResponse('404 Not Found3')
        else:
            return funcObj(request)

urlpatterns = [
    url(r'^favicon\.ico$',favicon),
    #url(r'^epsoftadmin/', admin.site.urls),
    url(r'^(?P<app>(\w+))/(?P<function>(\w+))/$', addressroute),
    url(r'^(?P<app>(\w+))/$', addressroute),
    url(r'^$', addressroute),
]