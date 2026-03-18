# CCNA 200-301 Exam Coach — Section 08 Study Guide
## Days 46–50 | QoS, Security Fundamentals, Port Security, DHCP Snooping
### Transcripts 093–102 | Jeremy's IT Lab Complete Course

---

## SECTION 1: EXAM KNOWLEDGE MAP

| # | Video | Day | Topic | CCNA Domain | Exam Weight |
|---|-------|-----|-------|-------------|-------------|
| 093 | QoS Part 1 | Day 46 | IP phones, Voice VLANs, PoE, QoS intro (bandwidth/delay/jitter/loss), tail drop, RED/WRED | IP Services | 10% |
| 094 | Voice VLANs Lab | Day 46 Lab | Configure voice VLAN, PoE policing, switchport voice vlan command | IP Services | 10% |
| 095 | QoS Part 2 | Day 47 | Classification/marking, PCP/CoS, DSCP (DF/EF/AF/CS), trust boundaries, CBWFQ, LLQ, shaping/policing | IP Services | 10% |
| 096 | QoS Lab | Day 47 Lab | Apply QoS policy-map, class-map, marking, MLS QoS configuration | IP Services | 10% |
| 097 | Security Fundamentals | Day 48 | CIA triad, attack types (DoS/DDoS, spoofing, reflection/amplification, MITM, recon, malware, social engineering, password), MFA, AAA, RADIUS/TACACS+ | Security Fundamentals | 15% |
| 098 | Kali Linux Demo Lab | Day 48 Lab | DHCP starvation attack demo, ARP poisoning demo, Kali Linux tools | Security Fundamentals | 15% |
| 099 | Port Security | Day 49 | Port security overview, violation modes (shutdown/restrict/protect), sticky MACs, aging types, err-disable | Security Fundamentals | 15% |
| 100 | Port Security Lab | Day 49 Lab | Configure port-security, sticky learning, aging, err-disable recovery | Security Fundamentals | 15% |
| 101 | DHCP Snooping | Day 50 | Trusted/untrusted ports, DHCP starvation/poisoning attacks, binding table, rate-limiting, Option 82 | Security Fundamentals | 15% |
| 102 | DHCP Snooping Lab | Day 50 Lab | ip dhcp snooping, trust ports, rate-limit, Option 82 behavior, binding table verification | Security Fundamentals | 15% |

**Exam Objectives Covered:**
- 4.6 Describe QoS concepts including marking, device trust, prioritization, shaping, policing, and congestion management
- 5.1 Define key security concepts (threats, vulnerabilities, exploits, mitigation techniques)
- 5.2 Describe security program elements (user awareness, training, physical access control)
- 5.5 Describe security password policies (complexity, MFA, certificates, biometrics)
- 5.6 Configure and verify AAA for device access (RADIUS, TACACS+)
- 5.7 Configure and verify Layer 2 security features (DHCP snooping, port security)

---

## SECTION 2: MUST-KNOW CONCEPTS

---

### Concept 1: IP Phones, Voice VLANs, and PoE

**IP Phone Internal Architecture:**
- An IP phone contains an internal **3-port mini-switch**
  - Port 1: uplink to the external network switch
  - Port 2: downlink to a connected PC
  - Port 3: internal connection to the phone itself
- This allows **one switch port** to serve both the phone and PC simultaneously
- PC traffic flows through the IP phone to the switch

**Voice VLAN (Recommended Best Practice):**
- Separate voice traffic and data traffic into **different VLANs** on the same physical port
- PC traffic is sent **untagged** (access VLAN)
- IP phone traffic is sent **tagged** with the Voice VLAN ID (dot1q)
- Enables **QoS policies** to be applied differently to voice vs. data

**Voice VLAN Configuration:**
```
SW(config)# vlan 10
SW(config-vlan)# name DATA
SW(config)# vlan 20
SW(config-vlan)# name VOICE
SW(config)# interface fa0/1
SW(config-if)# switchport mode access
SW(config-if)# switchport access vlan 10        ! PC data traffic — untagged
SW(config-if)# switchport voice vlan 20         ! Phone voice traffic — tagged dot1q
```

**PoE (Power over Ethernet):**
- Allows a **Power Sourcing Equipment (PSE)** — typically a switch — to deliver DC power to a **Powered Device (PD)** over the Ethernet cable
- PDs: IP phones, IP cameras, wireless access points
- Process: PSE sends low-power test signal → determines PD power need → supplies required power
- **Power Policing** prevents PDs from drawing excessive power:

| Command | Behavior |
|---------|----------|
| `power inline police` | Default: err-disables port + syslog if PD draws too much power |
| `power inline police action err-disable` | Same as above (explicit form) |
| `power inline police action log` | Restarts interface + syslog; does NOT err-disable |

---

### Concept 2: QoS Introduction — Why QoS and Key Metrics

