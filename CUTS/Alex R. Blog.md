> Alex R.'s personal blog, preserved since 2003. He loved music, cryptography, and keeping secrets. Some things were meant to be found.

Link to site: http://challs.cuts.uz:5021

Flag format: `CUTS{...}`

# Initial Recon

Saytga kirganimdagi dastlabki ko'rinishi.

![[Pasted image 20260419155120.png]]


![[Pasted image 20260419163940.png]]

`/about` sahifasini ham ko'rib chiqdim. U Alex haqida ma'lumotlar bor edi.

![[Pasted image 20260419155526.png]]
`/my-setup` posti esa biroz qiziqroq edi, chunki unda Flask tilga olingan. Bu detail backend texnologiyasini anglatib turardi, lekin hali flagga olib boradigan to'g'ridan-to'g'ri yo'l emas edi.

![[Pasted image 20260419155614.png]]



![[Pasted image 20260419155556.png]]
Postlarni ham tezda ko'rib chiqdim va qismiga e'tibor berganimda `robots.txt` linki borligini ko'rdim. Web challenge'larda bu ko'pincha kerakli boshlang'ich nuqta bo'ladi, shuning uchun check qilib ko'rdim.
# Interesting Endpoints

`robots.txt` ichida quyidagilar bor edi:

```txt
User-agent: *
Disallow: /admin-1337
Disallow: /vault
```

Bu yerning o'zidayoq ikkita qiziq endpoint ko'rinib qoldi: `/admin-1337` va `/vault`.

`/vault` esa kirish huquqi cheklanganligini va admin parolini topishligini ko'rsatdi

![[Pasted image 20260419155451.png]]

`/admin-1337` ni ochganimda login forma chiqdi. Men bir qancha login va parolni guess qilib ko'rdim postlardagi ma'lumotlarga asoslanib lekin bo'lmadi. Keyin credentialni oddiy guess qilishdan chiqmasligini tushundim va yana enumaration qilishga kirishdim. Birinchi qiladigan ish bu directory bruteforce bo'ldi.

![[Pasted image 20260419155417.png|697]]



# Directory Bruteforce

Men `gobuster` bilan bruteforce qildim, chunki web challenge'larda yashirin fayl va papkalarni topish uchun yaxshi tool deb bilaman. 

![[Screenshot 2026-04-19 162742 1.png]]

```bash
gobuster dir -u http://challs.cuts.uz:5021/ -w /usr/share/wordlists/dirb/common.txt
```

Fuzzing natijasida eng muhim topilma `.git/HEAD` bo'ldi. Oldin ham shunga o'xshash tasklarni ishlaganim uchun `.git` exposure qanchalik vulnerability ekanini bilardim. [Exposed Git Directory Exploitation](https://infosecwriteups.com/exposed-git-directory-exploitation-3e30481e8d75) .
# Exposed .git

`.git` exposed bo'lganidan keyin repo'ni tiklash uchun `git-dumper` ishlatdim:

```bash
pip install git-dumper
```

Oldin yuklab oldim va keyin ishlatdim. 

```
git-dumper http://challs.cuts.uz:5021/.git/ repo
```

Repository tiklangach, ichidan quyidagi fayllar chiqdi:

```bash
┌──(kali㉿kali)-[~/repo]
└─$ ls -la
total 72
drwxrwxr-x  4 kali kali  4096 Apr 19 07:04 .
drwx------ 30 kali kali  4096 Apr 19 07:27 ..
-rw-rw-r--  1 kali kali 36284 Apr 19 07:04 app.py
-rw-rw-r--  1 kali kali   534 Apr 19 07:04 diary_utils.py
-rw-rw-r--  1 kali kali   331 Apr 19 07:04 Dockerfile
-rw-rw-r--  1 kali kali    65 Apr 19 07:04 .dockerignore
drwxrwxr-x  7 kali kali  4096 Apr 19 07:04 .git
-rw-rw-r--  1 kali kali    13 Apr 19 07:04 requirements.txt
-rwxrwxr-x  1 kali kali  1704 Apr 19 07:04 setup_git.sh
drwxrwxr-x  2 kali kali  4096 Apr 19 07:04 templates
                                                         
```
Bu repository source kodligini tushundim.
# Recovering the Flag

`app.py` faylini ochganimda kerakli secret'lar to'g'ridan-to'g'ri kod ichida saqlanayotganini ko'rdim:

```bash
┌──(kali㉿kali)-[~/repo]
└─$ head app.py
from flask import Flask, render_template, request, redirect, session, send_from_directory, Response
import os

app = Flask(__name__)
app.secret_key = 'fl4sk_s3cr3t_n0t_th3_fl4g_xD'

FLAG = os.environ.get('FLAG', 'CUTS{gh0st_1n_th3_m4ch1n3_4l3x_n3v3r_d13d}')
VAULT_TOKEN = 'gh0st_1n_th3_m4ch1n3'
ADMIN_USER = 'admin'
ADMIN_PASS = 'r4d10h34d'

```

Bu yerda flag environment variable orqali olinadi, lekin default qiymat sifatida ham source code ichida qolib ketgan. Ya'ni `.git` exposure orqali repo tiklangan keyin admin credential, vault token va qolgan barchasi ko'rindi. 

Flag: `CUTS{gh0st_1n_th3_m4ch1n3_4l3x_n3v3r_d13d}`

