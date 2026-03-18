# CCNA 200-301 Exam Coach — Section 06 Study Guide
## Days 36–40 | IP Services: CDP/LLDP, NTP, DNS, DHCP, SNMP
### Transcripts 073–082 | Jeremy's IT Lab Complete Course

---

## SECTION 1: EXAM KNOWLEDGE MAP

| # | Video | Day | Topic | CCNA Domain | Exam Weight |
|---|-------|-----|-------|-------------|-------------|
| 073 | CDP & LLDP | Day 36 | Layer 2 discovery protocols, CDP/LLDP config and verification | IP Services | 10% |
| 074 | CDP & LLDP Lab | Day 36 Lab | Enable/disable CDP and LLDP, show neighbors, timer tuning | IP Services | 10% |
| 075 | NTP | Day 37 | Network Time Protocol — stratum, modes, authentication, hardware/software clock | IP Services | 10% |
| 076 | NTP Lab | Day 37 Lab | NTP client/server/peer config, ntp master, show ntp associations | IP Services | 10% |
| 077 | DNS | Day 38 | DNS resolution, router as DNS client/server, ip name-server, ip host | IP Services | 10% |
| 078 | DNS Lab | Day 38 Lab | Configure DNS server on router, static hostname mappings, show hosts | IP Services | 10% |
| 079 | DHCP | Day 39 | DHCP DORA process, server config, relay agent (ip helper-address), client config | IP Services | 10% |
| 080 | DHCP Lab | Day 39 Lab | Configure DHCP pools, excluded addresses, relay agent, show ip dhcp binding | IP Services | 10% |
| 081 | SNMP | Day 40 | SNMP architecture (NMS/agent/MIB), versions, message types, port numbers | IP Services | 10% |
| 082 | SNMP Lab | Day 40 Lab | SNMPv2c community strings, trap destinations, show snmp | IP Services | 10% |

**Exam Objectives Covered:**
- 4.6 Configure and verify DHCP client and relay
- 2.9 Interpret the output of show commands to identify CDP and LLDP neighbors
- 4.5 Describe the use of syslog features including facilities and levels (time accuracy context — NTP)
- 4.8 Configure network devices for remote access using SSH (NTP/DNS as foundation)
- 5.4 Configure and verify device access control using local passwords
- 4.9 Describe the capabilities and function of TFTP/FTP in the network (port number context)
- 1.5 Compare TCP to UDP (SNMP/NTP/DNS use UDP; relevant to understanding IP Services protocols)

---

## SECTION 2: MUST-KNOW CONCEPTS

---

### Concept 1: CDP Overview

**What CDP Does:**
- **Cisco Discovery Protocol** — Cisco proprietary Layer 2 discovery protocol
- Allows directly connected Cisco devices to share information about themselves
- Enabled by **DEFAULT** on Cisco routers, switches, firewalls, and IP phones
- NOT forwarded — CDP messages are **processed and discarded** by the receiving device; they never pass beyond the directly connected neighbor

**Key Facts:**
- Multicast MAC address: **0100.0CCC.CCCC**
- Default hello (advertisement) timer: **60 seconds**
- Default holdtime: **180 seconds** (3× the hello timer)
- **CDPv2** is sent by default (`cdp advertise-v2` is on)
- CDPv2 shares additional info (native VLAN, duplex) that CDPv1 does not

**Information CDP Shares:**
- Hostname
- IP address (management/interface)
- Device type / platform
- IOS version
- Capabilities (router, switch, phone, etc.)
- Native VLAN
- Duplex setting (CDPv2 only)

**Security Consideration:** CDP reveals detailed topology and version information. It is often **disabled in production environments** facing untrusted networks (e.g., on interfaces connected to ISP or public networks).

---

### Concept 2: CDP Configuration Commands

```
! Enable / disable CDP globally (default: enabled)
R1(config)# cdp run
R1(config)# no cdp run

! Enable / disable CDP on a specific interface (default: enabled)
R1(config-if)# cdp enable
R1(config-if)# no cdp enable

! Tune CDP timers
R1(config)# cdp timer <seconds>         ! Hello timer (default: 60s)
R1(config)# cdp holdtime <seconds>      ! Holdtime (default: 180s)

! Enable / disable CDPv2 (default: enabled)
R1(config)# cdp advertise-v2
R1(config)# no cdp advertise-v2         ! Downgrade to CDPv1

! Verification commands
R1# show cdp                            ! Global CDP status + current timers
R1# show cdp neighbors                  ! Summary table of CDP neighbors
R1# show cdp neighbors detail           ! Full detail — includes IP address, IOS version
R1# show cdp entry <hostname>           ! Info for one specific neighbor
R1# show cdp interface                  ! CDP status per interface (enabled/disabled, timers)
R1# show cdp traffic                    ! CDP packet counters (sent/received/errors)
```

**Key Config Note:** Disabling CDP globally with `no cdp run` overrides any per-interface `cdp enable` settings.

---

### Concept 3: LLDP Overview

