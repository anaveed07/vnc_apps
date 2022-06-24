#!/usr/bin/python

import sys, os
import traceback

from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
import json
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
# import web
from django.shortcuts import render
from .vnc_settings import *
import commands
# from din_novnc_remote_console import DinNovncRemoteConsole

from .din_novnc_remote_console import DinNovncRemoteConsole
#from dinvnc.din_novnc import DinNovncRemoteConsole
#import logging

#log = logging.getLogger(__name__)
# from .vnclog import VNCLog
# from .vnclog import logging as log
import logging
log = logging.getLogger('vnc')
#from view import render
#from lib.hash_key import GenerateHash

import simplejson
# from Crypto.Cipher import AES
from wtools2.libs.encryption_utils import encrypt_string, decrypt_string
import base64

# force stdout to stderr
sys.stdout = sys.stderr

# Add local directories to the system path
#include_dirs = [ 'lib' ]
#for dirname in include_dirs:
#  sys.path.append( os.path.dirname(__file__) + '/' + dirname )

# Change to the directory this file is located in
#os.chdir( os.path.dirname(__file__) )

# Turn on/off debugging
# web.config.debug = False

# Import our libraries
from .lib.hash_key import GenerateHash

### Templates
#render = web.template.render('templates', base='base')
# render = web.template.render(TEMPLATE_FOLDER, cache=False)

#urls = (
#  '/connect',  'pconnect',
#  '/auto_vnc', 'vnc'
#  #'/',        'index'
#)

urls = (
  '/index',   'index',
  '/refresh',   'refresh'
)
#'/testae',   'testae',
# app = web.application(urls, globals())

class ParamsClass(object):
    pass

@method_decorator(csrf_exempt, name='dispatch')
class index(View):
    def get(self, request):
        """ run the proxy on port """
        #Verify token
        #then
        
        # input = request.GET
        #Decrypt
        # log.info("Into the get function of the VNC REST")
        try:
            prmt = request.GET.get('prmt')


            drpt_data = decrypt_string(prmt)
            params = dict([part.split('=') for part in drpt_data.split('&')])
            
            prms = ParamsClass()
            for name, value in params.items():
                setattr(prms,  name, value)

            vm_port_number = request.GET.get('port')
            if vm_port_number is None: return
            token = required(prms, 'token')
            if token is None: return
            # vm_db_id = required(prms, 'vm_id')
            # if vm_db_id is None: return
            vm_server = request.GET.get('host')
            if vm_server is None: return
            # vm_name = required(prms, 'vm_name')
            # if vm_name is None: return
            
            fwidth = required(prms, 'fwidth')
            if fwidth is None: return
            fheight = required(prms, 'fheight')
            if fheight is None: return


        except:
            traceback.print_exc()
            # log.debug("input : %s" % input)
            # log.exception("GET Exception occur")
            return render(request, 'azure_console/error.html', {'message': 'There is some issue %s'%(traceback.format_exc(10))})
            # raise web.internalerror()


    def post(self, request):
        """ Start Proxy on appropriate port, Only post data """

        try:
            # prmt = required(input, 'prmt')
            prmt = request.POST.get('prmt')


            drpt_data = decrypt_string(prmt)
            params = dict([part.split('=') for part in drpt_data.split('&')])
            
            prms = ParamsClass()
            for name, value in params.items():
                setattr(prms,  name, value)
                
            vm_port_number = required(prms, 'port')
            if vm_port_number is None: return
            token = required(prms, 'token')
            if token is None: return
            # vm_db_id = required(prms, 'vm_id')
            # if vm_db_id is None: return
            vm_server = required(prms, 'host')
            if vm_server is None: return



            dinvncr = DinNovncRemoteConsole()

            # Now start the fresh thread again
            querystring = dinvncr.din_novnc_remote_console(token=token, serverIP=vm_server, vncPort=vm_port_number)

            print('Query String --->> ', querystring)

            # log.info("Command Output: %s" % querystring)

            object = {}
            server_ip = get_serverip()
            #object['proxy_port'] = novnc_web_port
            object['proxy_port'] = (querystring)
            object['server_ip'] =  server_ip
            object['vnc_url'] =  "http://%s/azure-vnc/index?host=%s&port=%s" % (server_ip, server_ip)
            object['querystring'] =  querystring


            # return simplejson.dumps(object)
            return generic_response(response_body=object, http_status=200)
            #return render.index("dinCloud vnc console", vm_name, vm_port_number, vm_db_id, vm_server)
            # else:
            #     # log.info("Token Verification failed: ")
            #     # log.debug("input : %s" % input)
            #     # log.debug("params : %s" % params)
            #     return generic_response(response_body={'error': traceback.format_exc(10)}, http_status=200)
            #     # return render(request, 'kvm_console/error.html', {'message': 'Auth Failed'})
            #
        except:
            traceback.print_exc()
            # log.debug("input : %s" % input)
            # log.exception("POST Exception occur")
            return generic_response(response_body={'error': traceback.format_exc(10)}, http_status=200)
            # return render(request, 'kvm_console/error.html', {'message': 'There is some issue %s'%(traceback.format_exc(10))})


# Configure HTTP error pages
def unauthorized( message='This page requires proper authorization to view.' ):
  log.info("Wrong URL provided. which don't exist")
  result = { 'title':'401 Authorization Required', 'message':message }
  # return web.unauthorized( render.error( result ) )
# app.unauthorized = unauthorized

def forbidden( message='Access is forbidden to the requested page.' ):
  result = { 'title':'403 Forbidden', 'message':message }
  # return web.forbidden( render.error( result ) )
# app.forbidden = forbidden

def notfound( message='The server cannot find the requested page.' ):
  log.info("Wrong URL provided. which don't exist")
  result = { 'title':'404 Not Found', 'message':message }
  # return web.notfound( render.error( result ) )
# app.notfound = notfound

def internalerror(message='Something went wrong. We will look into it. Please try again later' ):
    log.info(message)
    result = { 'title':'500 internal error', 'message':message }
    #web.ctx.status = '500 internal error'
    #web.header('Content-Type', 'Application/json')
    #return message
    # return web.internalerror( render.error( result ) )
# app.internalerror = internalerror

def required(input, key):
    """
    Require an input parameter
    """
    val = None
    try:
        val = getattr(input, key)
    except AttributeError:
        # web.ctx.status = STATUS_MAP[400]
        return "%s parameter required" % key
    return val

def required2(input, key):
    """
    Require an input parameter
    """
    val = None
    try:
        val = getattr(input, key)
    except AttributeError:
        # web.ctx.status = STATUS_MAP[400]
        return None,"%s parameter required" % key
    return val,"Received"

def get_serverip():
    #cmd = "ifconfig %s | grep inet | grep -v inet6 | cut -d':' -f2 | awk {' print $1 '} | head -n 1" % settings.DIN_SERVER_INTERFACE
    #return commands.getoutput(cmd).split("\n")[1].split()[1][5:]
    #return commands.getoutput(cmd)
    return SERVER_IP


# if __name__ == "__main__":
#     print ("Running")
#     app.run(VNCLog)
# application = app.wsgifunc(VNCLog)


def generic_response(response_body, http_status=200, header_dict={"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "*"}, mime='application/json'):
    msg = json.dumps(response_body, cls=DjangoJSONEncoder)
    resp = HttpResponse(msg, status=http_status, content_type=mime)
    for name, value in header_dict.items():
        resp[name] = value
    return resp
