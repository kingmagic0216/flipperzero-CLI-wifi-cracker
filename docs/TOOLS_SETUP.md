# Tools Setup Options

You have two options for organizing the required tools (hashcat and hcxtools):

## Option 1: System-Wide Installation (Current Setup) ✅ Recommended

**Current Status:**
- ✅ Hashcat: `C:\hashcat\hashcat-7.1.2\` (in system PATH)
- ✅ hcxtools: Installed in WSL

**Pros:**
- Tools available system-wide for all projects
- Smaller repository size
- Standard installation approach
- Easy to update tools independently

**Cons:**
- Requires PATH setup
- Tools need to be installed separately

**This is the recommended setup and what you currently have!**

---

## Option 2: Repo-Local Installation (Portable)

If you want everything self-contained in the repo:

### Setup Steps:

1. **Create tools/bin directory:**
   ```powershell
   mkdir tools\bin
   ```

2. **Copy hashcat to repo:**
   ```powershell
   # Copy hashcat folder
   xcopy /E /I C:\hashcat\hashcat-7.1.2 tools\bin\hashcat-7.1.2
   ```

3. **Add to .gitignore (optional):**
   ```
   # Tools (if you don't want to commit them)
   tools/bin/hashcat-7.1.2/
   ```

**Pros:**
- Fully portable - everything in one folder
- No PATH setup needed
- Easy to share/distribute
- Version control for tool versions

**Cons:**
- Larger repository size (~400MB for hashcat)
- Duplicates tools if used in multiple projects
- Need to update tools in each repo

---

## How the App Finds Tools

The app checks in this order:

1. **Local tools directory:** `tools/bin/` (if exists)
2. **System PATH:** Standard Windows PATH
3. **WSL:** For hcxtools (automatically detected)

So you can use **either** approach - the app will find tools in either location!

---

## Recommendation

**Keep your current setup (Option 1)** - it's cleaner and more standard. The app already works with it.

Only use Option 2 if you:
- Need a fully portable/self-contained setup
- Want to distribute the entire project with tools included
- Don't want to rely on system PATH

---

## Current Status

✅ **You're all set!** Both tools are installed and the app can find them:
- Hashcat: In PATH (after terminal restart) or at `C:\hashcat\hashcat-7.1.2\`
- hcxtools: Available via WSL (automatically detected)

No need to move anything - your current setup is perfect!