**What LLDP Does:**
- **Link Layer Discovery Protocol** — IEEE standard **802.1AB**; vendor-neutral
- Industry standard equivalent of CDP; works with Cisco, Juniper, HP, and other vendors
- Disabled by **DEFAULT** on Cisco devices (unlike CDP which is on by default)
- Can run **simultaneously** alongside CDP — they are independent protocols

**Key Facts:**
- Multicast MAC address: **0180.C200.000E**
- NOT forwarded — processed and discarded by the receiving device
- Default hello (advertisement) timer: **30 seconds**
- Default holdtime: **120 seconds** (4× the hello timer)
- Default reinit delay: **2 seconds** (delay before LLDP is initialized on an interface after being enabled)
- LLDP has **separate TX and RX controls** per interface (must enable both to discover neighbors)

**LLDP vs CDP at a glance:**
- CDP = Cisco proprietary, on by default, 60s/180s timers
- LLDP = IEEE standard, off by default, 30s/120s timers, requires TX AND RX enabled per interface

---

### Concept 4: LLDP Configuration Commands

```
! Enable / disable LLDP globally (default: disabled on Cisco)
R1(config)# lldp run
R1(config)# no lldp run

! Enable / disable LLDP transmit on interface (must enable separately from receive)
R1(config-if)# lldp transmit
R1(config-if)# no lldp transmit

! Enable / disable LLDP receive on interface
R1(config-if)# lldp receive
R1(config-if)# no lldp receive

! Tune LLDP timers
R1(config)# lldp timer <seconds>        ! Hello timer (default: 30s)
R1(config)# lldp holdtime <seconds>     ! Holdtime (default: 120s)
R1(config)# lldp reinit <seconds>       ! Reinit delay (default: 2s)

! Verification commands
R1# show lldp                           ! Global LLDP status + current timers
R1# show lldp neighbors                 ! Summary table of LLDP neighbors
R1# show lldp neighbors detail          ! Full detail — includes IP, capabilities
R1# show lldp entry <hostname>          ! Info for one specific LLDP neighbor
R1# show lldp interface                 ! LLDP TX/RX status per interface
R1# show lldp traffic                   ! LLDP packet counters
```

**Key Config Note:** To fully discover a neighbor via LLDP, you must enable BOTH `lldp transmit` AND `lldp receive` on the interface. Enabling only one direction is not sufficient.

---

### Concept 5: NTP (Network Time Protocol)

**Why Accurate Time Matters:**
- **Syslog and log correlation** — timestamps must be accurate to troubleshoot events across devices
- **Security certificates** — SSL/TLS certificates have validity periods tied to system time
- **Time-based ACLs** — access rules that activate at specific times
- **SNMP** — event timestamps in traps and polling data

**Hardware Clock vs Software Clock:**
- **Hardware clock (calendar):** battery-backed, persists across reboots, tends to **drift** over time
- **Software clock:** used during router operation; initialized from hardware clock on boot; reset if power lost

**NTP Basics:**
- Uses **UDP port 123**
- Accuracy: ~**1 ms** on a LAN; ~**50 ms** over WAN/internet
- NTP corrects the **software clock** on the router; `ntp update-calendar` also syncs the hardware clock

**NTP Stratum Hierarchy:**

| Stratum | Description |
|---------|-------------|
| 0 | Reference clocks (atomic clock, GPS receiver) — NOT a network device; never sends NTP packets |
| 1 | NTP servers directly connected to stratum 0 reference clocks; most accurate |
| 2 | Sync from stratum 1; each hop adds 1 to the stratum number |
| ... | Each additional hop adds 1 |
| 15 | Maximum usable stratum level |
| 16 | Unsynchronized — device considers itself unsynced |

**Rule:** Lower stratum number = more accurate = preferred.

**NTP Modes:**

| Mode | Command | Description |
|------|---------|-------------|
| Client | `ntp server <ip>` | Router syncs FROM the specified server |
| Server | `ntp master <stratum>` | Router acts AS an NTP server for others |
| Symmetric Active (Peer) | `ntp peer <ip>` | Mutual sync — both devices can sync from each other; provides redundancy |

A device can be **both client and server simultaneously** (syncs from upstream, serves downstream).

---

### Concept 6: NTP Configuration Commands

