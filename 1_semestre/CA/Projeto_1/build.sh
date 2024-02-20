#Edes Main
g++ C++/EdesMain.cpp -o C++/edes -lssl -lcrypto

#Des Main
g++ C++/DesMain.cpp -o C++/des -lssl -lcrypto

#Enc
g++ C++/encrypt.cpp -o C++/enc -lssl -lcrypto

#Dec
g++ C++/decrypt.cpp -o C++/dec -lssl -lcrypto

#Speed
g++ C++/speed.cpp -o C++/speed -lssl -lcrypto