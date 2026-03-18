[< Back to All Sections](../README.md#section-study-guides)

# CCNA 200-301 Exam Coach — Section 07 Study Guide
## Days 41–45 | IP Services: Syslog, SSH/Telnet, FTP/TFTP, Static NAT, Dynamic NAT/PAT
### Transcripts 083–092 | Jeremy's IT Lab Complete Course

---

## SECTION 1: EXAM KNOWLEDGE MAP

| # | Video | Day | Topic | CCNA Domain | Exam Weight |
|---|-------|-----|-------|-------------|-------------|
| 083 | Syslog | Day 41 | Message logging, severity levels, destinations, timestamps | IP Services | 10% |
| 084 | Syslog Lab | Day 41 Lab | Configure console/buffer/VTY/external logging, terminal monitor | IP Services | 10% |
| 085 | SSH and Telnet | Day 42 | Telnet vs SSH, RSA key generation, VTY configuration, console security | Security Fundamentals | 15% |
| 086 | SSH and Telnet Lab | Day 42 Lab | Full SSH setup, transport input, login local, switch SVI management | Security Fundamentals | 15% |
| 087 | FTP and TFTP | Day 43 | File transfer protocols, IOS upgrade process, FTP active/passive mode | IP Services | 10% |
| 088 | FTP and TFTP Lab | Day 43 Lab | Copy IOS via TFTP/FTP, show flash, boot system, file management | IP Services | 10% |
| 089 | Static NAT | Day 44 | RFC 1918, NAT terminology (inside/outside local/global), static one-to-one mapping | IP Services | 10% |
| 090 | Static NAT Lab | Day 44 Lab | ip nat inside/outside, static mapping, show ip nat translations | IP Services | 10% |
| 091 | Dynamic NAT and PAT | Day 45 | NAT pool, ACL selection, PAT/overload, interface-based PAT | IP Services | 10% |
| 092 | Dynamic NAT and PAT Lab | Day 45 Lab | Full dynamic NAT/PAT config, pool exhaustion behavior, debug ip nat | IP Services | 10% |

**Exam Objectives Covered:**
- 4.5 Describe the use of syslog features including facilities and levels
- 4.8 Configure network devices for remote access using SSH
- 5.4 Configure and verify device access control using local passwords
- 4.9 Describe the capabilities and function of TFTP/FTP in the network
- 4.1 Configure and verify inside source NAT using static and pools
- 4.2 Configure and verify inside source NAT using PAT (interface and pool)

---

## SECTION 2: MUST-KNOW CONCEPTS

---

### Concept 1: Syslog Overview

**What Syslog Does:**
- **Industry-standard protocol** for logging messages from network devices
- Devices send log messages to one or more destinations for monitoring and troubleshooting
- Uses **UDP port 514**
- One-way push: the device sends messages to the server — the server cannot request or pull messages, and cannot change device settings (contrast with SNMP)

**Four Syslog Message Destinations:**

| Destination | Command | Default Behavior |
|-------------|---------|-----------------|
| Console line | `logging console` | All levels (0–7) enabled by default |
| Buffer (RAM) | `logging buffered` | All levels (0–7) enabled by default |
| VTY lines (Telnet/SSH) | `logging monitor` | **Disabled by default**; also requires `terminal monitor` per session |
| External syslog server | `logging host` | Disabled until configured |

**Syslog Message Format:**
```
seq: time stamp: %facility-severity-MNEMONIC:description
```
Example: `*Mar 1 00:00:17.905: %LINK-3-UPDOWN: Interface GigabitEthernet0/0, changed state to up`

- `LINK` = facility (which part of the system generated the message)
- `3` = severity level
- `UPDOWN` = mnemonic (short identifier)
- Description = human-readable explanation of the event

---

### Concept 2: Syslog Severity Levels

**8 severity levels — memorize all 8 (0–7):**

| Level | Name | Description | Mnemonic Word |
|-------|------|-------------|---------------|
| 0 | Emergency | System is unusable | **E**very |
| 1 | Alert | Immediate action required | **A**wesome |
| 2 | Critical | Critical condition | **C**isco |
| 3 | Error | Error condition | **E**ngineer |
| 4 | Warning | Warning condition | **W**ill |
| 5 | Notice | Normal but significant | **N**eed |
| 6 | Informational | Informational message | **I**ce |
| 7 | Debugging | Debug-level message | **D**aily |

**Mnemonic:** "Every Awesome Cisco Engineer Will Need Ice cream Daily"

**Critical Rule — Level Filtering:**
- Setting `logging buffered 4` means levels **0, 1, 2, 3, AND 4** are logged
- Lower number = more severe; the filter shows everything **at or more severe** than the configured level
- "Level 4 (Warning) and higher severity" = levels 0 through 4

---

### Concept 3: Syslog Configuration

```
! Console logging (default: all levels / debugging)
R(config)# logging console 7               ! All levels (0-7); can specify by name or number
R(config)# logging console warnings        ! Levels 0-4 only

! Buffer (RAM) logging
R(config)# logging buffered 8192 debugging ! Size in bytes, then level
R(config)# logging buffered 4              ! Levels 0-4 (Warning and more severe)

! VTY (Telnet/SSH) logging — disabled by default
R(config)# logging monitor informational   ! Enables on VTY; must still run terminal monitor

! External syslog server
R(config)# logging host 192.168.1.100
R(config)# logging trap debugging          ! Set level sent to external server

! Global enable (usually on by default)
R(config)# logging on

! Prevent log messages from interrupting typing at console or VTY
R(config-line)# logging synchronous

! Timestamps and sequence numbers
R(config)# service timestamps log datetime ! Timestamps with real clock date/time
R(config)# service timestamps log uptime   ! Timestamps with router uptime instead
R(config)# service sequence-numbers        ! Prepend sequence numbers to messages

! Required every new VTY session (EXEC mode, not config mode)
R# terminal monitor                        ! Show syslog on current Telnet/SSH session

! View log buffer and current logging settings
R# show logging
```

**Key Behavioral Notes:**
- `terminal monitor` is an **EXEC-mode** command, not a config command
- It must be re-run at the start of **every new** Telnet or SSH session — it does not persist
- `logging synchronous` prevents log messages from splitting a command you are typing mid-line

---

### Concept 4: Syslog vs SNMP

| Feature | Syslog | SNMP |
|---------|--------|------|
| Direction | One-way push (device → server) | Two-way (get/set/trap) |
| Server can pull data? | NO | YES (Get, GetNext, GetBulk) |
| Server can change config? | NO | YES (Set) |
| Transport | UDP 514 | UDP 161 (agent), 162 (trap) |
| Purpose | Event logging | Performance monitoring + config management |

---

### Concept 5: Telnet vs SSH

**Telnet:**
- Developed in **1969** — one of the oldest remote access protocols
- Uses **TCP port 23**
- Sends ALL data — including usernames, passwords, and commands — in **plain text**
- No encryption whatsoever; any attacker who can intercept the traffic can read everything
- Still used in isolated lab environments; should **never** be used in production

**SSH (Secure Shell):**
- Developed in **1995**; SSHv2 released **2006** (major security improvements)
- Uses **TCP port 22**
- Provides **encryption** (protects data in transit) and **authentication**
- If a device supports both SSHv1 and SSHv2, `show ip ssh` displays version **1.99**
- **SSHv2 only** is strongly preferred and should be forced with `ip ssh version 2`
- Requires an **RSA key pair** to be generated before SSH will function

**SSH Required Configuration Steps (all five are required for CCNA):**
1. Set a unique hostname (default "Router" will not work)
2. Set a domain name (`ip domain-name`)
3. Generate RSA key pair (`crypto key generate rsa`)
4. Create at least one local user account (`username` + `secret`)
5. Configure VTY lines (`login local` + `transport input ssh`)

---

### Concept 6: SSH and Telnet Configuration

```
! Step 1: Hostname (must not be default "Router" or "Switch")
R(config)# hostname R1

! Step 2: Domain name (used with hostname to generate RSA key)
R(config)# ip domain-name jeremysitlab.com

! Step 3: Generate RSA key pair (minimum 768 bits; 2048 recommended)
R(config)# crypto key generate rsa modulus 2048

! Step 4: Create local user account
R(config)# username jeremy secret cisco123

! Enable password (for privilege EXEC access)
R(config)# enable secret cisco

! Step 5: Configure VTY lines
R(config)# line vty 0 15
R(config-line)# login local                  ! Authenticate with local username/password
R(config-line)# transport input ssh          ! SSH only (blocks Telnet)
R(config-line)# transport input telnet ssh   ! Allow both (use only in lab)
R(config-line)# transport input telnet       ! Telnet only (insecure — avoid in production)
R(config-line)# exec-timeout 5 0            ! Auto-logout after 5 minutes of inactivity

! Force SSHv2 only (best practice)
R(config)# ip ssh version 2

! Console port security
R(config)# line console 0
R(config-line)# password cisco              ! Local password on console
R(config-line)# login                       ! Require password (not local username)
R(config-line)# logging synchronous         ! Prevent logs interrupting input
R(config-line)# exec-timeout 5 0

! Layer 2 switch — management SVI for remote access
SW(config)# interface vlan 1
SW(config-if)# ip address 192.168.1.200 255.255.255.0
SW(config-if)# no shutdown
SW(config)# ip default-gateway 192.168.1.1  ! Required for switch to reach other subnets

! Verify SSH
R# show ip ssh                              ! SSH version, authentication settings
R# show ssh                                 ! Currently active SSH sessions
```

---

### Concept 7: FTP and TFTP Overview

**TFTP (Trivial File Transfer Protocol):**
- Uses **UDP port 69**
- Extremely simple — no authentication, no encryption, no directory browsing
- Operations: **upload and download files only** (no rename, no delete, no listing)
- Has its own reliability mechanism: every DATA block is acknowledged; timers for retransmission
- Initial connection to port 69; then both sides switch to randomly chosen **TIDs (Transfer IDs)**
- Best for: IOS upgrades within a trusted, controlled network segment

**FTP (File Transfer Protocol):**
- Developed in **1971**; uses **TCP ports 20** (data) and **21** (control)
- Username/password authentication required — but **no encryption** (credentials sent in plain text)
- **FTPS** = FTP wrapped in SSL/TLS (encrypted upgrade to FTP)
- **SFTP** = SSH File Transfer Protocol (completely different protocol — uses SSH)
- Full functionality: upload, download, list directory contents, navigate directories, rename and delete files
- Two separate connections:
  - **Control connection** — TCP port 21, persistent, carries commands
  - **Data connection** — TCP port 20, opened and closed per file transfer

**FTP Connection Modes:**

| Mode | Who Opens Data Connection | Firewall Impact |
|------|--------------------------|-----------------|
| **Active** (default) | Server initiates → client | Often blocked by client-side firewall |
| **Passive** | Client initiates → server | Works through firewalls (client controls) |

---

### Concept 8: FTP vs TFTP Comparison

| Feature | FTP | TFTP |
|---------|-----|------|
| Transport | TCP | UDP |
| Control port | 21 | — |
| Data port | 20 | 69 |
| Authentication | Yes (username/password) | No |
| Encryption | No (use FTPS or SFTP) | No |
| Directory navigation | Yes | No |
| Rename / delete files | Yes | No |
| Reliability | TCP built-in | Own ACK/retransmit mechanism |
| Typical use | Full-featured file management | Simple IOS upgrades in trusted networks |

---

### Concept 9: IOS File System and Upgrade Process

**Useful verification commands:**
```
R# show version                              ! Current IOS version, uptime, hardware
R# show flash                                ! Contents of flash filesystem (IOS images)
R# show file systems                         ! All available file systems and their types
```

**IOS Upgrade via TFTP:**
```
R# copy tftp flash
  Address of remote host? 192.168.1.100
  Source filename? c2900-universalk9-mz.SPA.155-3.M4a.bin
  Destination filename? [press Enter to accept default]
```

**IOS Upgrade via FTP:**
```
! Set FTP credentials (stored in running-config)
R(config)# ip ftp username jeremy
R(config)# ip ftp password cisco123

! Copy from FTP server
R# copy ftp flash
  Address of remote host? 192.168.1.100
  Source filename? c2900-universalk9-mz.SPA.155-3.M4a.bin
  Destination filename? [press Enter to accept default]
```

**Boot and cleanup:**
```
! Tell router which IOS to boot (survives reload)
R(config)# boot system flash:c2900-universalk9-mz.SPA.155-3.M4a.bin

! Reload to boot new image
R# reload

! After confirming new IOS is working, delete old image to free flash space
R# delete flash:old-ios-image.bin
```

---

### Concept 10: NAT Overview and Terminology

**Why NAT Exists:**
- IPv4 address space (~4.3 billion addresses) is exhausted
- RFC 1918 defines **private IP ranges** — not routable on the public internet

**Private IP Address Ranges (RFC 1918):**

| Class | Range | CIDR |
|-------|-------|------|
| A | 10.0.0.0 – 10.255.255.255 | 10.0.0.0/8 |
| B | 172.16.0.0 – 172.31.255.255 | 172.16.0.0/12 |
| C | 192.168.0.0 – 192.168.255.255 | 192.168.0.0/16 |

**NAT Translates** private (inside) IP addresses to public (outside) addresses, enabling internet access.

**Four NAT Address Terms — memorize all four:**

| Term | Definition | Example |
|------|-----------|---------|
| **Inside Local** | Private IP of the inside host as configured on its NIC | 192.168.1.1 |
| **Inside Global** | Public IP representing the inside host on the outside network | 100.0.0.1 |
| **Outside Local** | IP of the outside host as seen from inside the network (usually same as Outside Global) | 8.8.8.8 |
| **Outside Global** | Actual public IP of the outside host | 8.8.8.8 |

**Memory hook:** Inside = your side. Local = private view. Global = public view.
- Inside Local → "our private IP"
- Inside Global → "our public IP"

---

### Concept 11: Static NAT

**How Static NAT Works:**
- Creates a **permanent, one-to-one mapping** between a specific inside local (private) IP and a specific inside global (public) IP
- Mapping is manually configured and does **not time out**
- Traffic flow: **bidirectional** — allows both outbound (host → internet) AND inbound (internet → host) translation
- Use case: servers that must be reachable from the internet (web servers, mail servers)
- Limitation: each private IP requires its own dedicated public IP — **not scalable** for large internal networks

**Static NAT Configuration:**
```
! Step 1: Mark the inside interface (facing internal hosts)
R(config)# interface g0/1
R(config-if)# ip nat inside

! Step 2: Mark the outside interface (facing the internet/ISP)
R(config)# interface g0/0
R(config-if)# ip nat outside

! Step 3: Create the static mapping (inside local ↔ inside global)
R(config)# ip nat inside source static 192.168.1.1 100.0.0.1
R(config)# ip nat inside source static 192.168.1.2 100.0.0.2
R(config)# ip nat inside source static 192.168.1.3 100.0.0.3

! Verify
R# show ip nat translations          ! Full NAT table; static entries always present
R# show ip nat statistics            ! Hit counts, interfaces marked inside/outside
R# clear ip nat translation *        ! Clears dynamic entries ONLY; static entries remain
R# clear ip nat translation inside 192.168.1.1 100.0.0.1   ! Clear specific entry
```

---

### Concept 12: Dynamic NAT

**How Dynamic NAT Works:**
- Router maintains a **pool** of public IP addresses
- When an inside host sends traffic outbound, the router dynamically assigns an available inside global IP from the pool
- Still **one-to-one** at any given moment (one private IP per public IP)
- An **ACL** identifies which source IP addresses are eligible for translation:
  - PERMIT in the ACL = translate this source IP
  - DENY in the ACL = do NOT translate (but also does NOT drop the packet — it is simply forwarded untranslated)
- **Pool exhaustion:** if all public IPs in the pool are in use and a new host needs one, the router **DROPS** the packet
- Entries time out automatically when idle; can also be cleared manually

**Dynamic NAT Configuration:**
```
! Step 1: Define the pool of public IP addresses
R(config)# ip nat pool POOL1 100.0.0.0 100.0.0.3 prefix-length 24
! OR with netmask keyword:
R(config)# ip nat pool POOL1 100.0.0.0 100.0.0.3 netmask 255.255.255.0

! Step 2: Create ACL to identify which inside hosts to translate
R(config)# access-list 1 permit 192.168.1.0 0.0.0.255

! Step 3: Mark interfaces (same as static NAT)
R(config)# interface g0/1
R(config-if)# ip nat inside
R(config)# interface g0/0
R(config-if)# ip nat outside

! Step 4: Link ACL to pool (no overload = Dynamic NAT, one-to-one)
R(config)# ip nat inside source list 1 pool POOL1
```

---

### Concept 13: PAT (Port Address Translation) — NAT Overload

**How PAT Works:**
- PAT translates **both the IP address AND the port number**
- Many inside local addresses can share a **single inside global IP address**
- Router tracks each session by the unique combination: inside local IP + source port → inside global IP + translated port
- Over **65,000 port numbers** available → supports thousands of simultaneous sessions per public IP
- This is the **most common form of NAT** — used in virtually every home router and most enterprise networks
- **Inbound limitation:** PAT does NOT support unsolicited inbound connections (no pre-existing mapping for the destination) — contrast with static NAT

**PAT Configuration — Two Methods:**

**Method 1: PAT using a pool** (when you have multiple public IPs but want to share them)
```
R(config)# ip nat pool POOL1 100.0.0.0 100.0.0.3 prefix-length 24
R(config)# access-list 1 permit 192.168.1.0 0.0.0.255
R(config)# ip nat inside source list 1 pool POOL1 overload   ! "overload" = PAT
```

**Method 2: PAT using an interface** (most common — uses the ISP-assigned IP of the outside interface)
```
R(config)# access-list 1 permit 192.168.1.0 0.0.0.255
R(config)# ip nat inside source list 1 interface g0/0 overload
! g0/0 = outside interface; its IP is used as the inside global address
```

**Verify and troubleshoot:**
```
R# show ip nat translations          ! Shows IP+port mappings for PAT entries
R# show ip nat statistics            ! Hit counts, interfaces, pool usage
R# clear ip nat translation *        ! Clear all dynamic/PAT entries
R# debug ip nat                      ! Real-time output of each NAT translation event
```

---

## SECTION 3: COMMON EXAM TRAPS

| Trap | Correct Answer |
|------|---------------|
| "Telnet is secure because it uses TCP?" | FALSE — TCP provides reliability, NOT security. Telnet sends everything including passwords in plain text. Use SSH. |
| "SSH only requires generating RSA keys to work?" | FALSE — SSH requires ALL FIVE steps: hostname, domain name, RSA keys, local user account, AND VTY configuration (`login local` + `transport input ssh`) |
| "If a device shows SSH version 1.99, does it support SSHv2?" | YES — version 1.99 means the device supports BOTH v1 and v2. Force v2 only with `ip ssh version 2`. |
| "TFTP uses TCP for reliability?" | FALSE — TFTP uses **UDP port 69**. It has its own ACK/retransmit mechanism for reliability, separate from TCP. |
| "FTP uses only one TCP port?" | FALSE — FTP uses TWO ports: **21** (control/commands, persistent) and **20** (data transfers, opened per file). |
| "FTP provides encrypted transfers?" | FALSE — FTP uses plain-text credentials and data. Use **FTPS** (FTP over SSL/TLS) or **SFTP** (SSH-based, different protocol) for encryption. |
| "FTP active mode works through all firewalls?" | FALSE — In **active** mode, the **server** initiates the data connection back to the client, which is often blocked by client-side firewalls. Use **passive** mode through firewalls. |
| "Syslog level 4 means only Warning messages are logged?" | FALSE — Setting level 4 logs everything from level 0 (Emergency) **through** level 4 (Warning). Lower number = more severe. |
| "`terminal monitor` is configured in global config?" | FALSE — `terminal monitor` is an **EXEC-mode** command typed in the active terminal session. It must be re-issued every new Telnet/SSH session. |
| "Logging synchronous goes in global config?" | FALSE — `logging synchronous` is a **line-mode** command entered under `line console 0` or `line vty 0 15`. |
| "DENY in a NAT ACL drops the packet?" | FALSE — In Dynamic NAT, DENY in the ACL means "do not translate this source IP" but the packet is **forwarded normally**, not dropped. |
| "Static NAT allows inbound connections from outside?" | TRUE — Static NAT creates a permanent bi-directional mapping, so outside hosts CAN initiate connections to the inside host using its inside global IP. |
| "PAT allows unsolicited inbound connections?" | FALSE — PAT only creates translation entries when an inside host initiates traffic outbound. There is no pre-existing mapping for unsolicited inbound traffic. |
| "Inside Local is the public IP of the inside host?" | FALSE — **Inside Local** = the **private** IP assigned to the inside host. **Inside Global** = the public IP representing that host. |
| "PAT requires a pool of public IPs?" | FALSE — PAT can use a single interface IP (`interface` keyword) — all inside hosts share the one public IP assigned to the outside interface. |
| "Clearing NAT translations removes static entries?" | FALSE — `clear ip nat translation *` removes **dynamic** entries only. Static NAT mappings remain until manually removed from the config. |
| "Syslog and SNMP are equivalent monitoring tools?" | FALSE — Syslog is one-way push only (device → server, server cannot pull or set). SNMP is two-way (Get/Set/Trap — manager can read and change device config). |

---

## SECTION 4: COMPLETE COMMAND REFERENCE

### Syslog Commands
```
R(config)# logging console <level>           ! Console (0-7 or name); default: all/debugging
R(config)# logging buffered <size> <level>   ! RAM buffer; size in bytes, then level
R(config)# logging monitor <level>           ! VTY lines; default: off
R(config)# logging host <ip-address>         ! Send to external syslog server
R(config)# logging trap <level>              ! Set level for external server messages
R(config)# logging on                        ! Enable logging globally (default: on)
R(config-line)# logging synchronous          ! Prevent logs interrupting typing (line mode)
R# terminal monitor                          ! Show syslog on current VTY session (EXEC)
R(config)# service timestamps log datetime   ! Prepend date/time to log messages
R(config)# service timestamps log uptime     ! Prepend uptime to log messages instead
R(config)# service sequence-numbers          ! Prepend sequence numbers to log messages
R# show logging                              ! View log buffer contents and current settings
```

### SSH and Telnet Commands
```
R(config)# hostname R1                               ! Required — must not be default name
R(config)# ip domain-name jeremysitlab.com           ! Required for RSA key generation
R(config)# crypto key generate rsa modulus 2048      ! Generate RSA key pair (enables SSH)
R(config)# crypto key zeroize rsa                    ! Delete RSA keys (disables SSH)
R(config)# ip ssh version 2                          ! Force SSHv2 only (best practice)
R(config)# ip ssh time-out 60                        ! SSH negotiation timeout in seconds
R(config)# ip ssh authentication-retries 2           ! Max failed login attempts
R(config)# username jeremy secret cisco123           ! Local user with encrypted password
R(config)# enable secret cisco                       ! Enable (privilege EXEC) password
R(config)# line vty 0 15
R(config-line)# login local                          ! Authenticate against local user database
R(config-line)# transport input ssh                  ! SSH only (blocks Telnet)
R(config-line)# transport input telnet               ! Telnet only (insecure)
R(config-line)# transport input telnet ssh           ! Allow both protocols
R(config-line)# transport input none                 ! Block all remote access
R(config-line)# exec-timeout 5 0                     ! Auto-logout: 5 min, 0 sec
R(config)# line console 0
R(config-line)# password cisco
R(config-line)# login                                ! Password auth (no username required)
R(config-line)# logging synchronous
SW(config)# interface vlan 1                         ! Switch SVI for management
SW(config-if)# ip address 192.168.1.200 255.255.255.0
SW(config-if)# no shutdown
SW(config)# ip default-gateway 192.168.1.1           ! Required on Layer 2 switch
R# show ip ssh                                       ! SSH version, authentication info
R# show ssh                                          ! Active SSH sessions
```

### FTP and TFTP Commands
```
! View file systems and current IOS
R# show version                              ! IOS version, hardware, uptime
R# show flash                                ! Flash filesystem contents
R# show file systems                         ! All file systems (flash, nvram, tftp, ftp...)

! TFTP transfers
R# copy tftp flash                           ! Copy from TFTP server to flash
R# copy flash tftp                           ! Back up IOS to TFTP server
R# copy running-config tftp                  ! Back up running config to TFTP

! FTP credentials (stored in running-config)
R(config)# ip ftp username jeremy
R(config)# ip ftp password cisco123

! FTP transfers
R# copy ftp flash                            ! Copy from FTP server to flash
R# copy flash ftp                            ! Back up IOS to FTP server

! IOS boot and management
R(config)# boot system flash:<filename>      ! Specify which IOS to boot
R# reload                                    ! Restart router (loads new IOS)
R# delete flash:<filename>                   ! Delete file from flash
R# verify flash:<filename>                   ! Verify file integrity (MD5 check)
```

### Static NAT Commands
```
! Mark interfaces
R(config-if)# ip nat inside                  ! Interface facing internal hosts
R(config-if)# ip nat outside                 ! Interface facing internet/ISP

! Create static one-to-one mappings
R(config)# ip nat inside source static <inside-local> <inside-global>
! Examples:
R(config)# ip nat inside source static 192.168.1.1 100.0.0.1
R(config)# ip nat inside source static 192.168.1.2 100.0.0.2

! Verify
R# show ip nat translations                  ! NAT table (static entries always shown)
R# show ip nat statistics                    ! Hit counters and interface designations
R# clear ip nat translation *                ! Clear dynamic entries (static remain)
R# clear ip nat translation inside <local> <global>   ! Clear specific entry
```

### Dynamic NAT and PAT Commands
```
! Define pool of public addresses
R(config)# ip nat pool POOL1 100.0.0.0 100.0.0.3 prefix-length 24
R(config)# ip nat pool POOL1 100.0.0.0 100.0.0.3 netmask 255.255.255.0

! ACL to identify traffic to translate
R(config)# access-list 1 permit 192.168.1.0 0.0.0.255

! Dynamic NAT (one-to-one from pool, no overload)
R(config)# ip nat inside source list 1 pool POOL1

! PAT using pool (many-to-many with port tracking)
R(config)# ip nat inside source list 1 pool POOL1 overload

! PAT using outside interface IP (most common — one public IP for all inside hosts)
R(config)# ip nat inside source list 1 interface g0/0 overload

! Verify and troubleshoot
R# show ip nat translations                  ! Full table with port numbers for PAT
R# show ip nat statistics                    ! Pool usage, hit/miss counts
R# clear ip nat translation *                ! Clear all dynamic/PAT entries
R# debug ip nat                              ! Real-time NAT translation events
R# no debug ip nat                           ! Stop NAT debug output
```

---

## SECTION 5: EXAM QUICK-REFERENCE TABLES

### Syslog Severity Levels Quick Reference

| Level | Name | Mnemonic | Typical Cause |
|-------|------|----------|---------------|
| 0 | Emergency | Every | System crash or total failure |
| 1 | Alert | Awesome | Immediate manual intervention required |
| 2 | Critical | Cisco | Hardware failure, software error |
| 3 | Error | Engineer | Interface errors, routing failures |
| 4 | Warning | Will | Configuration warnings, near-threshold events |
| 5 | Notice | Need | Interface up/down state changes |
| 6 | Informational | Ice | Normal operational messages |
| 7 | Debugging | Daily | Detailed debug output (very verbose) |

### Remote Access Protocol Comparison

| Feature | Telnet | SSH |
|---------|--------|-----|
| TCP Port | 23 | 22 |
| Encryption | None (plain text) | Yes (encrypted) |
| Authentication | Password (plain text) | Username/password or key-based |
| Introduced | 1969 | 1995 (v2: 2006) |
| RSA keys required? | No | Yes |
| Production use | No (insecure) | Yes (recommended) |
| Version indicator | N/A | "1.99" = supports v1 and v2 |

### FTP vs TFTP Quick Reference

| Feature | FTP | TFTP |
|---------|-----|------|
| Transport | TCP | UDP |
| Port(s) | 20 (data), 21 (control) | 69 |
| Authentication | Yes (username/password) | No |
| Encryption | No | No |
| Encrypted alternative | FTPS (SSL/TLS) or SFTP | None standard |
| Directory browsing | Yes | No |
| Rename / delete | Yes | No |
| Connection modes | Active (server initiates data) / Passive (client initiates data) | N/A |
| Reliability | TCP (inherent) | Own ACK/retransmit per block |

### NAT Type Comparison

| Feature | Static NAT | Dynamic NAT | PAT (Overload) |
|---------|-----------|-------------|----------------|
| Mapping | Permanent one-to-one | Dynamic one-to-one | Many-to-one (port-based) |
| Public IPs needed | One per private IP | One per active session | One for all hosts |
| Inbound connections | YES (bi-directional) | No (outbound-initiated only) | No (outbound-initiated only) |
| Entry timeout | Never | Yes (idle timeout) | Yes (idle timeout) |
| Scalability | Low | Medium | High |
| Typical use | Servers needing public access | Medium networks with IP pools | Home/enterprise internet access |

### Key Port Numbers for Days 41–45

| Protocol | Port | Transport | Notes |
|---------|------|-----------|-------|
| SSH | 22 | TCP | Encrypted remote access |
| Telnet | 23 | TCP | Plain-text remote access (avoid in production) |
| FTP control | 21 | TCP | Commands and authentication |
| FTP data | 20 | TCP | Actual file transfer |
| TFTP | 69 | UDP | Simple file transfer, no auth |
| Syslog | 514 | UDP | One-way log message push |

---

## SECTION 6: PRACTICE QUIZ

**1.** A network admin types `logging buffered 4` on a router. Which syslog messages will be stored in the RAM buffer?
- A) Only Warning (level 4) messages
- B) Levels 4 through 7 (Warning, Notice, Informational, Debugging)
- C) Levels 0 through 4 (Emergency, Alert, Critical, Error, Warning)
- D) All messages regardless of level

