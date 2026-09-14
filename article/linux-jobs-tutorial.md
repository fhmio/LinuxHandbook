---
title: "Linux Command Tutorial: jobs"
date: 2026-09-14T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'bash'
  - 'jobs'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-jobs-tutorial"
description: "Authoritative reference tutorial for jobs, detailing shell job control, backgrounding (bg), foregrounding (fg), and job state management."
upstream_suite: "bash"
upstream_version: "bash 5.2"
posix_standard: "posix-standard-strict"
research_date: "2026-09-14"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: bash | **POSIX**: POSIX.1-2024 | **Safety Tier**: safe-read-only | **Scope**: process-management

`jobs` is a shell built-in command that lists the active jobs (background and stopped processes) in the current shell session.

- **Upstream Project & Provenance**: Core feature of POSIX shells (bash, zsh, ksh). Job control was originally introduced in the C shell (csh).
- **Portability & Standards Baseline**: Strictly standardized in POSIX.1-2024. Available on all compliant UNIX-like environments.
- **Target Research Implementation**: Audited against **GNU Bash 5.2**.
- **Applicability & Lifecycle**: Essential for terminal multitasking. Used in conjunction with `bg` (background), `fg` (foreground), and `Ctrl+Z` to suspend, resume, and manage multiple command pipelines from a single terminal window.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
jobs [-lnprs] [jobspec ...]
```

### 2.2 Execution Model & Adjacency Requirement

- `jobs` is entirely managed within the shell's internal memory. It does not exist as an external binary (e.g., in `/bin/`).
- A "job" is a process or pipeline launched by the shell. It has a **jobspec** (like `%1`, `%2`) distinct from a Process ID (PID).
- Jobs can be in three states: **Running** (in the background or foreground), **Stopped** (suspended via `Ctrl+Z`), or **Done** (completed).
- Closing a terminal shell will typically send a `SIGHUP` (hangup) signal to all running and stopped jobs attached to it, killing them unless explicitly disowned (`disown`).

---

## 3. Options

### 3.1 Primary Flags

| Short Flag | Long Flag | Description | POSIX Defined |
|:---|:---|:---|:---:|
| `-l` | (None) | List the PIDs in addition to the normal information. | Yes |
| `-n` | (None) | List only jobs whose status has changed since the last notification. | Yes |
| `-p` | (None) | List only the PIDs of the process group leaders of the active jobs. | Yes |
| `-r` | (None) | Restrict output to running jobs only. | No |
| `-s` | (None) | Restrict output to stopped jobs only. | No |

### 3.2 Jobspec Identifiers

You can refer to a specific job using these formats:
- `%N` : Job number `N` (e.g., `%1`).
- `%+` or `%%` : The current (most recently suspended or backgrounded) job.
- `%-` : The previous job.
- `%string` : The job whose command line starts with `string`.

---

## 4. Basic Usage

### 4.1 Quick-Reference Cheatsheet Card

| Operation | Command | Notes |
|:---|:---|:---|
| List all jobs | `jobs` | Shows job number, state, and command. |
| List jobs with PIDs | `jobs -l` | Includes the Process ID. |
| Suspend current task | `Ctrl+Z` | Sends `SIGTSTP`. Places job in "Stopped" state. |
| Resume in foreground | `fg %1` | Brings job 1 back to the terminal. |
| Resume in background | `bg %1` | Starts execution of a stopped job in the background. |
| Kill a job | `kill %1` | Sends `SIGTERM` to the process group of job 1. |

### 4.2 Suspending and Viewing Jobs

If you run a long command (like `sleep 100` or `top`) and press `Ctrl+Z`, it is suspended:

```console
$ sleep 100
^Z
[1]+  Stopped                 sleep 100

