## Part 1

Install on Server Vm
```
sudo apt-get install freeradius
```

After in each Vm, change the network settings to not attached.

### SWL3

```
vlan database
vlan 1
exit

conf t
ip routing
int f1/0
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

### Both VM

Go to conections and put manually the ip, mask and gateway, test conectivity


## Part 2

### Server VM

```
sudo vim etc/freeradius/3.0/clients.conf
```

Insert the following code
```
client 10.0.0.1 {
    secret = radiuskey
}
```

```
sudo vim /etc/freeradius/3.0/users
```

Insert the following code
```
"labredes" Cleartext-Password := "labcom"
```

Confirm that radius.service is `active`.
```
systemctl status freeradius
```

If it isn't start it
```
systemctl start freeradius
```


### SWL3

```
conf t
aaa new-model
aaa authentication dot1x default group radius
dot1x system-auth-control
radius-server host 10.0.0.100 auth-port 1812 key radiuskey
interface FastEthernet1/0
dot1x port-control auto
end 
write
```


### User VM

Go to conections and add to 802.1X security your credentials in this case `labredes` `labcom`



