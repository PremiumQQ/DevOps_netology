# Домашнее задание к занятию "6.5. Elasticsearch"


## Обязательная задача 1

В этом задании вы потренируетесь в:

- установке elasticsearch
- первоначальном конфигурировании elastcisearch
- запуске elasticsearch в docker
Используя докер образ centos:7 как базовый и документацию по установке и запуску Elastcisearch:

- составьте Dockerfile-манифест для elasticsearch
- соберите docker-образ и сделайте push в ваш docker.io репозиторий
- запустите контейнер из получившегося образа и выполните запрос пути / c хост-машины
Требования к elasticsearch.yml:

- данные path должны сохраняться в /var/lib
- имя ноды должно быть netology_test

В ответе приведите:

- текст Dockerfile манифеста

```
# Pull base image.
FROM centos:centos7

MAINTAINER Alexander <kvetalex@gmail.com>

ENV ES_PKG_NAME elasticsearch-7.15.2

RUN groupadd -g 1000 elasticsearch && useradd elasticsearch -u 1000 -g 1000

RUN yum makecache && \
    yum -y install wget \
    yum -y install perl-Digest-SHA


# Install Elasticsearch.
RUN \
  cd / && \
  wget https://artifacts.elastic.co/downloads/elasticsearch/$ES_PKG_NAME-linux-x86_64.tar.gz && \
  wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.15.2-linux-x86_64.tar.gz.sha512 && \
  shasum -a 512 -c elasticsearch-7.15.2-linux-x86_64.tar.gz.sha512 && \
  tar -xzf $ES_PKG_NAME-linux-x86_64.tar.gz && \
  rm -f $ES_PKG_NAME-linux-x85_64.tar.gz && \
  mv /$ES_PKG_NAME /elasticsearch

RUN mkdir /var/lib/logs /var/lib/data

COPY elasticsearch.yml /elasticsearch/config

RUN chmod -R 777 /elasticsearch && \
    chmod -R 777 /var/lib/logs && \
    chmod -R 777 /var/lib/data

USER elasticsearch
# Define default command.
CMD ["/elasticsearch/bin/elasticsearch"]

# Expose ports.
#   - 9200: HTTP
#   - 9300: transport
EXPOSE 9200
EXPOSE 9300
```

- ссылку на образ в репозитории dockerhub

https://hub.docker.com/repository/docker/premiumq/elasticsearch

- ответ elasticsearch на запрос пути / в json виде

```json
{
  "name" : "e99ae101ffae",
  "cluster_name" : "netology_test",
  "cluster_uuid" : "itZFlFJ5RMuaA47v8UJu8Q",
  "version" : {
    "number" : "7.15.2",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "93d5a7f6192e8a1a12e154a2b81bf6fa7309da0c",
    "build_date" : "2021-11-04T14:04:42.515624022Z",
    "build_snapshot" : false,
    "lucene_version" : "8.9.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```
Подсказки:

- возможно вам понадобится установка пакета perl-Digest-SHA для корректной работы пакета shasum
- при сетевых проблемах внимательно изучите кластерные и сетевые настройки в elasticsearch.yml
- при некоторых проблемах вам поможет docker директива ulimit
- elasticsearch в логах обычно описывает проблему и пути ее решения
Далее мы будем работать с данным экземпляром elasticsearch.

## Обязательная задача 2

В этом задании вы научитесь:

- создавать и удалять индексы
- изучать состояние кластера
- обосновывать причину деградации доступности данных
Ознакомтесь с документацией и добавьте в elasticsearch 3 индекса, в соответствии со таблицей:

Имя	Количество реплик	Количество шард
ind-1	0	1
ind-2	1	2
ind-3	2	4
Получите список индексов и их статусов, используя API и приведите в ответе на задание.

```
vagrant@server1:~$ curl 'localhost:9200/_cat/indices?v'
health status index            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .geoip_databases UE3bMfOPQ62MTdvkXa5BAw   1   0         41            0     38.8mb         38.8mb
green  open   ind-1            U-cakyDuSUO6ox2mcAlBFA   1   0          0            0       208b           208b
yellow open   ind-3            g9-eiZjlSjijliyfg90ykQ   4   2          0            0       379b           379b
yellow open   ind-2            fio0eSr1SG6ISanNlv5nZw   2   1          0            0       416b           416b
```

Получите состояние кластера elasticsearch, используя API.

```
vagrant@server1:~$ curl -X GET "localhost:9200/_cluster/health?pretty"
{
  "cluster_name" : "netology_test",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 8,
  "active_shards" : 8,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 10,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 44.44444444444444
}
```

Как вы думаете, почему часть индексов и кластер находится в состоянии yellow?

