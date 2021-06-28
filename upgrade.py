#upgrade the switch using Netmiko

import netmiko
import time
import re
from datetime import datetime
import sys
import traceback
import logging



class SwitchUpgrade():
    #connect to a switch
    def connection():
        #logging the output of the program
        logging.basicConfig(filename='test.log', level=logging.DEBUG)
        logger = logging.getLogger("netmiko")

        mgmt_ip=input('Enter the mgmt IP of the switch: ')
        user=input('Enter the switch username: ')
        pswrd=input('Enter the switch password: ')
        connection= netmiko.ConnectHandler(ip=mgmt_ip,device_type='arista_eos',username=user,password=pswrd,fast_cli=False)
        print('\nConnection Successful \n')
        return connection
    #Action on switch
    def outputs(connection):
        try: 
            version=connection.send_command('show version',expect_string=r'#')
            print(version)
            dir_op=connection.send_command('dir',expect_string=r'#')
            image=input('Input the image in 4.x.xF/M format: ')
            eos_image='EOS-'+image+'.swi'
            print('\nUpgrading to '+eos_image+'\n')


            #check if the imgae is already present in the flash
            if eos_image in dir_op:
                connection.send_command('no prompt %H...%D{%H:%M:%S}%v%P',expect_string=r'#')
                connection.send_command('configure terminal',expect_string=r'#')
                connection.send_command_timing('boot system flash:'+eos_image,delay_factor=2)
                connection.send_command('prompt %H...%D{%H:%M:%S}%v%P',expect_string=r'#')

            else:
                start_time=datetime.now()
                cmnd=('getimage '+image)
                output =connection.send_command(cmnd,delay_factor=2,expect_string=r'reload')
                #time.sleep(180)
                connection.send_command('no prompt %H...%D{%H:%M:%S}%v%P',expect_string=r'#')
                connection.send_command('configure terminal',expect_string=r'#')
                connection.send_command_timing('boot system flash:'+eos_image,delay_factor=2)
                connection.send_command('prompt %H...%D{%H:%M:%S}%v%P',expect_string=r'#')


            #check status and reload
            output =connection.send_command('show boot-config',expect_string=r'#')
            print(output)
            confirm=input('Is boot-config looks good, do you want to reload? Enter Yes/No: ')
            if confirm=='Yes'.lower():
                connection.send_command('reload now')
                quit()

            else:
                print('You dont want to reboot, that is fine, connection will be closed')
            
            connection.disconnect()

        except Exception as e:
            print(e)
            #print(traceback.print_exception(*exc_info))
            connection.disconnect()



def main():

    connect=SwitchUpgrade.connection()
    outputs=SwitchUpgrade.outputs(connect)


if __name__=='__main__':
    main()