**Why QoS is Needed:**
- Modern networks are **converged** — voice, video, and data share the same IP infrastructure
- Different traffic types compete for bandwidth; without QoS all traffic gets equal treatment
- **QoS** = a set of tools used to give different treatment (priority, bandwidth guarantees) to different packet types

**Four Key QoS Metrics:**

| Metric | Definition | Voice Requirement |
|--------|-----------|-------------------|
| **Bandwidth** | Total capacity of the link (bits/sec) | Reserve minimum guaranteed bandwidth |
| **Delay** | Time from source to destination (one-way) | ≤ 150 ms one-way |
| **Jitter** | Variation in one-way delay between packets | ≤ 30 ms |
| **Loss** | % of packets that never reach destination | ≤ 1% |

- IP phones use a **jitter buffer** to absorb jitter and deliver a smooth, fixed-delay audio stream

**Tail Drop and TCP Global Synchronization:**
- When a queue fills up, new packets are dropped — this is **tail drop**
- TCP senders detect loss and reduce their send rate simultaneously → all flows throttle down at once, then all ramp up at once → **TCP global synchronization** (waves of congestion)

**Solution — RED / WRED:**
- **RED (Random Early Detection):** Randomly drops packets from some TCP flows *before* the queue is full → staggered slow-down; avoids synchronized global waves
- **WRED (Weighted RED):** Improved RED that applies different drop thresholds per traffic class (e.g., drop best-effort packets earlier than voice)

---

### Concept 3: QoS Classification and Marking

**Classification** identifies which traffic class a packet belongs to. Methods:
- **ACL** — traffic permitted by the ACL receives specific treatment
- **NBAR (Network Based Application Recognition)** — deep packet inspection up to Layer 7
- **PCP/CoS field** in the 802.1Q dot1q header (Layer 2)
- **DSCP field** in the IP header (Layer 3)

**PCP / CoS (Priority Code Point):**
- Found in the **802.1Q (dot1q) tag** — only available on trunk links or access ports with a Voice VLAN
- 3 bits → 8 values (0–7)
- Key values: PCP 0 = best effort; PCP 3 = call signaling (IP phones); PCP 5 = voice traffic

**DSCP (Differentiated Services Code Point):**
- Found in the **IP header ToS byte** (6 bits DSCP + 2 bits ECN)
- Replaced the older **IP Precedence (IPP)** field (3-bit, 8 values)
- DSCP provides 64 possible values; standardized markings defined by RFC 4954

**Standard DSCP Markings — Memorize These:**

| Marking | Full Name | DSCP Decimal | Use Case |
|---------|-----------|-------------|---------|
| **DF** | Default Forwarding | 0 | Best effort — regular traffic |
| **EF** | Expedited Forwarding | 46 | Low loss/latency/jitter — voice |
| **AF** | Assured Forwarding | Formula: 8x+2y | 12 standard values across 4 classes |
| **CS** | Class Selector | 0,8,16,24,32,40,48,56 | Backward compatibility with IPP |

**Assured Forwarding (AF) Values:**
- Format: **AF(class)(drop-precedence)** — class 1–4, drop precedence 1–3
- Formula for decimal DSCP value: **8 × class + 2 × drop-precedence**
- Higher class = higher priority; higher drop precedence = dropped first during congestion
- **AF41 = best treatment** (class 4, drop 1 → DSCP 34); **AF13 = worst treatment** (class 1, drop 3 → DSCP 14)

| | Drop 1 (Low) | Drop 2 (Med) | Drop 3 (High) |
|--|-------------|-------------|--------------|
| **Class 4** | AF41 = 34 | AF42 = 36 | AF43 = 38 |
| **Class 3** | AF31 = 26 | AF32 = 28 | AF33 = 30 |
| **Class 2** | AF21 = 18 | AF22 = 20 | AF23 = 22 |
| **Class 1** | AF11 = 10 | AF12 = 12 | AF13 = 14 |

**RFC 4954 Recommended Markings:**
- Voice: EF | Interactive Video: AF4x | Streaming Video: AF3x | High-Priority Data: AF2x | Best Effort: DF

---

### Concept 4: Trust Boundaries and Queuing

**Trust Boundary:**
- Defines where a network device **trusts vs. ignores** the QoS markings of received messages
- **Trusted:** forward the packet without changing its DSCP/CoS markings
- **Not Trusted:** re-mark the packet according to local policy

**Best Practice for IP Phones:**
- Move the trust boundary to the IP phone itself (configured on the switch port)
- PC traffic arriving through the IP phone has its markings overridden — a PC user cannot fake high-priority markings

**Queuing / Congestion Management:**
- Multiple queues exist per interface; classification places packets in the right queue
- A **scheduler** decides which queue to service next

