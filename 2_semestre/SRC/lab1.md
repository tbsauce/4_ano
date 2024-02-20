# Part B 

## Part 1

### Router 1
```
conf t
int f0/0
ip add 10.0.0.1 255.255.255.0
ip ospf 1 area 0
no shutdown
int f0/1
ip add 10.1.1.1 255.255.255.0
ip ospf 1 area 0
no shutdown
end

write
```

### Router 2
```
conf t
int f0/0
ip add 10.1.1.2 255.255.255.0
ip ospf 1 area 0
no shutdown
int f0/1
ip add 10.2.2.2 255.255.255.0
ip ospf 1 area 0
no shutdown
end

write
```

### PC 1
```
ip 10.0.0.101/24 10.0.0.1
save
```

### PC 2
```
ip 10.0.0.102/24 10.0.0.1
save
```

### PC 3
```
ip 10.2.2.103/24 10.2.2.2
save
```

## Part 2

### SWL3A

```
conf t
int f1/15
switchport mode trunk
exit 

int f1/14
switchport mode trunk
end

write
```

### SWL3B

```
conf t
int f1/14
switchport mode trunk
exit

ip routing
int vlan 1
no autostate
ip add 10.0.0.1 255.255.255.0
ip ospf 1 area 0
no shut
exit

int f0/1
ip address 10.1.1.11 255.255.255.0
ip ospf 1 area 0
no shut
end 

write
```

## Part 3

### PC 2

```
ip 10.0.2.102/24 10.0.2.1
save
```

### PC 4

```
ip 10.0.3.104/24 10.0.3.1
save
```

### SWL3A
```
vlan database
vlan 2
vlan 3
exit

write
```



### SWL3B
```
vlan database
vlan 2
vlan 3
exit

conf t
ip routing
int vlan 2
no autostate
ip add 10.0.2.1 255.255.255.0
ip ospf 1 area 0
no shut
exit

int vlan 3
no autostate
ip add 10.0.3.1 255.255.255.0
ip ospf 1 area 0
no shut
end

write
``` 

## Part 4

### SWL3A
``` 
conf t
int range f1/12 - 14
channel-group 1 mode on
int Port-channel 1
switchport mode trunk
end

write
``` 

### SWL3B
``` 
conf t
int range f1/12 - 14
channel-group 1 mode on
int Port-channel 1
switchport mode trunk
end

write
``` 