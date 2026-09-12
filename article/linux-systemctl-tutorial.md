---
title: "Linux Command Tutorial: systemctl"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'systemd'
  - 'systemctl'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-systemctl-tutorial"
description: "Authoritative reference tutorial for systemctl (systemd), detailing system and service management, unit lifecycle commands, boot performance analysis, dependency tracking, and unit file overrides."
upstream_suite: "systemd"
upstream_version: "systemd 256"
posix_standard: "None"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

`systemctl` is the central command-line management interface for the systemd init system and service manager. It controls systemd units (services, sockets, timers, mounts, targets, slices), manages unit files, inspects dependencies, queries system states, and executes power management operations.

- **Upstream Project & Provenance**: Maintained within **systemd** (`systemd`), developed as the core control client communicating with `systemd` (PID 1) via D-Bus (`org.freedesktop.systemd1`).
- **Portability & Standards Baseline**: Linux-specific system manager tool; not standardized in IEEE Std 1003.1-2024 (POSIX.1-2024). It supersedes SysVinit (`service`, `chkconfig`) and Upstart.
- **Target Research Implementation**: Audited against **systemd 256** (`systemctl(1)`).
- **Applicability & Lifecycle**: The default service and process management binary across major Linux distributions (Debian, Ubuntu, RHEL, Fedora, Arch Linux, openSUSE).

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
systemctl [OPTIONS...] COMMAND [PATTERN...]
```

### 2.2 Communication Architecture and D-Bus IPC

`systemctl` acts as a D-Bus client connecting to the system message bus or the private socket `/run/systemd/private` exposed directly by PID 1.
- In user mode (`--user`), `systemctl` connects to the per-user service manager instance via `$XDG_RUNTIME_DIR/systemd/private`.
- Operations are submitted as method calls to `org.freedesktop.systemd1.Manager`. Changes to unit files on disk are not loaded into memory until an explicit `daemon-reload` signal is sent.

### 2.3 Unit Types

systemd organizes managed entities into distinct unit types identified by their file suffix:
- `.service`: Daemon processes and application services.
- `.socket`: IPC or network sockets for socket activation.
- `.timer`: Monotonic or calendar event schedulers (cron replacement).
- `.mount` / `.automount`: Filesystem mount points and on-demand mount triggers.
- `.target`: Grouping units representing runlevels or synchronization milestones (e.g. `multi-user.target`).
- `.slice` / `.scope`: Control group (cgroup) resource allocation trees.
- `.path`: Inotify-based file and directory change monitors.

---

## 3. Options

### 3.1 Primary Operational Commands

| Command | Category | Description |
|:---|:---|:---|
| `start UNIT...` | Lifecycle | Start (activate) one or more loaded units. |
| `stop UNIT...` | Lifecycle | Stop (deactivate) one or more loaded units. |
| `restart UNIT...` | Lifecycle | Stop and immediately start one or more units. |
| `reload UNIT...` | Lifecycle | Ask unit daemon to reload its configuration without restarting. |
| `reload-or-restart` | Lifecycle | Reload daemon config if supported; otherwise restart. |
| `status [UNIT...]` | Inspection | Show concise runtime status, PID, memory, and recent log entries. |
| `is-active UNIT...` | Inspection | Check whether unit is active; exits with code 0 if active. |
| `is-failed UNIT...` | Inspection | Check whether unit has failed; exits with code 0 if failed. |
| `enable UNIT...` | Persistence | Create symlinks to start unit automatically at boot. |
| `disable UNIT...` | Persistence | Remove autostart symlinks, disabling boot activation. |
| `mask UNIT...` | Security | Symlink unit file to `/dev/null`, preventing any activation. |
| `unmask UNIT...` | Security | Restore masked unit file to operational state. |
| `edit UNIT...` | Configuration | Create or modify drop-in override files (`override.conf`). |
| `cat UNIT...` | Configuration | Display unit file contents alongside all active drop-in overrides. |
| `daemon-reload` | Manager | Reload systemd manager configuration and re-read all unit files. |
| `list-units` | Manager | List loaded and active units in memory. |
| `list-timers` | Manager | List active timers with next execution times and elapsed intervals. |

### 3.2 Global Command Flags

| Option | Long Option | Description | Default |
|:---|:---|:---|:---|
| `-t TYPE` | `--type=TYPE` | Filter output by unit type (`service`, `socket`, `timer`, etc.). | All types |
| `--state=STATE` | `--state=STATE` | Filter by load, active, or sub-state (`active`, `failed`, etc.). | Active units |
| `-a` | `--all` | Display all units in memory, including inactive and dead units. | Filtered |
| `--now` | `--now` | Combine enable/disable with immediate start/stop. | Autostart change only |
| `--user` | `--user` | Talk to calling user's service manager instance. | System instance |
| `--failed` | `--failed` | List only units in failed operational state. | Off |
| `--no-pager` | `--no-pager` | Suppress output redirection into a pager (`less`). | Pager enabled |
| `--no-legend` | `--no-legend` | Suppress table header and footer summaries. | Printed |
| `-p NAME` | `--property=NAME` | Show specific property with `show` command. | All properties |
| `-H HOST` | `--host=HOST` | Execute operation on remote host via SSH transport. | Local host |

---

## 4. Basic Usage

### 4.1 Inspecting Service Status

Check the operational health, active cgroup, memory consumption, and recent log output of a service:

```console
$ systemctl status sshd.service
● sshd.service - OpenSSH server daemon
     Loaded: loaded (/usr/lib/systemd/system/sshd.service; enabled; preset: enabled)
     Active: active (running) since Fri 2026-09-12 10:00:15 UTC; 9h ago
       Docs: man:sshd(8)
             man:sshd_config(5)
   Main PID: 789 (sshd)
      Tasks: 1 (limit: 9452)
     Memory: 6.2M (peak: 8.4M)
        CPU: 1.124s
     CGroup: /system.slice/sshd.service
             └─789 "sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups"

