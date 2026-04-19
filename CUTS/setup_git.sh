#!/bin/bash
# Creates realistic git history with a "removed hardcoded credentials" commit
set -e

cd /app

# Remove any leftover files that shouldn't be in the fake git history
rm -f WRITEUP.md docker-compose.yml
rm -rf repo/

git init
git config user.email "alex@alex-r.local"
git config user.name "Alex R."

# === COMMIT 1: Initial setup with hardcoded password ===
cat > config.py << 'EOF'
# Blog configuration - Alex R. personal site
# TODO: move these to environment variables before going live

SECRET_KEY = "fl4sk_s3cr3t_n0t_th3_fl4g_xD"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "r4d10h34d"

DEBUG = True
HOST = "0.0.0.0"
PORT = 5000
EOF

git add config.py
git commit -m "initial commit: personal blog, basic structure, admin panel"

# === COMMIT 2: Added diary encryption feature ===
cat > diary_utils.py << 'EOF'
# Vigenere cipher utility - for encrypting personal notes
def vigenere_encrypt(text, key):
    result = []
    key = key.lower()
    ki = 0
    for c in text:
        if c.isalpha():
            shift = ord(key[ki % len(key)]) - ord('a')
            if c.isupper():
                result.append(chr((ord(c) - ord('A') + shift) % 26 + ord('A')))
            else:
                result.append(chr((ord(c) - ord('a') + shift) % 26 + ord('a')))
            ki += 1
        else:
            result.append(c)
    return ''.join(result)
EOF

git add diary_utils.py
git commit -m "feat: add diary encryption with vigenere cipher"

# === COMMIT 3: Remove hardcoded credentials ===
rm config.py
git add -A
git commit -m "security: removed hardcoded credentials from config.py -- never commit secrets!!"

echo "[+] Git history created successfully."
echo "[+] Commits:"
git log --oneline