| Method | Description |
|--------|------------|
| **FIFO** | Default — first in, first out; no priority differentiation |
| **Weighted Round-Robin** | Cycles through queues; takes more data from higher-priority queues each round |
| **CBWFQ (Class-Based Weighted Fair Queuing)** | Guarantees each class a minimum % of bandwidth during congestion |
| **LLQ (Low Latency Queuing)** | Adds a strict priority queue to CBWFQ; always served first if not empty — ideal for voice/video |

**LLQ Caveat:** If the strict priority queue is always busy, lower-priority queues may starve. Use **policing** to cap the strict priority queue's bandwidth.

**Shaping vs. Policing:**

| Feature | Shaping | Policing |
|---------|---------|---------|
| Action when rate exceeded | Buffers traffic in queue | Drops traffic (or re-marks) |
| Effect on traffic | Delays excess; smooths bursts | Discards or re-marks excess |
| Typical use | Egress — match ISP's CIR | Ingress or egress rate enforcement |

---

### Concept 5: CIA Triad and Key Security Terminology

**CIA Triad — Foundation of Security:**

| Principle | Meaning |
|-----------|---------|
| **Confidentiality** | Only authorized users can access data |
| **Integrity** | Data cannot be tampered with by unauthorized users; data is correct and authentic |
| **Availability** | Network/systems must be operational and accessible to authorized users |

**Key Security Terms:**

| Term | Definition |
|------|-----------|
| **Vulnerability** | A potential weakness that could compromise CIA |
| **Exploit** | Something that can be used to take advantage of a vulnerability |
| **Threat** | The potential for a vulnerability to be exploited |
| **Mitigation** | A technique or control that reduces or eliminates a threat |

**Critical Rule:** No system is perfectly secure. Defense is about reducing risk, not eliminating it.

---

### Concept 6: Common Attack Types

**DoS / DDoS Attacks (threaten Availability):**
- **DoS:** Single attacker floods a target with traffic to exhaust resources
- **TCP SYN Flood:** Attacker sends thousands of SYN packets; target replies with SYN-ACK; attacker never sends final ACK → connection table fills up → legitimate connections denied
- **DDoS:** Attacker uses a **botnet** (many infected machines) to amplify the flood

**Spoofing Attacks:**
- Use a **fake source IP or MAC address** to deceive the target
- Example: **DHCP Exhaustion** — attacker floods DHCP Discover messages with spoofed MAC addresses, exhausting the DHCP pool

**Reflection / Amplification Attacks:**
- **Reflection:** Attacker spoofs the target's IP as the source; a reflector (e.g., DNS server) sends large replies to the target
- **Amplification:** The reflector's reply is much larger than the attacker's request → the attack traffic is multiplied

**Man-in-the-Middle (MITM) Attacks:**
- Attacker positions themselves between source and destination to intercept or modify traffic
- Common method: **ARP Spoofing / ARP Poisoning** — attacker sends a crafted ARP Reply that overwrites a victim's ARP cache with the attacker's MAC address

**Reconnaissance Attacks:**
- Information-gathering to support future attacks (not directly harmful)
- Examples: `nslookup`, `whois` queries, port scanning

**Malware Types:**

| Type | How It Spreads | Primary Damage |
|------|---------------|----------------|
| **Virus** | Requires a host program; spreads via file sharing | Corrupts/modifies files |
| **Worm** | Self-replicating; spreads without user interaction | Network congestion; payload damage |
| **Trojan Horse** | Disguised as legitimate software; user installs it | Various; often opens backdoors |

**Social Engineering Attacks:**

| Attack | Description |
|--------|------------|
| **Phishing** | Fraudulent emails with fake links impersonating trusted organizations |
| **Spear Phishing** | Targeted phishing at specific company employees |
| **Whaling** | Phishing targeted at executives/high-profile individuals |
| **Vishing** | Voice phishing (phone calls) |
| **Smishing** | SMS-based phishing |
| **Watering Hole** | Compromise a website the target frequently visits |
| **Tailgating** | Physically following an authorized person through a secured door |

**Password Attacks:**
- **Dictionary Attack:** Tries common words and known passwords from a list
- **Brute Force Attack:** Tries every possible combination of characters

**Strong Password Criteria:** ≥8 characters; mix of upper/lowercase; letters + numbers; special characters; changed regularly

---

### Concept 7: MFA and AAA

**Multi-Factor Authentication (MFA):**
- Requires two or more of:
  - **Something you know** — password, PIN
  - **Something you have** — mobile push notification, badge/token
  - **Something you are** — biometrics (fingerprint, face scan, retina)
- Even if an attacker steals a password, they cannot log in without the second factor

**Digital Certificates:**
- Used to verify the identity of a website or entity
- Entity submits a **CSR (Certificate Signing Request)** to a **CA (Certificate Authority)**
- CA signs and issues the certificate; browsers/clients verify the CA's signature

**AAA Framework:**

