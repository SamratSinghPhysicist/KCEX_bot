#!/usr/bin/env python3
"""
1-Click Switch Google Drive Account & Update GitHub Secrets
===========================================================
This tool makes switching to a NEW Google Drive account completely effortless:
1. Launches Google's official authorization page in your browser.
2. You simply sign into your NEW Google Account and click "Allow".
3. Automatically captures the new permanent token.
4. Updates your local rclone config.
5. Automatically encrypts and updates the GitHub secret 'RCLONE_CONFIG' via GitHub API!
"""

import os
import sys
import json
import base64
import shutil
import subprocess
from pathlib import Path
from typing import Optional

# Try importing requests and nacl
try:
    import requests
    from nacl import encoding, public
except ImportError:
    print("[Error] Missing required packages. Run: pip install requests pynacl")
    sys.exit(1)


def find_rclone() -> str:
    rclone_path = shutil.which("rclone")
    if rclone_path:
        return rclone_path

    winget_rclone = Path(os.path.expandvars(
        r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Rclone.Rclone_Microsoft.Winget.Source_8wekyb3d8bbwe\rclone-v1.75.1-windows-amd64\rclone.exe"
    ))
    if winget_rclone.exists():
        return str(winget_rclone)

    local_app_data = Path(os.environ.get("LOCALAPPDATA", ""))
    for p in local_app_data.glob("**/rclone.exe"):
        if p.is_file():
            return str(p)

    return ""


def get_github_token() -> Optional[str]:
    env_path = Path(__file__).resolve().parent / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("GITHUB_TOKEN"):
                    return line.split("=", 1)[1].strip()
    return os.environ.get("GITHUB_TOKEN")


def update_github_secret(secret_name: str, secret_value: str, gh_token: str, repo: str = "SamratSinghPhysicist/KCEX_bot") -> bool:
    headers = {
        "Authorization": f"Bearer {gh_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 1. Fetch repo public key
    pk_url = f"https://api.github.com/repos/{repo}/actions/secrets/public-key"
    r_pk = requests.get(pk_url, headers=headers)
    if r_pk.status_code != 200:
        print(f"[!] Failed to fetch GitHub public key: {r_pk.text}")
        return False

    pk_data = r_pk.json()
    key_id = pk_data["key_id"]
    public_key_b64 = pk_data["key"]

    # 2. Encrypt using PyNaCl SealedBox
    pub_key = public.PublicKey(public_key_b64.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(pub_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    encrypted_b64 = base64.b64encode(encrypted).decode("utf-8")

    # 3. Update secret
    secret_url = f"https://api.github.com/repos/{repo}/actions/secrets/{secret_name}"
    payload = {
        "encrypted_value": encrypted_b64,
        "key_id": key_id
    }
    r_put = requests.put(secret_url, headers=headers, json=payload)
    return r_put.status_code in [201, 204]


def main():
    print("=" * 80)
    print("  CONNECT NEW GOOGLE DRIVE ACCOUNT (1-CLICK SETUP)")
    print("=" * 80)
    print("This script will open a browser window for you to log into your NEW account.")
    print("After you click 'Allow', the token and GitHub Secrets will update automatically.")
    print("=" * 80)

    rclone_bin = find_rclone()
    if not rclone_bin:
        print("[Error] rclone was not found on your system. Run: winget install Rclone.Rclone")
        return

    gh_token = get_github_token()
    if not gh_token:
        print("[Error] Could not find GITHUB_TOKEN in .env. Please ensure GITHUB_TOKEN is set.")
        return

    print("\n[1/3] Launching Google Authorization in your default browser...")
    print("      >>> When the browser opens, sign into your NEW Google Drive account.")
    print("      >>> Click 'Allow' to grant Google Drive access.\n")

    cmd = [rclone_bin, "authorize", "drive"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    stdout_data, stderr_data = proc.communicate()

    if "{" not in stdout_data or "refresh_token" not in stdout_data:
        print(f"[Error] Failed to capture authorization token from rclone.")
        print(f"Stdout: {stdout_data}")
        print(f"Stderr: {stderr_data}")
        return

    # Extract JSON token from rclone output
    raw_lines = stdout_data.splitlines()
    token_json = ""
    for line in raw_lines:
        s = line.strip()
        if s.startswith("{") and s.endswith("}") and "refresh_token" in s:
            token_json = s
            break

    if not token_json:
        # Try extracting between ---> and <---
        capture = False
        parts = []
        for line in raw_lines:
            if "--->" in line:
                capture = True
                continue
            if "<---" in line:
                capture = False
                break
            if capture:
                parts.append(line.strip())
        token_json = "".join(parts)

    if not token_json:
        print("[Error] Could not parse token JSON from rclone output.")
        return

    print("[+] Successfully received authorization token from Google!")

    # Format new rclone.conf content
    new_conf = (
        "[gdrive]\n"
        "type = drive\n"
        "scope = drive\n"
        "client_id =\n"
        "client_secret =\n"
        f"token = {token_json}\n"
        "team_drive =\n"
    )

    # 2. Save locally to %APPDATA%\rclone\rclone.conf
    appdata = os.environ.get("APPDATA", "")
    conf_dir = Path(appdata) / "rclone"
    conf_dir.mkdir(parents=True, exist_ok=True)
    conf_file = conf_dir / "rclone.conf"
    conf_file.write_text(new_conf, encoding="utf-8")
    print(f"[2/3] Local rclone configuration updated at: {conf_file}")

    # 3. Update GitHub Secret
    print("[3/3] Uploading encrypted configuration to GitHub Repository Secrets...")
    ok = update_github_secret("RCLONE_CONFIG", new_conf, gh_token)
    if ok:
        print("\n" + "=" * 80)
        print("  ALL DONE! NEW GOOGLE DRIVE ACCOUNT CONNECTED SUCCESSFULLY!")
        print("=" * 80)
        print("  - Local config updated with new account.")
        print("  - GitHub secret 'RCLONE_CONFIG' updated automatically.")
        print("  - Target folder on new drive: 'Binance_Historical_Data'")
        print("\nYou can now start the GitHub Actions workflow:")
        print("  👉 https://github.com/SamratSinghPhysicist/KCEX_bot/actions")
        print("=" * 80)
    else:
        print("[!] Failed to update secret on GitHub. Please check your GITHUB_TOKEN permissions.")


if __name__ == "__main__":
    main()
