# Домашнее задание к занятию "6.4. PostgreSQL"


## Обязательная задача 1

Используя docker поднимите инстанс PostgreSQL (версию 13). Данные БД сохраните в volume.

```
vagrant@server1:~$ docker ps
CONTAINER ID   IMAGE         COMMAND                  CREATED         STATUS         PORTS
         NAMES
0841054b59f3   postgres:13   "docker-entrypoint.s…"   4 seconds ago   Up 4 seconds   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   postgresql-docker
```

Подключитесь к БД PostgreSQL используя psql.

```
vagrant@server1:~$ docker exec -it postgresql-docker bash
root@0841054b59f3:/# psql -U postgres
psql (13.6 (Debian 13.6-1.pgdg110+1))
Type "help" for help.

postgres=#
```

Воспользуйтесь командой \? для вывода подсказки по имеющимся в psql управляющим командам.

Найдите и приведите управляющие команды для:

 - вывода списка БД
```
postgres=# \l+
                                                                   List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges   |  Size   | Tablespace |
   Description
-----------+----------+----------+------------+------------+-----------------------+---------+------------+-------------
-------------------------------
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 |                       | 7901 kB | pg_default | default admi
nistrative connection database
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +| 7753 kB | pg_default | unmodifiable
 empty database
           |          |          |            |            | postgres=CTc/postgres |         |            |
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +| 7753 kB | pg_default | default temp
late for new databases
           |          |          |            |            | postgres=CTc/postgres |         |            |
(3 rows)
```
 - подключения к БД
```
postgres=# \conninfo
You are connected to database "postgres" as user "postgres" via socket in "/var/run/postgresql" at port "5432".
```
 - вывода списка таблиц
```
postgres=# \dtS+
                                        List of relations
   Schema   |          Name           | Type  |  Owner   | Persistence |    Size    | Description
------------+-------------------------+-------+----------+-------------+------------+-------------
 pg_catalog | pg_aggregate            | table | postgres | permanent   | 56 kB      |
 pg_catalog | pg_am                   | table | postgres | permanent   | 40 kB      |
 pg_catalog | pg_amop                 | table | postgres | permanent   | 80 kB      |
 pg_catalog | pg_amproc               | table | postgres | permanent   | 64 kB      |
 pg_catalog | pg_attrdef              | table | postgres | permanent   | 8192 bytes |
 pg_catalog | pg_attribute            | table | postgres | permanent   | 456 kB     |
```
 - вывода описания содержимого таблиц
```
postgres=# \dS+
                                            List of relations
   Schema   |              Name               | Type  |  Owner   | Persistence |    Size    | Description
------------+---------------------------------+-------+----------+-------------+------------+-------------
 pg_catalog | pg_aggregate                    | table | postgres | permanent   | 56 kB      |
 pg_catalog | pg_am                           | table | postgres | permanent   | 40 kB      |
 pg_catalog | pg_amop                         | table | postgres | permanent   | 80 kB      |
 pg_catalog | pg_amproc                       | table | postgres | permanent   | 64 kB      |
 pg_catalog | pg_attrdef                      | table | postgres | permanent   | 8192 bytes |
```
 - выхода из psql
```
postgres=# \q
root@0841054b59f3:/#
```

## Обязательная задача 2

Используя psql создайте БД test_database.

```
postgres=# CREATE DATABASE test_database;
CREATE DATABASE
```

Изучите бэкап БД.

Восстановите бэкап БД в test_database.
```
vagrant@server1:~$ docker exec -it postgresql-docker bash
root@0841054b59f3:/# psql -U postgres -f /tmp/test_dump.sql  test_database
SET
SET
SET
SET
SET
 set_config
------------

(1 row)

SET
SET
SET
SET
SET
SET
CREATE TABLE
ALTER TABLE
CREATE SEQUENCE
ALTER TABLE
ALTER SEQUENCE
ALTER TABLE
COPY 8
 setval
--------
      8
(1 row)

ALTER TABLE
```

Перейдите в управляющую консоль psql внутри контейнера.
```
root@0841054b59f3:/# psql -U postgres
psql (13.6 (Debian 13.6-1.pgdg110+1))
Type "help" for help.
```

Подключитесь к восстановленной БД и проведите операцию ANALYZE для сбора статистики по таблице.
```
postgres=# \c test_database
You are now connected to database "test_database" as user "postgres".
test_database=# \dt
         List of relations
 Schema |  Name  | Type  |  Owner
--------+--------+-------+----------
 public | orders | table | postgres
(1 row)

test_database=# ANALYZE VERBOSE public.orders;
INFO:  analyzing "public.orders"
INFO:  "orders": scanned 1 of 1 pages, containing 8 live rows and 0 dead rows; 8 rows in sample, 8 estimated total rows
ANALYZE
```

Используя таблицу pg_stats, найдите столбец таблицы orders с наибольшим средним значением размера элементов в байтах.
```
test_database=# SELECT avg_width FROM pg_stats WHERE tablename='orders';
 avg_width
-----------
         4
        16
         4
(3 rows)
```

Приведите в ответе команду, которую вы использовали для вычисления и полученный результат.

```
test_database=# SELECT attname, avg_width FROM pg_stats WHERE tablename = 'orders' order by avg_width desc limit 1;
 attname | avg_width
---------+-----------
 title   |        16
(1 row)
```

## Обязательная задача 3

Архитектор и администратор БД выяснили, что ваша таблица orders разрослась до невиданных размеров и поиск по ней занимает долгое время. Вам, как успешному выпускнику курсов DevOps в нетологии предложили провести разбиение таблицы на 2 (шардировать на orders_1 - price>499 и orders_2 - price<=499).

Предложите SQL-транзакцию для проведения данной операции.

```
test_database=# CREATE TABLE orders_more_499_price (CHECK (price > 499)) INHERITS (orders);
CREATE TABLE
test_database=# INSERT INTO orders_more_499_price SELECT * FROM orders WHERE price > 499;
INSERT 0 3
test_database=# CREATE TABLE orders_less_499_price (CHECK (price <= 499)) INHERITS (orders);
CREATE TABLE
test_database=# INSERT INTO orders_LESS_499_price SELECT * FROM orders WHERE price <= 499;
INSERT 0 5
test_database=# DELETE FROM ONLY orders;
DELETE 8
test_database=# \dt
                 List of relations
 Schema |         Name          | Type  |  Owner
--------+-----------------------+-------+----------
 public | orders                | table | postgres
 public | orders_less_499_price | table | postgres
 public | orders_more_499_price | table | postgres
(3 rows)
```

Можно ли было изначально исключить "ручное" разбиение при проектировании таблицы orders?

```
CREATE RULE orders_insert_to_more AS ON INSERT TO orders WHERE ( price > 499 ) DO INSTEAD INSERT INTO orders_more_499_price VALUES (NEW.*);
CREATE RULE orders_insert_to_less AS ON INSERT TO orders WHERE ( price <= 499 ) DO INSTEAD INSERT INTO orders_less_499_price VALUES (NEW.*);
```

## Обязательная задача 4

Используя утилиту pg_dump создайте бекап БД test_database.

```
export PGPASSWORD=netology && pg_dump -h localhost -U postgres test_database > /tmp/test_database_backup.sql
```

Как бы вы доработали бэкап-файл, чтобы добавить уникальность значения столбца title для таблиц test_database?

Добавить свойство UNIQUE

```
title character varying(80) NOT NULL UNIQUE,
```