```
! Manually set the software clock (privileged EXEC mode — NOT config mode)
R1# clock set 12:00:00 17 March 2026

! Manually set the hardware clock (privileged EXEC mode)
R1# calendar set 12:00:00 17 March 2026

! Sync hardware clock FROM software clock (manual, one-time)
R1# clock update-calendar

! Sync software clock FROM hardware clock (manual, one-time)
R1# clock read-calendar

! Configure timezone (offset from UTC in hours)
R1(config)# clock timezone EST -5

! Configure daylight saving time (DST) — recurring rule
R1(config)# clock summer-time EDT recurring 2 Sunday March 02:00 1 Sunday November 02:00

! NTP client — sync from external server
R1(config)# ntp server 216.239.35.0 prefer    ! prefer = this server is preferred over others
R1(config)# ntp server 216.239.35.4           ! second server for redundancy

! NTP server — make this router an NTP server
R1(config)# ntp master 8                      ! stratum 8; default if no number given = 8
R1(config)# ntp source loopback0             ! use loopback IP as source of NTP packets

! NTP peer — symmetric active mode (mutual sync)
R2(config)# ntp peer 10.0.12.1

! Auto-sync hardware clock from NTP (ongoing)
R1(config)# ntp update-calendar

! NTP Authentication
R1(config)# ntp authenticate                          ! Enable NTP authentication
R1(config)# ntp authentication-key 1 md5 Jeremy1      ! Define key number 1 with MD5
R1(config)# ntp trusted-key 1                         ! Mark key 1 as trusted
R1(config)# ntp server 216.239.35.0 key 1             ! Use key 1 when syncing from this server

! Verification
R1# show clock                                        ! Current software clock time
R1# show clock detail                                 ! Time + source (NTP, hardware clock, etc.)
R1# show ntp associations                             ! NTP server list; * = synced, + = candidate
R1# show ntp status                                   ! Sync state, stratum, reference IP
R1# show ntp config                                   ! Configured NTP settings
```

**Key Facts:**
- `clock set` operates in **privileged EXEC mode**, not config mode
- `ntp master` without a stratum number defaults to stratum **8**
- Stratum 0 → the reference clock; stratum 1 → directly connected NTP server; `ntp master 8` → router claims stratum 8
- The `*` in `show ntp associations` indicates the **currently synced** server

---

### Concept 7: DNS

**What DNS Does:**
- Resolves human-readable hostnames (e.g., `google.com`) to IP addresses
- Uses **port 53** — both TCP and UDP
  - UDP port 53 for standard queries
  - TCP port 53 for large responses (over 512 bytes) and zone transfers

**DNS Resolution Process:**
1. Client checks its local **hosts file** (static entries) first
2. If not found, client sends a **DNS query** to the configured DNS server
3. DNS server responds with the IP address (or forwards the query upstream)

**Cisco Router DNS Roles:**

| Role | Description |
|------|-------------|
| DNS Client | Router can resolve names for management purposes (e.g., `ping google.com`) |
| DNS Server | Router can answer DNS queries from hosts; stores static hostname-to-IP mappings |

**Key IOS Default:** `ip domain lookup` is **enabled by default** — the router will attempt DNS resolution when you type an unrecognized string in EXEC mode (can cause delays; use `no ip domain lookup` in labs to disable).

```
! Configure router as a DNS server
R1(config)# ip dns server                         ! Enable DNS server function
R1(config)# ip host PC1 192.168.1.10              ! Static hostname mapping
R1(config)# ip host PC2 192.168.1.20
R1(config)# ip host SRV1 10.0.1.100

! Configure router as a DNS client
R1(config)# ip name-server 8.8.8.8               ! Specify DNS server to use for lookups
R1(config)# ip name-server 8.8.4.4               ! Secondary DNS server
R1(config)# ip domain lookup                      ! Enable DNS resolution (default: on)
R1(config)# no ip domain lookup                   ! Disable DNS resolution (common in labs)
R1(config)# ip domain-name jeremysitlab.com       ! Default domain suffix for unqualified names

! Verification
R1# show hosts                                    ! Hostname table (static entries + cached DNS results)
```

---

### Concept 8: DHCP

**What DHCP Provides to Clients:**
- IP address + subnet mask
- Default gateway
- DNS server address
- Domain name
- Lease time (how long the IP is valid)

**DORA Process (4-message exchange):**

| Step | Message | Src IP | Dst IP | Src Port | Dst Port | Description |
|------|---------|--------|--------|----------|----------|-------------|
| 1 | **Discover** | 0.0.0.0 | 255.255.255.255 | 68 | 67 | Client broadcasts to find DHCP servers |
| 2 | **Offer** | Server IP | 255.255.255.255 | 67 | 68 | Server offers an IP address + configuration |
| 3 | **Request** | 0.0.0.0 | 255.255.255.255 | 68 | 67 | Client broadcasts acceptance of offer |
| 4 | **ACK** | Server IP | 255.255.255.255 | 67 | 68 | Server confirms IP assignment |

**Why Request is still broadcast:** The client has received offers from potentially multiple DHCP servers. Broadcasting the Request informs ALL servers which offer was accepted, so that servers whose offers were declined can reclaim their offered addresses.

**DHCP Relay Agent:**
- DHCP Discover is a broadcast — routers do NOT forward broadcasts by default
- The relay agent (`ip helper-address`) solves this by converting the broadcast Discover into a **unicast** packet directed to the central DHCP server
- Configured on the **router interface facing the clients** (where the Discover arrives)

