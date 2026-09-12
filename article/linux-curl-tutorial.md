---
title: "Linux Command Tutorial: curl"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'curl'
  - 'curl'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-curl-tutorial"
description: "Authoritative reference tutorial for curl (curl), detailing URL data transfers, HTTP/HTTPS client operations, REST API interactions, authentication, headers, and transfer performance tuning."
upstream_suite: "curl"
upstream_version: "curl 8.12.0"
posix_standard: "None"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: curl (curl 8.12.0) | **POSIX**: None (De-facto Standard) | **Safety Tier**: unprivileged-filesystem-write | **Scope**: network-transfer-http

`curl` is a command-line utility and client library for transferring data using network protocols including HTTP, HTTPS, FTP, FTPS, SFTP, SCP, LDAP, IMAP, and SMTP. It provides robust control over HTTP methods, request headers, cookies, authentication mechanisms, proxy connections, and SSL/TLS validation.

- **Upstream Project & Provenance**: Created by Daniel Stenberg, maintained by the **curl** project (`curl`), built upon `libcurl`.
- **Portability & Standards Baseline**: De-facto universal standard network client; not standardized in IEEE Std 1003.1-2024 (POSIX.1-2024).
- **Target Research Implementation**: Audited against **curl 8.12.0** (`curl(1)`).
- **Applicability & Lifecycle**: The primary tool for REST API testing, automated asset downloading, web scraping, and health checks across Linux, BSD, macOS, and Windows.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
curl [options / URLs...]
```

### 2.2 Execution and Stream Model

- **Default Output**: `curl` streams downloaded payload content directly to standard output (`stdout`). If stdout is a terminal, binary data is printed unless redirected or written to a file via `-o` or `-O`.
- **Informational Stream**: Progress meters, status reports, and connection metadata are emitted to standard error (`stderr`).
- **URL Globbing**: `curl` supports built-in pattern matching and multiple URL processing:
  ```bash
  curl "https://example.com/archive_[2024-2026]_[01-12].tar.gz" -o "archive_#1_#2.tar.gz"
  ```

---

## 3. Options

### 3.1 Core Transfer and Output Flags

| Option | Long Option | Description | Default |
|:---|:---|:---|:---|
| `-o file` | `--output file` | Write output payload to specified file path instead of stdout. | `stdout` |
| `-O` | `--remote-name` | Write output to local file named matching the remote URL file component. | `stdout` |
| `-s` | `--silent` | Silent mode: suppress progress meter and informational status messages. | Progress enabled |
| `-S` | `--show-error` | When used with `-s`, show error messages on stderr if the transfer fails. | Errors suppressed |
| `-v` | `--verbose` | Output detailed protocol negotiation, headers, and TLS handshake info. | Normal output |
| `-I` | `--head` | Fetch HTTP headers only (sends HTTP `HEAD` request). | `GET` request |
| `-i` | `--include` | Include HTTP response headers in the output stream before body payload. | Body only |
| `-L` | `--location` | Follow HTTP redirects (`301`, `302`, `307`, `308`). | Do not follow |
| `-f` | `--fail` | Fail silently (exit code 22) on HTTP server errors (`4xx`, `5xx`). | Returns error body |
| `-C -` | `--continue-at -` | Automatically resume an interrupted download from local file offset. | Overwrites from start |

### 3.2 HTTP Request and Protocol Options

| Option | Long Option | Description | Default |
|:---|:---|:---|:---|
| `-X CMD` | `--request CMD` | Specify custom HTTP request method (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`). | `GET` / `POST` |
| `-d DATA` | `--data DATA` | Send specified HTTP POST data (`application/x-www-form-urlencoded`). | No body |
| `--data-raw` | `--data-raw` | Send data without interpreting leading `@` as a file reference. | Raw data |
| `-F NAME=@FILE`| `--form NAME=@FILE`| Send multipart/form-data POST request (e.g. file uploads). | Disabled |
| `-H HEADER` | `--header HEADER` | Append extra HTTP request header (e.g. `-H "Accept: application/json"`). | Default headers |
| `-u USER:PWD` | `--user USER:PWD` | Provide credentials for Basic, Digest, or NTLM server authentication. | Unauthenticated |
| `-b DATA` | `--cookie DATA` | Send cookies via string (`name=value`) or read from Netscape cookie file. | No cookies |
| `-c FILE` | `--cookie-jar FILE`| Save received session cookies to specified file after transfer concludes. | Discard cookies |
| `-m SEC` | `--max-time SEC` | Maximum time in seconds allowed for the entire operation to run. | Indefinite |
| `--connect-timeout`| `--connect-timeout`| Maximum time in seconds allowed for network connection establishment. | 300 seconds |
| `-w FORMAT` | `--write-out FORMAT` | Print custom formatted variables (e.g. `%{http_code}`, `%{time_total}`). | Off |
| `-k` | `--insecure` | Allow insecure TLS connections without validating certificates. | Strict TLS validation |
| `--retry NUM` | `--retry NUM` | Retry failed transfers `NUM` times on transient network errors. | 0 (no retry) |

---

