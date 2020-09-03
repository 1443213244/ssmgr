#!/bin/bash

IPT='iptables'
IP=('112.73.24.219' '149.129.59.34' '8.210.6.77' '157.119.73.119')



SetFirewalld(){
    $IPT -F

    for((i=0;i<=${#IP[@]}-1;i++))
    do
        $IPT -I INPUT -p tcp -s ${IP[i]} --dport 1025:30000 -j ACCEPT
        $IPT -I INPUT -p tcp -s ${IP[i]} --dport 22 -j ACCEPT
        $IPT -I INPUT -s ${IP[i]} -p icmp -j ACCEPT
    done

    
    $IPT -A INPUT -p tcp --dport 1025:30000 -j DROP
    $IPT -A INPUT -p tcp --dport 22 -j DROP
    $IPT -A INPUT -p icmp -j DROP    
    $IPT -nvL

}


CheckSSR(){
      
            SetFirewalld
}

CheckSSR






