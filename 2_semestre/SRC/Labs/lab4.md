# Active-Active Scenario
## PC1
```
ip 10.2.2.100/24 10.2.2.10
save
```

## PC2
```
ip 200.2.2.100/24 200.2.2.10
save
```

## R1

```
conf t
interface f0/0
ip address 10.1.1.10 255.255.255.0
no shutdown
interface f0/1
ip address 10.2.2.10 255.255.255.0
no shutdown
ip route 0.0.0.0 0.0.0.0 10.1.1.2

end
write
```
## R2

```
conf t

interface f0/0
ip address 200.1.1.10 255.255.255.0
no shutdown
interface f0/1
ip address 200.2.2.10 255.255.255.0
no shutdown
ip route 192.1.0.0 255.255.254.0 200.1.1.1

end
write
```


## FireWall 1

```
configure

set system host-name FW1
set interfaces ethernet eth0 address 200.1.1.1/24
set interfaces ethernet eth2 address 10.1.1.1/24
set interfaces ethernet eth5 address 10.0.0.1/24
set protocols static route 0.0.0.0/0 next-hop 200.1.1.10
set protocols static route 10.2.2.0/24 next-hop 10.1.1.10
commit



set nat source rule 10 outbound-interface eth0
set nat source rule 10 source address 10.0.0.0/8
set nat source rule 10 translation address 192.1.0.1-192.1.0.10
commit



set high-availability vrrp group FWCluster vrid 10
set high-availability vrrp group FWCluster interface eth5
set high-availability vrrp group FWCluster virtual-address 192.168.100.1/24
set high-availability vrrp sync-group FWCluster member FWCluster
set high-availability vrrp group FWCluster rfc3768-compatibility

set service conntrack-sync accept-protocol 'tcp,udp,icmp'
set service conntrack-sync failover-mechanism vrrp sync-group FWCluster
set service conntrack-sync interface eth5
set service conntrack-sync mcast-group 225.0.0.50
set service conntrack-sync disable-external-cache

commit



set zone-policy zone INSIDE description "Inside (Internal Network)"
set zone-policy zone INSIDE interface eth2
set zone-policy zone OUTSIDE description "Outside (Internet)"
set zone-policy zone OUTSIDE interface eth0

set firewall name FROM-INSIDE-TO-OUTSIDE rule 10 action accept
set firewall name FROM-INSIDE-TO-OUTSIDE rule 10 protocol udp
set firewall name FROM-INSIDE-TO-OUTSIDE rule 10 destination port 5000-6000

set firewall name FROM-OUTSIDE-TO-INSIDE rule 10 action accept
set firewall name FROM-OUTSIDE-TO-INSIDE rule 10 state established enable

set zone-policy zone INSIDE from OUTSIDE firewall name FROM-OUTSIDE-TO-INSIDE
set zone-policy zone OUTSIDE from INSIDE firewall name FROM-INSIDE-TO-OUTSIDE
commit
```

## FireWall 2

```
configure

set system host-name FW2
set interfaces ethernet eth0 address 200.1.1.2/24
set interfaces ethernet eth2 address 10.1.1.2/24
set interfaces ethernet eth5 address 10.0.0.2/24
set protocols static route 0.0.0.0/0 next-hop 200.1.1.10
set protocols static route 10.2.2.0/24 next-hop 10.1.1.10
commit



set nat source rule 10 outbound-interface eth0
set nat source rule 10 source address 10.0.0.0/8
set nat source rule 10 translation address 192.1.0.1-192.1.0.10
commit



set high-availability vrrp group FWCluster vrid 10
set high-availability vrrp group FWCluster interface eth5
set high-availability vrrp group FWCluster virtual-address 192.168.100.1/24
set high-availability vrrp sync-group FWCluster member FWCluster
set high-availability vrrp group FWCluster rfc3768-compatibility

set service conntrack-sync accept-protocol 'tcp,udp,icmp'
set service conntrack-sync failover-mechanism vrrp sync-group FWCluster
set service conntrack-sync interface eth5
set service conntrack-sync mcast-group 225.0.0.50
set service conntrack-sync disable-external-cache

commit



set zone-policy zone INSIDE description "Inside (Internal Network)"
set zone-policy zone INSIDE interface eth2
set zone-policy zone OUTSIDE description "Outside (Internet)"
set zone-policy zone OUTSIDE interface eth0

set firewall name FROM-INSIDE-TO-OUTSIDE rule 10 action accept
set firewall name FROM-INSIDE-TO-OUTSIDE rule 10 protocol udp
set firewall name FROM-INSIDE-TO-OUTSIDE rule 10 destination port 5000-6000

set firewall name FROM-OUTSIDE-TO-INSIDE rule 10 action accept
set firewall name FROM-OUTSIDE-TO-INSIDE rule 10 state established enable

set zone-policy zone INSIDE from OUTSIDE firewall name FROM-OUTSIDE-TO-INSIDE
set zone-policy zone OUTSIDE from INSIDE firewall name FROM-INSIDE-TO-OUTSIDE
commit
```