**Answer: C** — Syslog level filtering includes the specified level AND all **more severe** (lower-numbered) levels. Setting level 4 (Warning) logs levels 0 (Emergency) through 4 (Warning). Higher-numbered levels (5 Notice, 6 Informational, 7 Debugging) are not stored.

---

**2.** An admin connects via SSH to a router and needs to see syslog messages in real time. The router has `logging monitor debugging` configured. What else must the admin do?
- A) Enter `logging synchronous` in global config
- B) Run `terminal monitor` from the EXEC prompt in the current session
- C) Add `logging vty` to the line vty configuration
- D) Nothing — `logging monitor` automatically enables syslog on VTY sessions

**Answer: B** — `logging monitor` enables syslog output to VTY lines at the configured level, but VTY display is **disabled by default per session**. The admin must run `terminal monitor` in EXEC mode at the start of each new Telnet or SSH session. This is not persistent.

---

**3.** A network engineer attempts to configure SSH on a new router but receives an error when running `crypto key generate rsa`. The hostname is set to "R1". What is the most likely missing requirement?
- A) The enable secret has not been set
- B) The `ip ssh version 2` command has not been entered
- C) The `ip domain-name` has not been configured
- D) No local user account exists

**Answer: C** — RSA key generation requires BOTH the hostname AND the domain name, because the key label is formed as `hostname.domain-name`. Without `ip domain-name`, the `crypto key generate rsa` command will fail or prompt for the domain. All five SSH steps are required.

