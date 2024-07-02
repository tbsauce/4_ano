# Commandos novos
## PC1
```shell
ip 10.2.2.100/24 10.2.2.10
save
```


## PC2
```shell
ip 200.2.2.100/24 200.2.2.10
save
```

## PC3(Blocked Computer)
```shell
ip 200.2.2.200/24 200.2.2.10
save
```

## DMZ-Server
```shell
configure
set system host-name DMZ
set interfaces ethernet eth0 address 192.1.1.100/24

set protocols static route 0.0.0.0/0 next-hop 192.1.1.200

commit
save
exit
```

## PC5
```shell
ip 10.3.3.100/24 10.3.3.10/24
save
```

## Load-Balancers

### LB1A
```shell
configure
set system host-name LB1A
set interfaces ethernet eth0 address 10.1.1.1/24
set interfaces ethernet eth1 address 10.0.4.1/24
set interfaces ethernet eth2 address 10.0.0.2/24
set interfaces ethernet eth3 address 10.0.3.1/24

set protocols static route 10.0.0.0/8 next-hop 10.1.1.10


set load-balancing wan interface-health eth3 nexthop 10.0.3.2
set load-balancing wan interface-health eth1 nexthop 10.0.4.2 
set load-balancing wan rule 1 inbound-interface eth0 
set load-balancing wan rule 1 interface eth1 weight 1 
set load-balancing wan rule 1 interface eth3 weight 1 
set load-balancing wan sticky-connections inbound 
set load-balancing wan disable-source-nat

set high-availability vrrp group LBCluster vrid 10 
set high-availability vrrp group LBCluster interface eth2 
set high-availability vrrp group LBCluster virtual-address 192.168.100.1/24 
set high-availability vrrp sync-group LBCluster member LBCluster 
set high-availability vrrp group LBCluster rfc3768-compatibility

set service conntrack-sync accept-protocol 'tcp,udp,icmp' 
set service conntrack-sync failover-mechanism vrrp sync-group LBCluster 
set service conntrack-sync interface eth2 
set service conntrack-sync mcast-group 225.0.0.50 
set service conntrack-sync disable-external-cache

commit
save
exit
```

### LB2A
```shell
configure 
set system host-name LB2A
set interfaces ethernet eth0 address 10.0.9.1/24 
set interfaces ethernet eth1 address 200.1.1.1/24 
set interfaces ethernet eth2 address 10.0.10.1/24 
set interfaces ethernet eth3 address 10.0.7.2/24 
set protocols static route 200.2.2.0/24 next-hop 200.1.1.10 

set load-balancing wan interface-health eth0 nexthop 10.0.9.2 
set load-balancing wan interface-health eth3 nexthop 10.0.7.1
set load-balancing wan rule 1 inbound-interface eth1 
set load-balancing wan rule 1 interface eth0 weight 1 
set load-balancing wan rule 1 interface eth3 weight 1 
set load-balancing wan sticky-connections inbound 
set load-balancing wan disable-source-nat


set high-availability vrrp group LBCluster vrid 10 
set high-availability vrrp group LBCluster interface eth2 
set high-availability vrrp group LBCluster virtual-address 192.168.100.1/24 
set high-availability vrrp sync-group LBCluster member LBCluster 
set high-availability vrrp group LBCluster rfc3768-compatibility

set service conntrack-sync accept-protocol 'tcp,udp,icmp' 
set service conntrack-sync failover-mechanism vrrp sync-group LBCluster 
set service conntrack-sync interface eth2 
set service conntrack-sync mcast-group 225.0.0.50 
set service conntrack-sync disable-external-cache

commit
save
exit
```

### LB1B
```shell
configure
set system host-name LB1B
set interfaces ethernet eth0 address 10.1.1.2/24
set interfaces ethernet eth1 address 10.0.6.1/24
set interfaces ethernet eth2 address 10.0.0.1/24
set interfaces ethernet eth3 address 10.0.5.1/24
set protocols static route 10.0.0.0/8 next-hop 10.1.1.10

set load-balancing wan interface-health eth1 nexthop 10.0.6.2
set load-balancing wan interface-health eth3 nexthop 10.0.5.2 
set load-balancing wan rule 1 inbound-interface eth0 
set load-balancing wan rule 1 interface eth1 weight 1 
set load-balancing wan rule 1 interface eth3 weight 1 
set load-balancing wan sticky-connections inbound 
set load-balancing wan disable-source-nat

set high-availability vrrp group LBCluster vrid 10 
set high-availability vrrp group LBCluster interface eth2 
set high-availability vrrp group LBCluster virtual-address 192.168.100.1/24 
set high-availability vrrp sync-group LBCluster member LBCluster 
set high-availability vrrp group LBCluster rfc3768-compatibility

set service conntrack-sync accept-protocol 'tcp,udp,icmp' 
set service conntrack-sync failover-mechanism vrrp sync-group LBCluster 
set service conntrack-sync interface eth2 
set service conntrack-sync mcast-group 225.0.0.50 
set service conntrack-sync disable-external-cache

commit
save 
exit
```

