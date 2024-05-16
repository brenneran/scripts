# Default values for parameters
$CertificateName = 'ASP.NET Core HTTPS development certificate'
$TargetStoreLocation = 'LocalMachine'
$TargetStoreName = 'Root'

# Start the process to generate the development trust certificate
$process = Start-Process -FilePath 'dotnet' -ArgumentList 'dev-certs https' -PassThru -Wait

# Check if the certificate generation process completed successfully
if ($process.ExitCode -ne 0) {
    Write-Error "Failed to generate the development trust certificate using 'dotnet dev-certs https'. Exit code: $($process.ExitCode)"
    exit 1
}

# Check if the certificate already exists in LocalMachine's Root store
$certificates = Get-ChildItem -Path "Cert:\$($TargetStoreLocation)\$($TargetStoreName)"
$certificate = $certificates | Where-Object { $_.FriendlyName -eq $CertificateName }

if ($certificate -eq $null) {
    Write-Warning "Certificate '$CertificateName' not found in Cert:\$($TargetStoreLocation)\$($TargetStoreName). Attempting to import the certificate..."

    # Path to export the certificate PFX file and its password
    $pfxPath = "C:\Downloads\dotnet.pfx"
    $password = "123456"

    # Export the HTTPS development certificate using dotnet dev-certs
    dotnet dev-certs https --export-path $pfxPath --password $password

    # Check if the PFX file was successfully created
    if (-not (Test-Path $pfxPath)) {
        Write-Error "Failed to export the certificate. PFX file not found at '$pfxPath'."
        exit 1
    }

    # Import the exported PFX certificate into the LocalMachine's trusted root certificate store (Root)
    $cert = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2
    try {
        $cert.Import($pfxPath, $password, [System.Security.Cryptography.X509Certificates.X509KeyStorageFlags]::PersistKeySet)
    } catch {
        Write-Error "Failed to import the certificate. $_"
        exit 1
    }

    # Open the certificate store for the LocalMachine's trusted root certificate store (Root)
    $store = New-Object System.Security.Cryptography.X509Certificates.X509Store($TargetStoreName, $TargetStoreLocation)
    $store.Open([System.Security.Cryptography.X509Certificates.OpenFlags]::ReadWrite)

    # Add the imported certificate to the LocalMachine's trusted root certificate store (Root)
    try {
        $store.Add($cert)
    } catch {
        Write-Error "Failed to add the certificate to LocalMachine's Root store. $_"
        exit 1
    }

    # Close the LocalMachine's trusted root certificate store (Root)
    $store.Close()

    Write-Host "Certificate '$CertificateName' imported into Cert:\$($TargetStoreLocation)\$($TargetStoreName)'" -ForegroundColor Blue
}
else {
    Write-Host "Certificate '$CertificateName' already exists in Cert:\$($TargetStoreLocation)\$($TargetStoreName)'" -ForegroundColor Green
}
