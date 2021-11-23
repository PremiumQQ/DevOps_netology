1)  
2)   
vagrant@vagrant:~$ touch MUJIK  
vagrant@vagrant:~$ ls -ilh  
total 420K  
131084 -rw-rw-r-- 1 vagrant vagrant    0 Nov 21 06:18  MUJIK  
262153 drwxrwxr-x 3 vagrant vagrant 4.0K Nov 16 12:52  node  
131085 -rw-r--r-- 1 vagrant vagrant  13K Oct 31 10:32 'qqq'$'\033\033'  
131081 -rw-r--r-- 1 vagrant vagrant 397K Oct 31 10:22  ynchronizedWriters  
vagrant@vagrant:~$ chmod 0755 MUJIK  
vagrant@vagrant:~$ ls -ilh  
total 420K  
131084 -rwxr-xr-x 1 vagrant vagrant    0 Nov 21 06:18  MUJIK  
262153 drwxrwxr-x 3 vagrant vagrant 4.0K Nov 16 12:52  node  
131085 -rw-r--r-- 1 vagrant vagrant  13K Oct 31 10:32 'qqq'$'\033\033'  
131081 -rw-r--r-- 1 vagrant vagrant 397K Oct 31 10:22  ynchronizedWriters  
  
Из этого следует вывод, что нет, не могут. Они ссылаются на один и тот же файл, inode одинаковый.   
3)  
vagrant@vagrant:~$ lsblk  
NAME                 MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT  
sda                    8:0    0   64G  0 disk  
├─sda1                 8:1    0  512M  0 part /boot/efi  
├─sda2                 8:2    0    1K  0 part  
└─sda5                 8:5    0 63.5G  0 part  
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm  /  
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm  [SWAP]  
sdb                    8:16   0  2.5G  0 disk  
sdc                    8:32   0  2.5G  0 disk  
4)  
root@vagrant:~# sudo cfdisk /dev/sdb  
  
Syncing disks.  
root@vagrant:~# lsblk  
NAME                 MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT  
sda                    8:0    0   64G  0 disk  
├─sda1                 8:1    0  512M  0 part /boot/efi  
├─sda2                 8:2    0    1K  0 part  
└─sda5                 8:5    0 63.5G  0 part  
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm  /  
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm  [SWAP]  
sdb                    8:16   0  2.5G  0 disk  
├─sdb1                 8:17   0  512M  0 part  
└─sdb2                 8:18   0    2G  0 part  
sdc                    8:32   0  2.5G  0 disk  
5)   
root@vagrant:~# sfdisk -d /dev/sdb|sfdisk /dev/sdc  
Checking that no-one is using this disk right now ... OK  
  
Disk /dev/sdc: 2.51 GiB, 2684354560 bytes, 5242880 sectors  
Disk model: VBOX HARDDISK  
Units: sectors of 1 * 512 = 512 bytes  
Sector size (logical/physical): 512 bytes / 512 bytes  
I/O size (minimum/optimal): 512 bytes / 512 bytes  
  
>>> Script header accepted.  
>>> Script header accepted.  
>>> Script header accepted.  
>>> Script header accepted.  
>>> Script header accepted.  
>>> Script header accepted.  
>>> Created a new GPT disklabel (GUID: 1969E17D-54C4-914E-8B6B-2711F77A6FF2).  
/dev/sdc1: Created a new partition 1 of type 'Linux filesystem' and of size 512 MiB.  
/dev/sdc2: Created a new partition 2 of type 'Linux filesystem' and of size 2 GiB.  
/dev/sdc3: Done.  
  
New situation:  
Disklabel type: gpt  
Disk identifier: 1969E17D-54C4-914E-8B6B-2711F77A6FF2  
  
Device       Start     End Sectors  Size Type  
/dev/sdc1     2048 1050623 1048576  512M Linux filesystem  
/dev/sdc2  1050624 5242846 4192223    2G Linux filesystem  
  
