# PowerShell script to upload files to Google Cloud VM
# Usage: ./upload-to-vm.ps1

# Configuration - UPDATE THESE VALUES
$INSTANCE_NAME = "your-instance-name"  # Your VM instance name
$ZONE = "your-zone"                     # e.g., us-central1-a
$DESTINATION_PATH = "~/gph-backend"

Write-Host "========================================" -ForegroundColor Green
Write-Host "Uploading GPH Backend to Google Cloud VM" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Check if gcloud is installed
if (!(Get-Command gcloud -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: gcloud CLI not found!" -ForegroundColor Red
    Write-Host "Please install Google Cloud SDK from: https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    exit 1
}

Write-Host "Instance: $INSTANCE_NAME" -ForegroundColor Cyan
Write-Host "Zone: $ZONE" -ForegroundColor Cyan
Write-Host "Destination: $DESTINATION_PATH" -ForegroundColor Cyan
Write-Host ""

$continue = Read-Host "Continue with upload? (y/n)"
if ($continue -ne "y") {
    Write-Host "Upload cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Uploading files..." -ForegroundColor Yellow

try {
    # Upload all files
    gcloud compute scp --recurse . "${INSTANCE_NAME}:${DESTINATION_PATH}" --zone=$ZONE
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Upload Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. SSH into your VM:" -ForegroundColor White
    Write-Host "   gcloud compute ssh $INSTANCE_NAME --zone=$ZONE" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "2. Run deployment:" -ForegroundColor White
    Write-Host "   cd $DESTINATION_PATH" -ForegroundColor Yellow
    Write-Host "   chmod +x deploy.sh" -ForegroundColor Yellow
    Write-Host "   sudo bash deploy.sh" -ForegroundColor Yellow
    Write-Host ""
}
catch {
    Write-Host ""
    Write-Host "ERROR: Upload failed!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Verify instance name and zone are correct" -ForegroundColor White
    Write-Host "2. Check if you're logged in: gcloud auth list" -ForegroundColor White
    Write-Host "3. Verify VM is running: gcloud compute instances list" -ForegroundColor White
    exit 1
}
