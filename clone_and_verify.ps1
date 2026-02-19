# Ouroboros Git Clone and Verification Script for Windows
# This script clones the repository, verifies the clone, and checks essential files

# Configuration
$RepoDir = "C:\\Users\\bam\\Documents\\bot"
$GitRepoUrl = "https://github.com/joi-lab/ouroboros.git"
$Branch = "ouroboros"

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
    return $principal.IsInRrole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

Write-Colored "=== Ouroboros Git Clone and Verification ===" $ColorBlue
Write-Colored "Starting clone and verification process..."

# Check if running as administrator
if (-not (Test-Admin)) {
    Write-Colored "WARNING: This script should be run as Administrator for best results." $ColorYellow
    Write-Colored "Press Enter to continue anyway, or Ctrl+C to cancel."
    Read-Host
}

# Check prerequisites
Write-Colored "Checking prerequisites..." $ColorBlue

# Check Git
$GitCheck = Get-Command git -ErrorAction SilentlyContinue
if (-not $GitCheck) {
    Write-Colored "Git not found. Please install Git from https://git-scm.com/download/win" $ColorRed
    Write-Colored "Press Enter to open the download page..."
    Start-Process "https://git-scm.com/download/win"
    Read-Host
    exit 1
} else {
    Write-Colored "Git found: $($GitCheck.Source)" $ColorGreen
}

# Check directory
Write-Colored "Checking target directory: $RepoDir" $ColorBlue
if (-not (Test-Path $RepoDir)) {
    New-Item -ItemType Directory -Force -Path $RepoDir | Out-Null
    Write-Colored "Created directory: $RepoDir" $ColorGreen
} else {
    Write-Colored "Directory exists: $RepoDir" $ColorGreen
}

# Test write permissions
try {
    $testFile = Join-Path $RepoDir "test_permission.txt"
    Set-Content -Path $testFile -Value "test" -Encoding UTF8
    Remove-Item -Path $testFile
    Write-Colored "Write permission OK: $RepoDir" $ColorGreen
} catch {
    Write-Colored "ERROR: Cannot write to directory: $RepoDir" $ColorRed
    Write-Colored "Please check permissions or choose a different directory." $ColorRed
    exit 1
}

# Clone repository
Push-Location $RepoDir
Write-Colored "Cloning repository from $GitRepoUrl (branch: $Branch)..." $ColorBlue

if (Test-Path "ouroboros") {
    Write-Colored "Repository already exists. Updating..." $ColorYellow
    git pull origin $Branch
    
    if ($LASTEXITCODE -ne 0) {
        Write-Colored "Failed to update repository. Please check your internet connection and try again." $ColorRed
        exit 1
    }
} else {
    git clone --branch $Branch $GitRepoUrl ouroboros
    
    if ($LASTEXITCODE -ne 0) {
        Write-Colored "Failed to clone repository. Please check your internet connection and try again." $ColorRed
        exit 1
    }
}

Write-Colored "Repository cloned/updated successfully!" $ColorGreen

# Verify clone
$repoPath = Join-Path $RepoDir "ouroboros"
Write-Colored "Verifying repository contents..." $ColorBlue

# Check if repository directory exists
if (-not (Test-Path $repoPath)) {
    Write-Colored "ERROR: Repository directory not found after clone." $ColorRed
    exit 1
}

# Check essential files
$essentialFiles = @("README.md", "BIBLE.md", "VERSION", "ouroboros/agent.py", "colab_launcher.py")
$missingFiles = @()

foreach ($file in $essentialFiles) {
    $filePath = Join-Path $repoPath $file
    if (Test-Path $filePath) {
        Write-Colored "  ✓ $file" $ColorGreen
    } else {
        Write-Colored "  ✗ $file (missing)" $ColorRed
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Colored "WARNING: $($missingFiles.Count) essential files missing" $ColorYellow
    Write-Colored "This may affect functionality. Please check the repository." $ColorYellow
}

# Verify git status
Write-Colored "Checking git status..." $ColorBlue
git status

# Check current branch
$currentBranch = git branch --show-current
Write-Colored "Current branch: $currentBranch" $ColorGreen

if ($currentBranch -ne $Branch) {
    Write-Colored "WARNING: Expected branch '$Branch' but found '$currentBranch'" $ColorYellow
}

# Get repository size
$repoSize = (Get-ChildItem $repoPath -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
Write-Colored "Repository size: {0:N2} MB" -f $repoSize $ColorGreen

# Create summary
Write-Colored "`nClone Summary:" $ColorBlue
Write-Colored "  Target Directory: $RepoDir" $ColorGreen
Write-Colored "  Repository URL: $GitRepoUrl" $ColorGreen
Write-Colored "  Branch: $Branch" $ColorGreen
Write-Colored "  Repository Location: $repoPath" $ColorGreen
Write-Colored "  Repository Size: {0:N2} MB" -f $repoSize $ColorGreen

Write-Colored "`nVerification completed!" $ColorGreen
Write-Colored "Next steps:" $ColorBlue
Write-Colored "1. Review the configuration files" $ColorYellow
Write-Colored "2. Set up API keys in configuration" $ColorYellow
Write-Colored "3. Run the launcher script" $ColorYellow
Write-Colored "4. Test basic functionality" $ColorYellow

Pop-Location