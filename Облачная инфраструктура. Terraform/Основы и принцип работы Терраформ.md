# Домашнее задание к занятию "7.3. Основы и принцип работы Терраформ"


## Задача 1. Создадим бэкэнд в S3 (необязательно, но крайне желательно).

Если в рамках предыдущего задания у вас уже есть аккаунт AWS, то давайте продолжим знакомство со взаимодействием терраформа и aws.

1) Создайте s3 бакет, iam роль и пользователя от которого будет работать терраформ. Можно создать отдельного пользователя, а можно использовать созданного в рамках предыдущего задания, просто добавьте ему необходимы права, как описано здесь.
2) Зарегистрируйте бэкэнд в терраформ проекте как описано по ссылке выше.

## Задача 2. Инициализируем проект и создаем воркспейсы.

1) Выполните terraform init:
   если был создан бэкэнд в S3, то терраформ создат файл стейтов в S3 и запись в таблице dynamodb.
   иначе будет создан локальный файл со стейтами.
2) Создайте два воркспейса stage и prod.
```
premiumq@TOP:/opt/terraform$ sudo terraform workspace new stage
[sudo] пароль для premiumq:
Created and switched to workspace "stage"!

You're now on a new, empty workspace. Workspaces isolate their state,
so if you run "terraform plan" Terraform will not see any existing state
for this configuration.
premiumq@TOP:/opt/terraform$ sudo terraform workspace new prod
Created and switched to workspace "prod"!

You're now on a new, empty workspace. Workspaces isolate their state,
so if you run "terraform plan" Terraform will not see any existing state
for this configuration.
```
3) В уже созданный aws_instance добавьте зависимость типа инстанса от вокспейса, что бы в разных ворскспейсах использовались разные instance_type.
```
locals {
instance_type = {
    stage = "1"
    prod  = "2"
    }
}
```
```
resource "yandex_compute_instance" "vm-1" {
  name = "terraform1"

  resources {
    cores  = 2
    memory = 2
    core_fraction = local.instance_type[terraform.workspace]
  }
```
4) Добавим count. Для stage должен создаться один экземпляр ec2, а для prod два.
```
locals {
  instance_count = {
    stage = 1
    prod = 2
  }
}
```
```
resource "yandex_compute_instance" "vm-1" {
  name = "terraform1"
   count = local.instance_count[terraform.workspace]
```
5) Создайте рядом еще один aws_instance, но теперь определите их количество при помощи for_each, а не count.
```
locals {
  instance_for_each = {
    stage = 1
    prod  = 2
  }
}
```

6) Что бы при изменении типа инстанса не возникло ситуации, когда не будет ни одного инстанса добавьте параметр жизненного цикла create_before_destroy = true в один из рессурсов aws_instance.
```
  lifecycle {
    create_before_destroy = true
  }
```
7) При желании поэкспериментируйте с другими параметрами и рессурсами.

В виде результата работы пришлите:

Вывод команды terraform workspace list.

```
premiumq@TOP:/opt/terraform$ terraform workspace list
  default
* prod
  stage
```

Вывод команды terraform plan для воркспейса prod.