## 4. Basic Usage

### 4.1 Quick-Reference Cheatsheet Card

| Operation | Command Pattern | Copyable One-Liner | Notes |
|:---|:---|:---|:---|
| Retrieve URL content | `curl [url]` | `curl https://httpbin.org/get` | Streams payload directly to stdout |
| Inspect response headers | `curl -I [url]` | `curl -I https://www.example.com` | Sends HEAD request to check headers |
| Download file locally | `curl -fSL -O [url]` | `curl -fSL -O https://example.com/archive.tar.gz` | Follows redirects and writes remote name |
| Silent fail in scripts | `curl -sSfL [url] -o [file]` | `curl -sSfL https://example.com/file.txt -o file.txt` | Exits non-zero on HTTP errors without progress bar |
| JSON POST request | `curl -sS -X POST [url] -H ... -d ...` | `curl -sS -X POST https://api.example.com/data -H "Content-Type: application/json" -d '{"key":"value"}'` | Sends structured JSON body |
| Resume download | `curl -C - -O [url]` | `curl -C - -O https://example.com/large.iso` | Resumes interrupted download from byte offset |
| Unix socket query | `curl --unix-socket [path] [url]` | `sudo curl --unix-socket /var/run/docker.sock http://localhost/version` | Communicates with local daemon IPC sockets |

### 4.2 Retrieving Web Content to Standard Output

Download a remote webpage or API response directly:

```bash
curl https://httpbin.org/get
```

Output:

```json
{
  "args": {}, 
  "headers": {
    "Accept": "*/*", 
    "Host": "httpbin.org", 
    "User-Agent": "curl/8.12.0"
  }, 
  "origin": "192.0.2.1", 
  "url": "https://httpbin.org/get"
}
```

### 4.3 Inspecting Response Headers with `-I`

Inspect server headers, caching policies, and status codes without downloading payload bodies:

```bash
curl -I https://www.example.com
```

Output:

```console
HTTP/2 200 
content-type: text/html; charset=UTF-8
content-length: 1256
date: Sat, 12 Sep 2026 18:30:15 GMT
cache-control: max-age=604800
etag: "3147526947"
server: ECS (dcb/7F42)
```

### 4.4 Downloading Files Locally with Progress

Save a remote asset locally matching its remote filename (`-O`) while following redirects (`-L`):

```bash
curl -fSL -O https://github.com/torvalds/linux/archive/refs/tags/v6.13.tar.gz
```

---

## 5. Practical Operations

### 5.1 Interacting with REST APIs (JSON POST Request)

Send an authenticated JSON payload with explicit headers and inspect the response:

```bash
curl -sS -X POST https://api.example.com/v1/auth \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"username":"admin","token":"sec-key-9812"}'
```

Output:

```json
{
  "status": "authenticated",
  "expires_in": 3600,
  "access_token": "eyJhbGciOiJIUzI1NiIsIn..."
}
```

### 5.2 Resuming Interrupted Downloads

Resume an interrupted multi-gigabyte ISO download without restarting from byte zero:

```bash
curl -C - -O https://releases.ubuntu.com/noble/ubuntu-24.04-live-server-amd64.iso
```

Output:

```console
** Resuming transfer from byte position 489210450
###################################################                       78.2%
```

### 5.3 Measuring HTTP Performance and Latency

Use `-w` (`--write-out`) to extract millisecond-precision timing breakdowns across DNS, TCP connect, TLS handshake, and transfer phases:

```bash
curl -s -o /dev/null -w "\
    DNS Lookup:        %{time_namelookup}s\n\
    TCP Connect:       %{time_connect}s\n\
    TLS Handshake:     %{time_appconnect}s\n\
    Time to First Byte:%{time_starttransfer}s\n\
    Total Time:        %{time_total}s\n\
    HTTP Status Code:  %{http_code}\n" https://www.example.com
```

Output:

```text
    DNS Lookup:        0.012410s
    TCP Connect:       0.038192s
    TLS Handshake:     0.079450s
    Time to First Byte:0.114520s
    Total Time:        0.128415s
    HTTP Status Code:  200
```

### 5.4 Uploading Files via Multipart Form Data (`-F`)

Upload binary files (such as images or documents) to API endpoints expecting `multipart/form-data`:

```bash
curl -fS -X POST https://api.example.com/v1/media \
  -H "Authorization: Bearer my-secret-token" \
  -F "file=@/home/user/document.pdf;type=application/pdf" \
  -F "category=invoices"
```

---

## 6. Advanced Usage

### 6.1 Communicating Over Unix Domain Sockets

Communicate directly with local daemons (such as the Docker or containerd APIs) without exposing TCP sockets:

```bash
sudo curl --unix-socket /var/run/docker.sock http://localhost/v1.41/version
```

Output:

```json
{
  "Platform": { "Name": "Docker Engine - Community" },
  "Version": "26.1.4",
  "ApiVersion": "1.41",
  "MinAPIVersion": "1.12",
  "GitCommit": "5ef4b30",
  "GoVersion": "go1.21.11",
  "Os": "linux",
  "Arch": "amd64"
}
```