---

**4.** Which statement correctly describes the difference between FTP active mode and passive mode?
- A) In active mode, the client opens both the control and data connections to the server
- B) In passive mode, the server initiates the data connection to the client on a random port
- C) In active mode, the server opens the data connection (TCP 20) to the client; in passive mode, the client opens the data connection to the server
- D) Passive mode uses UDP instead of TCP for the data connection

**Answer: C** — In **active** mode (default), the server initiates the TCP port 20 data connection back to the client. This is often blocked by client-side firewalls. In **passive** mode, the client initiates both connections (control to port 21, data to a server-specified port), which works through most firewalls.

---

**5.** A router has four inside hosts (192.168.1.1–192.168.1.4) and a NAT pool with only two public IPs (100.0.0.1–100.0.0.2). Dynamic NAT (without PAT) is configured. A fifth host (192.168.1.5) sends traffic while all pool IPs are in use. What happens?
- A) 192.168.1.5's packet is translated using a random port and sent out
- B) The oldest NAT entry is automatically removed to accommodate the new host
- C) 192.168.1.5's packet is dropped because no pool IPs are available
- D) 192.168.1.5 falls back to using its private IP, which is sent untranslated

**Answer: C** — Dynamic NAT (without overload/PAT) is strictly one-to-one. When the pool is exhausted, new translation requests are **dropped**. This is pool exhaustion. Adding the `overload` keyword enables PAT, allowing many hosts to share each public IP using port multiplexing.