The partition table has been altered.  
Calling ioctl() to re-read partition table.  
Syncing disks.  
root@vagrant:~# lsblk  
NAME                 MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT  
sda                    8:0    0   64G  0 disk  
├─sda1                 8:1    0  512M  0 part /boot/efi  
├─sda2                 8:2    0    1K  0 part  
└─sda5                 8:5    0 63.5G  0 part  
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm  /  
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm  [SWAP]  
sdb                    8:16   0  2.5G  0 disk  
├─sdb1                 8:17   0  512M  0 part  
└─sdb2                 8:18   0    2G  0 part  
sdc                    8:32   0  2.5G  0 disk  
├─sdc1                 8:33   0  512M  0 part  
└─sdc2                 8:34   0    2G  0 part  
root@vagrant:~#  
6)    
root@vagrant:~# mdadm --zero-superblock --force /dev/sd{b1,c1}  
mdadm: Unrecognised md component device - /dev/sdb2  
mdadm: Unrecognised md component device - /dev/sdc2  
root@vagrant:~# wipefs --all --force /dev/sd{b1,c1}  
root@vagrant:~# mdadm --create --verbose /dev/md1 -l 1 -n 2 /dev/sd{b1,c1}  
mdadm: Note: this array has metadata at the start and  
    may not be suitable as a boot device.  If you plan to  
    store '/boot' on this device please ensure that  
    your boot-loader understands md/v1.x metadata, or use  
    --metadata=0.90  
mdadm: size set to 2094080K  
Continue creating array? yes  
mdadm: Defaulting to version 1.2 metadata  
mdadm: array /dev/md1 started.  
root@vagrant:~# lsblk  
NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT  
sda                    8:0    0   64G  0 disk  
├─sda1                 8:1    0  512M  0 part  /boot/efi  
├─sda2                 8:2    0    1K  0 part  
└─sda5                 8:5    0 63.5G  0 part  
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm   /  
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]  
sdb                    8:16   0  2.5G  0 disk  
├─sdb1                 8:17   0    2G  0 part  
│ └─md1                9:1    0    2G  0 raid1  
└─sdb2                 8:18   0  511M  0 part  
sdc                    8:32   0  2.5G  0 disk  
├─sdc1                 8:33   0    2G  0 part  
│ └─md1                9:1    0    2G  0 raid1  
└─sdc2                 8:34   0  511M  0 part  
root@vagrant:~#  
7)  
root@vagrant:~# mdadm --zero-superblock --force /dev/sd{b2,c2}  
root@vagrant:~# wipefs --all --force /dev/sd{b2,c2}  
root@vagrant:~# mdadm --create --verbose /dev/md0 -l 0 -n 2 /dev/sd{b2,c2}  
mdadm: chunk size defaults to 512K  
mdadm: Defaulting to version 1.2 metadata  
mdadm: array /dev/md0 started.  
root@vagrant:~# lsblk  
NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT  
sda                    8:0    0   64G  0 disk  
├─sda1                 8:1    0  512M  0 part  /boot/efi  
├─sda2                 8:2    0    1K  0 part  
└─sda5                 8:5    0 63.5G  0 part  
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm   /  
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]  
sdb                    8:16   0  2.5G  0 disk   
├─sdb1                 8:17   0    2G  0 part  
│ └─md1                9:1    0    2G  0 raid1  
└─sdb2                 8:18   0  511M  0 part  
  └─md0                9:0    0 1017M  0 raid0  
sdc                    8:32   0  2.5G  0 disk  
├─sdc1                 8:33   0    2G  0 part  
│ └─md1                9:1    0    2G  0 raid1  
└─sdc2                 8:34   0  511M  0 part  
  └─md0                9:0    0 1017M  0 raid0  
root@vagrant:~#  
8)   
root@vagrant:~# pvcreate /dev/md1 /dev/md0  
  Physical volume "/dev/md1" successfully created.  
  Physical volume "/dev/md0" successfully created.  
root@vagrant:~#  
9)  
root@vagrant:~# vgcreate vg1 /dev/md1 /dev/md0  
  Volume group "vg1" successfully created  
10)   
root@vagrant:~# lvcreate -L 100M vg1 /dev/md0  
  Logical volume "lvol0" created.  
root@vagrant:~# lvs  
  LV     VG        Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert  
  lvol0  vg1       -wi-a----- 100.00m  
  root   vgvagrant -wi-ao---- <62.54g  
  swap_1 vgvagrant -wi-ao---- 980.00m  
root@vagrant:~#  
11)  
root@vagrant:~# mkfs.ext4 /dev/vg1/lvol0  
mke2fs 1.45.5 (07-Jan-2020)  
Creating filesystem with 25600 4k blocks and 25600 inodes  
  
Allocating group tables: done                              
Writing inode tables: done                              
Creating journal (1024 blocks): done  
Writing superblocks and filesystem accounting information: done  
12)  
root@vagrant:~# mkdir /tmp/new  
root@vagrant:~# mount /dev/vg1/lvol0 /tmp/new  
root@vagrant:~#  
13)   
root@vagrant:~# wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz  
--2021-11-21 08:01:35--  https://mirror.yandex.ru/ubuntu/ls-lR.gz  
Resolving mirror.yandex.ru (mirror.yandex.ru)... 213.180.204.183, 2a02:6b8::183  
Connecting to mirror.yandex.ru (mirror.yandex.ru)|213.180.204.183|:443... connected.  
HTTP request sent, awaiting response... 200 OK  
Length: 22479776 (21M) [application/octet-stream]  
Saving to: ‘/tmp/new/test.gz’  
  
