#upgrade the switch using Netmiko

import netmiko
import time
import re
import sys
import traceback
import logging



class CleanFlash():
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
    
    def flash(connection):
        essential_files=['persist', 'scripts', 'schedule', 'startup-config', 'Fossil', 'SsuRestore.log', 'SsuRestoreLegacy.log', 
                            'boot-config', 'boot-extensions', 'debug', 'cron.d', 'rc.d', 'rc.eos']
        try:
            #getting the directory output and getting the filenames in one list
            directory_op=connection.send_command('dir',expect_string=r'#')
            filename=connection.send_command('bash ls /mnt/flash',expect_string=r'#').split('\t')
            op=[item.split(' ') for item in filename]
            #print(op)
            final_list=sum(op,[])
            for i in final_list:
                if i =='':
                    final_list.remove(i)
            
            #check the EOS image from boot-config and keep the image file in the directory
            boot_version=connection.send_command('show boot-config',expect_string=r'#').split()
            version_index=boot_version.index('image:')
            image=boot_version[version_index+1].split('flash:/')
            essential_files.append(image[1])
            #print(essential_files)

            print("WARNING: This script will reset the configuration of this switch and wipe the flash disk of all unnecessary files. \nIt will remove ALL SWI images except the one specified in the boot-config file. \nPlease be sure that this is really what you want to do. \nThis is IRREVERSIBLE!")
            confirm=input("Are you sure Enter Yes/No: ")
            #deleting the rest of the files except Essential files
            if confirm=='Yes'.lower():
                for item in final_list:
                    if item not in essential_files:
                        connection.send_command_timing('delete flash:'+item)
            
            print(connection.send_command('dir',expect_string=r'#'))
            connection.disconnect()

            
        except Exception as e:
            print(e)
            print(traceback.print_exception(*exc_info))
            connection.disconnect()


def main():
    connect=CleanFlash.connection()
    CleanFlash.flash(connect)

if __name__=='__main__':
    main()
