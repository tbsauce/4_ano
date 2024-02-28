Rede Nat

No attached to conect to gns3

```
vlan database
vlan 1
exit

conf t
ip routing
int f 1/0
switchport mode access
switchport access vlan 1
int vlan 1
no shut 
ip add 10.1.0.1 255.255.255.0
int f0/0
no shut
ip add 10.0.0.1 255.255.255.0
end
write

```

insert credentials and then start again free radius

edit redes

802.1x 

meter o 