| Component | Meaning | Example |
|-----------|---------|---------|
| **Authentication** | Verify identity | Login with username/password |
| **Authorization** | Grant appropriate access/permissions | Allow access to some files, deny others |
| **Accounting** | Record user activities | Log which commands were run, when |

**AAA Protocols:**

| Protocol | Standard | Transport | Ports |
|---------|----------|-----------|-------|
| **RADIUS** | Open standard | UDP | 1812 (auth), 1813 (accounting) |
| **TACACS+** | Cisco proprietary | TCP | 49 |

- Cisco's AAA server product: **ISE (Identity Services Engine)**
- TACACS+ encrypts the entire payload; RADIUS only encrypts the password field

---

### Concept 8: Port Security

**What Port Security Does:**
- A **Layer 2 switch security feature** that controls which source MAC addresses are allowed into a switchport
- Default behavior: one MAC address allowed; violation triggers **err-disable**

**Port Security Requirements:**
- Must be configured on **access ports** (not trunk ports, not EtherChannel members)
- Must explicitly enable with `switchport port-security`

**Three Ways to Define Allowed MACs:**
1. **Static** — manually enter the MAC address (`switchport port-security mac-address <mac>`)
2. **Dynamic** — allow the first MAC that appears (learned at runtime; lost on reload)
3. **Sticky** — dynamically learned AND saved to running-config (`switchport port-security mac-address sticky`)

**Sticky Secure MACs:**
- Saved to running-config as static entries — survive reboots if you `copy run start`
- Disabling sticky converts sticky addresses back to dynamic; enabling converts existing dynamic to sticky

**Secure MAC Aging:**

| Type | Behavior |
|------|---------|
| **Absolute** (default) | Timer starts when MAC is learned; expires regardless of traffic |
| **Inactivity** | Timer resets every time a frame from that MAC is received |

- Default aging time: 0 (no aging — MACs never expire)
- Configured with: `switchport port-security aging time <minutes>`

**Three Violation Modes:**

| Mode | Action on Unauthorized Frame | Interface Disabled? | Syslog/SNMP? | Counter Incremented? |
|------|------------------------------|---------------------|--------------|----------------------|
| **Shutdown** (default) | Err-disables the port | YES | YES (when disabled) | Set to 1 |
| **Restrict** | Discards unauthorized frames | NO | YES (each frame) | YES |
| **Protect** | Discards unauthorized frames | NO | NO | NO |

**Re-enabling an Err-Disabled Port:**

```
! Manual recovery:
SW(config)# interface fa0/1
SW(config-if)# shutdown
SW(config-if)# no shutdown

! Automatic recovery (recommended):
SW(config)# errdisable recovery cause psecure-violation
SW(config)# errdisable recovery interval 300     ! Recovery check interval (default 300 sec)
```

**Port Security Configuration:**
```
SW(config)# interface fa0/1
SW(config-if)# switchport mode access              ! Port security requires access mode
SW(config-if)# switchport port-security            ! Enable port security (default: 1 MAC, shutdown)
SW(config-if)# switchport port-security maximum 2  ! Allow up to 2 MACs
SW(config-if)# switchport port-security mac-address aaaa.bbbb.cccc   ! Static entry
SW(config-if)# switchport port-security mac-address sticky            ! Enable sticky learning
SW(config-if)# switchport port-security violation restrict            ! Set violation mode
SW(config-if)# switchport port-security aging time 60                 ! Age out after 60 min
SW(config-if)# switchport port-security aging type inactivity         ! Reset timer on activity

! Verification
SW# show port-security                      ! Summary of all secured ports
SW# show port-security interface fa0/1      ! Detail for one port
SW# show port-security address              ! All secure MAC addresses
SW# show mac address-table secure           ! Secure MACs in the MAC table
```

---

### Concept 9: DHCP Snooping

**What DHCP Snooping Does:**
- A **Layer 2 switch security feature** that filters DHCP messages on untrusted ports
- Only filters DHCP messages; all other traffic passes through unaffected
- All ports are **untrusted by default** — uplink ports toward DHCP servers must be manually marked trusted

**Trusted vs. Untrusted Port Behavior:**

| Condition | Action |
|-----------|--------|
| DHCP message on **trusted** port | Forward normally without inspection |
| **Server** message (OFFER, ACK, NAK) on **untrusted** port | **Discard** |
| **Client** message (DISCOVER, REQUEST) on **untrusted** port | Check source MAC == CHADDR field; forward if match, discard if mismatch |
| **Client** message (RELEASE, DECLINE) on **untrusted** port | Check source IP + interface against binding table; forward if match, discard if mismatch |

**DHCP Snooping Binding Table:**
- Automatically created when a client successfully leases an IP
- Entry contains: MAC address, IP address, VLAN, interface, lease time
- Used to validate RELEASE/DECLINE messages

**DHCP Attacks Prevented by DHCP Snooping:**

