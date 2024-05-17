# PowerShell script that was tested and used using Packer

## Install QT spesific version

## Install localhost and import it to LocalMachine/Root store for packer use.
### Requirements
- Chocolatey Software
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
choco feature enable -n=allowGlobalConfirmation
```

- Install OpenSSL.Light
```powershell
choco install OpenSSL.Light
```
