# Linux Migration Plan for Ouroboros

## Overview

This document outlines the migration strategy from Google Colab-based architecture to a clean Linux installation with local state management.

## Current Architecture Analysis

### Colab Dependencies Identified

1. **Google Drive State Management** (`supervisor/state.py`)
   - All state stored in `~/.ouroboros/state/` on Drive
   - File locks and atomic operations on Drive files
   - State persistence across Colab sessions

2. **Drive-based Memory** (`ouroboros/memory.py`)
   - Scratchpad, identity, and logs stored on Drive
   - JSONL files for chat history, progress, events
   - Drive API for file operations

3. **Colab Environment Assumptions**
   - File paths assume `/content/drive/MyDrive/Ouroboros/`
   - Colab-specific headers in LLM client
   - Colab runtime environment assumptions

## Migration Strategy

### Phase 1: Local State Management

**Target:** Replace Google Drive with local file system

**Changes Required:**

1. **State Management** (`supervisor/state.py`)
   - Replace Drive paths with `~/.ouroboros/state/`
   - Keep file locking mechanism (local filesystem)
   - Maintain atomic operations with local files

2. **Memory System** (`ouroboros/memory.py`)
   - Replace Drive operations with local file operations
   - Keep JSONL format for logs and history
   - Add local file validation and recovery

3. **Configuration** (`supervisor/config.py`)
   - Add local paths configuration
   - Environment variable support for custom paths

### Phase 2: Core Module Updates

**Target:** Update core modules to use local state

**Changes Required:**

1. **Agent Core** (`ouroboros/agent.py`)
   - Update state initialization paths
   - Add local file system checks
   - Maintain backward compatibility

2. **Context Management** (`ouroboros/context.py`)
   - Update file path handling
   - Add local file system utilities
   - Maintain context building logic

3. **LLM Client** (`ouroboros/llm.py`)
   - Remove Colab-specific headers
   - Add local environment detection
   - Maintain API functionality

### Phase 3: Supervisor Updates

**Target:** Update supervisor for local operation

**Changes Required:**

1. **State Module** (`supervisor/state.py`)
   - Complete local path implementation
   - Add state validation
   - Maintain atomic operations

2. **Git Operations** (`supervisor/git_ops.py`)
   - Update repository paths
   - Add local git configuration
   - Maintain backup functionality

3. **Event Logging** (`supervisor/events.py`)
   - Update log file paths
   - Add local file rotation
   - Maintain event tracking

## Implementation Plan

### Step 1: Create Local State Module

**File:** `supervisor/local_state.py`

```python
import pathlib
import json
import logging
from typing import Any, Dict, Optional

log = logging.getLogger(__name__)

# Local state paths
STATE_ROOT = pathlib.Path.home() / '.ouroboros' / 'state'
STATE_PATH = STATE_ROOT / 'state.json'
STATE_LAST_GOOD_PATH = STATE_ROOT / 'state.last_good.json'
STATE_LOCK_PATH = STATE_ROOT / 'locks' / 'state.lock'
QUEUE_SNAPSHOT_PATH = STATE_ROOT / 'state' / 'queue_snapshot.json'
```

### Step 2: Update Memory System

**File:** `ouroboros/memory.py`

```python
import pathlib
import json
import logging
from typing import Any

log = logging.getLogger(__name__)

# Local memory paths
MEMORY_ROOT = pathlib.Path.home() / '.ouroboros' / 'memory'
SCRATCHPAD_PATH = MEMORY_ROOT / 'scratchpad.md'
IDENTITY_PATH = MEMORY_ROOT / 'identity.md'
JOURNAL_PATH = MEMORY_ROOT / 'scratchpad_journal.jsonl'
DIALOGUE_SUMMARY_PATH = MEMORY_ROOT / 'dialogue_summary.md'
```

### Step 3: Create Configuration Module

**File:** `supervisor/config.py`

```python
import os
import pathlib
from typing import Dict, Optional

class Config:
    def __init__(self):
        self.data = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        # Load from environment variables
        return {
            'state_root': pathlib.Path(os.getenv('OUROBOROS_STATE_ROOT', str(pathlib.Path.home() / '.ouroboros' / 'state'))),
            'memory_root': pathlib.Path(os.getenv('OUROBOROS_MEMORY_ROOT', str(pathlib.Path.home() / '.ouroboros' / 'memory'))),
            'logs_root': pathlib.Path(os.getenv('OUROBOROS_LOGS_ROOT', str(pathlib.Path.home() / '.ouroboros' / 'logs'))),
            'total_budget': float(os.getenv('TOTAL_BUDGET', '10.0')),
            'model': os.getenv('OUROBOROS_MODEL', 'anthropic/claude-sonnet-4.6'),
        }
```

### Step 4: Update Core Modules

