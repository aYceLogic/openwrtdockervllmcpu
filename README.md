Description
-----------
This is a small project that demonstrate how to run vllm server on arm64 OpenWrt router using cpu. Not for performance but for experimentation. Docker image for cpu inference llm https://hub.docker.com/r/openeuler/vllm-cpu

Tested on https://one.openwrt.org https://openwrt.org/toh/openwrt/one 1gb of ram though should function on models with less ram, if it fails enable swap on fast usb. Hardware info https://one.openwrt.org/hardware/

Setup Openwrt
-------------

opkg update

opkg install kmod-usb-core kmod-usb2 kmod-usb3

opkg install kmod-usb-storage kmod-usb-storage-uas block-mount

opkg install kmod-fs-ext4 e2fsprogs

Mount USB (Ideally fast usb 8GB+ , 3.0 or above recommended, but if you don't have one, a fast usb2.0 will do)
----------

/sbin/block mount

block info

block detect | uci import fstab

#block detect > /etc/config/fstab

nano /etc/config/fstab (edit if needed)

service fstab boot

set fstab.@mount[-1]uci.enabled='1'

uci commit fstab

reboot

Install Docker
---------------

opkg install coreutils-nproc luci-app-dockerman docker docker-compose dockerd

Setup the mount point for docker 
---------------------------------

uci set dockerd.globals.data_root='/mnt/sda/docker'

uci commit

reboot

Deploy to OpenWRT
-----------------

Run deploy.sh to run install docker image, and download model and start vllm server