```
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # yandex_compute_instance.node_for_each["prod"] will be created
  + resource "yandex_compute_instance" "node_for_each" {
      + created_at                = (known after apply)
      + folder_id                 = (known after apply)
      + fqdn                      = (known after apply)
      + hostname                  = (known after apply)
      + id                        = (known after apply)
      + metadata                  = {
          + "ssh-keys" = <<-EOT
                ubuntu:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC/FUOU+m4iae8M0fyOWW/53ziQxpwGEb5LHTGhqlwTQgKvrtM7DmCbVIYFwRAZQuLLYslCe70kZe3aVKe4NsyqSrOwG30LeGjQBADqv8k0nu95oqoHRLXzvvFxyfmv8GJ1K14kibJm+4Pu2FXi+lDY3T9PpPtqolI6XZ7g9Lyuvo4qaBbydtiMlZHvJsVkv6bM+ekeFqSrDD/vSFYyFit5kFo8opg/AvJ7zHBc88fJ5GN8r29PMw35LiiU016R9YHo4+WNQIP53FZwLVGVtmY7PEXdaDo6TWd2qNlOri9kX6F+w14qkT7cadpTS0qL0i283siwXoybJiiVm7WgO+9Sm0wcpLs6mgBxJmNP9fy0hlRsf+K+MaCKQoPVKLrqNYg/EVJcyuGuctgK2g7ZPxsxPUV2tn8dRmgvU8YHh3BDop5V3I9hMATCYaVgycHlMnFpBeXgxofWdJr46KFbp8+yKrdR0kIeP3I/3C873uY4V55TvkXjwsR1BhM3/I44dcc= root@TOP
            EOT
        }
      + name                      = "node02-prod-for_each"
      + network_acceleration_type = "standard"
      + platform_id               = "standard-v1"
      + service_account_id        = (known after apply)
      + status                    = (known after apply)
      + zone                      = (known after apply)

      + boot_disk {
          + auto_delete = true
          + device_name = (known after apply)
          + disk_id     = (known after apply)
          + mode        = (known after apply)

          + initialize_params {
              + block_size  = (known after apply)
              + description = (known after apply)
              + image_id    = "fd87va5cc00gaq2f5qfb"
              + name        = (known after apply)
              + size        = (known after apply)
              + snapshot_id = (known after apply)
              + type        = "network-hdd"
            }
        }

      + network_interface {
          + index              = (known after apply)
          + ip_address         = (known after apply)
          + ipv4               = true
          + ipv6               = (known after apply)
          + ipv6_address       = (known after apply)
          + mac_address        = (known after apply)
          + nat                = true
          + nat_ip_address     = (known after apply)
          + nat_ip_version     = (known after apply)
          + security_group_ids = (known after apply)
          + subnet_id          = (known after apply)
        }

      + placement_policy {
          + host_affinity_rules = (known after apply)
          + placement_group_id  = (known after apply)
        }

      + resources {
          + core_fraction = 2
          + cores         = 2
          + memory        = 2
        }

      + scheduling_policy {
          + preemptible = (known after apply)
        }
    }

  # yandex_compute_instance.node_for_each["stage"] will be created
  + resource "yandex_compute_instance" "node_for_each" {
      + created_at                = (known after apply)
      + folder_id                 = (known after apply)
      + fqdn                      = (known after apply)
      + hostname                  = (known after apply)
      + id                        = (known after apply)
      + metadata                  = {
          + "ssh-keys" = <<-EOT
                ubuntu:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC/FUOU+m4iae8M0fyOWW/53ziQxpwGEb5LHTGhqlwTQgKvrtM7DmCbVIYFwRAZQuLLYslCe70kZe3aVKe4NsyqSrOwG30LeGjQBADqv8k0nu95oqoHRLXzvvFxyfmv8GJ1K14kibJm+4Pu2FXi+lDY3T9PpPtqolI6XZ7g9Lyuvo4qaBbydtiMlZHvJsVkv6bM+ekeFqSrDD/vSFYyFit5kFo8opg/AvJ7zHBc88fJ5GN8r29PMw35LiiU016R9YHo4+WNQIP53FZwLVGVtmY7PEXdaDo6TWd2qNlOri9kX6F+w14qkT7cadpTS0qL0i283siwXoybJiiVm7WgO+9Sm0wcpLs6mgBxJmNP9fy0hlRsf+K+MaCKQoPVKLrqNYg/EVJcyuGuctgK2g7ZPxsxPUV2tn8dRmgvU8YHh3BDop5V3I9hMATCYaVgycHlMnFpBeXgxofWdJr46KFbp8+yKrdR0kIeP3I/3C873uY4V55TvkXjwsR1BhM3/I44dcc= root@TOP
            EOT
        }
      + name                      = "node01-prod-for_each"
      + network_acceleration_type = "standard"
      + platform_id               = "standard-v1"
      + service_account_id        = (known after apply)
      + status                    = (known after apply)
      + zone                      = (known after apply)

      + boot_disk {
          + auto_delete = true
          + device_name = (known after apply)
          + disk_id     = (known after apply)
          + mode        = (known after apply)

          + initialize_params {
              + block_size  = (known after apply)
              + description = (known after apply)
              + image_id    = "fd87va5cc00gaq2f5qfb"
              + name        = (known after apply)
              + size        = (known after apply)
              + snapshot_id = (known after apply)
              + type        = "network-hdd"
            }
        }

      + network_interface {
          + index              = (known after apply)
          + ip_address         = (known after apply)
          + ipv4               = true
          + ipv6               = (known after apply)
          + ipv6_address       = (known after apply)
          + mac_address        = (known after apply)
          + nat                = true
          + nat_ip_address     = (known after apply)
          + nat_ip_version     = (known after apply)
          + security_group_ids = (known after apply)
          + subnet_id          = (known after apply)
        }

      + placement_policy {
          + host_affinity_rules = (known after apply)
          + placement_group_id  = (known after apply)
        }

      + resources {
          + core_fraction = 2
          + cores         = 2
          + memory        = 2
        }

      + scheduling_policy {
          + preemptible = (known after apply)
        }
    }

  # yandex_compute_instance.vm-1 will be created
  + resource "yandex_compute_instance" "vm-1" {
      + created_at                = (known after apply)
      + folder_id                 = (known after apply)
      + fqdn                      = (known after apply)
      + hostname                  = (known after apply)
      + id                        = (known after apply)
      + metadata                  = {
          + "ssh-keys" = <<-EOT
                ubuntu:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC/FUOU+m4iae8M0fyOWW/53ziQxpwGEb5LHTGhqlwTQgKvrtM7DmCbVIYFwRAZQuLLYslCe70kZe3aVKe4NsyqSrOwG30LeGjQBADqv8k0nu95oqoHRLXzvvFxyfmv8GJ1K14kibJm+4Pu2FXi+lDY3T9PpPtqolI6XZ7g9Lyuvo4qaBbydtiMlZHvJsVkv6bM+ekeFqSrDD/vSFYyFit5kFo8opg/AvJ7zHBc88fJ5GN8r29PMw35LiiU016R9YHo4+WNQIP53FZwLVGVtmY7PEXdaDo6TWd2qNlOri9kX6F+w14qkT7cadpTS0qL0i283siwXoybJiiVm7WgO+9Sm0wcpLs6mgBxJmNP9fy0hlRsf+K+MaCKQoPVKLrqNYg/EVJcyuGuctgK2g7ZPxsxPUV2tn8dRmgvU8YHh3BDop5V3I9hMATCYaVgycHlMnFpBeXgxofWdJr46KFbp8+yKrdR0kIeP3I/3C873uY4V55TvkXjwsR1BhM3/I44dcc= root@TOP
            EOT
        }
      + name                      = "terraform1"
      + network_acceleration_type = "standard"
      + platform_id               = "standard-v1"
      + service_account_id        = (known after apply)
      + status                    = (known after apply)
      + zone                      = (known after apply)

      + boot_disk {
          + auto_delete = true
          + device_name = (known after apply)
          + disk_id     = (known after apply)
          + mode        = (known after apply)

          + initialize_params {
              + block_size  = (known after apply)
              + description = (known after apply)
              + image_id    = "fd87va5cc00gaq2f5qfb"
              + name        = (known after apply)
              + size        = (known after apply)
              + snapshot_id = (known after apply)
              + type        = "network-hdd"
            }
        }

      + network_interface {
          + index              = (known after apply)
          + ip_address         = (known after apply)
          + ipv4               = true
          + ipv6               = (known after apply)
          + ipv6_address       = (known after apply)
          + mac_address        = (known after apply)
          + nat                = true
          + nat_ip_address     = (known after apply)
          + nat_ip_version     = (known after apply)
          + security_group_ids = (known after apply)
          + subnet_id          = (known after apply)
        }

      + placement_policy {
          + host_affinity_rules = (known after apply)
          + placement_group_id  = (known after apply)
        }

      + resources {
          + core_fraction = 100
          + cores         = 2
          + memory        = 2
        }

      + scheduling_policy {
          + preemptible = (known after apply)
        }
    }

  # yandex_vpc_network.network-1 will be created
  + resource "yandex_vpc_network" "network-1" {
      + created_at                = (known after apply)
      + default_security_group_id = (known after apply)
      + folder_id                 = (known after apply)
      + id                        = (known after apply)
      + labels                    = (known after apply)
      + name                      = "network1"
      + subnet_ids                = (known after apply)
    }

  # yandex_vpc_subnet.subnet-1 will be created
  + resource "yandex_vpc_subnet" "subnet-1" {
      + created_at     = (known after apply)
      + folder_id      = (known after apply)
      + id             = (known after apply)
      + labels         = (known after apply)
      + name           = "subnet1"
      + network_id     = (known after apply)
      + v4_cidr_blocks = [
          + "192.168.10.0/24",
        ]
      + v6_cidr_blocks = (known after apply)
      + zone           = "ru-central1-a"
    }

Plan: 5 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + external_ip_address_vm_1 = (known after apply)
  + internal_ip_address_vm_1 = (known after apply)

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take exactly these actions if you run "terraform apply" now.
```