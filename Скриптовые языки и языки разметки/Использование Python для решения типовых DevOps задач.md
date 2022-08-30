# Домашнее задание к занятию "4.2. Использование Python для решения типовых DevOps задач"

## Обязательная задача 1

Есть скрипт:
```python
#!/usr/bin/env python3
a = 1
b = '2'
c = a + b
```

### Вопросы:
| Вопрос  | Ответ |
| ------------- | ------------- |
| Какое значение будет присвоено переменной `c`?  | TypeError: unsupported operand type(s) for +: 'int' and 'str'. Python не понимает переменная это строка или число. |
| Как получить для переменной `c` значение 12?  | c = (str(a) + str(b)), либо реализовать через int c помощью умножений и сложений.  |
| Как получить для переменной `c` значение 3?  | c = (int (a) + int (b))  |

## Обязательная задача 2
Мы устроились на работу в компанию, где раньше уже был DevOps Engineer. Он написал скрипт, позволяющий узнать, какие файлы модифицированы в репозитории, относительно локальных изменений. Этим скриптом недовольно начальство, потому что в его выводе есть не все изменённые файлы, а также непонятен полный путь к директории, где они находятся. Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?

```python
#!/usr/bin/env python3

import os

bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
        break
```

### Ваш скрипт:

```python
#!/usr/bin/env python3

import os

director = "~/netology/sysadm-homeworks"
bash_command = [f"cd {director}", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('modified:', director)
        print(prepare_result)
```

### Вывод скрипта при запуске при тестировании:
```
vagrant@vagrant:~$ python pyt.py
        ~/netology/sysadm-homeworks   README.md
```

## Обязательная задача 3
1. Доработать скрипт выше так, чтобы он мог проверять не только локальный репозиторий в текущей директории, а также умел воспринимать путь к репозиторию, который мы передаём как входной параметр. Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями.

### Ваш скрипт:

```python
import os
import sys

director = ""
try:
    director = sys.argv[1]
except:
    print("Директория задана не корректно")

if director != "":
    bash_command = [f"cd {director}", "git status "]
    list_dir = os.listdir(director);

    if list_dir.__contains__(".git"):
        result_os = os.popen(' && '.join(bash_command)).read()
        for result in result_os.split('\n'):
            if result.find('modified') != -1:
                prepare_result = result.replace('modified:', director)
                print(prepare_result)
    else:
        print("В директории отсутствуют файлы .git")
```

### Вывод скрипта при запуске при тестировании:
```
vagrant@vagrant:~$ python pyt.py ~/netology/sysadm-homeworks
        ~/netology/sysadm-homeworks   README.md
vagrant@vagrant:~$ python pyt.py /usr
        There is no git repository on the entered path
```

## Обязательная задача 4
1. Наша команда разрабатывает несколько веб-сервисов, доступных по http. Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис. Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS имена. Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, который недоступен для разработчиков. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. Будем считать, что наша разработка реализовала сервисы: `drive.google.com`, `mail.google.com`, `google.com`.

### Ваш скрипт:
```python
import socket
import time

hosts = {"drive.google.com": {"ipv4": "192.168.1.1"}, "mail.google.com": {
    "ipv4": "192.168.1.2"}, "google.com": {"ipv4": "192.168.1.3"}}

with open('host_test.log', 'a') as file:
    while True:
        for host in hosts.keys():
            cur_ip = hosts[host]["ipv4"]
            check_ip = socket.gethostbyname(host)
            if check_ip != cur_ip:
                print(f"""[ERROR] {host} IP mismatch: {cur_ip} {check_ip}""")
                file.writelines(f"[ERROR] {host} IP mismatch: {cur_ip} {check_ip}")
                hosts[host]["ipv4"] = check_ip
            else:
                print(f"""{host} - {cur_ip}""")
                file.writelines(f"""{host} - {cur_ip}""")
        time.sleep(10)
```

### Вывод скрипта при запуске при тестировании:
```
vagrant@vagrant:~$ python test_py.py
[ERROR] drive.google.com IP mismatch: 192.168.0.1 142.250.74.46
[ERROR] mail.google.com IP mismatch: 172.16.0.1 142.250.74.101
[ERROR] google.com IP mismatch: 10.0.0.1 142.250.74.142
drive.google.com - 142.250.74.46
mail.google.com - 142.250.74.101
google.com - 142.250.74.142
```