```
Первичный шард и реплика не могут находиться на одном узле, если копия не назначена. 
Поэтому, один узел не может размещать копии.

```

Удалите все индексы.

```
vagrant@server1:~$ curl -X DELETE 'http://localhost:9200/_all'
{"acknowledged":true}
```

Важно

При проектировании кластера elasticsearch нужно корректно рассчитывать количество реплик и шард, иначе возможна потеря данных индексов, вплоть до полной, при деградации системы.

## Обязательная задача 3

В данном задании вы научитесь:

- создавать бэкапы данных
- восстанавливать индексы из бэкапов
Создайте директорию {путь до корневой директории с elasticsearch в образе}/snapshots.
Используя API зарегистрируйте данную директорию как snapshot repository c именем netology_backup.
Приведите в ответе запрос API и результат вызова API для создания репозитория.

```
curl -XPOST localhost:9200/_snapshot/netology_backup?pretty -H 'Content-Type: application/json' -d'{"type": "fs", "settings": { "location":"/elasticsearch/snapshots" }}'
{
  "acknowledged" : true
}
```

Создайте индекс test с 0 реплик и 1 шардом и приведите в ответе список индексов.

```
curl -X PUT "localhost:9200/test?pretty" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  }
}
'
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "test"
}

curl -X GET 'http://localhost:9200/_cat/indices?v' 
health status index            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .geoip_databases es74GYJCWPpcdbU2FsdGVk   1   0         42            0     41.1mb         41.1mb
green  open   test             SC5vtg8MrRqmJ_P7QsdfFf   1   0          0            0       208b           208b
```

Создайте snapshot состояния кластера elasticsearch.

Приведите в ответе список файлов в директории со snapshotами.

```
curl -X PUT localhost:9200/_snapshot/netology_backup/elasticsearch?wait_for_completion=true
{"snapshot":{"snapshot":"elasticsearch","uuid":"ed0U73ORTpylzoL0sKeG4g","repository":"netology_backup","version_id":7150299,"version":"7.15.2","indices":["test",".geoip_databases"],"data_streams":[],"include_global_state":true,"state":"SUCCESS","start_time":"2021-12-09T06:56:12.048Z","start_time_in_millis":1639032972048,"end_time":"2021-12-09T06:56:13.050Z","end_time_in_millis":1639032973050,"duration_in_millis":1002,"failures":[],"shards":{"total":2,"failed":0,"successful":2},"feature_states":[{"feature_name":"geoip","indices":[".geoip_databases"]}]}}


-rw-r--r-- 1 elasticsearch elasticsearch   831 Dec  9 06:56 index-0
-rw-r--r-- 1 elasticsearch elasticsearch     8 Dec  9 06:56 index.latest
drwxr-xr-x 4 elasticsearch elasticsearch  4096 Dec  9 06:56 indices
-rw-r--r-- 1 elasticsearch elasticsearch 27702 Dec  9 06:56 meta-OWrm1emqGA8sm39w4LrTn0.dat
-rw-r--r-- 1 elasticsearch elasticsearch   440 Dec  9 06:56 snap-OWrm1emqGA8sm39w4LrTn0.dat
```

Удалите индекс test и создайте индекс test-2. Приведите в ответе список индексов.

```
curl -X DELETE 'http://localhost:9200/test?pretty'
{
  "acknowledged" : true
}

curl -X PUT "localhost:9200/test-2?pretty" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  }
}
'
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "test-2"
}
curl -X GET 'http://localhost:9200/_cat/indices?v' 
health status index            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .geoip_databases es74GYJCWPpcdbU2FsdGVk   1   0         42            0     41.1mb         41.1mb
green  open   test-2           GxoBACxjSQzvGai9HhYmmZ   1   0          0            0       208b           208b
```

Восстановите состояние кластера elasticsearch из snapshot, созданного ранее.
Приведите в ответе запрос к API восстановления и итоговый список индексов.

```
curl -X POST "localhost:9200/_snapshot/netology_backup/elasticsearch/_restore?pretty" -H 'Content-Type: application/json' -d'
{
  "indices": "test"
}
'
{
  "accepted" : true
}
anantahari@ubuntu:~$ curl -X GET 'http://localhost:9200/_cat/indices?v' 
health status index            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .geoip_databases es74GYJCWPpcdbU2FsdGVk   1   0         42            0     41.1mb         41.1mb
green  open   test-2           GxoBACxjSQzvGai9HhYmmZ   1   0          0            0       208b           208b
green  open   test             1CykHLQy1k6aGxoBACxjSQ   1   0          0            0       208b           208b
```

Подсказки:

- возможно вам понадобится доработать elasticsearch.yml в части директивы path.repo и перезапустить elasticsearch