```
! Configure a DHCP server on a Cisco router
R1(config)# ip dhcp excluded-address 192.168.1.1 192.168.1.10    ! Exclude gateway + reserved IPs
R1(config)# ip dhcp excluded-address 192.168.1.254               ! Exclude single IP

R1(config)# ip dhcp pool POOL_LAN1                               ! Create and name the pool
R1(dhcp-config)# network 192.168.1.0 255.255.255.0              ! Subnet to assign addresses from
R1(dhcp-config)# default-router 192.168.1.1                     ! Default gateway for clients
R1(dhcp-config)# dns-server 8.8.8.8                             ! DNS server for clients
R1(dhcp-config)# domain-name jeremysitlab.com                   ! Domain name for clients
R1(dhcp-config)# lease 0 12                                     ! Lease duration: 0 days, 12 hours
R1(dhcp-config)# lease infinite                                  ! Infinite lease (not recommended)

! Configure DHCP relay agent (on the interface FACING the clients — where Discover arrives)
R1(config-if)# ip helper-address 10.0.2.100                     ! IP of the central DHCP server

! Configure a router interface to obtain its IP via DHCP (router as DHCP client)
R1(config-if)# ip address dhcp

! Verification
R1# show ip dhcp binding                  ! Active leases: IP-to-MAC mapping table
R1# show ip dhcp pool                     ! Pool stats (total addresses, leased, available)
R1# show ip dhcp server statistics        ! DHCP message counters (Discover, Offer, Request, ACK)
R1# show ip dhcp conflict                 ! Addresses flagged as conflicted (detected via ping/ARP)
R1# show running-config | section dhcp   ! View DHCP configuration
```

**Excluded Addresses Best Practice:** Always exclude the range BEFORE creating the pool. The excluded-address command prevents those IPs from being offered to clients, even if they fall within the pool's network range.

---

### Concept 9: SNMP

**What SNMP Does:**
- **Simple Network Management Protocol** — monitors and manages network devices from a central location
- Allows an NMS (Network Management Station) to read statistics from and make changes to network devices

**Two Main Device Roles:**

| Role | Description |
|------|-------------|
| **Managed Device (SNMP Agent)** | Router, switch, or firewall being monitored; runs the SNMP agent process; contains the MIB |
| **NMS (Network Management Station)** | The "SNMP server" or management platform; polls agents, receives notifications, can send changes |

**MIB (Management Information Base):**
- A hierarchical database of variables (called **OIDs — Object Identifiers**) on the managed device
- Contains: interface status, CPU utilization, memory usage, traffic counters, hostname, routing table, etc.
- OIDs are organized in a tree structure; each OID uniquely identifies one variable

**SNMP Versions:**

| Version | Authentication | Encryption | Notes |
|---------|---------------|------------|-------|
| SNMPv1 | Community strings (plaintext) | None | Original version; insecure |
| SNMPv2c | Community strings (plaintext) | None | Adds GetBulk, Inform; 'c' = community; still plaintext |
| SNMPv3 | Username + password | Yes (AES/DES) | Current recommendation; only secure version |

**SNMP Messages:**

| Message | Direction | Acknowledged? | Purpose |
|---------|-----------|---------------|---------|
| Get | NMS → Agent | Yes (Response) | Request the value of a specific OID |
| GetNext | NMS → Agent | Yes (Response) | Request the next OID in the MIB tree |
| GetBulk | NMS → Agent | Yes (Response) | Request multiple OIDs in one message (v2c+) |
| Set | NMS → Agent | Yes (Response) | Write/change an OID value on the managed device |
| Trap | Agent → NMS | **NO** | Unsolicited event notification; fire-and-forget |
| Inform | Agent → NMS | Yes (Response) | Acknowledged notification; agent retransmits if no ACK (v2c+) |
| Response | Agent → NMS | — | Reply to any Get or Set request from NMS |

**Port Numbers:**
- **UDP 161** — SNMP Agent listens here (receives Get/Set messages from NMS)
- **UDP 162** — NMS/Manager listens here (receives Trap/Inform messages from agents)

---

### Concept 10: SNMP Configuration

```
! SNMPv2c configuration on the managed device (router/switch)
R1(config)# snmp-server community Jeremy1 RO              ! Read-only community string (NMS can only read)
R1(config)# snmp-server community Jeremy2 RW              ! Read-write community string (NMS can read and change)

! Configure trap destination (tell the agent where to send traps/informs)
R1(config)# snmp-server host 192.168.1.100 version 2c Jeremy1    ! Send traps to NMS at this IP using community Jeremy1

! Enable trap notifications (by default, traps are not sent)
R1(config)# snmp-server enable traps                      ! Enable all trap types
R1(config)# snmp-server enable traps snmp linkup linkdown  ! Enable only specific trap types

! Optional informational settings
R1(config)# snmp-server location "Data Center - Rack 3"   ! Device physical location
R1(config)# snmp-server contact admin@company.com         ! Contact information

! Verification
R1# show snmp                                             ! SNMP global status and message counters
R1# show snmp community                                   ! Configured community strings
R1# show snmp host                                        ! Configured trap/inform destinations
```

**Community String Security Note:** SNMPv1 and SNMPv2c community strings are sent in **plaintext**. Anyone who can capture packets on the network can read them. Use SNMPv3 in production environments where security matters.

---

## SECTION 3: COMMON EXAM TRAPS