# Load-Balancing Scenario

## PC1
```
ip 10.2.2.100/24 10.2.2.10
save
```

## PC2
```
ip 200.2.2.100/24 200.2.2.10
save
```

## R1
```
conf t
interface f0/0
ip address 10.1.1.10 255.255.255.0
no shutdown
interface f0/1
ip address 10.2.2.10 255.255.255.0
no shutdown
ip route 0.0.0.0 0.0.0.0 10.1.1.1

end
write
```

## R2

```
conf t

interface f0/0
ip address 200.1.1.10 255.255.255.0
no shutdown
interface f0/1
ip address 200.2.2.10 255.255.255.0
no shutdown
ip route 192.1.0.0 255.255.255.0 200.1.1.1

end
write
```


## FireWall 1

```
configure

set system host-name FW1
set interfaces ethernet eth0 address 10.0.3.1/24
set interfaces ethernet eth2 address 10.0.1.1/24
set protocols static route 0.0.0.0/0 next-hop 10.0.3.10
set protocols static route 10.2.2.0/24 next-hop 10.0.1.10
commit



set nat source rule 10 outbound-interface eth0
set nat source rule 10 source address 10.0.0.0/8
set nat source rule 10 translation address 192.1.0.1-192.1.0.10
commit
```

## FireWall 2

```
configure

set system host-name FW2
set interfaces ethernet eth0 address 10.0.4.2/24
set interfaces ethernet eth2 address 10.0.2.2/24
set protocols static route 0.0.0.0/0 next-hop 10.0.4.10
set protocols static route 10.2.2.0/24 next-hop 10.0.2.10
commit



set nat source rule 10 outbound-interface eth0
set nat source rule 10 source address 10.0.0.0/8
set nat source rule 10 translation address 192.1.0.1-192.1.0.10
commit
```

## LB 1

```
configure

set system host-name LB1

set interfaces ethernet eth0 address 10.1.1.1/24
set interfaces ethernet eth1 address 10.0.1.10/24
set interfaces ethernet eth2 address 10.0.2.10/24

set protocols static route 10.2.2.0/24 next-hop 10.1.1.10

set load-balancing wan interface-health eth1 nexthop 10.0.1.1
set load-balancing wan interface-health eth2 nexthop 10.0.2.2
set load-balancing wan rule 1 inbound-interface eth0
set load-balancing wan rule 1 interface eth1 weight 1
set load-balancing wan rule 1 interface eth2 weight 1
set load-balancing wan sticky-connections inbound
set load-balancing wan disable-source-nat

commit
```

## LB 2

```
configure

set system host-name LB2

set interfaces ethernet eth0 address 200.1.1.1/24
set interfaces ethernet eth1 address 10.0.3.10/24w
set interfaces ethernet eth2 address 10.0.4.10/24

set protocols static route 200.2.2.0/24 next-hop 200.1.1.10

set load-balancing wan interface-health eth1 nexthop 10.0.3.1
set load-balancing wan interface-health eth2 nexthop 10.0.4.2
set load-balancing wan rule 1 inbound-interface eth0
set load-balancing wan rule 1 interface eth1 weight 1
set load-balancing wan rule 1 interface eth2 weight 1
set load-balancing wan sticky-connections inbound
set load-balancing wan disable-source-nat
commit
```