---

**6.** Which NAT address term describes the public IP address that represents an inside host when its traffic is seen on the outside network?
- A) Inside Local
- B) Outside Global
- C) Outside Local
- D) Inside Global

**Answer: D** — **Inside Global** is the public IP representing the inside host as seen from the outside network. Inside Local = the private IP configured on the inside host. Outside Global = the actual public IP of the destination (outside) host.

---

**7.** An admin configures: `ip nat inside source list 1 interface g0/0 overload`. Access-list 1 has a `deny` statement for host 192.168.1.50. Traffic from 192.168.1.50 reaches the router. What happens?
- A) The packet is dropped by NAT
- B) The packet is forwarded without NAT translation (sent with the original private source IP)
- C) The packet matches the overload rule and is translated anyway
- D) The packet is dropped by the access list

**Answer: B** — In Dynamic NAT and PAT, a DENY in the NAT ACL means "do not translate this source address." The packet is **not dropped** — it is forwarded normally with its private source IP unchanged. The ACL here is used only to select which traffic gets translated, not to filter traffic.

---

**8.** A small office has one public IP address assigned by the ISP on interface g0/0. Which NAT configuration allows all 50 internal hosts (192.168.1.0/24) to share this single public IP for internet access?
- A) `ip nat inside source list 1 pool POOL1`
- B) `ip nat inside source static 192.168.1.0 [public-ip]`
- C) `ip nat inside source list 1 interface g0/0 overload`
- D) `ip nat inside source list 1 pool POOL1 overload`

