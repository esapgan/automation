#upgrade the switch using Netmiko

import netmiko
import time

#connect to a switch
connection= netmiko.ConnectHandler(ip='10.81.117.55',device_type='arista_eos',username='admin',password='')

print(connection.send_command('show ip int brief'))
dir_op=connection.send_command('dir')
print(dir_op)
image=input('Input the image in 4.x.x format: ')
#print(image)
eos_image='EOS-'+image+'.swi'
print(eos_image)

#check if the imgae is already present in the flash
if eos_image in dir_op:
    config_commands=['config','boot system flash:'+eos_image]
    #print(config_commands)
    output=connection.send_config_set(config_commands)
    print(output)

else:
    config_commands=['config','getimage '+image]
    print(config_commands)
    connection.send_config_set(config_commands)
    print('Downloading '+eos_image)
    time.sleep(120)
    config_commands=['config','boot system flash:'+eos_image]
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