| Attack | How It Works | What Snooping Does |
|--------|-------------|-------------------|
| **DHCP Starvation** | Attacker floods DISCOVER messages with spoofed MACs to exhaust the DHCP pool | Drops messages where source MAC ≠ CHADDR |
| **DHCP Poisoning (MITM)** | Rogue DHCP server sends OFFER with attacker's IP as default gateway | Drops DHCP server messages on untrusted ports |

**DHCP Snooping Rate-Limiting:**
- Limits DHCP message rate per interface — triggers err-disable if exceeded
- `errdisable recovery cause dhcp-rate-limit` enables automatic recovery

**DHCP Option 82 (Relay Agent Information):**
- By default, Cisco switches add Option 82 to DHCP messages they forward (even if not acting as relay agents)
- By default, switches **drop** DHCP messages with Option 82 received on untrusted ports
- In multi-switch deployments, Option 82 must be consistently enabled or disabled across all switches to avoid drops

**DHCP Snooping Configuration:**
```
! Enable DHCP snooping globally and per VLAN
SW(config)# ip dhcp snooping
SW(config)# ip dhcp snooping vlan 10            ! Must enable per VLAN

! Mark uplink/server-facing ports as trusted
SW(config)# interface g0/1
SW(config-if)# ip dhcp snooping trust

! Rate-limit DHCP messages on untrusted ports
SW(config)# interface fa0/1
SW(config-if)# ip dhcp snooping limit rate 15   ! Max 15 DHCP messages/second

! Automatic recovery from err-disable due to rate limit
SW(config)# errdisable recovery cause dhcp-rate-limit

! Disable Option 82 insertion (if causing drops in multi-switch setup)
SW(config)# no ip dhcp snooping information option

! Verification
SW# show ip dhcp snooping                       ! Global settings and trusted ports
SW# show ip dhcp snooping binding               ! Binding table (MAC, IP, VLAN, interface)
SW# show ip dhcp snooping statistics            ! Forwarded, dropped, discarded counts
```

---

## SECTION 3: COMMON EXAM TRAPS

| Trap | Correct Answer |
|------|---------------|
| "QoS is only needed when the network is slow?" | FALSE — QoS is about **prioritization**, not raw speed. Even a fast network benefits from QoS to protect voice/video quality during bursts of data traffic. |
| "PCP/CoS markings work on all link types?" | FALSE — PCP is in the **802.1Q tag**, which is only present on **trunk links** or access ports with a **Voice VLAN**. It is NOT available on untagged links (e.g., between two routers). |
| "DSCP and IP Precedence use the same number of bits?" | FALSE — IP Precedence (old) used **3 bits** (8 values); DSCP (current) uses **6 bits** (64 values). DSCP backward-compatible with IPP via CS values. |
| "EF (Expedited Forwarding) DSCP value is 48?" | FALSE — EF decimal DSCP = **46**. CS6 = 48. Don't confuse them. |
| "AF41 has a higher drop probability than AF13?" | FALSE — Drop precedence is the **second digit**. AF4**1** has drop precedence 1 (low). AF1**3** has drop precedence 3 (high). AF41 gets **best treatment**; AF13 gets worst. |
| "LLQ guarantees no starvation of lower-priority queues?" | FALSE — LLQ's strict priority queue is **always served first**, which can **starve** other queues. Policing the strict queue prevents starvation. |
| "Shaping drops excess traffic to enforce rate limits?" | FALSE — **Shaping buffers** excess traffic in a queue (smooths bursts). **Policing drops** excess traffic. |
| "CIA triad: Integrity means only authorized users access data?" | FALSE — **Confidentiality** = access control. **Integrity** = data is not tampered with and is authentic. |
| "A Virus can spread without user interaction?" | FALSE — A **Virus** requires a host program and spreads when users share infected files. A **Worm** spreads autonomously without user interaction. |
| "RADIUS uses TCP for all communications?" | FALSE — **RADIUS uses UDP** (ports 1812/1813). **TACACS+ uses TCP** (port 49). |
| "TACACS+ only encrypts the password in the packet?" | FALSE — **TACACS+ encrypts the entire payload**. RADIUS only encrypts the password field. |
| "Port security can be configured on trunk ports?" | FALSE — Port security requires the port to be in **access mode** first (`switchport mode access`). It cannot be applied to trunk ports. |
| "The Protect violation mode generates a syslog message?" | FALSE — **Protect** silently discards unauthorized frames with NO syslog, NO SNMP, and NO violation counter increment. Only **Restrict** and **Shutdown** generate alerts. |
| "Sticky MACs are permanently saved automatically?" | FALSE — Sticky MACs are saved to **running-config**, not startup-config. You must `copy running-config startup-config` to make them survive a reboot. |
| "DHCP snooping blocks all non-DHCP traffic on untrusted ports?" | FALSE — DHCP snooping **only filters DHCP messages**. All other traffic passes through normally on untrusted ports. |
| "DHCP OFFER messages on trusted ports are dropped by snooping?" | FALSE — DHCP server messages (OFFER, ACK, NAK) on **trusted** ports are forwarded normally. They are only dropped on **untrusted** ports. |
| "DHCP Snooping must be enabled globally and that's sufficient?" | FALSE — DHCP snooping requires **two steps**: enable globally (`ip dhcp snooping`) AND enable per VLAN (`ip dhcp snooping vlan <id>`). |
| "Port security's default violation mode is Restrict?" | FALSE — Default violation mode is **Shutdown** (err-disables the port). |