| Trap | Correct Answer |
|------|---------------|
| "CDP is disabled by default on Cisco devices?" | FALSE — CDP is **ENABLED** by default on Cisco routers, switches, firewalls, and IP phones |
| "LLDP is enabled by default on Cisco devices?" | FALSE — LLDP is **DISABLED** by default on Cisco devices; must be manually enabled with `lldp run` |
| "CDP forwards messages to neighboring devices beyond the directly connected one?" | FALSE — CDP messages are **processed and discarded** by the receiving device; they are NEVER forwarded |
| "CDP default hello timer vs LLDP default hello timer?" | CDP = **60 seconds**; LLDP = **30 seconds** (LLDP is half of CDP) |
| "CDP holdtime vs LLDP holdtime?" | CDP = **180 seconds** (3× timer); LLDP = **120 seconds** (4× timer) |
| "Only enabling `lldp transmit` on an interface is enough to discover neighbors?" | FALSE — LLDP requires BOTH `lldp transmit` AND `lldp receive` enabled on the interface |
| "CDP and LLDP cannot run on the same device simultaneously?" | FALSE — both protocols can run at the same time; they are independent |
| "NTP uses TCP for time synchronization?" | FALSE — NTP uses **UDP port 123** |
| "Stratum 0 is an NTP server on the network?" | FALSE — stratum 0 is the **reference clock** (atomic clock, GPS), NOT a network device; stratum 1 servers connect to it |
| "A lower NTP stratum number means less accurate?" | FALSE — **LOWER stratum = MORE accurate** and preferred (closer to stratum 0 reference clock) |
| "`ntp master` makes a router sync FROM an external server?" | FALSE — `ntp master` makes the router **act AS an NTP server** for others; `ntp server <ip>` is client mode |
| "DNS uses only UDP port 53?" | FALSE — DNS uses **both TCP and UDP port 53** (UDP for standard queries; TCP for large responses and zone transfers) |
| "`ip domain lookup` is disabled by default in Cisco IOS?" | FALSE — `ip domain lookup` is **ENABLED by default**; use `no ip domain lookup` to disable it |
| "DHCP Discover is sent unicast to the server's IP address?" | FALSE — DHCP Discover is a **broadcast** (src: 0.0.0.0, dst: 255.255.255.255); the client doesn't know the server's IP yet |
| "DHCP Request is unicast to the selected DHCP server?" | FALSE — DHCP Request is **still a broadcast** (255.255.255.255); this informs all DHCP servers which offer was accepted |
| "The DHCP relay agent `ip helper-address` is configured on the server-side interface?" | FALSE — configure `ip helper-address` on the interface **facing the clients** (where Discover arrives) |
| "SNMP Trap is acknowledged by the NMS?" | FALSE — **Trap is fire-and-forget** (no ACK); **Inform** is the acknowledged version |
| "SNMP agent listens on UDP port 162?" | FALSE — Agent listens on **UDP 161** (receives Get/Set); NMS listens on **UDP 162** (receives Trap/Inform) |
| "SNMPv2c encrypts community strings for security?" | FALSE — SNMPv2c uses **plaintext** community strings; only **SNMPv3** provides authentication and encryption |
| "SNMPv1 supports GetBulk for efficient polling?" | FALSE — **GetBulk was introduced in SNMPv2c**; SNMPv1 only has Get, GetNext, Set, Trap |

---

## SECTION 4: COMPLETE COMMAND REFERENCE

### CDP Commands
```
R(config)# cdp run                                   ! Enable CDP globally (default: enabled)
R(config)# no cdp run                                ! Disable CDP globally
R(config-if)# cdp enable                             ! Enable CDP on this interface (default: enabled)
R(config-if)# no cdp enable                          ! Disable CDP on this interface
R(config)# cdp timer <seconds>                       ! Set hello timer (default: 60s)
R(config)# cdp holdtime <seconds>                    ! Set holdtime (default: 180s)
R(config)# cdp advertise-v2                          ! Enable CDPv2 (default: enabled)
R(config)# no cdp advertise-v2                       ! Downgrade to CDPv1
R# show cdp                                          ! Global CDP status and timers
R# show cdp neighbors                                ! Neighbor table (brief summary)
R# show cdp neighbors detail                         ! Full detail per neighbor (IP, IOS version, platform)
R# show cdp entry <hostname>                         ! Details for one specific neighbor
R# show cdp interface [interface]                    ! CDP status per interface
R# show cdp traffic                                  ! CDP packet counters
```

### LLDP Commands
```
R(config)# lldp run                                  ! Enable LLDP globally (default: disabled)
R(config)# no lldp run                               ! Disable LLDP globally
R(config-if)# lldp transmit                          ! Enable LLDP transmit on interface
R(config-if)# no lldp transmit                       ! Disable LLDP transmit
R(config-if)# lldp receive                           ! Enable LLDP receive on interface
R(config-if)# no lldp receive                        ! Disable LLDP receive
R(config)# lldp timer <seconds>                      ! Set hello timer (default: 30s)
R(config)# lldp holdtime <seconds>                   ! Set holdtime (default: 120s)
R(config)# lldp reinit <seconds>                     ! Set reinit delay (default: 2s)
R# show lldp                                         ! Global LLDP status and timers
R# show lldp neighbors                               ! Neighbor table (brief summary)
R# show lldp neighbors detail                        ! Full detail per neighbor
R# show lldp entry <hostname>                        ! Details for one specific neighbor
R# show lldp interface [interface]                   ! LLDP TX/RX status per interface
R# show lldp traffic                                 ! LLDP packet counters
```

