import logging
import subprocess as commands
import time
# from dinvnc.exceptions import InvalidArgumentError

# from exceptions import InvalidArgumentError

# from exceptions import InvalidArgumentError


class InvalidArgumentError(Exception):
    pass



log = logging.getLogger(__name__)

NOVNC_WEBSERVER_PORT_RANGE_START=7000
NOVNC_WEBSOCKET_PORT_RANGE_START=8000
# SERVER_IP = "10.253.109.127"
# SERVER_IP = "10.247.109.57"
# SERVER_IP = "10.247.109.52"
SERVER_IP = "console.dincloud.com"
DIN_SERVER_INTERFACE="eth0"
# DIN_BASE_DIR="/var/www/vnc-scripts"
DIN_BASE_DIR="/var/www/wtoolgui/wtools2/apps/vnc_console/azure_vnc"

class DinClass(object):
    pass

class DinNovncRemoteConsole:

    def __init__(self):
        self.web_server_ip = SERVER_IP #self._get_serverip()
        #self.web_server_ip = self._get_serverip()

    def din_novnc_remote_console(self, **kwargs): #server_ip, vnc_port, vm_db_id, vm_name

        dino = DinClass()

        # do some validation checking...
        if (len(kwargs)) < 3:
            raise IndexError('Expected at least 3 arguments got: %d' % len(kwargs))

        required = [ 'token', 'serverIP', 'vncPort']
        # optional = [ 'vmMAC' ]

        for name, value in kwargs.items():
            if name in required:
                setattr(dino,  name, value)
            else:
                raise InvalidArgumentError("Invalid argument: %s.  Expected one of %s" % (name, ", ".join(required )))
        try:
            vnc_websockify_cmd ="{0}/startvnc.sh {1} {2} {3}".format(DIN_BASE_DIR, dino.token, dino.serverIP, dino.vncPort)
            print('Command -->>> ', vnc_websockify_cmd)
            output = commands.getoutput(vnc_websockify_cmd)
            print(output)
            print('OUT PUT from manage-novnc ---->>', output)

            return output
            # time.sleep(2)
        except:
            return "error"

    # def din_novnc_disable_remote_console(self, **kwargs):
    #     dino = DinClass()
    #
    #     # do some validation checking...
    #     if (len(kwargs)) < 4:
    #         raise IndexError('Expected at least 4 arguments got: %d' % len(kwargs))
    #
    #     required = [ 'serverIP', 'vncPort', 'resourceID', 'vmName' ]
    #     optional = [ 'vmMAC' ]
    #
    #     for name, value in kwargs.items():
    #         if name in required + optional:
    #             setattr(dino,  name, value)
    #         else:
    #             raise InvalidArgumentError("Invalid argument: %s.  Expected one of %s" % (name, ", ".join(required + optional)))
    #
    #     vnc_websockify_dis_cmd ="%s/manage-novnc.sh dis-vnc-console -n %s -d %s -i %s -v %s" % (DIN_BASE_DIR, dino.vmName, dino.resourceID, dino.serverIP, dino.vncPort)
    #     dis_output = commands.getoutput(vnc_websockify_dis_cmd)
    #     return dis_output
        
    def _get_serverip(self):
        #cmd = "ifconfig %s" % DIN_SERVER_INTERFACE
        #return commands.getoutput(cmd).split("\n")[1].split()[1][5:]
        cmd = "ifconfig %s | grep inet | grep -v inet6 | cut -d':' -f2 | awk {' print $1 '} | head -n 1" % DIN_SERVER_INTERFACE
        return commands.getoutput(cmd)

#if __name__ == '__main__':
#    din_con = DinNovncRemoteConsole()
#    din_con.din_novnc_remote_console(serverIP='', vncPort='', resourceID='', vmName='')
    