Sep 12 10:00:15 server systemd[1]: Starting OpenSSH server daemon...
Sep 12 10:00:15 server sshd[789]: Server listening on 0.0.0.0 port 22.
Sep 12 10:00:15 server sshd[789]: Server listening on :: port 22.
Sep 12 10:00:15 server systemd[1]: Started OpenSSH server daemon.
```

### 4.2 Starting and Stopping Services

Control service execution state immediately:

```bash
# Start service
sudo systemctl start nginx.service

# Stop service
sudo systemctl stop nginx.service

# Restart service
sudo systemctl restart nginx.service

# Reload configuration gracefully without dropping connections
sudo systemctl reload nginx.service
```

---

## 5. Practical Operations

### 5.1 Enabling Services for Boot-Time Activation

Enable a service to launch automatically when reaching `multi-user.target`, and immediately activate it with `--now`:

```bash
sudo systemctl enable --now nginx.service
```

Disable autostart and terminate the running daemon simultaneously:

```bash
sudo systemctl disable --now nginx.service
```

### 5.2 Safe Unit Customization with Drop-In Overrides

Never modify vendor-supplied unit files in `/usr/lib/systemd/system/`. Instead, use `systemctl edit` to generate drop-in overrides in `/etc/systemd/system/<unit>.d/override.conf`:

```bash
sudo systemctl edit nginx.service
```

Add configuration overrides (e.g. adjust file descriptor limits and restart behavior):

```ini
### Editing /etc/systemd/system/nginx.service.d/override.conf
[Service]
LimitNOFILE=65535
Restart=on-failure
RestartSec=5s
```

Review the complete merged unit definition with `cat`:

```console
$ systemctl cat nginx.service
# /usr/lib/systemd/system/nginx.service
[Unit]
Description=The NGINX HTTP and reverse proxy server
After=syslog.target network-online.target remote-fs.target nss-lookup.target
...

# /etc/systemd/system/nginx.service.d/override.conf
[Service]
LimitNOFILE=65535
Restart=on-failure
RestartSec=5s
```

### 5.3 Diagnosing and Resetting Failed Units

Identify all services currently in an error state:

```console
$ systemctl --failed
  UNIT          LOAD   ACTIVE SUB    DESCRIPTION
● badapp.service loaded failed failed Custom Internal Application Service

1 loaded units listed.
```

Clear execution failure records after resolving the underlying issue:

```bash
sudo systemctl reset-failed badapp.service
```

### 5.4 Auditing System Timers

Audit all scheduled systemd timers (replacements for cron jobs):

```console
$ systemctl list-timers
NEXT                         LEFT          LAST                         PASSED       UNIT                         ACTIVATES
Sat 2026-09-12 20:00:00 UTC  45min left    Sat 2026-09-12 19:00:00 UTC  14min ago    sysstat-collect.timer        sysstat-collect.service
Sun 2026-09-13 00:00:00 UTC  4h 45min left Sat 2026-09-12 00:00:12 UTC  19h ago      logrotate.timer              logrotate.service
Sun 2026-09-13 03:24:00 UTC  8h left       Sat 2026-09-12 03:15:00 UTC  16h ago      systemd-tmpfiles-clean.timer systemd-tmpfiles-clean.service
```

---

## 6. Advanced Usage

### 6.1 Programmatic Status Probing in Automation Scripts

Use `is-active` with `--quiet` for clean condition checking in shell pipelines:

```bash
if systemctl is-active --quiet nginx.service; then
    echo "NGINX is operational."
else
    echo "CRITICAL: NGINX is inactive! Attempting restart..." >&2
    sudo systemctl restart nginx.service