### NTP Commands
```
R# clock set <hh:mm:ss> <day> <month> <year>         ! Set software clock (EXEC mode — not config)
R# calendar set <hh:mm:ss> <day> <month> <year>      ! Set hardware clock (EXEC mode)
R# clock update-calendar                             ! Sync hardware clock FROM software clock (one-time)
R# clock read-calendar                               ! Sync software clock FROM hardware clock (one-time)
R(config)# clock timezone <zone-name> <UTC-offset>   ! Set timezone (e.g., EST -5)
R(config)# clock summer-time <name> recurring ...    ! Configure recurring DST rules
R(config)# ntp server <ip> [prefer]                  ! Client mode — sync from this server
R(config)# ntp master [stratum]                      ! Server mode — act as NTP server (default stratum: 8)
R(config)# ntp peer <ip>                             ! Symmetric active (peer) mode — mutual sync
R(config)# ntp source <interface>                    ! Use this interface IP as the NTP source
R(config)# ntp update-calendar                       ! Auto-sync hardware clock from NTP (ongoing)
R(config)# ntp authenticate                          ! Enable NTP authentication
R(config)# ntp authentication-key <num> md5 <key>    ! Define an NTP authentication key
R(config)# ntp trusted-key <num>                     ! Mark key as trusted
R(config)# ntp server <ip> key <num>                 ! Use authentication key for this server
R# show clock [detail]                               ! Current time (detail shows source)
R# show ntp associations                             ! NTP server list (* = synced, + = candidate)
R# show ntp status                                   ! Synchronization state, stratum, reference
R# show ntp config                                   ! NTP configuration summary
```

### DNS Commands
```
R(config)# ip dns server                             ! Enable router as DNS server
R(config)# ip host <hostname> <ip-address>           ! Add static hostname-to-IP mapping
R(config)# ip name-server <ip-address>               ! Specify DNS server for lookups
R(config)# ip domain lookup                          ! Enable DNS resolution (default: on)
R(config)# no ip domain lookup                       ! Disable DNS resolution
R(config)# ip domain-name <domain>                   ! Set default domain suffix for unqualified names
R# show hosts                                        ! View hostname table (static entries + cached results)
```

### DHCP Commands
```
R(config)# ip dhcp excluded-address <start-ip> [end-ip]      ! Exclude IP or range from pool
R(config)# ip dhcp pool <pool-name>                          ! Create DHCP pool and enter config mode
R(dhcp-config)# network <network-address> <subnet-mask>      ! Define the address pool subnet
R(dhcp-config)# default-router <gateway-ip>                  ! Default gateway to assign to clients
R(dhcp-config)# dns-server <dns-ip>                          ! DNS server to assign to clients
R(dhcp-config)# domain-name <domain>                         ! Domain name for clients
R(dhcp-config)# lease <days> [hours] [minutes]               ! Lease duration (default: 1 day)
R(dhcp-config)# lease infinite                               ! Permanent lease (use with caution)
R(config-if)# ip helper-address <dhcp-server-ip>             ! Relay agent — forward DHCP broadcasts to server
R(config-if)# ip address dhcp                                ! Configure interface as DHCP client
R# show ip dhcp binding                                      ! Active leases (IP-to-MAC table)
R# show ip dhcp pool                                         ! Pool statistics (total, leased, available)
R# show ip dhcp server statistics                            ! DHCP message counters
R# show ip dhcp conflict                                     ! Conflicted addresses
R# show running-config | section dhcp                        ! View DHCP configuration in running config
```

### SNMP Commands
```
R(config)# snmp-server community <string> {RO|RW}            ! Set community string (RO = read-only, RW = read-write)
R(config)# snmp-server host <nms-ip> version {1|2c|3} <community>   ! Trap/Inform destination
R(config)# snmp-server enable traps [trap-type]              ! Enable trap notifications (all or specific types)
R(config)# snmp-server location <text>                       ! Describe device's physical location
R(config)# snmp-server contact <text>                        ! Responsible contact info
R# show snmp                                                 ! SNMP global status and packet counters
R# show snmp community                                       ! Configured community strings
R# show snmp host                                            ! Configured trap/inform destinations
```

---

## SECTION 5: EXAM QUICK-REFERENCE TABLES

### CDP vs LLDP Comparison

| Feature | CDP | LLDP |
|---------|-----|------|
| Standard | Cisco proprietary | IEEE 802.1AB (open standard) |
| Default state (Cisco) | **Enabled** | **Disabled** |
| Hello timer | 60 seconds | 30 seconds |
| Holdtime | 180 seconds (3× timer) | 120 seconds (4× timer) |
| Reinit delay | N/A | 2 seconds |
| Multicast MAC | 0100.0CCC.CCCC | 0180.C200.000E |
| Forwarded beyond directly connected? | No | No |
| Per-interface TX/RX control? | No (single `cdp enable`) | Yes (`lldp transmit` + `lldp receive` separately) |
| Versions | CDPv1 / CDPv2 (default: v2) | Single version |
| Can run simultaneously? | Yes | Yes |