### 6.2 Managing Cookie Sessions Across Requests

Persist session cookies across multiple API invocations:

```bash
# Authenticate and save session cookies to cookie jar
curl -s -c /tmp/cookies.txt -X POST https://app.example.com/login \
  -d "user=admin&pass=secret"

# Make subsequent authenticated calls using saved cookies
curl -s -b /tmp/cookies.txt https://app.example.com/dashboard/data
```

### 6.3 Enforcing Strict Timeouts and Retries in CI/CD Pipelines

Prevent automated scripts from hanging indefinitely due to packet loss or dead endpoints:

```bash
curl -sSfL \
  --connect-timeout 5 \
  --max-time 30 \
  --retry 3 \
  --retry-delay 2 \
  https://storage.googleapis.com/ci-assets/dependencies.tar.gz -o deps.tar.gz
```

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status

`curl` returns precise error codes signaling the exact layer of transfer failure:

| Exit Code | Description |
|:---|:---|
| `0` | Success: transfer completed successfully. |
| `6` | Could not resolve host (DNS lookup failed). |
| `7` | Failed to connect to host or proxy (TCP connection refused or unreachable). |
| `22` | HTTP page not retrieved (returned when `-f` is used and server returns `4xx` or `5xx`). |
| `28` | Operation timeout (`--max-time` or `--connect-timeout` expired). |
| `35` | SSL/TLS handshake failed. |
| `52` | Empty reply from server (server closed connection without sending data). |
| `60` | Peer certificate cannot be authenticated with known CA certificates. |

### 7.2 Environment Variables

| Variable | Description |
|:---|:---|
| `http_proxy`, `https_proxy` | Default proxy servers used for HTTP and HTTPS transfers. |
| `no_proxy` | Comma-separated list of hostnames/domains that bypass proxy routing. |
| `CURL_CA_BUNDLE` | Path to custom CA certificate bundle file for TLS verification. |

### 7.3 Configuration Files

| Path | Purpose |
|:---|:---|
| `~/.curlrc` | Per-user configuration file containing persistent command-line flags. |
| `/etc/curlrc` | Global system-wide configuration file. |

---

## 8. Safety, Security, and Portability

### 8.1 Insecure TLS Bypasses (`-k`, `--insecure`)

> [!CAUTION]
> **Insecure TLS Bypasses (`-k`, `--insecure`)**: Using `-k` disables all cryptographic verification of the remote server's TLS certificate, completely opening connections to Man-in-the-Middle (MITM) attacks. Never pass `-k` in production environments; use `--cacert /path/to/ca.pem` to specify custom CA certificates.

### 8.2 Credential Exposure in Process Tables

> [!WARNING]
> Passing credentials directly in flags (e.g. `-u user:password`) exposes plaintext credentials to all system users through `/proc/<pid>/cmdline` and process inspection tools. Use `--netrc-file` or environment pipes instead.

### 8.3 Portability Constraints

`curl` is cross-platform across all major operating systems. On minimal embedded systems or recovery environments where `curl` is omitted, `wget` or `busybox wget` may serve as alternatives.

---

## 9. Best Practices

### 9.1 Always Combine `-f` and `-sS` in Shell Automation

> [!TIP]
> **Always Combine `-f` and `-sS` in Automation**: By default, `curl` exits with status `0` even on HTTP `404` or `500` responses, saving error HTML into files. Combining `-f` (`--fail`) with `-sS` (`--silent --show-error`) guarantees non-zero exit codes on server errors while keeping pipelines clean.

*Upstream Rationale*: By default, `curl` exits with status `0` even if an HTTP server returns `404 Not Found` or `500 Internal Server Error`, writing HTML error pages into target files. Combining `-f` (`--fail`) and `-sS` (`--silent --show-error`) guarantees that HTTP error codes trigger non-zero script failures while suppressing terminal progress bars.

### 9.2 Always Define Explicit Connection and Execution Timeouts

> [!IMPORTANT]
> **Define Explicit Timeouts**: `curl` defaults to waiting indefinitely if TCP connections stall silently. Always set `--connect-timeout` (e.g. 5–10s) and `--max-time` (e.g. 30–60s) in automation scripts.

*Upstream Rationale*: `curl(1)` documentation notes that `curl` defaults to waiting indefinitely for server responses if TCP connections stall silently. In automated pipelines, always enforce `--connect-timeout` (e.g. 5–10s) and `--max-time` (e.g. 30–60s) to prevent unbounded thread execution.

### 9.3 Prefer URL Quoting in Shell Invocations

*Upstream Rationale*: URL query parameters often contain characters reserved by shells (such as `?`, `&`, `=`, `[`). Omitting quotation marks causes the shell to split background jobs or attempt glob expansions before `curl` receives the argument. Always enclose URLs within single or double quotes.

---

## References

1. `curl(1)` — curl command-line tool manual: <https://curl.se/docs/manpage.html>
2. Everything curl — The official guide by Daniel Stenberg: <https://everything.curl.dev/>
3. curl GitHub Repository: <https://github.com/curl/curl>
