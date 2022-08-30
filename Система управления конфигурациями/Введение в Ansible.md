# Домашнее задание к занятию "10.01 Введение в Ansible"


## Подготовка к выполнению

1) Установите ansible версии 2.10 или выше.
```
premiumq@TOP:~$ ansible --version
ansible [core 2.12.5]
  python version = 3.8.10 (default, Mar 15 2022, 12:22:08) [GCC 9.4.0]
  jinja version = 2.10.1

```
2) Создайте свой собственный публичный репозиторий на github с произвольным именем.
3) Скачайте playbook из репозитория с домашним заданием и перенесите его в свой репозиторий.

## Основная часть

1) Попробуйте запустить playbook на окружении из test.yml, зафиксируйте какое значение имеет факт some_fact для указанного хоста при выполнении playbook'a.
```
premiumq@TOP:/opt/ansible/playbook$ ansible-playbook site.yml -i inventory/test.yml

PLAY [Print os facts] **************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [localhost]

TASK [Print OS] ********************************************************************************************************
ok: [localhost] => {
    "msg": "Ubuntu"
}

TASK [Print fact] ******************************************************************************************************
ok: [localhost] => {
    "msg": 12
}

PLAY RECAP *************************************************************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
2) Найдите файл с переменными (group_vars) в котором задаётся найденное в первом пункте значение и поменяйте его на 'all default fact'.
```
premiumq@TOP:/opt/ansible/playbook/group_vars/all$ cat examp.yml
---
  some_fact: "all default fact"
```
3) Воспользуйтесь подготовленным (используется docker) или создайте собственное окружение для проведения дальнейших испытаний.
4) Проведите запуск playbook на окружении из prod.yml. Зафиксируйте полученные значения some_fact для каждого из managed host.
```
premiumq@TOP:/opt/ansible/playbook$ ansible-playbook site.yml -i inventory/prod.yml

PLAY [Print os facts] **************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] ********************************************************************************************************
ok: [centos7] => {
    "msg": "Ubuntu"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}

TASK [Print fact] ******************************************************************************************************
ok: [centos7] => {
    "msg": "el"
}
ok: [ubuntu] => {
    "msg": "deb"
}

PLAY RECAP *************************************************************************************************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
5) Добавьте факты в group_vars каждой из групп хостов так, чтобы для some_fact получились следующие значения: для deb - 'deb default fact', для el - 'el default fact'.
```
premiumq@TOP:/opt/ansible/playbook/group_vars$ cat deb/examp.yml
---
  some_fact: "deb default fact"
premiumq@TOP:/opt/ansible/playbook/group_vars$ cat el/examp.yml
---
  some_fact: "el default fact"
```
6) Повторите запуск playbook на окружении prod.yml. Убедитесь, что выдаются корректные значения для всех хостов.
```
premiumq@TOP:/opt/ansible/playbook$ ansible-playbook site.yml -i inventory/prod.yml

PLAY [Print os facts] **************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] ********************************************************************************************************
ok: [centos7] => {
    "msg": "Ubuntu"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}

TASK [Print fact] ******************************************************************************************************
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}

PLAY RECAP *************************************************************************************************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
7) При помощи ansible-vault зашифруйте факты в group_vars/deb и group_vars/el с паролем netology.
```
premiumq@TOP:/opt/ansible/playbook/group_vars$ sudo cat deb/examp.yml
$ANSIBLE_VAULT;1.1;AES256
32363830646263376633303562306131316233313736643431653464393164376565323639616638
3565613538386336613134316136636163613635373438330a656635353330353739333835643238
31663761383662336365656663656331626165663334353962326561353166613833366365616564
6433396366306663310a316365303936336438376233653864326363383566636665366137666461
36346338353866633765383566376238336636613135393336373534346166336630383933653965
3931373433633738333864383538653361363431663931663134
premiumq@TOP:/opt/ansible/playbook/group_vars$ sudo cat el/examp.yml
$ANSIBLE_VAULT;1.1;AES256
38343338323633623932663364616435306137316164356133373262303566396334313036386535
6237666364616431356132633863623932346438383638350a333639313338623633653931333431
30303062623966333064383566646364333733633539626239633362393333383366316539343030
6135383464386537300a393930313933396665323963653934663066363331633264356362356333
38383338363037303063616234663332383534626361386430626435323833613035336161623061
3834373233346433396361663935386531383539643863393962
```
8) Запустите playbook на окружении prod.yml. При запуске ansible должен запросить у вас пароль. Убедитесь в работоспособности.
```
premiumq@TOP:/opt/ansible/playbook$ sudo ansible-playbook site.yml -i inventory/prod.yml --ask-vault-pass
Vault password:

PLAY [Print os facts] **************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [centos7]
ok: [ubuntu]

TASK [Print OS] ********************************************************************************************************
ok: [centos7] => {
    "msg": "Ubuntu"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}

TASK [Print fact] ******************************************************************************************************
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}

