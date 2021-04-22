#Python program to connect to the device and print a basic output

import netmiko
connection=netmiko.ConnectHandler(ip="172.28.160.230", device_type="arista_eos", username="admin", password="Super123")
#print(connection)

print(connection.send_command('show ip int brief'))
print(connection.send_command('show version'))