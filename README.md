5) RAM:1024mb  
CPU:1 cpu  
HDD:64gb  
video:8mb  
6) В файле конфигурации добавить 2 строки:  
config.vm.provider "virtualbox" do |vb|  
     vb.memory = "2048"  
     vb.cpu = "4"  
   end  
8) Какой переменной можно задать длину журнала history, и на какой строчке manual это описывается?  
HISTSIZE - влияет на количество команд которые записываюся в истории - строка 630  
HISTFILESIZE - влияет на количество строк записываемых в историю - строка 621  

Значение ignoreboth является сокращением для ignorespace и ignoredups.   
ignorespace - если строка начинается с пробела, она не сохраняется в истории  
ignoredups - если строка дублируется (соответсвует предыдущей записи), она не сохраняется в истории  

9) Используется в списках (строка 206), зарезервированных словах (139 строка)   
10) touch {000001..100000}.txt - создало в директории 100.000 файлов  
на 300.000 файлов вышла ошибка Argument list too long  
11) Возвращает статус 0 или 1 на условие [[ -d /tmp ]]. Если /tmp есть, вернется 1. Если нет, то 0.  
Правда не понял что делает -d, проверка на наличие директории?  
12) mkdir /tmp/new_path_dir/  
cp /bin/bash /tmp/new_path_dir/  
type -a bash  
bash is /tmp/new_path_dir/bash  
bash is /usr/bin/bash  
bash is /bin/bash  
Далее я решил перенести в папку local, чтобы соответствовало заданию bash is /usr/local/bin/bash  
vagrant@vagrant:~$ sudo -i  
root@vagrant:~# ls -all  
root@vagrant:~# cd ..  
root@vagrant:/usr# cd local  
root@vagrant:/usr/local# ls -all  
root@vagrant:/usr/local# cd bin  
root@vagrant:/usr/local/bin# ls -all  
root@vagrant:/usr/local/bin# cp /bin/bash /usr/local/bin/  
root@vagrant:/usr/local/bin# type -a bash  
bash is /tmp/new_path_dir/bash  
bash is /usr/local/bin/bash  
bash is /usr/bin/bash  
bash is /bin/bash  
На выводе появилась лишняя строчка bash is /usr/bin/bash, следуя заданию, попробовал ее удалить  
root@vagrant:/bin# rm -r /usr/bin/bash  
root@vagrant:/bin# type -a bash  
bash is /tmp/new_path_dir/bash  
bash is /usr/local/bin/bash  
Но она удалилась вместе с bash is /bin/bash  
Восстановил ее  
root@vagrant:/bin# cp /usr/local/bin/bash /bin/bash  
root@vagrant:/bin# type -a bash  
bash is /tmp/new_path_dir/bash  
bash is /usr/local/bin/bash  
bash is /usr/bin/bash  
bash is /bin/bash  
После этого не стал дальше экспериментировать, т.к. это системные файлы и как я понял, они взаимозаменяемые  
13)   
at - команда запускается в указанное время (в параметре)  
batch - запускается когда уровень загрузки системы снизится ниже 1.5  
