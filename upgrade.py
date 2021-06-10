#upgrade the switch using Netmiko

import netmiko
import time
import re
from datetime import datetime

#connect to a switch

class SwitchUpgrade():

    def connection():

        mgmt_ip=input('Enter the mgmt IP of the switch: ')
        user=input('Enter the switch username: ')
        pswrd=input('Enter the switch password: ')
        connection= netmiko.ConnectHandler(ip=mgmt_ip,device_type='arista_eos',username=user,password=pswrd,fast_cli=False)
        print('connection successful')
        return connection

    def outputs(connection):
        try: 
            print(connection.send_command('show version'))
            dir_op=connection.send_command('dir')
            image=input('Input the image in 4.x.xF/M format: ')
            #print(image)
            eos_image='EOS-'+image+'.swi'
            print('Upgrading to '+eos_image)

            #check if the imgae is already present in the flash
            if eos_image in dir_op:
                connection.send_config_set('boot system flash:'+eos_image)

            else:
                start_time=datetime.now()
                cmnd=('getimage '+image)
                #output=connection.send_command(cmnd)
                #time.sleep(180)
                output =connection.send_command(cmnd,delay_factor=5)
                config_commands=['boot system flash:'+eos_image]
                connection.send_config_set(config_commands)

            #check status and reload
            output=connection.send_command('show boot-config')
            print(output)
            confirm=input('Is boot-config looks good, do you want to reload? Enter Yes/No: ')
            if confirm=='Yes':
                connection.send_command('reload now')
            else:
                print('You dont want to reboot, that is fine, connection will be closed')
                connection.disconnect()
        except:
            print('except')
            connection.disconnect()

def main():

    connect=SwitchUpgrade.connection()
    output=SwitchUpgrade.outputs(connect)

if __name__=='__main__':
    main()


