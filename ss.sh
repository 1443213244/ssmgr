#!/bin/bash


echo "编译环境"
 if [[ -f /etc/redhat-release ]]; then
        release="centos"
        yum install epel-release -y
	yum install gcc gettext autoconf libtool automake make pcre-devel asciidoc xmlto c-ares-devel libev-devel libsodium-devel mbedtls-devel iptables-services -y
        systemPackage="yum"
    elif grep -Eqi "debian" /etc/issue; then
        release="debian"
        systemPackage="apt"
    elif grep -Eqi "ubuntu" /etc/issue; then
        release="ubuntu"
        systemPackage="apt"
    elif grep -Eqi "centos|red hat|redhat" /etc/issue; then
        release="centos"
        systemPackage="yum"
    elif grep -Eqi "debian" /proc/version; then
        release="debian"
        systemPackage="apt"
    elif grep -Eqi "ubuntu" /proc/version; then
        release="ubuntu"
        systemPackage="apt"
    elif grep -Eqi "centos|red hat|redhat" /proc/version; then
        release="centos"
        systemPackage="yum"
    fi
echo "************下载必要库************"
$systemPackage -y install python-pip
pip install cymysql==0.9.14
echo "*****cymysql下载成功*****"
$systemPackage install -y supervisor

echo "************下载源码************"
$systemPackage install git
cd /usr/local/src
git clone https://github.com/shadowsocks/shadowsocks-libev.git

echo "************编译************"
cd /usr/local/src/shadowsocks-libev
git submodule update --init --recursive
sh autogen.sh
./configure --disable-documentation
make
make install

echo "************配置进程文件************"
mv /root/ssmgr/ss.ini /etc/supervisord.d/
mv /root/ssmgr/ss_firewalld.ini /etc/supervisord.d/

echo "************重启进程************"
supervisorctl reload

#设置开机启动
systemctl enable supervisord
#启动supervisord:
systemctl start supervisord