fi
```

### 6.2 Inspecting Specific Properties via `show`

Extract discrete unit properties formatted for automated consumption without parsing multiline output:

```console
$ systemctl show -p ActiveState,SubState,MainPID,MemoryCurrent sshd.service
ActiveState=active
SubState=running
MainPID=789
MemoryCurrent=6537216
```

Extract single values in shell scripts:

```bash
PID=$(systemctl show -p MainPID --value sshd.service)
echo "Main PID of SSHD is: $PID"
```

### 6.3 Analyzing Unit Dependency Hierarchies

Visualize direct and inverse dependency trees:

```console
$ systemctl list-dependencies --before sshd.service
sshd.service
● ├─multi-user.target
● └─graphical.target
```

Trace required dependencies in reverse order:

```console
$ systemctl list-dependencies --reverse sshd.service
sshd.service
● └─multi-user.target
●   └─graphical.target
```

### 6.4 Masking Units to Prevent Accidental Invocation

Masking completely disables a unit by symlinking its configuration file to `/dev/null`. Even explicit `systemctl start` commands will be refused:

```bash
# Mask service
sudo systemctl mask apache2.service

# Attempting to start returns an error
sudo systemctl start apache2.service
# Failed to start apache2.service: Unit apache2.service is masked.

# Unmask service when needed
sudo systemctl unmask apache2.service
```

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status

`systemctl` conforms to the Linux Standard Base (LSB) exit code conventions when querying `status`:

| Exit Code | Meaning |
|:---|:---|
| `0` | Program is running or service is OK. |
| `1` | Program is dead and `/var/run` PID file exists. |
| `2` | Program is dead and `/var/lock` lock file exists. |
| `3` | Program is not running (stopped). |
| `4` | Program or service status is unknown. |

For `is-active`, exit code `0` indicates active, while non-zero indicates inactive or failed.

### 7.2 Environment Variables

| Variable | Description |
|:---|:---|
| `SYSTEMD_PAGER` | Pager binary to use (defaults to `less`). Overridden by `--no-pager`. |
| `SYSTEMD_COLORS` | Controls colored terminal output (`1` enables, `0` disables). |
| `XDG_RUNTIME_DIR` | Directory containing user D-Bus sockets for `systemctl --user`. |

### 7.3 Unit File Precedence Hierarchy

Systemd searches for unit files across three primary directories in strict order of priority:

| Priority | Directory | Role |
|:---|:---|:---|
| 1 (Highest) | `/etc/systemd/system/` | Local system administrator configurations and drop-ins. |
| 2 | `/run/systemd/system/` | Ephemeral runtime units created dynamically by daemons. |
| 3 (Lowest) | `/usr/lib/systemd/system/` | Distribution and vendor-packaged unit files. |

---

## 8. Safety, Security, and Portability

### 8.1 Destructive Operations and Safety Controls

Executing `systemctl isolate`, `reboot`, `poweroff`, or `emergency` immediately alters system runlevel state:
- Running `systemctl isolate rescue.target` shuts down all non-essential services, terminating remote SSH connections.
- Masking units (`systemctl mask`) prevents accidental auto-activation by packaging scripts or dependency pulls.

### 8.2 Privilege Boundaries

Modifying system units requires `root` privileges via D-Bus PolicyKit authorization. Unprivileged users can manage their own user units via `systemctl --user` without requiring `sudo`.

### 8.3 Portability Constraints

`systemctl` depends strictly on systemd as PID 1. Systems utilizing alternative init systems (OpenRC, runit, SysVinit, s6) or container base images lacking systemd do not provide `systemctl`.

---

## 9. Best Practices

### 9.1 Always Use `systemctl edit` for Overrides

*Upstream Rationale*: Editing vendor unit files in `/usr/lib/systemd/system/` is an anti-pattern; package updates automatically overwrite local modifications. Using `systemctl edit <unit>` creates non-destructive drop-in snippets under `/etc/systemd/system/<unit>.d/override.conf` that survive package upgrades.

### 9.2 Execute `systemctl daemon-reload` After Manual File Changes

*Upstream Rationale*: `systemd(1)` caches parsed unit definitions in user-space memory. Modifying unit files on disk directly without issuing `systemctl daemon-reload` leaves PID 1 running old dependency graphs, causing unpredictable behavior or missing units.

### 9.3 Use `systemctl is-active --quiet` for Scripting

*Upstream Rationale*: Scraping text output from `systemctl status` using `grep` is unreliable due to localized strings, terminal color escape codes, and log excerpt variations. `systemctl is-active --quiet <unit>` evaluates service state directly via D-Bus and signals status through the exit code.

---

## References

1. `systemctl(1)` — systemd system and service manager manual: <https://www.freedesktop.org/software/systemd/man/latest/systemctl.html>
2. `systemd.unit(5)` — systemd unit configuration reference: <https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html>
3. `systemd.service(5)` — systemd service unit configuration reference: <https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html>
4. systemd GitHub Repository: <https://github.com/systemd/systemd>
