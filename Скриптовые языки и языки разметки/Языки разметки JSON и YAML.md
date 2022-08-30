# Домашнее задание к занятию "4.3. Языки разметки JSON и YAML"


## Обязательная задача 1
Мы выгрузили JSON, который получили через API запрос к нашему сервису:
```
    { "info" : "Sample JSON output from our service\t",
        "elements" : [                  // отсутствует пробел
            { "name" : "first",
            "type" : "server",
            "ip" : "7175"               // нужно взять в кавычки и перевести в ip адрес. Должно быть 0.0.28.7, но я сомневаюсь что такой ip адрес реален.
            },                          // не хватает запятой
            { "name" : "second",
            "type" : "proxy",
            "ip" : "71.78.22.43"        // не хватает закрывающей кавычки у ip и 71.78.22.43 тоже нужно взять в кавычки, т.к. это строка
            }
        ]
    }
```
  Нужно найти и исправить все ошибки, которые допускает наш сервис

## Обязательная задача 2
В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: `{ "имя сервиса" : "его IP"}`. Формат записи YAML по одному сервису: `- имя сервиса: его IP`. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.

### Ваш скрипт:

```python
import socket
import time
import yaml
import json

hosts = {"drive.google.com": {"ipv4": "192.168.1.1"}, "mail.google.com": {
    "ipv4": "192.168.1.2"}, "google.com": {"ipv4": "192.168.1.3"}}
number = 1
while True:
    try:
        with open('../DZ/ip_json.json', 'w') as config_json, open('../DZ/ip_yaml.yaml', 'w') as config_yaml:
            for host in hosts.keys():
                cur_ip = hosts[host]["ipv4"]
                check_ip = socket.gethostbyname(host)
                if check_ip != cur_ip:
                    print(f"{{\"{host}\":\"{cur_ip}\"}}")
                    json.dump({host: cur_ip}, config_json)
                    yaml.dump([{host: cur_ip}], config_yaml)
                    hosts[host]["ipv4"] = check_ip
                else:
                    print(f"{{\"{host}\":\"{cur_ip}\"}}")
                    json.dump({host: cur_ip}, config_json)
                    yaml.dump([{host: cur_ip}], config_yaml)
        print(f'Цикл {number}-го скрипта завершен.')
        number += 1
        time.sleep(2)
    except:
        print('Сожалею мисье, но что-то сломалось')
        exit()
```

### Вывод скрипта при запуске при тестировании:
```
{"drive.google.com":"142.250.74.46"}
{"mail.google.com":"142.250.74.101"}
{"google.com":"142.250.74.142"}
Цикл 2-го скрипта завершен.
```

### json-файл(ы), который(е) записал ваш скрипт:
```json
{"drive.google.com":"142.250.74.46"}
{"mail.google.com":"142.250.74.101"}
{"google.com":"142.250.74.142"}
```

### yaml-файл(ы), который(е) записал ваш скрипт:
```yaml
- drive.google.com:142.250.74.46
- mail.google.com:142.250.74.101
- google.com:142.250.74.142
```