### LB2B
```shell
configure
set system host-name LB2B 

set interfaces ethernet eth0 address 10.0.11.2/24 
set interfaces ethernet eth1 address 200.1.1.2/24 
set interfaces ethernet eth2 address 10.0.10.2/24 
set interfaces ethernet eth3 address 10.0.8.2/24 
set protocols static route 200.2.2.0/24 next-hop 200.1.1.10


set load-balancing wan interface-health eth0 nexthop 10.0.11.1 
set load-balancing wan interface-health eth3 nexthop 10.0.8.1 
set load-balancing wan rule 1 inbound-interface eth1 
set load-balancing wan rule 1 interface eth0 weight 1 
set load-balancing wan rule 1 interface eth3 weight 1 
set load-balancing wan sticky-connections inbound 
set load-balancing wan disable-source-nat

set high-availability vrrp group LBCluster vrid 10 
set high-availability vrrp group LBCluster interface eth2 
set high-availability vrrp group LBCluster virtual-address 192.168.100.1/24 
set high-availability vrrp sync-group LBCluster member LBCluster 
set high-availability vrrp group LBCluster rfc3768-compatibility

set service conntrack-sync accept-protocol 'tcp,udp,icmp' 
set service conntrack-sync failover-mechanism vrrp sync-group LBCluster 
set service conntrack-sync interface eth2 
set service conntrack-sync mcast-group 225.0.0.50 
set service conntrack-sync disable-external-cache

commit
save
exit
```

### LB3
```shell
configure
set system host-name LB3

set interfaces ethernet eth0 address 192.1.1.200/24 
set interfaces ethernet eth1 address 10.0.12.2/24 
set interfaces ethernet eth2 address 10.0.13.1/24

set load-balancing wan interface-health eth1 nexthop 10.0.12.1
set load-balancing wan interface-health eth2 nexthop 10.0.13.2
set load-balancing wan rule 1 inbound-interface eth0
set load-balancing wan rule 1 interface eth1 weight 1 
set load-balancing wan rule 1 interface eth2 weight 1 
set load-balancing wan sticky-connections inbound 
set load-balancing wan disable-source-nat

commit
save
exit
```

## Firewalls

