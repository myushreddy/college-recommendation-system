# Start FastAPI Server
# Run this script from the backend directory

Write-Host "Starting College Recommendation API..." -ForegroundColor Green
Write-Host "Server will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Documentation: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Change to backend directory
Set-Location $PSScriptRoot

# Start uvicorn
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