### NTP Stratum Reference

| Stratum | Description |
|---------|-------------|
| 0 | Reference clock (atomic clock, GPS) — not a network device |
| 1 | Server directly connected to stratum 0 — most accurate NTP servers on the internet |
| 2 | Syncs from stratum 1 — each hop adds 1 |
| ... | Continues incrementing per hop |
| 15 | Maximum usable stratum level |
| 16 | Device considers itself unsynchronized |

**Memory aid:** `ntp master` with no argument defaults to stratum **8**. Lower number = better = preferred.

### DHCP DORA Messages

| Step | Message | Src IP | Dst IP | Src Port | Dst Port | Notes |
|------|---------|--------|--------|----------|----------|-------|
| 1 | Discover | 0.0.0.0 | 255.255.255.255 | 68 | 67 | Broadcast — client finds servers |
| 2 | Offer | Server IP | 255.255.255.255 | 67 | 68 | Server proposes an IP address |
| 3 | Request | 0.0.0.0 | 255.255.255.255 | 68 | 67 | Broadcast — client accepts an offer |
| 4 | ACK | Server IP | 255.255.255.255 | 67 | 68 | Server confirms IP assignment |

### SNMP Message Summary

| Message | Direction | Acknowledged? | Version | Purpose |
|---------|-----------|---------------|---------|---------|
| Get | NMS → Agent | Yes | v1/v2c/v3 | Read one OID value |
| GetNext | NMS → Agent | Yes | v1/v2c/v3 | Read next OID in MIB tree |
| GetBulk | NMS → Agent | Yes | v2c/v3 only | Read multiple OIDs efficiently |
| Set | NMS → Agent | Yes | v1/v2c/v3 | Change an OID value |
| Trap | Agent → NMS | **NO** | v1/v2c/v3 | Unsolicited event notification |
| Inform | Agent → NMS | Yes | v2c/v3 only | Acknowledged event notification |
| Response | Agent → NMS | — | v1/v2c/v3 | Reply to Get/Set from NMS |

### SNMP Version Comparison

| Feature | SNMPv1 | SNMPv2c | SNMPv3 |
|---------|--------|---------|--------|
| Authentication | Community string (plaintext) | Community string (plaintext) | Username + password |
| Encryption | None | None | Yes (AES/DES) |
| GetBulk message | No | Yes | Yes |
| Inform message | No | Yes | Yes |
| Recommended for production? | No | Limited use | **YES** |

### IP Services Port Numbers Quick Reference

| Protocol | Port | Transport | Direction |
|---------|------|-----------|-----------|
| DNS | 53 | TCP + UDP | Server listens |
| DHCP server | 67 | UDP | Server listens |
| DHCP client | 68 | UDP | Client listens |
| NTP | 123 | UDP | Bidirectional |
| SNMP agent | 161 | UDP | Agent listens (Get/Set from NMS) |
| SNMP manager | 162 | UDP | NMS listens (Trap/Inform from agents) |
| Syslog | 514 | UDP | Server listens |

---

## SECTION 6: PRACTICE QUIZ

**1.** Which statement about CDP is correct?

- A) CDP is disabled by default and must be manually enabled with `cdp run`
- B) CDP messages are forwarded to all routers in the network
- C) CDP is enabled by default on Cisco routers and switches
- D) CDP uses the multicast address 0180.C200.000E

**Answer: C** — CDP is **enabled by default** on Cisco routers, switches, firewalls, and IP phones. No configuration is required to start using it. Option A describes LLDP. CDP messages are processed and discarded (not forwarded). The multicast MAC 0180.C200.000E belongs to LLDP; CDP uses 0100.0CCC.CCCC.

---

**2.** A network admin wants to discover non-Cisco neighbors on an interface. The admin runs `show lldp neighbors` but sees no output. What is the most likely cause?

- A) LLDP cannot detect non-Cisco devices
- B) LLDP is disabled by default on Cisco devices and has not been enabled
- C) The `show lldp neighbors` command requires a specific interface argument
- D) LLDP uses a different command: `show lldp table`

**Answer: B** — LLDP is **disabled by default** on Cisco devices. The admin must first enable it globally with `lldp run`, then enable both `lldp transmit` and `lldp receive` on the relevant interfaces. LLDP is the correct protocol for discovering non-Cisco neighbors.

---

**3.** What are the default hello timer and holdtime for CDP and LLDP respectively?

- A) CDP: 30s / 120s — LLDP: 60s / 180s
- B) CDP: 60s / 180s — LLDP: 30s / 120s
- C) CDP: 60s / 120s — LLDP: 30s / 180s
- D) Both protocols use 60s hello and 180s holdtime

**Answer: B** — CDP defaults: **60 second** hello, **180 second** holdtime (3×). LLDP defaults: **30 second** hello, **120 second** holdtime (4×). LLDP also has a 2-second reinit delay that CDP does not have.