---

## SECTION 4: COMPLETE COMMAND REFERENCE

### Voice VLAN and PoE Commands
```
! Configure data and voice VLANs on a port
SW(config)# vlan 10
SW(config)# vlan 20
SW(config)# interface fa0/1
SW(config-if)# switchport mode access
SW(config-if)# switchport access vlan 10          ! Data VLAN (PC — untagged)
SW(config-if)# switchport voice vlan 20           ! Voice VLAN (IP phone — dot1q tagged)

! PoE policing
SW(config-if)# power inline police               ! Err-disable + syslog if PD draws too much
SW(config-if)# power inline police action err-disable   ! Explicit form of above
SW(config-if)# power inline police action log    ! Restart interface + syslog (no err-disable)

! Verification
SW# show interfaces fa0/1 switchport              ! Shows access VLAN and voice VLAN
SW# show power inline                             ! PoE status for all ports
SW# show power inline fa0/1                       ! PoE detail for one port
```

### Port Security Commands
```
! Enable port security (port must be in access mode first)
SW(config-if)# switchport mode access
SW(config-if)# switchport port-security           ! Enable with defaults (max 1, shutdown)

! Set maximum number of allowed MAC addresses
SW(config-if)# switchport port-security maximum 3

! Configure allowed MACs
SW(config-if)# switchport port-security mac-address aaaa.bbbb.cccc   ! Static
SW(config-if)# switchport port-security mac-address sticky            ! Enable sticky

! Set violation mode
SW(config-if)# switchport port-security violation shutdown    ! Default — err-disable
SW(config-if)# switchport port-security violation restrict    ! Drop + log, no disable
SW(config-if)# switchport port-security violation protect     ! Silent drop, no log

! Configure aging
SW(config-if)# switchport port-security aging time 60         ! Age out after 60 minutes
SW(config-if)# switchport port-security aging type absolute   ! Default — timer starts on learn
SW(config-if)# switchport port-security aging type inactivity ! Timer resets on activity
SW(config-if)# switchport port-security aging static          ! Also age out static entries

! Err-disable recovery
SW(config)# errdisable recovery cause psecure-violation        ! Auto-recover port security
SW(config)# errdisable recovery interval 300                   ! Check interval (default 300s)

! Manual re-enable after err-disable
SW(config-if)# shutdown
SW(config-if)# no shutdown

! Verification
SW# show port-security                            ! Summary: all secured ports
SW# show port-security interface fa0/1            ! Detail: one port
SW# show port-security address                    ! All secure MAC addresses
SW# show mac address-table secure                 ! Secure MACs in MAC table
SW# show errdisable recovery                      ! Err-disable recovery settings
```

### DHCP Snooping Commands
```
! Enable DHCP snooping globally and per VLAN
SW(config)# ip dhcp snooping                      ! Enable globally
SW(config)# ip dhcp snooping vlan 10              ! Must also enable per VLAN
SW(config)# ip dhcp snooping vlan 10,20,30        ! Multiple VLANs

! Configure trusted ports (uplinks toward DHCP servers)
SW(config-if)# ip dhcp snooping trust             ! Mark port as trusted

! Rate-limit on untrusted ports
SW(config-if)# ip dhcp snooping limit rate 15     ! Max 15 DHCP msgs/sec

! Auto-recover from rate-limit err-disable
SW(config)# errdisable recovery cause dhcp-rate-limit

! Option 82 (disable if causing inter-switch drops)
SW(config)# no ip dhcp snooping information option   ! Disable Option 82 insertion

! Verification
SW# show ip dhcp snooping                         ! Global config, trusted ports, Option 82
SW# show ip dhcp snooping binding                 ! Binding table entries
SW# show ip dhcp snooping statistics              ! Counters (forwarded, dropped)
```

---

## SECTION 5: EXAM QUICK-REFERENCE TABLES

### QoS DSCP Standard Markings

| Marking | Full Name | DSCP Decimal | Use Case (RFC 4954) |
|---------|-----------|-------------|---------------------|
| DF | Default Forwarding | 0 | Best effort traffic |
| EF | Expedited Forwarding | 46 | Voice (low loss/latency/jitter) |
| AF41 | Assured Forwarding 4-1 | 34 | Interactive video (best AF) |
| AF31 | Assured Forwarding 3-1 | 26 | Streaming video |
| AF21 | Assured Forwarding 2-1 | 18 | High-priority data |
| CS6 | Class Selector 6 | 48 | Network control (OSPF, routing) |
| CS0 | Class Selector 0 | 0 | Same as DF; best effort |

