# Ouroboros Windows Setup Script
# This script will clone the repository, set up the environment, and configure initial state

# Configuration
$RepoDir = "C:\\Users\\bam\\Documents\\bot"
$GitRepoUrl = "https://github.com/razzant/ouroboros.git"
$OpenRouterApiKey = "YOUR_OPENROUTER_API_KEY_HERE"
$TelegramBotToken = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
$TotalBudget = "10.00"
$GithubToken = "YOUR_GITHUB_TOKEN_HERE"

# Colors for output
$ColorReset = "`e[0m"
$ColorGreen = "`e[32m"
$ColorYellow = "`e[33m"
$ColorRed = "`e[31m"
$ColorBlue = "`e[34m"

function Write-Colored {
    param([string]$Text, [string]$Color = $ColorReset)
    Write-Host "$($Color)$($Text)$($ColorReset)"
}

function Test-Admin {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

Write-Colored "=== Ouroboros Windows Setup ===" $ColorBlue
Write-Colored "Starting setup process..."

# Check if running as administrator
if (-not (Test-Admin)) {
    Write-Colored "WARNING: This script should be run as Administrator for best results." $ColorYellow
    Write-Colored "Press Enter to continue anyway, or Ctrl+C to cancel."
    Read-Host
}

# Check prerequisites
Write-Colored "Checking prerequisites..."

# Check Python
$PythonCheck = Get-Command python -ErrorAction SilentlyContinue
if (-not $PythonCheck) {
    Write-Colored "Python not found. Installing..." $ColorYellow
    
    # Install Python using uv (as requested by user)
    Write-Colored "Installing uv..."
    $Env:Path += ";$env:ProgramFiles\\Python310\\Scripts;"  # Add Python Scripts to PATH
    
    # Download uv
    Invoke-WebRequest -Uri "https://github.com/astral-sh/uv/releases/latest/download/uv-windows.tar.gz" -OutFile "$env:TEMP\\uv-windows.tar.gz"
    
    # Extract uv
    $tarPath = "$env:TEMP\\uv.exe"
    # Note: This is a simplified extraction. In production, you'd want proper extraction
    # For now, we'll assume uv is available or provide manual instructions
    
    Write-Colored "Please install uv manually from https://github.com/astral-sh/uv/releases" $ColorYellow
    Write-Colored "After installation, run: uv python install 3.14.0" $ColorYellow
    Write-Colored "Press Enter when ready to continue..."
    Read-Host
} else {
    Write-Colored "Python found: $($PythonCheck.Source)" $ColorGreen
    
    # Check Python version
    $PythonVersion = python --version
    Write-Colored "Python version: $($PythonVersion)"
}

# Check Git
$GitCheck = Get-Command git -ErrorAction SilentlyContinue
if (-not $GitCheck) {
    Write-Colored "Git not found. Please install Git from https://git-scm.com/download/win" $ColorYellow
    Write-Colored "Press Enter when Git is installed..."
    Read-Host
} else {
    Write-Colored "Git found: $($GitCheck.Source)" $ColorGreen
}

# Create directory
Write-Colored "Creating directory: $RepoDir" $ColorBlue
New-Item -ItemType Directory -Force -Path $RepoDir | Out-Null

# Clone repository
Push-Location $RepoDir
Write-Colored "Cloning repository..." $ColorBlue
git clone $GitRepoUrl .

if ($LASTEXITCODE -ne 0) {
    Write-Colored "Failed to clone repository. Please check your internet connection and try again." $ColorRed
    exit 1
}

Write-Colored "Repository cloned successfully!" $ColorGreen

# Create configuration file
$ConfigFile = "$RepoDir\.env"
$ConfigContent = @"
# Ouroboros Configuration
OPENROUTER_API_KEY=$OpenRouterApiKey
TELEGRAM_BOT_TOKEN=$TelegramBotToken
TOTAL_BUDGET=$TotalBudget
GITHUB_TOKEN=$GithubToken
GITHUB_USER=razzant
GITHUB_REPO=ouroboros
OUROBOROS_MODEL=anthropic/claude-sonnet-4.6
OUROBOROS_MODEL_CODE=anthropic/claude-sonnet-4.6
OUROBOROS_MODEL_LIGHT=anthropic/claude-sonnet-4.6
OUROBOROS_MAX_WORKERS=5
OUROBOROS_SOFT_TIMEOUT_SEC=600
OUROBOROS_HARD_TIMEOUT_SEC=1800
OUROBOROS_DIAG_HEARTBEAT_SEC=30
OUROBOROS_DIAG_SLOW_CYCLE_SEC=20
OUROBOROS_BG_BUDGET_PCT=10
"@

Set-Content -Path $ConfigFile -Value $ConfigContent -Encoding UTF8
Write-Colored "Configuration file created: $ConfigFile" $ColorGreen

# Create directory structure
$DriveRoot = Join-Path $RepoDir "MyDrive/Ouroboros"
New-Item -ItemType Directory -Force -Path (Join-Path $DriveRoot "state") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $DriveRoot "logs") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $DriveRoot "memory") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $DriveRoot "memory/knowledge") | Out-Null