/tmp/new/test.gz          100%[====================================>]  21.44M  15.2MB/s    in 1.4s  
  
2021-11-21 08:01:37 (15.2 MB/s) - ‘/tmp/new/test.gz’ saved [22479776/22479776]  
root@vagrant:/tmp/new# ls  
lost+found  test.gz  
14)  
root@vagrant:/tmp/new# lsblk  
NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT  
sda                    8:0    0   64G  0 disk  
├─sda1                 8:1    0  512M  0 part  /boot/efi  
├─sda2                 8:2    0    1K  0 part  
└─sda5                 8:5    0 63.5G  0 part  
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm   /  
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]  
sdb                    8:16   0  2.5G  0 disk  
├─sdb1                 8:17   0    2G  0 part  
│ └─md1                9:1    0    2G  0 raid1  
└─sdb2                 8:18   0  511M  0 part  
  └─md0                9:0    0 1017M  0 raid0  
    └─vg1-lvol0      253:2    0  100M  0 lvm   /tmp/new  
sdc                    8:32   0  2.5G  0 disk  
├─sdc1                 8:33   0    2G  0 part  
│ └─md1                9:1    0    2G  0 raid1  
└─sdc2                 8:34   0  511M  0 part  
  └─md0                9:0    0 1017M  0 raid0  
    └─vg1-lvol0      253:2    0  100M  0 lvm   /tmp/new  
15)  
root@vagrant:/tmp/new# gzip -t /tmp/new/test.gz  
root@vagrant:/tmp/new# echo $?  
0  
16)   
root@vagrant:/tmp/new# pvmove /dev/md0 /dev/md1  
  /dev/md0: Moved: 8.00%  
  /dev/md0: Moved: 100.00%  
root@vagrant:/tmp/new# cd  
root@vagrant:~# lsblk  
NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT  
sda                    8:0    0   64G  0 disk  
├─sda1                 8:1    0  512M  0 part  /boot/efi  
├─sda2                 8:2    0    1K  0 part  
└─sda5                 8:5    0 63.5G  0 part  
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm   /  
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]  
sdb                    8:16   0  2.5G  0 disk  
├─sdb1                 8:17   0    2G  0 part  
│ └─md1                9:1    0    2G  0 raid1  
│   └─vg1-lvol0      253:2    0  100M  0 lvm   /tmp/new  
└─sdb2                 8:18   0  511M  0 part  
  └─md0                9:0    0 1017M  0 raid0  
sdc                    8:32   0  2.5G  0 disk  
├─sdc1                 8:33   0    2G  0 part  
│ └─md1                9:1    0    2G  0 raid1  
│   └─vg1-lvol0      253:2    0  100M  0 lvm   /tmp/new  
└─sdc2                 8:34   0  511M  0 part  
  └─md0                9:0    0 1017M  0 raid0  
17)   
root@vagrant:~# mdadm /dev/md1 --fail /dev/sdb1  
mdadm: set /dev/sdb1 faulty in /dev/md1  
root@vagrant:~# cat /proc/mdstat  
Personalities : [linear] [multipath] [raid0] [raid1] [raid6] [raid5] [raid4] [raid10]  
md0 : active raid0 sdc2[1] sdb2[0]  
      1041408 blocks super 1.2 512k chunks  
  
md1 : active raid1 sdc1[1] sdb1[0](F)  
      2094080 blocks super 1.2 [2/1] [_U]  
  
unused devices: <none>  
18)   
root@vagrant:~# dmesg | grep md1  
[ 2984.205698] md/raid1:md1: not clean -- starting background reconstruction  
[ 2984.205699] md/raid1:md1: active with 2 out of 2 mirrors  
[ 2984.205708] md1: detected capacity change from 0 to 2144337920  
[ 2984.206773] md: resync of RAID array md1  
[ 2994.689074] md: md1: resync done.  
[ 6577.209526] md/raid1:md1: Disk failure on sdb1, disabling device.  
               md/raid1:md1: Operation continuing on 1 devices.  
19)  
root@vagrant:~# gzip -t /tmp/new/test.gz  
root@vagrant:~# echo $?  
0  
20)  
PS E:\netology> vagrant destroy  
    default: Are you sure you want to destroy the 'default' VM? [y/N] y  
==> default: Forcing shutdown of VM...  
==> default: Destroying VM and associated drives...  
  
  