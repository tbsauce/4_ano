## Configure Firewall

On Gns3 right click on the firewall and configure it.

+ Console type: telnet
+ **Check** Auto Start Console
+ **Check** Start VM in headless mode
+ RAM: 512M
+ Network Adapters: 6
+ **Check** Network option "Allow GNS3 to use any ... adapter".

## PC1
```
ip 10.1.1.100/24 10.1.1.1
save
```

## PC2
```
ip 192.1.1.40/24 192.1.1.1
save
```

## PC3
```
ip 192.1.1.140/24 192.1.1.1
save
```

## PC4
```
ip 200.1.1.100/24 200.1.1.1
save
```

## FireWall Vm

```
configure

set interfaces ethernet eth0 address 200.1.1.1/24
set interfaces ethernet eth1 address 192.1.1.1/24
set interfaces ethernet eth2 address 10.1.1.1/24
commit
```

```
set nat source rule 100 outbound-interface eth0
set nat source rule 100 source address 10.1.1.0/24
set nat source rule 100 translation address 192.1.0.1-192.1.0.10
commit
```


```
set zone-policy zone INSIDE description "Inside (Internal Network)"
set zone-policy zone INSIDE interface eth2
set zone-policy zone DMZ description "DMZ (Server Farm)"
set zone-policy zone DMZ interface eth1
set zone-policy zone OUTSIDE description "Outside (Internet)"
set zone-policy zone OUTSIDE interface eth0
commit
```

```
set firewall name FROM-INSIDE-TO-OUTSIDE rule 10 description "Accept ICMP Echo Request"
set firewall name FROM-INSIDE-TO-OUTSIDE rule 10 action accept
set firewall name FROM-INSIDE-TO-OUTSIDE rule 10 protocol icmp
set firewall name FROM-INSIDE-TO-OUTSIDE rule 10 icmp type 8
set firewall name TO-INSIDE rule 10 description "Accept Established-Related Connections"
set firewall name TO-INSIDE rule 10 action accept
set firewall name TO-INSIDE rule 10 state established enable
set firewall name TO-INSIDE rule 10 state related enable
set zone-policy zone INSIDE from OUTSIDE firewall name TO-INSIDE
set zone-policy zone OUTSIDE from INSIDE firewall name FROM-INSIDE-TO-OUTSIDE
commit
```

```
set firewall name FROM-INSIDE-TO-DMZ rule 10 description "Accept ICMP Echo Request"
set firewall name FROM-INSIDE-TO-DMZ rule 10 action accept
set firewall name FROM-INSIDE-TO-DMZ rule 10 protocol icmp
set firewall name FROM-INSIDE-TO-DMZ rule 10 icmp type 8
set firewall name FROM-INSIDE-TO-DMZ rule 10 destination address 192.1.1.0/24
set zone-policy zone INSIDE from DMZ firewall name TO-INSIDE
set zone-policy zone DMZ from INSIDE firewall name FROM-INSIDE-TO-DMZ
commit
```

Why before this point i couldnt ping the dmz? from outside?
```
set firewall name FROM-OUTSIDE-TO-DMZ rule 10 description "Accept ICMP Echo Request"
set firewall name FROM-OUTSIDE-TO-DMZ rule 10 action accept
set firewall name FROM-OUTSIDE-TO-DMZ rule 10 protocol icmp
set firewall name FROM-OUTSIDE-TO-DMZ rule 10 icmp type 8
set firewall name FROM-OUTSIDE-TO-DMZ rule 10 destination address 192.1.1.40
set firewall name FROM-DMZ-TO-OUTSIDE rule 10 description "Accept Established-Related Connections"
set firewall name FROM-DMZ-TO-OUTSIDE rule 10 action accept
set firewall name FROM-DMZ-TO-OUTSIDE rule 10 state established enable
set firewall name FROM-DMZ-TO-OUTSIDE rule 10 state related enable
set zone-policy zone OUTSIDE from DMZ firewall name FROM-DMZ-TO-OUTSIDE
set zone-policy zone DMZ from OUTSIDE firewall name FROM-OUTSIDE-TO-DMZ
commit
```


```
set firewall name FROM-OUTSIDE-TO-DMZ rule 12 description "Accept UDP-8080"
set firewall name FROM-OUTSIDE-TO-DMZ rule 12 action accept
set firewall name FROM-OUTSIDE-TO-DMZ rule 12 protocol udp
set firewall name FROM-OUTSIDE-TO-DMZ rule 12 destination address 192.1.1.140
set firewall name FROM-OUTSIDE-TO-DMZ rule 12 destination port 8080
commit
```

```
save
exit
```