PLAY RECAP *************************************************************************************************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
9) Посмотрите при помощи ansible-doc список плагинов для подключения. Выберите подходящий для работы на control node.
```
local
```
10) В prod.yml добавьте новую группу хостов с именем local, в ней разместите localhost с необходимым типом подключения.
```
premiumq@TOP:/opt/ansible/playbook/inventory$ cat prod.yml
---
  el:
    hosts:
      centos7:
        ansible_connection: docker
  deb:
    hosts:
      ubuntu:
        ansible_connection: docker
  local:
    hosts:
      ubuntu:
        ansible_connection: local
```
11) Запустите playbook на окружении prod.yml. При запуске ansible должен запросить у вас пароль. Убедитесь что факты some_fact для каждого из хостов определены из верных group_vars.
```
premiumq@TOP:/opt/ansible/playbook$ sudo ansible-playbook site.yml -i inventory/prod.yml --ask-vault-pass
Vault password:

PLAY [Print os facts] **************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [localhost]
ok: [centos7]
ok: [ubuntu]

TASK [Print OS] ********************************************************************************************************
ok: [centos7] => {
    "msg": "Ubuntu"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}
ok: [localhost] => {
    "msg": "Ubuntu"
}

TASK [Print fact] ******************************************************************************************************
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}
ok: [localhost] => {
    "msg": "all default fact"
}

PLAY RECAP *************************************************************************************************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
12) Заполните README.md ответами на вопросы. Сделайте git push в ветку master. В ответе отправьте ссылку на ваш открытый репозиторий с изменённым playbook и заполненным README.md.

<code>[Answers%20to%20question%2010.01](img/Answers%20to%20question%2010.01.md)
</code>

## Необязательная часть

1) При помощи ansible-vault расшифруйте все зашифрованные файлы с переменными.
```
premiumq@TOP:/opt/ansible/playbook$ sudo cat group_vars/deb/examp.yml
---
  some_fact: "deb default fact"
premiumq@TOP:/opt/ansible/playbook$ sudo cat group_vars/el/examp.yml
---
  some_fact: "el default fact"
```
2) Зашифруйте отдельное значение PaSSw0rd для переменной some_fact паролем netology. Добавьте полученное значение в group_vars/all/exmp.yml.
```
premiumq@TOP:/opt/ansible/playbook/group_vars/all$ ansible-vault encrypt_string PaSSw0rd
New Vault password:
Confirm New Vault password:
!vault |
          $ANSIBLE_VAULT;1.1;AES256
          35666133653930313565303937393734333530636464303630633961376361343166356164636537
          3330646634393966646439313161633733323938383535640a343830323537393964316263636666
          64313439633932626262646362613936323931633064346531616239383563393237363334666466
          3861326530306134360a373664636663613963313366653565363564333030346665346165376162
          3964
premiumq@TOP:/opt/ansible/playbook/group_vars/all$ cat examp.yml
---
  some_fact: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          35666133653930313565303937393734333530636464303630633961376361343166356164636537
          3330646634393966646439313161633733323938383535640a343830323537393964316263636666
          64313439633932626262646362613936323931633064346531616239383563393237363334666466
          3861326530306134360a373664636663613963313366653565363564333030346665346165376162
          3964
```
3) Запустите playbook, убедитесь, что для нужных хостов применился новый fact.
```
premiumq@TOP:/opt/ansible/playbook$ sudo ansible-playbook site.yml -i inventory/prod.yml --ask-vault-pass
Vault password:

PLAY [Print os facts] **************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [localhost]
ok: [centos7]
ok: [ubuntu]

TASK [Print OS] ********************************************************************************************************
ok: [centos7] => {
    "msg": "Ubuntu"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}
ok: [localhost] => {
    "msg": "Ubuntu"
}

TASK [Print fact] ******************************************************************************************************
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}
ok: [localhost] => {
    "msg": "PaSSw0rd"
}

PLAY RECAP *************************************************************************************************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
4) Добавьте новую группу хостов fedora, самостоятельно придумайте для неё переменную. В качестве образа можно использовать этот.
```
premiumq@TOP:/opt/ansible/playbook$ sudo ansible-playbook site.yml -i inventory/prod.yml --ask-vault-pass
Vault password:

PLAY [Print os facts] **************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [localhost]
ok: [fedora]
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] ********************************************************************************************************
ok: [centos7] => {
    "msg": "Ubuntu"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}
ok: [localhost] => {
    "msg": "Ubuntu"
}
ok: [fedora] => {
    "msg": "Ubuntu"
}

TASK [Print fact] ******************************************************************************************************
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}
ok: [fedora] => {
    "msg": "fed default fact"
}
ok: [localhost] => {
    "msg": "PaSSw0rd"
}

PLAY RECAP *************************************************************************************************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
fedora                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
5) Напишите скрипт на bash: автоматизируйте поднятие необходимых контейнеров, запуск ansible-playbook и остановку контейнеров.
```
#!/usr/local/env bash
docker-compose up -d
sudo ansible-playbook site.yml -i inventory/prod.yml --ask-vault-pass netology
docker-compose down
```
6) Все изменения должны быть зафиксированы и отправлены в вашей личный репозиторий.