$ jobs
[1]+  Stopped                 sleep 100
```
*(The `+` indicates it is the "current" job, meaning `fg` without arguments will target it).*

### 4.3 Viewing Job PIDs (`-l`)

If you need the PID to use with external utilities like `strace` or `gdb`:

```console
$ jobs -l
[1]+  8493 Stopped                 sleep 100
```

---

## 5. Practical Operations

### 5.1 Terminal Multitasking (The `fg` / `bg` Workflow)

A classic workflow is editing a file, compiling it, and running it, all in one terminal.
1. Open an editor: `$ vim main.c`
2. Realize you need to compile. Press `Ctrl+Z` to pause Vim.
3. Check status:
   ```console
   $ jobs
   [1]+  Stopped                 vim main.c
   ```
4. Compile your code: `$ gcc main.c`
5. Bring Vim back to the foreground: `$ fg`

### 5.2 Starting Jobs in the Background (`&`)

To launch a process directly into the background, append `&` to the command:

```console
$ wget https://example.com/largefile.iso &
[2] 10245
$ jobs
[1]-  Stopped                 vim main.c
[2]+  Running                 wget https://example.com/largefile.iso &
```

### 5.3 Resuming a Stopped Job in the Background (`bg`)

If you run a script, realize it will take a long time, and want your terminal back:
1. Suspend it: `Ctrl+Z`
2. Let it continue running invisibly:
   ```console
   $ bg %1
   [1]+ sleep 100 &
   ```

---

## 6. Advanced Usage

### 6.1 Detaching Jobs from the Terminal (`disown`)

If you start a background job but realize you need to close your SSH session, the job will normally be killed by `SIGHUP`. To remove a job from the shell's active job table and protect it from `SIGHUP`:

```console
$ sleep 900 &
[1] 2345
$ disown %1
$ jobs
(No output; the job is no longer tracked by the shell, but continues running).
```
*(Note: `disown` does not redirect output; if the job tries to print to the closed terminal, it will crash. Consider using `nohup` or `tmux` instead).*

### 6.2 Using `wait` in Shell Scripts

`jobs` is mostly for interactive use. In scripts, you use `wait` to block execution until background jobs finish:

```bash
#!/bin/bash
echo "Starting workers..."
sleep 5 &
sleep 10 &
wait
echo "All workers finished."
```

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | Success. |
| `1` | Invalid option or error evaluating jobspecs. |

### 7.2 Configuration Files

Job control behaves depending on the shell environment.
- In bash, if the `monitor` option (`set -m`) is disabled (which is the default in non-interactive scripts), job control is disabled.
- The `huponexit` shell option dictates whether the shell sends `SIGHUP` to all jobs when an interactive login shell exits.

---

## 8. Safety, Security, and Portability

### 8.1 The Stop Signal (SIGTSTP vs SIGSTOP)

Typing `Ctrl+Z` sends `SIGTSTP` (Terminal Stop) to the foreground job. A process *can* trap and ignore `SIGTSTP`. If a malicious or buggy process traps `SIGTSTP` and refuses to pause, you must open a second terminal and send the uncatchable `kill -STOP <PID>` (Signal 19) instead.

### 8.2 Standard Output Pollution

When a background job prints to standard output (`stdout`) or standard error (`stderr`), it will randomly interrupt your prompt. Job control does not isolate output. Always redirect background job output to a file or `/dev/null`:

```bash
$ my_script.sh > output.log 2>&1 &
```

---

## 9. Best Practices

1. **Use Job Identifiers with `kill`**:
   - *Guidance*: In an interactive shell, prefer `kill %1` over finding and typing the PID.
   - *Authoritative Justification*: `%1` targets the entire process group started by that job, ensuring child processes are also killed, whereas `kill PID` only kills the parent.
2. **Prefer Terminal Multiplexers for Long Tasks**:
   - *Guidance*: While `bg` and `disown` work, using `tmux` or `screen` is the authoritative best practice for managing long-running tasks over SSH, as they preserve scrollback and allow reattachment.

---

## References

1. **Bash Builtin Manual**: `man 1 bash` (Search for "JOB CONTROL")
2. **POSIX Specification**: [https://pubs.opengroup.org/onlinepubs/9699919799/utilities/jobs.html](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/jobs.html)