### Queuing Method Comparison

| Method | Priority? | Bandwidth Guarantee? | Best For |
|--------|-----------|---------------------|---------|
| FIFO | No | No | Simple networks, single traffic type |
| CBWFQ | Yes (weighted) | Yes (% guaranteed) | Multi-class data networks |
| LLQ | Strict priority queue | Yes + strict queue | Voice and video (low latency critical) |

### Malware Type Comparison

| Type | Requires Host? | Spreads Autonomously? | Primary Effect |
|------|----------------|----------------------|----------------|
| Virus | YES | No (needs user action) | Corrupts/modifies files |
| Worm | No | YES (self-replicating) | Network congestion + payload |
| Trojan Horse | No | No (user installs it) | Backdoor, various damage |

### AAA Protocol Comparison

| Feature | RADIUS | TACACS+ |
|---------|--------|---------|
| Standard | Open (RFC) | Cisco Proprietary |
| Transport | UDP | TCP |
| Auth/Author Port | 1812 | 49 |
| Accounting Port | 1813 | 49 |
| Encryption | Password only | Full payload |
| Combines Auth + Author? | YES | NO (separated) |

### Port Security Violation Mode Comparison

| Mode | Disables Port? | Syslog/SNMP? | Counter Increments? | Unauthorized Frame |
|------|---------------|--------------|---------------------|--------------------|
| Shutdown (default) | YES (err-disable) | YES | YES (set to 1) | Discarded |
| Restrict | NO | YES (per frame) | YES | Discarded |
| Protect | NO | NO | NO | Discarded |

### Key Port Numbers for Days 46–50

| Protocol | Port | Transport | Notes |
|---------|------|-----------|-------|
| RADIUS (auth) | 1812 | UDP | AAA authentication |
| RADIUS (accounting) | 1813 | UDP | AAA accounting |
| TACACS+ | 49 | TCP | Cisco AAA protocol |
| DHCP Server/Client | 67/68 | UDP | DHCP; filtered by DHCP snooping |
| Voice VLAN / 802.1p | N/A | N/A | PCP field in 802.1Q tag, 3 bits |

---

## SECTION 6: PRACTICE QUIZ

**1.** An IP phone is connected to switch port fa0/1. The switch port is configured with `switchport access vlan 10` and `switchport voice vlan 20`. A PC is plugged into the IP phone's PC port. How does traffic flow?
- A) Both PC and phone traffic are tagged with VLAN 20
- B) PC traffic is untagged (VLAN 10); phone traffic is tagged with VLAN 20 via dot1q
- C) PC traffic is tagged with VLAN 10; phone traffic is untagged
- D) The phone and PC must be connected to separate switch ports

**Answer: B** — The access VLAN (10) carries **untagged** PC data traffic. The voice VLAN (20) carries **tagged** (dot1q) IP phone traffic on the same physical port. This is the standard converged port configuration for IP phone + PC deployments.

---

**2.** A network engineer needs to prioritize VoIP traffic to meet the recommended one-way delay, jitter, and loss standards. Which DSCP marking should be applied to voice bearer traffic per RFC 4954?
- A) DF (DSCP 0)
- B) CS6 (DSCP 48)
- C) AF41 (DSCP 34)
- D) EF (DSCP 46)

**Answer: D** — **EF (Expedited Forwarding)**, DSCP decimal **46**, is the RFC 4954 recommendation for voice traffic requiring low loss, low latency, and low jitter. AF4x is used for interactive video; DF is best effort; CS6 is for network control traffic.

---

**3.** A switch port uses LLQ queuing. The strict priority queue is always 100% utilized with voice traffic. What is the risk and what is the recommended mitigation?
- A) Voice quality will degrade; increase the queue depth
- B) Lower-priority queues will starve; apply policing to cap the strict priority queue
- C) The port will err-disable; use RESTRICT violation mode
- D) DSCP markings will be overwritten; move the trust boundary to the router

**Answer: B** — LLQ's strict priority queue is always served first when it has traffic. If it's constantly full, lower-priority queues (data, video) receive **no service** and starve. The solution is to **police** the strict priority queue, capping how much bandwidth it can consume and ensuring other queues get scheduled.

---

**4.** Which statement best describes the difference between shaping and policing?
- A) Shaping drops excess traffic; policing buffers it
- B) Shaping buffers excess traffic to smooth the rate; policing drops (or re-marks) excess traffic
- C) Both shaping and policing drop excess traffic; they differ only in direction (ingress vs. egress)
- D) Shaping is used for voice; policing is used for data

**Answer: B** — **Shaping** delays excess traffic by placing it in a buffer — the traffic is smoothed and eventually sent, staying below the configured rate. **Policing** immediately drops or re-marks packets that exceed the configured rate, with no buffering.

