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

## Load-Balancers

### LB1A
```shell
configure
set system host-name LB1A
set interfaces ethernet eth0 address 10.1.1.1/24
set interfaces ethernet eth1 address 10.0.3.1/24
set interfaces ethernet eth2 address 10.0.0.2/24
set interfaces ethernet eth3 address 10.0.4.1/24
set protocols static route 10.2.2.0/24 next-hop 10.1.1.10

set load-balancing wan interface-health eth1 nexthop 10.0.3.2
set load-balancing wan interface-health eth3 nexthop 10.0.4.2 
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

set interfaces ethernet eth0 address 10.0.7.2/24 
set interfaces ethernet eth1 address 200.1.1.1/24 
set interfaces ethernet eth2 address 10.0.10.1/24 
set interfaces ethernet eth3 address 10.0.9.1/24 
set protocols static route 200.2.2.0/24 next-hop 200.1.1.10 

set load-balancing wan interface-health eth0 nexthop 10.0.7.1
set load-balancing wan interface-health eth3 nexthop 10.0.9.2 
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
set protocols static route 10.2.2.0/24 next-hop 10.1.1.10

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

## Firewalls

### FW1
```shell
configure
set system host-name FW1
set interfaces ethernet eth0 address 10.0.3.2/24
set interfaces ethernet eth1 address 10.0.7.1/24
set interfaces ethernet eth2 address 10.0.5.2/24
set interfaces ethernet eth3 address 10.0.8.1/24

set nat source rule 10 outbound-interface eth3
set nat source rule 10 outbound-interface eth1
set nat source rule 10 source address 10.0.0.0/8 
set nat source rule 10 translation address 192.1.0.1-192.1.0.10

set protocols static route 0.0.0.0/0 next-hop 10.0.7.2
set protocols static route 0.0.0.0/0 next-hop 10.0.8.2
set protocols static route 10.2.2.0/24 next-hop 10.0.3.1
set protocols static route 10.2.2.0/24 next-hop 10.0.5.1


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


set protocols static route 0.0.0.0/0 next-hop 10.0.9.1
set protocols static route 0.0.0.0/0 next-hop 10.0.11.2
set protocols static route 10.2.2.0/24 next-hop 10.0.4.1
set protocols static route 10.2.2.0/24 next-hop 10.0.6.1

set nat source rule 10 outbound-interface eth3
set nat source rule 10 outbound-interface eth1
set nat source rule 10 source address 10.0.0.0/8 
set nat source rule 10 translation address 192.1.0.11-192.1.0.20

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

ip route 0.0.0.0 0.0.0.0  10.1.1.1
ip route 0.0.0.0 0.0.0.0  10.1.1.2
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

  
ip route 192.1.0.0 255.255.255.0 200.1.1.2 
ip route 192.1.0.0 255.255.255.0 200.1.1.1

end
write
```