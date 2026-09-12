---
title: "Linux Command Tutorial: sed"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'GNU Sed'
  - 'sed'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-sed-tutorial"
description: "Authoritative reference tutorial for sed (GNU Sed), detailing stream editing, pattern/hold spaces, in-place modification (-i), and POSIX portability."
upstream_suite: "gnu-sed"
upstream_version: "GNU Sed 4.9"
posix_standard: "POSIX.1-2024"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: `GNU Sed 4.9` | **POSIX**: `POSIX.1-2024 (with GNU extensions)` | **Safety Tier**: `unprivileged-filesystem-write` | **Scope**: `Stream editing, in-place regex replacement (-i) & text transformations`

`sed` (stream editor) is a non-interactive text editor that processes input streams line by line according to an execution cycle. It applies user-defined commands (such as substitutions, deletions, insertions, and branch logic) to an internal pattern buffer, writing transformed results to standard output or updating files in place.

- **Upstream Project & Provenance**: Developed and maintained under **GNU Sed** (`sed`).
- **Portability & Standards Baseline**: Standardized in **IEEE Std 1003.1-2024 (POSIX.1-2024)**. GNU `sed` introduces in-place editing (`-i`), extended regular expressions (`-E`), zero-terminated streams (`-z`), and case-insensitive matching flags (`/I`).
- **Target Research Implementation**: Audited against **GNU Sed 4.9** (`sed(1)`).
- **Applicability & Lifecycle**: The standard command for programmatic text transformations, automated configuration editing, and stream sanitization in Linux.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
sed [OPTION]... {script-only-if-no-other-script} [input-file]...
sed [OPTION]... -e script... [input-file]...
sed [OPTION]... -f script-file... [input-file]...
```

### 2.2 Execution Cycle: Pattern Space vs Hold Space

`sed` operates by executing an infinite loop over each input line:
1. **Read**: Reads a line from the input stream, strips the trailing newline, and places it into the **Pattern Space** (temporary working buffer).
2. **Execute**: Evaluates commands in order. If an address matches (e.g. `/regex/` or `line_num`), the command executes on the pattern space.
3. **Output**: By default, prints the pattern space contents followed by a newline, unless `-n` (quiet mode) is specified.
4. **Hold Space**: A secondary persistent buffer used for multi-line accumulators, swapping data via `h` (hold), `H` (append to hold), `g` (get from hold), and `x` (exchange).

---

## 3. Options

### 3.1 Primary Operational Flags

| Short Flag | Long Flag | Description | POSIX Defined | Default |
|:---|:---|:---|:---:|:---|
| `-n` | `--quiet`, `--silent` | Suppress automatic printing of pattern space. | Yes | Auto-print |
| `-e script` | `--expression=script` | Add script commands to be executed. | Yes | N/A |
| `-f file` | `--file=script-file` | Add script commands contained in file. | Yes | N/A |
| `-i[SUFFIX]` | `--in-place[=SUFFIX]` | Edit files in place (creates backup if SUFFIX supplied). | No | Standard output |
| `-E`, `-r` | `--regexp-extended` | Use extended regular expressions (ERE). | Yes (in 2024) | Basic (BRE) |
| `-s` | `--separate` | Treat files as separate rather than a single continuous stream. | No | Off |
| `-z` | `--zero-terminated` | Separate lines by NUL characters (`\0`). | No | Off |

---

## 4. Basic Usage

### 4.1 Quick Reference & Common Invocations

| Task / Scenario | Command | Key Flags / Behavior |
|:---|:---|:---|
| First match substitution | `sed 's/foo/bar/' file.txt` | Replaces first occurrence per line |
| Global substitution | `sed 's/foo/bar/g' file.txt` | Replaces all occurrences per line |
| In-place edit with backup | `sed -i.bak 's/old/new/g' config.conf` | Modifies file and saves `config.conf.bak` |
| Filter and print matches only | `sed -n '/ERROR/p' app.log` | `-n` suppresses auto-print; `p` prints matches |
| Delete matching lines | `sed '/^#/d' config.conf` | `d` drops lines matching pattern |
| Delete blank lines | `sed '/^$/d' input.txt` | Deletes empty lines |
| Print line number range | `sed -n '10,20p' file.txt` | Prints lines 10 through 20 |
| Replace using custom delimiter | `sed 's\|/var/www\|/srv/www\|g' file` | Avoids escaping `/` forward slashes |
| Extended regex substitution | `sed -E 's/([0-9]+)/[\1]/g' file` | `-E` supports modern regex groupings without `\(` |

### 4.2 Simple String Substitution

```bash
echo "Server status: offline" | sed 's/offline/online/'
```

*Sample terminal output:*

```text
Server status: online
```

### 4.3 Suppressing Default Output with -n and /p

Printing only lines that match a regular expression:

```bash
sed -n '/ERROR/p' /var/log/syslog
```

---

## 5. Practical Operations

### 5.1 Safe In-Place Configuration Modification with Backup

Updating a configuration directive in `/etc/default/ufw` with a timestamped backup:

```bash
sed -i.bak 's/^IPV6=no/IPV6=yes/' /etc/default/ufw
```

- **Technical Analysis**: `-i.bak` writes changes to `/etc/default/ufw` while saving the pre-modified original file as `/etc/default/ufw.bak`.

### 5.2 Global Substitution with Custom Delimiters

When replacing paths with slashes, escaping every `/` with `\/` is prone to errors. `sed` allows using alternative delimiters (such as `|` or `#`):

```bash
sed 's|/var/www/html|/srv/www/public|g' nginx.conf
```

### 5.3 Deleting Commented and Blank Lines

Filtering out comments and whitespace lines:

```bash
sed -E '/^[[:space:]]*(#|$)/d' /etc/redis/redis.conf | head -n 5
```

- **Technical Analysis**: Matches lines where the first non-whitespace character is `#` or the end of the line (`$`), and executes the `d` (delete) command.

### 5.4 Slicing Specific Line Ranges

Printing lines 15 through 25 of a file:

```bash
sed -n '15,25p' /etc/passwd
```

---

## 6. Advanced Usage

### 6.1 Multi-Line Join via Pattern Space Branching

Joining two lines when a line ends with a backslash:

```bash
cat <<'EOF' | sed -E ':a; /\\$/ { N; s/\\\n//; ta }'
HOSTS="node1 \
node2 \
node3"
EOF
```

*Sample terminal output:*

```text
HOSTS="node1 node2 node3"
```

- `:a`: Defines branch label `a`.
- `N`: Appends the next line to pattern space.
- `s/\\\n//`: Strips the backslash and newline.
- `ta`: Loops back to label `a` if the substitution succeeded.

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | Success: all scripts executed cleanly. |
| `>0` | An error occurred (syntax error in script, file unreadable, write failure in `-i`). |

---

## 8. Safety, Security, and Portability

### 8.1 Critical Portability Trap: GNU sed -i vs macOS/BSD sed -i

> [!WARNING]
> **In-Place Flag Incompatibility Hazard**:
> - **GNU `sed`**: The backup extension argument is optional (`sed -i 's/foo/bar/' file` works without backup; `sed -i.bak` creates a backup).
> - **BSD/macOS `sed`**: The backup argument is **mandatory**. Passing `sed -i 's/foo/bar/' file` on macOS treats `'s/foo/bar/'` as the backup extension and `file` as the script, causing errors or corrupted files. On BSD/macOS, an explicit empty string `sed -i '' 's/foo/bar/' file` is required.

### 8.2 In-Place Editing Inode Replacement

> [!IMPORTANT]
> When `sed -i` modifies a file, it creates a temporary file in the same directory and renames it over the original file. This changes the file's **inode number**, breaking existing hard links and replacing symlinks with regular files unless `--follow-symlinks` is passed.

---

## 9. Best Practices

1. **Always Supply an Extension to `-i` in Production**:
   > [!IMPORTANT]
   > *Guidance*: Write `sed -i.bak '...' file` when modifying production configurations.
   > *Authoritative Justification*: Provides an instantaneous rollback file in the event of an erroneous regex match.

2. **Use Alternative Delimiters (`|` or `#`) for Paths**:
   > [!TIP]
   > *Guidance*: Avoid escaping slashes; write `s|old|new|` instead of `s/\/old/\/new\/`.
   > *Authoritative Justification*: GNU documentation notes that any single character can serve as the delimiter in `s` commands.

3. **Use `-E` for Modern Readable Regular Expressions**:
   > [!TIP]
   > *Guidance*: Pass `-E` to avoid backslash escaping on `(`, `)`, `+`, and `{}`.
   > *Authoritative Justification*: Standardized in POSIX.1-2024 and natively supported across all modern versions of GNU and BSD sed.

---

## References

1. **GNU Sed Manual**: [https://www.gnu.org/software/sed/manual/sed.html](https://www.gnu.org/software/sed/manual/sed.html)
2. **POSIX.1-2024 sed Specification**: The Open Group Base Specifications Issue 8. [https://pubs.opengroup.org/onlinepubs/9799919799/utilities/sed.html](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/sed.html)