---

**5.** An attacker sends thousands of ARP Reply frames to PC1, claiming that the MAC address of the default gateway (10.0.0.1) is the attacker's MAC. What attack is this, and what CIA principles does it threaten?
- A) DoS attack; threatens Availability
- B) ARP Spoofing / ARP Poisoning (MITM); threatens Confidentiality and Integrity
- C) DHCP Starvation; threatens Availability
- D) Brute Force attack; threatens Confidentiality

**Answer: B** — This is **ARP Poisoning**, a form of **Man-in-the-Middle attack**. By poisoning PC1's ARP cache, the attacker can intercept all traffic PC1 sends to the gateway (threatening **Confidentiality**) and potentially modify it before forwarding (threatening **Integrity**). Availability is not the primary concern here.

---

**6.** A company requires users to enter a password AND press "Accept" on a push notification on their registered phone to log in. What type of authentication is this?
- A) Single-factor authentication using TACACS+
- B) Multi-Factor Authentication (MFA) using "something you know" + "something you have"
- C) AAA authentication with RADIUS over UDP
- D) Biometric authentication combining voice and fingerprint

**Answer: B** — This is **MFA** combining: (1) **Something you know** (the password) and (2) **Something you have** (the registered phone that receives the push notification). MFA greatly reduces risk because an attacker who steals the password still cannot authenticate without the second factor.

---

**7.** Port security is configured on fa0/1 with violation mode **Restrict**. An attacker connects a device with an unauthorized MAC address and sends 50 frames. What happens?
- A) The port is err-disabled after the first unauthorized frame
- B) All 50 frames are forwarded; the unauthorized MAC is added to the allowed list
- C) All 50 frames are discarded; the port stays up; a syslog/SNMP alert is generated; the violation counter increments by 50
- D) All 50 frames are discarded; no log or counter activity occurs

**Answer: C** — **Restrict** mode silently discards unauthorized frames but keeps the port **active**. It generates a **syslog/SNMP alert** for each unauthorized frame and increments the **violation counter** by one per frame. Shutdown mode would err-disable the port; Protect mode would discard silently with no alert and no counter.

---

**8.** A switch has sticky port security enabled on fa0/1. After the switch learns MAC aaaa.bbbb.cccc dynamically, the admin runs `copy running-config startup-config`. The switch is then rebooted. What happens to the sticky MAC?
- A) The sticky MAC is lost — it must be re-learned after reboot
- B) The sticky MAC is retained — it was saved to startup-config before the reboot
- C) The sticky MAC is retained — sticky MACs are automatically saved to NVRAM
- D) The sticky MAC is retained only if the aging timer has not expired

**Answer: B** — Sticky MACs are saved to **running-config** (not startup-config automatically). After `copy running-config startup-config`, the entry is preserved in NVRAM and survives a reboot. Without that copy, the sticky MAC would be lost on reload.

---

**9.** DHCP snooping is enabled on a switch. SW1 is connected to SW2 via an uplink. SW2's uplink port toward SW1 is left as untrusted. A DHCP server is connected upstream of SW1. A client on SW2 sends a DHCP Discover. What happens?
- A) SW2 forwards the Discover to SW1; SW1 drops it because DHCP snooping is enabled
- B) SW1 sends a DHCP Offer back to SW2; SW2 drops it on the untrusted uplink port
- C) The DHCP Discover is forwarded correctly and the client receives an address
- D) SW2 drops the DHCP Discover because it came from an untrusted port

**Answer: B** — The client's DISCOVER is a **client message**, forwarded by SW2's untrusted port (client messages are allowed after CHADDR validation). SW1 forwards it to the DHCP server. The DHCP server sends an OFFER back through SW1 to SW2. But SW2 receives the DHCP **OFFER (server message)** on its uplink port — which is **untrusted** — and **drops it**. The fix: mark SW2's uplink port toward SW1 as `ip dhcp snooping trust`.

---

**10.** Which two statements are TRUE about TACACS+ compared to RADIUS?
- A) TACACS+ uses UDP; RADIUS uses TCP
- B) TACACS+ uses TCP port 49; RADIUS uses UDP ports 1812/1813
- C) TACACS+ encrypts the full payload; RADIUS only encrypts the password
- D) TACACS+ is an open standard; RADIUS is Cisco proprietary
- E) Both protocols combine authentication and authorization into a single process

**Answer: B and C** — TACACS+ uses **TCP port 49** for all communications; RADIUS uses **UDP port 1812** (auth) and **1813** (accounting). TACACS+ encrypts the **entire packet payload** for stronger security; RADIUS only encrypts the password field. TACACS+ is **Cisco proprietary**; RADIUS is the **open standard** — the opposite of option D. TACACS+ **separates** authentication, authorization, and accounting; RADIUS combines auth and authorization.