**Answer: C** — When you have only one public IP (the ISP-assigned address on the outside interface), use the **`interface` keyword** with **`overload`** (PAT). This allows all inside hosts to share the single IP using port multiplexing. Option D requires a defined pool of IPs, which is not applicable here.

---

**9.** A static NAT entry is configured: `ip nat inside source static 10.0.0.10 203.0.113.5`. Which of the following is true?
- A) Only inside hosts can initiate connections; outside hosts cannot reach 203.0.113.5
- B) Both inside-to-outside and outside-to-inside connections are supported via this mapping
- C) The mapping times out after the default idle timer expires
- D) Outside hosts can reach 10.0.0.10 directly without using NAT

**Answer: B** — Static NAT creates a **permanent, bi-directional** mapping. Inside hosts can reach the outside using the inside global IP, AND outside hosts can initiate connections to 203.0.113.5, which the router translates to 10.0.0.10. Static entries do not time out — they persist until removed from configuration.

---

**10.** Which combination correctly describes Telnet and SSH?
- A) Telnet: TCP 22, encrypted; SSH: TCP 23, plain text
- B) Telnet: UDP 23, plain text; SSH: UDP 22, encrypted
- C) Telnet: TCP 23, plain text; SSH: TCP 22, encrypted
- D) Telnet: TCP 23, encrypted; SSH: TCP 22, no encryption needed

**Answer: C** — **Telnet uses TCP port 23** and sends all data (including passwords) in plain text with no encryption. **SSH uses TCP port 22** and provides full encryption of the session. This is the most fundamental difference and a guaranteed CCNA exam topic.