### FW1
```shell
configure
set system host-name FW1
set interfaces ethernet eth0 address 10.0.3.2/24
set interfaces ethernet eth1 address 10.0.7.1/24
set interfaces ethernet eth2 address 10.0.5.2/24
set interfaces ethernet eth3 address 10.0.8.1/24
set interfaces ethernet eth4 address 10.0.12.1/24

set nat source rule 10 outbound-interface eth3
set nat source rule 10 source address 10.0.0.0/8 
set nat source rule 10 translation address 192.1.0.1-192.1.0.10
set nat source rule 20 outbound-interface eth1
set nat source rule 20 source address 10.0.0.0/8 
set nat source rule 20 translation address 192.1.0.1-192.1.0.10

set protocols static route 192.1.1.0/24 next-hop 10.0.12.2
set protocols static route 0.0.0.0/0 next-hop 10.0.7.2
set protocols static route 0.0.0.0/0 next-hop 10.0.8.2
set protocols static route 10.0.0.0/8 next-hop 10.0.3.1
set protocols static route 10.0.0.0/8 next-hop 10.0.5.1

set zone-policy zone INSIDE description "Inside (Internal Network)"
set zone-policy zone INSIDE interface eth0
set zone-policy zone INSIDE interface eth2
set zone-policy zone INSIDE default-action drop
set zone-policy zone OUTSIDE description "Outside (Internet)"
set zone-policy zone OUTSIDE default-action drop
set zone-policy zone OUTSIDE interface eth1
set zone-policy zone OUTSIDE interface eth3
set zone-policy zone DMZ description "DMZ (Server Farm)"
set zone-policy zone DMZ interface eth4
set zone-policy zone DMZ default-action drop

set firewall name FROM-INSIDE-TO-OUTSIDE rule 10 description "Accept UDP Echo Request"
set firewall name FROM-INSIDE-TO-OUTSIDE rule 10 action accept
set firewall name FROM-INSIDE-TO-OUTSIDE rule 10 protocol udp
set firewall name FROM-INSIDE-TO-OUTSIDE rule 10 destination port 2000-4000

set firewall name TO-INSIDE rule 10 description "Accept Established-Related Connections"
set firewall name TO-INSIDE rule 10 action accept
set firewall name TO-INSIDE rule 10 state established enable
set firewall name TO-INSIDE rule 10 state related enable

set firewall name FROM-INSIDE-TO-DMZ rule 10 description "Accept UDP Echo Request"
set firewall name FROM-INSIDE-TO-DMZ rule 10 action accept
set firewall name FROM-INSIDE-TO-DMZ rule 10 protocol udp
set firewall name FROM-INSIDE-TO-DMZ rule 10 destination port 2000-4000
set firewall name FROM-INSIDE-TO-DMZ rule 10 destination address 192.1.1.0/24

set firewall name FROM-INSIDE-TO-DMZ rule 20 description "Accept SSH from IT Personel Only"
set firewall name FROM-INSIDE-TO-DMZ rule 20 action accept
set firewall name FROM-INSIDE-TO-DMZ rule 20 destination address 192.1.1.0/24
set firewall name FROM-INSIDE-TO-DMZ rule 20 destination port 22
set firewall name FROM-INSIDE-TO-DMZ rule 20 protocol tcp
set firewall name FROM-INSIDE-TO-DMZ rule 20 source address 10.3.3.0/24

set firewall name FROM-INSIDE-TO-DMZ rule 30 description "Accept DNS access"
set firewall name FROM-INSIDE-TO-DMZ rule 30 action accept
set firewall name FROM-INSIDE-TO-DMZ rule 30 destination address 192.1.1.100/24
set firewall name FROM-INSIDE-TO-DMZ rule 30 destination port 53
set firewall name FROM-INSIDE-TO-DMZ rule 30 protocol tcp_udp

set firewall name FROM-INSIDE-TO-DMZ rule 40 description "Accept HTTP, HTTPS"
set firewall name FROM-INSIDE-TO-DMZ rule 40 action accept
set firewall name FROM-INSIDE-TO-DMZ rule 40 destination address 192.1.1.100/24
set firewall name FROM-INSIDE-TO-DMZ rule 40 destination port 80,443
set firewall name FROM-INSIDE-TO-DMZ rule 40 protocol tcp
set firewall name FROM-INSIDE-TO-DMZ rule 40 source address 10.0.0.0/8

set firewall group address-group BLOCKED_IPS address 200.2.2.200
set firewall name FROM-OUTSIDE-TO-DMZ rule 10 action drop
set firewall name FROM-OUTSIDE-TO-DMZ rule 10 protocol all
set firewall name FROM-OUTSIDE-TO-DMZ rule 10 source group address-group 'BLOCKED_IPS'

set firewall name FROM-OUTSIDE-TO-DMZ rule 20 description "Accept UDP Echo Request"
set firewall name FROM-OUTSIDE-TO-DMZ rule 20 action accept
set firewall name FROM-OUTSIDE-TO-DMZ rule 20 protocol udp
set firewall name FROM-OUTSIDE-TO-DMZ rule 20 destination port 2000-4000
set firewall name FROM-OUTSIDE-TO-DMZ rule 20 destination address 192.1.1.100/24
set firewall name FROM-OUTSIDE-TO-DMZ rule 20 source address !10.0.0.0/8
set firewall name FROM-OUTSIDE-TO-DMZ rule 20 source address !192.1.0.0/28

set firewall name FROM-OUTSIDE-TO-DMZ rule 40 description "Accept HTTPS"
set firewall name FROM-OUTSIDE-TO-DMZ rule 40 action accept
set firewall name FROM-OUTSIDE-TO-DMZ rule 40 destination address 192.1.1.100/24
set firewall name FROM-OUTSIDE-TO-DMZ rule 40 destination port 443
set firewall name FROM-OUTSIDE-TO-DMZ rule 40 protocol tcp
set firewall name FROM-OUTSIDE-TO-DMZ rule 40 source address !10.0.0.0/8
set firewall name FROM-OUTSIDE-TO-DMZ rule 40 source address !192.1.0.0/28

set firewall name FROM-DMZ-TO-OUTSIDE rule 10 description "Accept Established-Related Connections"
set firewall name FROM-DMZ-TO-OUTSIDE rule 10 action accept
set firewall name FROM-DMZ-TO-OUTSIDE rule 10 state established enable
set firewall name FROM-DMZ-TO-OUTSIDE rule 10 state related enable

set zone-policy zone INSIDE from OUTSIDE firewall name TO-INSIDE
set zone-policy zone OUTSIDE from INSIDE firewall name FROM-INSIDE-TO-OUTSIDE
set zone-policy zone INSIDE from DMZ firewall name TO-INSIDE
set zone-policy zone DMZ from INSIDE firewall name FROM-INSIDE-TO-DMZ
set zone-policy zone OUTSIDE from DMZ firewall name FROM-DMZ-TO-OUTSIDE
set zone-policy zone DMZ from OUTSIDE firewall name FROM-OUTSIDE-TO-DMZ

commit
save
exit
```

