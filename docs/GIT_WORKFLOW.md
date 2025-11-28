# 🔄 Git Workflow - Staying Synced with Moon Dev

## 📊 Your Fork Setup

```
Moon Dev's Original Repo (upstream)
    ↓ (you forked)
Your GitHub Fork (origin)
    ↓ (you cloned)
Your Local Machine
```

---

## 🚀 Quick Commands

### **Check Status:**
```bash
cd /Users/vamshi/poly/moon-dev-ai-agents

# See what you've changed locally
git status

# See your recent commits
git log --oneline -5

# See Moon Dev's recent commits
git log upstream/main --oneline -5
```

### **Sync with Moon Dev (Automated):**
```bash
./SYNC_WITH_MOONDEV.sh
```

This script will:
1. ✅ Fetch latest from Moon Dev
2. ✅ Show you what's new
3. ✅ Ask before merging
4. ✅ Ask before pushing to your fork

### **Sync with Moon Dev (Manual):**
```bash
# 1. Fetch latest from Moon Dev's repo
git fetch upstream

# 2. See what's new
git log --oneline main..upstream/main

# 3. See what files changed
git diff --stat main upstream/main

# 4. Merge updates
git merge upstream/main

# 5. Push to your fork
git push origin main
```

---

## 💾 Saving Your Work

### **Commit Your Changes:**
```bash
# See what you've changed
git status
git diff

# Add files
git add <filename>
# Or add all:
git add .

# Commit
git commit -m "Your commit message

Co-authored-by: factory-droid[bot] <138933559+factory-droid[bot]@users.noreply.github.com>"

# Push to your fork
git push origin main
```

### **Quick Save Everything:**
```bash
# Add all changes and commit
git add .
git commit -m "Save current work

Co-authored-by: factory-droid[bot] <138933559+factory-droid[bot]@users.noreply.github.com>"
git push origin main
```

---

## 🔄 Common Workflows

### **Workflow 1: You Made Changes, Now Sync with Moon Dev**

```bash
# 1. Commit your changes first
git add .
git commit -m "Your changes"
git push origin main

# 2. Then sync with Moon Dev
./SYNC_WITH_MOONDEV.sh
```

### **Workflow 2: Moon Dev Updated, You Have No Changes**

```bash
# Just sync
./SYNC_WITH_MOONDEV.sh
```

### **Workflow 3: Both You AND Moon Dev Made Changes**

```bash
# 1. Commit yours first
git add .
git commit -m "Your changes"

# 2. Fetch Moon Dev's
git fetch upstream

# 3. Merge (may have conflicts)
git merge upstream/main

# 4. If conflicts, fix them:
#    - Edit conflicted files
#    - git add <fixed-files>
#    - git commit

# 5. Push
git push origin main
```

---

## 🆘 Troubleshooting

### **"You have uncommitted changes"**

**Option A: Commit them**
```bash
git add .
git commit -m "WIP: save current work"
```

**Option B: Stash them (temporarily hide)**
```bash
git stash
# Do your git operations
git stash pop  # Restore your changes
```

### **"Merge conflict!"**

Don't panic! This just means you and Moon Dev edited the same file.

```bash
# 1. See conflicted files
git status

# 2. Open each file and look for:
<<<<<<< HEAD
Your changes
=======
Moon Dev's changes
>>>>>>> upstream/main

# 3. Edit the file - keep what you want, delete the markers

# 4. Mark as resolved
git add <fixed-file>

# 5. Finish merge
git commit

# 6. Push
git push origin main
```

### **"I messed up, undo!"**

**Undo last commit (keep changes):**
```bash
git reset --soft HEAD~1
```

**Undo last commit (discard changes):**
```bash
git reset --hard HEAD~1
```

**Undo changes to a file:**
```bash
git checkout -- <filename>
```

---

## 📁 What's Where

### **Remotes:**
```bash
origin    = Your GitHub fork (VamshiVerma/moon-dev-ai-agents)
upstream  = Moon Dev's original (moondevonyt/moon-dev-ai-agents)
```

### **Branches:**
```bash
main              = Your current local branch
origin/main       = Your fork's main branch on GitHub
upstream/main     = Moon Dev's main branch
```

### **Check remotes:**
```bash
git remote -v
```

---

## 🎯 Best Practices

### ✅ **DO:**
- Commit often with clear messages
- Sync with upstream regularly (weekly)
- Test before committing
- Push your commits to your fork
- Use the sync script for easy updates

### ❌ **DON'T:**
- Commit sensitive data (.env files, API keys)
- Force push unless you know what you're doing
- Delete .git directory
- Commit directly to upstream (you can't anyway)

---

## 🔍 Checking Your Setup

```bash
# See your remotes
git remote -v

# Should show:
# origin    https://github.com/VamshiVerma/moon-dev-ai-agents.git (fetch)
# origin    https://github.com/VamshiVerma/moon-dev-ai-agents.git (push)
# upstream  https://github.com/moondevonyt/moon-dev-ai-agents.git (fetch)
# upstream  https://github.com/moondevonyt/moon-dev-ai-agents.git (push)

# See your branch
git branch -vv

# See latest commits
git log --oneline --graph --all -10
```

---

## 📚 Quick Reference Card

| Action | Command |
|--------|---------|
| **Save your work** | `git add . && git commit -m "msg" && git push` |
| **Sync with Moon Dev** | `./SYNC_WITH_MOONDEV.sh` |
| **Check status** | `git status` |
| **See what changed** | `git diff` |
| **See commits** | `git log --oneline -10` |
| **Undo last commit** | `git reset --soft HEAD~1` |
| **Discard changes** | `git checkout -- <file>` |
| **Create branch** | `git checkout -b new-branch` |
| **Switch branch** | `git checkout main` |

---

## 🎓 Learning More

**Good Git tutorials:**
- https://learngitbranching.js.org/ (Interactive!)
- https://ohshitgit.com/ (For when things go wrong)
- https://git-scm.com/book/en/v2 (Official book)

**Common git terms:**
- **Repository (repo):** Your project's folder tracked by git
- **Commit:** A saved snapshot of your code
- **Branch:** A parallel version of your code
- **Remote:** A version of your repo on GitHub
- **Fork:** Your personal copy of someone else's repo
- **Upstream:** The original repo you forked from
- **Origin:** Your fork on GitHub
- **Merge:** Combining two branches
- **Pull:** Download and merge from remote
- **Push:** Upload your commits to remote
- **Fetch:** Download from remote (without merging)

---

**Built with ❤️ by Moon Dev**

Remember: When in doubt, commit your work first! 💾
