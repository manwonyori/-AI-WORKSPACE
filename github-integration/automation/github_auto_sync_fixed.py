#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
github_auto_sync_fixed.py

Purpose:
- Robust, encoding-safe Git auto sync script.
- Fixes common index corruption automatically.
- Excludes sensitive/unwanted files (updates .gitignore).
- Creates safe commit messages and pushes to remote.

Usage:
  python github_auto_sync_fixed.py --repo "C:\\Users\\8899y\\detail-pages" --remote origin --branch main \\
    --exclude "node_modules/,dist/,*.log,.DS_Store" \\
    --message "chore: automated sync"

Notes:
- If the repo has no remote, set it before running or pass --set-remote-url.
- The script writes logs to &lt;repo&gt;/.git/auto_sync.log
"""

import os
import sys
import argparse
import subprocess
import datetime
import shlex

DEFAULT_EXCLUDES = [
    "node_modules/",
    "dist/",
    ".cache/",
    "*.log",
    ".DS_Store",
    "Thumbs.db",
]

def run(cmd, cwd, check=True):
    """Run a shell command with UTF-8 text handling."""
    # Ensure environment forces UTF-8 to avoid Unicode issues
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    # Windows-safe execution
    if isinstance(cmd, str):
        cmd_list = shlex.split(cmd)
    else:
        cmd_list = cmd
    proc = subprocess.run(
        cmd_list,
        cwd=cwd,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        shell=False,
    )
    returncode = proc.returncode
    stdout = proc.stdout.strip()
    stderr = proc.stderr.strip()
    if check and returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd_list)}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}")
    return returncode, stdout, stderr

def log_write(repo, msg):
    log_path = os.path.join(repo, ".git", "auto_sync.log")
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}\n"
    try:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "a", encoding="utf-8", errors="replace") as f:
            f.write(line)
    except Exception as e:
        print(f"LOG WRITE ERROR: {e}", file=sys.stderr)
    print(line, end="")

def git_exists(repo):
    return os.path.isdir(os.path.join(repo, ".git"))

def ensure_repo(repo):
    if not os.path.isdir(repo):
        raise FileNotFoundError(f"Repo path not found: {repo}")
    if not git_exists(repo):
        # Initialize if not a git repo
        log_write(repo, "Initializing new git repository (git init)")
        run(["git", "init"], cwd=repo)

def fix_index_if_corrupt(repo):
    # Detect common corruption patterns by attempting a status
    try:
        run(["git", "status"], cwd=repo, check=True)
        return  # status is fine
    except RuntimeError as e:
        msg = str(e)
        suspicious = ("index file corrupt" in msg.lower()) or ("fatal: index" in msg.lower()) or ("index.lock" in msg.lower())
        if not suspicious:
            raise

    log_write(repo, "Detected possible index corruption. Attempting auto-repair...")
    index_path = os.path.join(repo, ".git", "index")
    lock_path = os.path.join(repo, ".git", "index.lock")
    try:
        if os.path.exists(lock_path):
            os.remove(lock_path)
            log_write(repo, f"Removed lock file: {lock_path}")
        if os.path.exists(index_path):
            os.remove(index_path)
            log_write(repo, "Removed corrupted index file.")
        # Rebuild index
        run(["git", "reset"], cwd=repo, check=True)
        log_write(repo, "Rebuilt index with 'git reset'.")
    except Exception as ex:
        raise RuntimeError(f"Failed to repair index: {ex}")

def update_gitignore(repo, excludes):
    if not excludes:
        return
    gi_path = os.path.join(repo, ".gitignore")
    existing = set()
    if os.path.exists(gi_path):
        with open(gi_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                s = line.strip()
                if s and not s.startswith("#"):
                    existing.add(s)
    changes = False
    with open(gi_path, "a", encoding="utf-8", errors="replace") as f:
        for pattern in excludes:
            if pattern not in existing:
                f.write(pattern + "\\n")
                changes = True
    if changes:
        log_write(repo, f"Updated .gitignore with patterns: {excludes}")

def ensure_remote(repo, remote, branch, set_remote_url):
    # Check current remotes
    rc, out, _ = run(["git", "remote", "-v"], cwd=repo, check=False)
    if remote in out:
        log_write(repo, f"Remote '{remote}' already configured.")
    else:
        if set_remote_url:
            # If user passed a URL, add as new remote
            run(["git", "remote", "add", remote, set_remote_url], cwd=repo, check=True)
            log_write(repo, f"Added remote '{remote}': {set_remote_url}")
        else:
            log_write(repo, f"WARNING: Remote '{remote}' not found and no URL provided. Push will fail.")

    # Ensure branch exists and is current
    # Create branch if missing
    rc, out, _ = run(["git", "branch", "--list", branch], cwd=repo, check=False)
    if not out.strip():
        run(["git", "checkout", "-b", branch], cwd=repo, check=True)
        log_write(repo, f"Created and switched to branch '{branch}'.")
    else:
        # Switch to branch
        run(["git", "checkout", branch], cwd=repo, check=True)
        log_write(repo, f"Switched to branch '{branch}'.")

def safe_commit(repo, message):
    # Stage all changes and commit if there is anything to commit
    run(["git", "add", "."], cwd=repo, check=True)
    rc, out, _ = run(["git", "status", "--porcelain"], cwd=repo, check=False)
    if not out.strip():
        log_write(repo, "No changes to commit.")
        return False
    if not message:
        message = "chore: automated sync"
    # Avoid non-ASCII issues in commit messages by forcing UTF-8 file encoding
    log_write(repo, f"Creating commit: {message}")
    run(["git", "commit", "-m", message], cwd=repo, check=True)
    return True

def safe_push(repo, remote, branch):
    try:
        run(["git", "push", "-u", remote, branch], cwd=repo, check=True)
        log_write(repo, f"Pushed to {remote}/{branch}.")
    except RuntimeError as e:
        log_write(repo, f"Push failed: {e}")
        # Possible first push or remote ahead: try pull --rebase, then push again
        try:
            run(["git", "pull", remote, branch, "--rebase"], cwd=repo, check=True)
            log_write(repo, "Pulled with rebase.")
            run(["git", "push", "-u", remote, branch], cwd=repo, check=True)
            log_write(repo, f"Pushed to {remote}/{branch} after rebase.")
        except Exception as e2:
            raise RuntimeError(f"Push still failing after rebase: {e2}")

def main():
    parser = argparse.ArgumentParser(description="Encoding-safe Git auto sync with index repair.")
    parser.add_argument("--repo", required=True, help="Path to target Git repository.")
    parser.add_argument("--remote", default="origin", help="Remote name (default: origin).")
    parser.add_argument("--branch", default="main", help="Branch name (default: main).")
    parser.add_argument("--exclude", default="", help="Comma-separated ignore patterns.")
    parser.add_argument("--message", default="", help="Commit message. Default: 'chore: automated sync'.")
    parser.add_argument("--set-remote-url", default="", help="If provided and remote missing, set this URL.")
    args = parser.parse_args()

    repo = os.path.abspath(args.repo)
    remote = args.remote
    branch = args.branch
    excludes = [e.strip() for e in args.exclude.split(",") if e.strip()]
    if not excludes:
        excludes = DEFAULT_EXCLUDES

    ensure_repo(repo)
    fix_index_if_corrupt(repo)
    update_gitignore(repo, excludes)
    ensure_remote(repo, remote, branch, args.set_remote_url)
    committed = safe_commit(repo, args.message)
    # Push regardless (handles first-time push too)
    safe_push(repo, remote, branch)

    log_write(repo, "Sync completed successfully." + (" (no new commit)" if not committed else ""))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Ensure we print in ASCII-safe form to avoid console encoding issues
        msg = str(e).encode("utf-8", errors="replace").decode("utf-8", errors="replace")
        print(f"[FATAL] {msg}", file=sys.stderr)
        sys.exit(1)