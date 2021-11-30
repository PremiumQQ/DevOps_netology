1)  
chdir("/tmp")  
2)  
/usr/share/misc/magic.mgc  
в терминале следующая строчка:  
openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLY) = 3  
3)  
В вопросе описывается зомби процесс.  
Создал фейковый зомби процесс, скомилировал и запустил скрипт. Удалил процесс, зомби процесс остался висеть.  
vagrant@vagrant:~$ lsof -nP | grep '(deleted)'  
zombie    6524                       vagrant  txt       REG              253,0    16784     131099 /home/vagrant/zombie (deleted)  
Попробовал просто убить процесс, получилось:  
vagrant@vagrant:~$ kill -KILL 6524  
Попробовал удалить через перенаправление:  
Создал второй дистркутор и перенаправил его:  
vagrant@vagrant:~$ bash 1>&2  
Перенаправил зомби процесс во второй дискриптор:  
vagrant@vagrant:~$ >/proc/6524/fd/2  
И убил второй дискриптор.  
4)   
Зомби процессы освобожают свои ресурсы, но висят в таблице процессов.
5)  
vagrant@vagrant:~$ sudo -i  
root@vagrant:~# root@vagrant:~# dpkg -L bpfcc-tools | grep sbin/opensnoop  
n/opensnoop-bpfcc-bash: root@vagrant:~#: command not found  
root@vagrant:~# /usr/sbin/opensnoop-bpfcc  
PID    COMM               FD ERR PATH  
878    vminfo              4   0 /var/run/utmp  
625    dbus-daemon        -1   2 /usr/local/share/dbus-1/system-services  
625    dbus-daemon        36   0 /usr/share/dbus-1/system-services  
625    dbus-daemon        -1   2 /lib/dbus-1/system-services  
625    dbus-daemon        36   0 /var/lib/snapd/dbus-1/system-services/  

6)   
vagrant@vagrant:~$ man 2 uname
в NOTES:
 Part of the utsname information is also accessible  via  /proc/sys/ker‐
       nel/{ostype, hostname, osrelease, version, domainname}.

7)  
;  - разделитель последовательных команд. Т.е. в первом случае отработала первая команда, потом вторая.  
&& - условный оператор (и / или). В данном случае отработала первая команда успешно, поэтому вторая даже не запускалась.  
set -e - прерывает сессию при любом успешном выполнении команды, кроме последней, думаю что вместо && вполне можно использовать, вывод должен быть одинаков.   

8)  
-e Немедленный выход, если команда завершается с ненулевым статусом  
-u При подстановке обрабатывать неустановленные переменные как ошибку  
-x Печатать команды и их аргументы по мере их выполнения.  
-o pipefail возвращаемое значение конвейера - это статус последней команды для выхода с ненулевым статусом или ноль, если ни одна команда не вышла с ненулевым статусом  
Эта команда хорошо будет смотреться в логировании (детализации вывода ошибок).  

9)  
D непрерывный сон (обычно IO)
Неактивный поток ядра
R работает или запускается (в очереди выполнения)
S прерывистый сон (ожидание завершения события)
T остановлен сигналом управления заданием
t остановлен отладчиком во время трассировки
W-подкачка (не действует с ядра 2.6.xx)
X мертв (никогда не должен быть замечен)
Z несуществующий ("зомби") процесс, завершенный, но не полученный его родителем

Допполнрительные символы это характеристики процессов, определающие их приоритет.