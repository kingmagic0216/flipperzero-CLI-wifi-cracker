# Security Configuration Guide

This document explains how to configure security settings for the WiFi Cracker application.

## Security Features

The application includes two security mechanisms:

1. **SECRET_KEY**: Used for Flask session security
2. **Authentication**: Optional password protection for the web interface
3. **Network Access Control**: Option to restrict access to localhost only

## Configuration via Environment Variables

### 1. SECRET_KEY (Recommended)

**Default**: Automatically generates a secure random key on each startup

**To set a custom key**:
```bash
# Windows (PowerShell)
$env:WIFI_CRACKER_SECRET_KEY="your-secure-random-key-here"

# Windows (CMD)
set WIFI_CRACKER_SECRET_KEY=your-secure-random-key-here

# Linux/Mac
export WIFI_CRACKER_SECRET_KEY="your-secure-random-key-here"
```

**Note**: If you don't set this, a new random key is generated each time the server starts. For production use, set a fixed key.

### 2. Authentication (Optional but Recommended)

**To enable password protection**:
```bash
# Windows (PowerShell)
$env:WIFI_CRACKER_PASSWORD="your-secure-password"

# Windows (CMD)
set WIFI_CRACKER_PASSWORD=your-secure-password

# Linux/Mac
export WIFI_CRACKER_PASSWORD="your-secure-password"
```

When authentication is enabled:
- All routes require HTTP Basic Authentication
- Use **any username** (it's ignored)
- Use the password you set in `WIFI_CRACKER_PASSWORD`
- Browsers will prompt for login automatically

### 3. Network Access Restriction (Optional)

**To restrict access to localhost only** (recommended for security):
```bash
# Windows (PowerShell)
$env:WIFI_CRACKER_HOST="127.0.0.1"

# Windows (CMD)
set WIFI_CRACKER_HOST=127.0.0.1

# Linux/Mac
export WIFI_CRACKER_HOST="127.0.0.1"
```

**Default**: `0.0.0.0` (accessible from network)

When restricted to localhost:
- Only accessible from the computer running the server
- Cannot be accessed from phones/tablets on the network
- More secure but less convenient

## Recommended Security Setup

For **maximum security** (production use):
```bash
# Set all three environment variables
export WIFI_CRACKER_SECRET_KEY="$(openssl rand -hex 32)"
export WIFI_CRACKER_PASSWORD="your-strong-password-here"
export WIFI_CRACKER_HOST="127.0.0.1"
```

For **convenience** (local network, trusted environment):
```bash
# Just set a password
export WIFI_CRACKER_PASSWORD="your-password-here"
# Leave others as defaults (network access enabled, auto-generated SECRET_KEY)
```

## Security Status Display

When you start the server, it will display the current security configuration:

```
🔒 Security Status:
  ✓ Authentication: ENABLED (password required)
  ✓ Network Access: RESTRICTED to localhost only
```

or

```
🔒 Security Status:
  ⚠ Authentication: DISABLED (set WIFI_CRACKER_PASSWORD to enable)
  ⚠ Network Access: OPEN to all devices on network
```

## Making Environment Variables Permanent

### Windows

**PowerShell** (User-level):
```powershell
[System.Environment]::SetEnvironmentVariable('WIFI_CRACKER_PASSWORD', 'your-password', 'User')
```

**CMD** (User-level):
```cmd
setx WIFI_CRACKER_PASSWORD "your-password"
```

### Linux/Mac

Add to `~/.bashrc` or `~/.zshrc`:
```bash
export WIFI_CRACKER_PASSWORD="your-password"
export WIFI_CRACKER_SECRET_KEY="your-secret-key"
export WIFI_CRACKER_HOST="127.0.0.1"
```

Then reload:
```bash
source ~/.bashrc  # or source ~/.zshrc
```

## Security Best Practices

1. **Always set a password** if the server is accessible from the network
2. **Use strong passwords** (at least 12 characters, mix of letters, numbers, symbols)
3. **Restrict to localhost** if you don't need network access
4. **Set a fixed SECRET_KEY** for production deployments
5. **Never commit passwords or keys** to version control
6. **Use HTTPS** in production (requires reverse proxy like nginx)

## Troubleshooting

**Can't access from phone after setting password?**
- Make sure you're entering the password correctly
- Check that `WIFI_CRACKER_HOST` is not set to `127.0.0.1` if you need network access

**Authentication not working?**
- Verify the environment variable is set: `echo $WIFI_CRACKER_PASSWORD` (Linux/Mac) or `echo %WIFI_CRACKER_PASSWORD%` (Windows)
- Make sure you're using HTTP Basic Auth (browser should prompt automatically)

**Want to disable authentication?**
- Simply unset the environment variable or restart without it set