---

**4.** Which statement correctly describes NTP stratum levels?

- A) Stratum 16 is the most accurate level — devices prefer stratum 16 servers
- B) Stratum 0 is a router that acts as the primary NTP server for an organization
- C) A lower stratum number indicates a more accurate time source closer to the reference clock
- D) Stratum 15 means the device is unsynchronized

**Answer: C** — **Lower stratum = more accurate = preferred**. Stratum 0 is the reference clock itself (atomic/GPS), not a network device. Stratum 16 means the device is **unsynchronized** (unusable). Stratum 15 is the maximum usable level.

---

**5.** R1 is configured with `ntp master 5`. R2 is configured with `ntp server 10.0.0.1` (pointing to R1). Which statement is true?

- A) R1 will sync its time from R2
- B) R1 acts as an NTP server at stratum 5; R2 syncs its time from R1 and becomes stratum 6
- C) Both routers sync from an external stratum 5 reference
- D) `ntp master 5` means R1 prefers stratum 5 servers over others

**Answer: B** — `ntp master 5` makes **R1 act as an NTP server** at stratum 5 (it claims to be a stratum 5 source). R2, configured as an NTP client of R1, syncs from R1 and becomes stratum **6** (one hop further than R1). R1 does not sync from R2 in this configuration.

---

**6.** During the DHCP DORA process, which messages are sent as broadcasts, and why is the Request still a broadcast even after the client has already chosen a server?

- A) Only Discover is broadcast; Request is unicast to the chosen server
- B) Discover and Request are broadcasts; Offer and ACK are unicast to the client
- C) All four DORA messages are broadcasts
- D) Discover and Request are broadcasts; this informs all DHCP servers of the outcome

**Answer: D** — Both **Discover** and **Request** are broadcasts (src: 0.0.0.0, dst: 255.255.255.255). The Request remains a broadcast because the client may have received offers from multiple DHCP servers. Broadcasting the Request informs ALL servers which offer was accepted, allowing the others to reclaim their offered addresses.

---

**7.** R1 has interface G0/0 (192.168.1.1/24) connected to a client subnet and G0/1 (10.0.0.1/30) connected toward the central DHCP server at 10.0.0.2. Where should `ip helper-address 10.0.0.2` be configured?

- A) On R1's G0/1 interface (facing the DHCP server)
- B) On the DHCP server itself
- C) On R1's G0/0 interface (facing the clients)
- D) On both G0/0 and G0/1 for redundancy

**Answer: C** — The DHCP relay agent command `ip helper-address` must be configured on the **interface facing the clients** — the interface where the DHCP Discover broadcast arrives (G0/0 in this case). The router converts the broadcast to a unicast and forwards it to the DHCP server's IP address.

---

**8.** An NMS sends a GetBulk message to a managed router. Which SNMP version is required, and which port does the router's SNMP agent listen on?

- A) SNMPv1 only; UDP port 162
- B) SNMPv2c or SNMPv3; UDP port 161
- C) SNMPv1 or SNMPv2c; UDP port 161
- D) SNMPv3 only; UDP port 162

**Answer: B** — **GetBulk was introduced in SNMPv2c** and is also supported in SNMPv3; it is NOT available in SNMPv1. The SNMP agent (managed device) listens on **UDP port 161** to receive Get/GetNext/GetBulk/Set messages from the NMS. UDP port 162 is where the NMS listens for Trap and Inform messages.

---

**9.** What is the key operational difference between an SNMP Trap and an SNMP Inform?

- A) Trap is sent from NMS to agent; Inform is sent from agent to NMS
- B) Trap is acknowledged by the NMS; Inform is not acknowledged
- C) Trap is not acknowledged (fire-and-forget); Inform is acknowledged and retransmitted if no ACK received
- D) Trap uses TCP; Inform uses UDP for reliability

**Answer: C** — **Trap** is a one-way, fire-and-forget notification — the agent sends it and does not know if the NMS received it. **Inform** is an acknowledged notification — if the NMS does not reply, the agent retransmits the Inform. Both use UDP. Inform was introduced in SNMPv2c and is more reliable but consumes more resources.

---

**10.** A security audit recommends upgrading SNMP from SNMPv2c to SNMPv3. What specific security capabilities does SNMPv3 provide that SNMPv2c lacks?

- A) SNMPv3 adds GetBulk and Inform messages not present in SNMPv2c
- B) SNMPv3 provides authentication (username/password) and encryption (AES/DES), which SNMPv2c lacks entirely
- C) SNMPv3 eliminates the need for community strings by using IP-based access control lists
- D) SNMPv3 uses TCP instead of UDP to ensure packet delivery and prevent eavesdropping

**Answer: B** — **SNMPv3 adds authentication** (username and password, not plaintext community strings) **and encryption** (AES or DES) to protect SNMP traffic from eavesdropping and tampering. SNMPv2c sends community strings in plaintext — any packet capture reveals the community string. Option A is wrong because GetBulk and Inform are SNMPv2c features (not SNMPv3 exclusives). SNMPv3 still uses UDP.
