choco install OpenSSL.Light
Import-Module $env:ChocolateyInstall\helpers\chocolateyProfile.psm1
refreshenv

==========
# Define the directory and file path
$directory = "C:\Downloads\openssl"
$filePath = "$directory\openssl.cnf"

# Create the directory if it does not exist
if (-Not (Test-Path -Path $directory)) {
    New-Item -ItemType Directory -Path $directory
}

# Define the contents of the openssl.cnf file
$configContent = @"
[req]
prompt                  = no
default_bits            = 2048
distinguished_name      = subject
req_extensions          = req_ext
x509_extensions         = x509_ext

[subject]
commonName              = localhost

[req_ext]
basicConstraints        = critical, CA:true
subjectAltName          = @alt_names

[x509_ext]
basicConstraints        = critical, CA:true
keyUsage                = critical, keyCertSign, cRLSign, digitalSignature,keyEncipherment
extendedKeyUsage        = critical, serverAuth
subjectAltName          = critical, @alt_names
1.3.6.1.4.1.311.84.1.1  = ASN1:UTF8String:ASP.NET Core HTTPS development certificate

[alt_names]
DNS.1                   = localhost
DNS.2                   = 127.0.0.1
"@

# Write the content to the file
Set-Content -Path $filePath -Value $configContent

Write-Host "The openssl.cnf file has been created at $filePath"

# Define the paths for the key, certificate, and PFX files
$keyFilePath = "$directory\localhost.key"
$certFilePath = "$directory\localhost.crt"
$pfxFilePath = "$directory\localhost.pfx"

# Run the OpenSSL commands to generate the private key and self-signed certificate
& openssl genpkey -algorithm RSA -out $keyFilePath -pkeyopt rsa_keygen_bits:2048
& openssl req -x509 -new -key $keyFilePath -out $certFilePath -days 365 -config $filePath

Write-Host "The private key has been created at $keyFilePath"
Write-Host "The self-signed certificate has been created at $certFilePath"

# Add the certificate to the Trusted Root Certification Authorities store
$cert = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2
$cert.Import($certFilePath)
$store = New-Object System.Security.Cryptography.X509Certificates.X509Store("Root","LocalMachine")
$store.Open("ReadWrite")
$store.Add($cert)
$store.Close()

# Define the password for the PFX file
$pfxPassword = ConvertTo-SecureString -String "{yourpassword}" -Force -AsPlainText

# Export the key and certificate to a PFX file
$pfxPasswordPlainText = "{yourpassword}"
& openssl pkcs12 -export -out $pfxFilePath -inkey $keyFilePath -in $certFilePath -password pass:$pfxPasswordPlainText

Write-Host "The certificate and key have been exported to $pfxFilePath"

# Import the PFX into the LocalMachine\Root store
Import-PfxCertificate -FilePath $pfxFilePath -CertStoreLocation Cert:\LocalMachine\Root -Password $pfxPassword

Write-Host "The PFX has been imported into the LocalMachine\Root store"