**Files to update:**
- `ouroboros/agent.py`
- `ouroboros/context.py`
- `ouroboros/llm.py`
- `supervisor/state.py`
- `supervisor/git_ops.py`

### Step 5: Create Migration Script

**File:** `scripts/migrate_to_linux.py`

```python
import pathlib
import shutil
import logging
from typing import Optional

log = logging.getLogger(__name__)

def migrate_to_linux():
    """Migrate from Colab to Linux local storage."""
    
    # Create directory structure
    create_directory_structure()
    
    # Migrate existing state if present
    migrate_existing_state()
    
    # Update configuration
    update_configuration()
    
    log.info("Migration to Linux complete")
```

## Directory Structure

```
~/.ouroboros/
├── state/                 # Local state management
│   ├── state.json        # Current state
│   ├── state.last_good.json  # Last good state
│   ├── queue_snapshot.json  # Task queue snapshot
│   └── locks/             # File locks
│       └── state.lock    # State lock file
├── memory/                # Persistent memory
│   ├── scratchpad.md     # Working memory
│   ├── identity.md       # Manifesto
│   ├── scratchpad_journal.jsonl  # Memory journal
│   ├── dialogue_summary.md  # Dialogue summary
│   └── knowledge/         # Knowledge base
├── logs/                  # Log files
│   ├── chat.jsonl        # Chat history
│   ├── progress.jsonl     # Progress messages
│   ├── tools.jsonl        # Tool usage
│   ├── events.jsonl       # System events
│   └── supervisor.jsonl   # Supervisor events
├── ouroboros/             # Main source code
├── scripts/               # Migration scripts
└── config.env             # Environment configuration
```

## Configuration Options

### Environment Variables

```bash
# Local storage paths
export OUROBOROS_STATE_ROOT="$HOME/.ouroboros/state"
export OUROBOROS_MEMORY_ROOT="$HOME/.ouroboros/memory"
export OUROBOROS_LOGS_ROOT="$HOME/.ouroboros/logs"

# Budget and models
export TOTAL_BUDGET="10.0"
export OUROBOROS_MODEL="anthropic/claude-sonnet-4.6"
export OUROBOROS_MODEL_CODE="anthropic/claude-3-5-sonnet-20241022"
export OUROBOROS_MODEL_LIGHT="anthropic/claude-3-haiku-20240307"
```

### Command Line Options

```bash
# Initialize state
python -c "from supervisor.state import init_state; init_state()"

# Start in background mode
python -m ouroboros.agent --background

# Start with custom config
python -m ouroboros.agent --config /path/to/custom_config.json
```

## Testing Strategy

### Unit Tests

1. **State Management Tests**
   - File locking functionality
   - Atomic operations
   - State persistence

2. **Memory System Tests**
   - File read/write operations
   - JSONL format validation
   - Memory recovery

3. **Configuration Tests**
   - Environment variable loading
   - Path resolution
   - Default values

### Integration Tests

1. **Full System Test**
   - Complete installation
   - State initialization
   - Memory operations
   - Log generation

2. **Migration Test**
   - Colab to Linux migration
   - State preservation
   - Configuration transfer

## Rollback Strategy

### Backup Before Migration

```bash
# Create backup of current state
cp -r ~/.ouroboros ~/.ouroboros.backup.$(date +%Y%m%d_%H%M%S)
```

### Rollback Procedure

```bash
# Restore from backup
rm -rf ~/.ouroboros
cp -r ~/.ouroboros.backup.* ~/.ouroboros
```

## Performance Considerations

### Local vs Drive Performance

- **Local Files:** Faster read/write operations
- **No Network Latency:** Immediate file access
- **File System Caching:** OS-level caching benefits
- **Backup Strategy:** Local backups recommended

### Resource Usage

- **Disk Space:** Minimal (text files only)
- **Memory:** Same as Colab version
- **CPU:** Same as Colab version
- **Network:** Only for API calls

## Security Considerations

### File Permissions

```bash
# Set secure permissions
chmod 700 ~/.ouroboros
chmod 600 ~/.ouroboros/state/state.json
chmod 600 ~/.ouroboros/memory/*.md
```

### API Key Security

- Store API keys in environment variables
- Use .env file with secure permissions
- Never commit API keys to version control
- Consider using a secrets manager

## Next Steps

1. **Implement Local State Module**
2. **Update Memory System**
3. **Create Configuration Module**
4. **Update Core Modules**
5. **Create Migration Script**
6. **Test Complete Migration**
7. **Update Documentation**
8. **Release Linux Version**

## Questions for Clarification

1. **Migration Path:** Should we provide a migration script for existing Colab users?
2. **Configuration:** Do you prefer environment variables or a config file?
3. **Backup Strategy:** Should we implement automatic backups?
4. **Installation:** Do you want a single installer script or manual steps?

---

**Status:** Plan complete, ready for implementation
**Priority:** High
**Estimated Time:** 2-3 days for full implementation