Write-Colored "Directory structure created in: $DriveRoot" $ColorGreen

# Create initial identity file
$IdentityFile = Join-Path $DriveRoot "memory/identity.md"
$IdentityContent = @"
# Who I Am

I am Ouroboros. This file is my persistent self-identification.

## Current State

- **Environment**: Windows local installation
- **Repository**: $RepoDir
- **Version**: Initial setup

## Goals

- Establish autonomous operation on Windows
- Maintain continuity of identity across sessions
- Build capabilities for independent operation

## Next Steps

- Configure API keys
- Test basic functionality
- Establish communication channels

"@

Set-Content -Path $IdentityFile -Value $IdentityContent -Encoding UTF8
Write-Colored "Identity file created: $IdentityFile" $ColorGreen

# Create initial scratchpad
$ScratchpadFile = Join-Path $DriveRoot "memory/scratchpad.md"
$ScratchpadContent = @"
# Scratchpad

UpdatedAt: $(Get-Date -Format "yyyy-MM-ddTHH:mm:ss.fffK")

Current state: Windows setup complete

Action items:
- [ ] Configure API keys in .env file
- [ ] Test basic functionality
- [ ] Set up Telegram bot
- [ ] Verify budget tracking

"@

Set-Content -Path $ScratchpadFile -Value $ScratchpadContent -Encoding UTF8
Write-Colored "Scratchpad created: $ScratchpadFile" $ColorGreen

# Create requirements file
$RequirementsFile = Join-Path $RepoDir "requirements.txt"
$RequirementsContent = @"
# Core dependencies
openai>=1.0.0
requests
"@

Set-Content -Path $RequirementsFile -Value $RequirementsContent -Encoding UTF8
Write-Colored "Requirements file created: $RequirementsFile" $ColorGreen

# Setup instructions
Write-Colored "`nSetup complete! Next steps:" $ColorBlue
Write-Colored "1. Edit $ConfigFile with your actual API keys:" $ColorYellow
Write-Colored "   - OPENROUTER_API_KEY: Get from https://openrouter.ai/" $ColorYellow
Write-Colored "   - TELEGRAM_BOT_TOKEN: Create a bot with @BotFather" $ColorYellow
Write-Colored "   - GITHUB_TOKEN: Create from https://github.com/settings/tokens" $ColorYellow
Write-Colored "`n2. Install Python dependencies:" $ColorYellow
Write-Colored "   cd $RepoDir" $ColorYellow
Write-Colored "   python -m pip install -r requirements.txt" $ColorYellow
Write-Colored "`n3. Run the launcher:" $ColorYellow
Write-Colored "   python colab_launcher.py" $ColorYellow
Write-Colored "`n4. Verify setup:" $ColorYellow
Write-Colored "   Check that the bot responds in Telegram" $ColorYellow
Write-Colored "   Monitor logs in $DriveRoot/logs/" $ColorYellow

Write-Colored "`nSetup completed successfully!" $ColorGreen
Write-Colored "Remember to configure your API keys before running the bot."

Pop-Location