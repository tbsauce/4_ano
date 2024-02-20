
# Building C++

```
./build.sh
```

# Running Encryption and Decryption Applications

### Only C++

```
echo "Hello, World!" | C++/enc key | C++/dec key
```
```
echo "Hello, World!" | C++/enc key edes | C++/dec key edes
```

![c_to_c](./img/c_to_c.png)

### Only Python

```
echo "Hello, World!" | python3 python/encrypt.py key | python3 python/decrypt.py key
```
```
echo "Hello, World!" | python3 python/encrypt.py key edes | python3 python/decrypt.py key edes
```
![p_to_p](./img/p_to_p.png)

### C++ to Python

```
echo "Hello, World!" | C++/enc key | python3 python/decrypt.py key
```
```
echo "Hello, World!" | C++/enc key edes | python3 python/decrypt.py key edes
```

![c_to_p](./img/c_to_p.png)
### Python to C++

```
echo "Hello, World!" | python3 python/encrypt.py key | C++/dec key
```
```
echo "Hello, World!" | python3 python/encrypt.py key edes | C++/dec key edes
```

![p_to_c](./img/p_to_c.png)

# Running Speed

```
C++/speed
```

![speed_inC](./img/speed_inC.png)


```
python3 python/speed.py
```

![speed_inP](./img/speed_inP.png)

# Edes

```
C++/edes
```
```
python3 python/edes_main.py
```

![edes](./img/edes.png)


# Des

```
C++/des
```
```
python3 python/des_main.py
```

![des](./img/des.png)





