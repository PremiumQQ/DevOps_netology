import socket
import time
import yaml
import json


hosts = {"drive.google.com": {"ipv4": "192.168.1.1"}, "mail.google.com": {
    "ipv4": "192.168.1.2"}, "google.com": {"ipv4": "192.168.1.3"}}
number = 1
while True:
    try:
        with open('ip_json.json', 'w') as config_json, open('ip_yaml.yaml', 'w') as config_yaml:
            for host in hosts.keys():
                cur_ip = hosts[host]["ipv4"]
                check_ip = socket.gethostbyname(host)
                if check_ip != cur_ip:
                    print(f"{{\"{host}\":\"{cur_ip}\"}}")
                    json.dump({host: cur_ip}, config_json)
                    yaml.dump([{host:cur_ip}], config_yaml)
                    hosts[host]["ipv4"] = check_ip
                else:
                    print(f"{{\"{host}\":\"{cur_ip}\"}}")
                    json.dump({host: cur_ip}, config_json)
                    yaml.dump([{host:cur_ip}], config_yaml)
        print(f'Цикл {number}-го скрипта завершен.')
        number += 1
        time.sleep(2)
    except:
        print('Сожалею мисье, но что-то сломалось')
        exit()