### FW2

```shell
configure

set system host-name FW2

set interfaces ethernet eth0 address 10.0.6.2/24
set interfaces ethernet eth1 address 10.0.11.1/24
set interfaces ethernet eth2 address 10.0.4.2/24
set interfaces ethernet eth3 address 10.0.9.2/24
set interfaces ethernet eth4 address 10.0.13.2/24


set protocols static route 192.1.1.0/24 next-hop 10.0.13.1
set protocols static route 0.0.0.0/0 next-hop 10.0.9.1
set protocols static route 0.0.0.0/0 next-hop 10.0.11.2
set protocols static route 10.0.0.0/8 next-hop 10.0.4.1
set protocols static route 10.0.0.0/8 next-hop 10.0.6.1

set nat source rule 10 outbound-interface eth3
set nat source rule 10 source address 10.0.0.0/8 
set nat source rule 10 translation address 192.1.0.11-192.1.0.20
set nat source rule 20 outbound-interface eth1
set nat source rule 20 source address 10.0.0.0/8 
set nat source rule 20 translation address 192.1.0.11-192.1.0.20

set zone-policy zone INSIDE description "Inside (Internal Network)"
set zone-policy zone INSIDE interface eth0
set zone-policy zone INSIDE interface eth2
set zone-policy zone INSIDE default-action drop
set zone-policy zone OUTSIDE description "Outside (Internet)"
set zone-policy zone OUTSIDE default-action drop
set zone-policy zone OUTSIDE interface eth1
set zone-policy zone OUTSIDE interface eth3
set zone-policy zone DMZ description "DMZ (Server Farm)"
set zone-policy zone DMZ interface eth4
set zone-policy zone DMZ default-action drop

set firewall name FROM-INSIDE-TO-OUTSIDE rule 10 description "Accept UDP Echo Request"
set firewall name FROM-INSIDE-TO-OUTSIDE rule 10 action accept
set firewall name FROM-INSIDE-TO-OUTSIDE rule 10 protocol udp
set firewall name FROM-INSIDE-TO-OUTSIDE rule 10 destination port 2000-4000

set firewall name TO-INSIDE rule 10 description "Accept Established-Related Connections"
set firewall name TO-INSIDE rule 10 action accept
set firewall name TO-INSIDE rule 10 state established enable
set firewall name TO-INSIDE rule 10 state related enable

set firewall name FROM-INSIDE-TO-DMZ rule 10 description "Accept UDP Echo Request"
set firewall name FROM-INSIDE-TO-DMZ rule 10 action accept
set firewall name FROM-INSIDE-TO-DMZ rule 10 protocol udp
set firewall name FROM-INSIDE-TO-DMZ rule 10 destination port 2000-4000
set firewall name FROM-INSIDE-TO-DMZ rule 10 destination address 192.1.1.0/24

set firewall name FROM-INSIDE-TO-DMZ rule 20 description "Accept SSH from IT Personel Only"
set firewall name FROM-INSIDE-TO-DMZ rule 20 action accept
set firewall name FROM-INSIDE-TO-DMZ rule 20 destination address 192.1.1.0/24
set firewall name FROM-INSIDE-TO-DMZ rule 20 destination port 22
set firewall name FROM-INSIDE-TO-DMZ rule 20 protocol tcp
set firewall name FROM-INSIDE-TO-DMZ rule 20 source address 10.3.3.0/24

set firewall name FROM-INSIDE-TO-DMZ rule 30 description "Accept DNS access"
set firewall name FROM-INSIDE-TO-DMZ rule 30 action accept
set firewall name FROM-INSIDE-TO-DMZ rule 30 destination address 192.1.1.100/24
set firewall name FROM-INSIDE-TO-DMZ rule 30 destination port 53
set firewall name FROM-INSIDE-TO-DMZ rule 30 protocol tcp_udp

set firewall name FROM-INSIDE-TO-DMZ rule 40 description "Accept HTTP, HTTPS"
set firewall name FROM-INSIDE-TO-DMZ rule 40 action accept
set firewall name FROM-INSIDE-TO-DMZ rule 40 destination address 192.1.1.100/24
set firewall name FROM-INSIDE-TO-DMZ rule 40 destination port 80,443
set firewall name FROM-INSIDE-TO-DMZ rule 40 protocol tcp
set firewall name FROM-INSIDE-TO-DMZ rule 40 source address 10.0.0.0/8

set firewall group address-group BLOCKED_IPS address 200.2.2.200
set firewall name FROM-OUTSIDE-TO-DMZ rule 10 action drop
set firewall name FROM-OUTSIDE-TO-DMZ rule 10 protocol all
set firewall name FROM-OUTSIDE-TO-DMZ rule 10 source group address-group 'BLOCKED_IPS'

set firewall name FROM-OUTSIDE-TO-DMZ rule 20 description "Accept UDP Echo Request"
set firewall name FROM-OUTSIDE-TO-DMZ rule 20 action accept
set firewall name FROM-OUTSIDE-TO-DMZ rule 20 protocol udp
set firewall name FROM-OUTSIDE-TO-DMZ rule 20 destination port 2000-4000
set firewall name FROM-OUTSIDE-TO-DMZ rule 20 destination address 192.1.1.100/24
set firewall name FROM-OUTSIDE-TO-DMZ rule 20 source address !10.0.0.0/8
set firewall name FROM-OUTSIDE-TO-DMZ rule 20 source address !192.1.0.0/28

set firewall name FROM-OUTSIDE-TO-DMZ rule 40 description "Accept HTTPS"
set firewall name FROM-OUTSIDE-TO-DMZ rule 40 action accept
set firewall name FROM-OUTSIDE-TO-DMZ rule 40 destination address 192.1.1.100/24
set firewall name FROM-OUTSIDE-TO-DMZ rule 40 destination port 443
set firewall name FROM-OUTSIDE-TO-DMZ rule 40 protocol tcp
set firewall name FROM-OUTSIDE-TO-DMZ rule 40 source address !10.0.0.0/8
set firewall name FROM-OUTSIDE-TO-DMZ rule 40 source address !192.1.0.0/28

set firewall name FROM-DMZ-TO-OUTSIDE rule 10 description "Accept Established-Related Connections"
set firewall name FROM-DMZ-TO-OUTSIDE rule 10 action accept
set firewall name FROM-DMZ-TO-OUTSIDE rule 10 state established enable
set firewall name FROM-DMZ-TO-OUTSIDE rule 10 state related enable

set zone-policy zone INSIDE from OUTSIDE firewall name TO-INSIDE
set zone-policy zone OUTSIDE from INSIDE firewall name FROM-INSIDE-TO-OUTSIDE
set zone-policy zone INSIDE from DMZ firewall name TO-INSIDE
set zone-policy zone DMZ from INSIDE firewall name FROM-INSIDE-TO-DMZ
set zone-policy zone OUTSIDE from DMZ firewall name FROM-DMZ-TO-OUTSIDE
set zone-policy zone DMZ from OUTSIDE firewall name FROM-OUTSIDE-TO-DMZ

commit
save
exit
```




## Routers
### Router 1
```shell 
conf t

interface f0/0
ip address 10.1.1.10 255.255.255.0
no shutdown

interface f0/1
ip address 10.2.2.10 255.255.255.0
no shutdown

interface f1/0
ip address 10.3.3.10 255.255.255.0
no shutdown

ip route 0.0.0.0 0.0.0.0 10.1.1.1
ip route 0.0.0.0 0.0.0.0 10.1.1.2
end
write
```

### Router 2
```shell 
conf t

interface f0/0
ip address 200.1.1.10 255.255.255.0
no shutdown

interface f0/1
ip address 200.2.2.10 255.255.255.0
no shutdown

ip route 0.0.0.0 0.0.0.0 200.1.1.1
ip route 0.0.0.0 0.0.0.0 200.1.1.2

end
write
```