# CCNA 200-301 Exam Coach — Section 04 Study Guide
## Days 26–30 | IP Connectivity (cont.) + Network Fundamentals: OSPF Parts 1–3, FHRPs, TCP & UDP
### Transcripts 050–062 | Jeremy's IT Lab Complete Course

---

## SECTION 1: EXAM KNOWLEDGE MAP

| # | Video | Day | Topic | CCNA Domain | Exam Weight |
|---|-------|-----|-------|-------------|-------------|
| 050 | OSPF Part 1 | Day 26 | Link state, OSPF areas, basic config, network command | IP Connectivity | 25% |
| 051 | OSPF Part 1 Lab | Day 26 Lab | Single-area OSPFv2 configuration, show ip protocols | IP Connectivity | 25% |
| 052 | OSPF Part 2 | Day 27 | OSPF cost, neighbor states, message types, interface config | IP Connectivity | 25% |
| 053 | OSPF Part 2 Lab | Day 27 Lab | Cost tuning, reference bandwidth, neighbor verification | IP Connectivity | 25% |
| 054 | OSPF Part 3 | Day 28 | Loopback, network types, DR/BDR, serial interfaces, LSA types | IP Connectivity | 25% |
| 055 | OSPF Part 3 Lab | Day 28 Lab | DR/BDR election, point-to-point config, neighbor requirements | IP Connectivity | 25% |
| 056 | FHRPs | Day 29 | HSRP, VRRP, GLBP — virtual IP/MAC, active/standby | IP Connectivity | 25% |
| 057 | FHRPs Lab | Day 29 Lab | HSRP configuration, preempt, show standby | IP Connectivity | 25% |
| 058 | TCP and UDP | Day 30 | Layer 4, connection-oriented vs connectionless, port numbers | Network Fundamentals | 20% |
| 059 | TCP/UDP Lab | Day 30 Lab | Port number identification, protocol selection reasoning | Network Fundamentals | 20% |

**Exam Objectives Covered:**
- 3.4 Configure and verify single area OSPFv2
- 3.5 Describe the purpose, functions, and concepts of first hop redundancy protocols
- 1.5 Compare TCP to UDP
- 1.6 Configure and verify IPv4 addressing and subnetting (port number context)
- 4.1 Configure and verify inside source NAT using static and pools (port number foundation)

---

## SECTION 2: MUST-KNOW CONCEPTS

---

### Concept 1: OSPF Overview and Areas

**What OSPF Does (3 Steps):**
1. **Become neighbors** — routers on the same segment discover each other
2. **Exchange LSAs** — share link state information to build the LSDB
3. **Calculate best routes** — each router independently runs Dijkstra's SPF algorithm

**Key Facts:**
- Stands for **Open Shortest Path First**; uses **Dijkstra's (SPF) Algorithm**
- Link State IGP — every router builds a complete map of the network
- OSPFv2 = IPv4 | OSPFv3 = IPv6
- AD = **110**
- LSAs have a **30-minute aging timer** — re-flooded when expired
- IP protocol number = **89**
- Hello messages sent to multicast **224.0.0.5** (all OSPF routers)

**OSPF Areas:**

| Term | Definition |
|------|-----------|
| Area | Set of routers and links sharing the same LSDB |
| Backbone Area | Area 0 — all other areas must connect to it |
| Internal Router | All interfaces in the same area |
| ABR (Area Border Router) | Interfaces in multiple areas; maintains separate LSDB per area |
| Backbone Router | Router with an interface in Area 0 |
| Intra-area route | Destination in the same OSPF area |
| Inter-area route | Destination in a different OSPF area |

**ABR Rules:**
- Recommended maximum: **2 areas** per ABR (3+ overburdens the router)
- Areas must be **contiguous** (no split areas)
- All areas must have **at least one ABR connected to Area 0**
- Interfaces in the same subnet must be in the **same area**

---

### Concept 2: OSPF Basic Configuration

```
! Method 1: network command (wildcard mask, specify area)
R1(config)# router ospf 1                        ! Process ID — locally significant
R1(config-router)# network 10.0.12.0 0.0.0.3 area 0
R1(config-router)# network 10.0.13.0 0.0.0.3 area 0
R1(config-router)# network 172.16.1.0 0.0.0.15 area 0

! Method 2: activate directly on interface
R1(config-if)# ip ospf 1 area 0

! Passive interface (stops hello messages; still advertises network)
R1(config-router)# passive-interface g2/0
R1(config-router)# passive-interface default        ! All passive
R1(config-router)# no passive-interface g0/0        ! Un-passive specific interface

! Advertise default route into OSPF
R1(config-router)# default-information originate

! Change AD (default 110)
R1(config-router)# distance 100

! Set router ID manually
R1(config-router)# router-id 1.1.1.1
```

**Key Config Notes:**
- Process ID is **locally significant** — routers with different Process IDs CAN become OSPF neighbors
- `network` command uses wildcard masks (same as EIGRP)
- OSPF process ID ≠ OSPF area number

---

### Concept 3: OSPF Cost (Metric)

**Formula:** `Cost = Reference Bandwidth / Interface Bandwidth`

**Default Reference Bandwidth = 100 Mbps:**

| Interface Speed | Default Cost |
|----------------|-------------|
| 10 Mbps (Ethernet) | 10 |
| 100 Mbps (FastEthernet) | 1 |
| 1 Gbps (GigabitEthernet) | 1 |
| 10 Gbps | 1 |

**Problem:** FastEthernet, GigabitEthernet, and 10GigE all have cost = 1 (can't differentiate!)

**Fix:** Change the reference bandwidth to a larger value on ALL routers:
```
R1(config-router)# auto-cost reference-bandwidth 100000   ! 100 Gbps reference
! Now: FastEthernet = 1000, GigEthernet = 100, 10GigE = 10
```

**Three Ways to Change OSPF Cost (priority order):**
1. Manual: `R1(config-if)# ip ospf cost <value>` — overrides everything
2. Change reference bandwidth: `auto-cost reference-bandwidth <Mbps>`
3. Change interface bandwidth: `bandwidth <Kbps>` — NOT recommended (affects other calculations)

**Total Cost Rule:** The OSPF cost to a destination = sum of **outgoing/exit interface** costs along the path.
- Loopback interfaces have a cost of **1**

---

### Concept 4: OSPF Neighbor States

OSPF adjacency formation goes through 7 states:

| State | Description |
|-------|-------------|
| **Down** | No hello received yet; router sends hello to 224.0.0.5 |
| **Init** | Hello received from neighbor, but my RID not in it yet |
| **2-Way** | Received hello containing my own RID; basic neighbor relationship formed; DR/BDR elected here |
| **ExStart** | Determine master/slave for exchange; higher RID = master |
| **Exchange** | Exchange DBD (Database Description) packets — summary of LSDB |
| **Loading** | Exchange LSR (requests) / LSU (updates) / LSAck (acknowledgements) for missing LSAs |
| **Full** | Identical LSDBs; full OSPF adjacency established |

**OSPF Message Types:**

| Type | Name | Purpose |
|------|------|---------|
| 1 | Hello | Discover/maintain neighbors; sent every 10s (Ethernet) |
| 2 | DBD (Database Description) | Summary of LSDB during exchange |
| 3 | LSR (Link State Request) | Request specific LSAs from neighbor |
| 4 | LSU (Link State Update) | Send requested LSAs |
| 5 | LSAck (Acknowledgement) | Confirm receipt of LSAs |

**Timers (Ethernet defaults):**
- Hello timer: **10 seconds**
- Dead timer: **40 seconds** (4 × hello; neighbor removed if no hello received)

---

### Concept 5: OSPF Network Types

| Network Type | Default On | DR/BDR? | Neighbor Discovery | Hello/Dead |
|-------------|-----------|---------|-------------------|-----------|
| **Broadcast** | Ethernet, FDDI | YES | Dynamic (224.0.0.5) | 10s / 40s |
| **Point-to-Point** | PPP, HDLC serial | NO | Dynamic (224.0.0.5) | 10s / 40s |
| **Non-Broadcast** | Frame Relay, X.25 | YES | Manual | 30s / 120s |

**CCNA Focus: Broadcast and Point-to-Point only**

**DR/BDR (Broadcast networks only):**
- **DR (Designated Router):** all routers form Full adjacency with DR
- **BDR (Backup Designated Router):** takes over if DR fails
- **DROther:** forms Full adjacency ONLY with DR and BDR; NOT with other DROthers
- DROthers still have the same LSDB — just exchange LSAs only via DR/BDR

**DR/BDR Election Priority:**
1. Highest OSPF **interface priority** (default = 1 on all interfaces)
2. Highest OSPF **Router ID**
- Priority 0 = router CANNOT be DR or BDR

**Election is non-preemptive** — DR/BDR keep roles until OSPF is reset, interface fails, or router is shut down.

**Key Multicast Addresses:**
- `224.0.0.5` — All OSPF routers (hello, general)
- `224.0.0.6` — DR and BDR only (DROthers send LSAs here)

**Configure network type on an interface:**
```
R1(config-if)# ip ospf network point-to-point    ! No DR/BDR election
R1(config-if)# ip ospf network broadcast
R1(config-if)# ip ospf priority 0               ! Prevent from being DR/BDR
R1(config-if)# ip ospf priority 255             ! Force to be DR
```

---

### Concept 6: OSPF Neighbor Requirements

For two routers to become OSPF neighbors, ALL of these must match:

| Requirement | Notes |
|-------------|-------|
| Area number | Must match |
| Same subnet | Interfaces must be in the same subnet |
| OSPF process not shutdown | Both must have active OSPF process |
| Unique Router IDs | Duplicate RIDs prevent neighbor formation |
| Hello and Dead timers | Must match |
| Authentication settings | Must match |
| IP MTU | Mismatch: routers may form neighbors but OSPF won't function properly |
| Network type | Mismatch: routers appear as neighbors but routes won't show in routing table |

---

### Concept 7: OSPF LSA Types (CCNA Relevant)

| LSA Type | Name | Generated By | Purpose |
|----------|------|-------------|---------|
| Type 1 | Router LSA | Every OSPF router | Lists router's ID and its OSPF-activated interfaces/networks |
| Type 2 | Network LSA | DR of a broadcast network | Lists routers attached to that multi-access network |
| Type 5 | AS External LSA | ASBR (Autonomous System Border Router) | Describes routes to destinations outside the OSPF AS |

**Loopback Interface:**
- Virtual interface — always up/up (never goes down unless manually shut)
- Provides a stable Router ID and a consistent IP to reach the router
- OSPF cost = 1 (regardless of speed)

---

### Concept 8: First Hop Redundancy Protocols (FHRPs)

**Problem:** If a host's default gateway router goes down, traffic to external networks stops — even if a second router is available.

**Solution:** Two or more routers share a **Virtual IP (VIP)** address. Hosts use the VIP as their default gateway. Routers send hello messages; one is Active, others are Standby.

**How Failover Works:**
1. Active router fails → stops sending hellos
2. Standby router promotes itself to Active
3. New Active router sends a **Gratuitous ARP** (unsolicited ARP reply, broadcast) to update switch MAC address tables
4. Hosts don't need to reconfigure — they still use the same VIP

**Non-preemptive by default** — original Active router does NOT automatically reclaim Active role when it returns (can be enabled with `preempt`).

**FHRP Comparison Table:**

| Feature | HSRP | VRRP | GLBP |
|---------|------|------|------|
| Standard | Cisco proprietary | Open (RFC 5798) | Cisco proprietary |
| Active/Standby terms | Active / Standby | Master / Backup | AVG / AVF |
| IPv6 support | HSRPv2 only | Yes | Yes |
| Load balancing | Per-VLAN (different active per subnet) | Per-VLAN | Within single subnet (up to 4 AVFs) |
| Multicast v4 | v1: 224.0.0.2 / v2: 224.0.0.102 | 224.0.0.18 | 224.0.0.102 |
| Virtual MAC | v1: 0000.0c07.acXX / v2: 0000.0c9f.fXXX | 0000.5e00.01XX | 0007.b400.XXYY |

**HSRP Virtual MAC:**
- v1: `0000.0c07.ac**XX**` (XX = group number in hex)
- v2: `0000.0c9f.f**XXX**` (XXX = group number in hex)

**GLBP Roles:**
- **AVG (Active Virtual Gateway):** elected leader; assigns virtual MACs to AVFs
- **AVF (Active Virtual Forwarder):** forwards traffic for its assigned hosts; up to 4 per group

---

### Concept 9: HSRP Configuration

```
! R1 (higher priority = becomes Active)
R1(config-if)# standby version 2                  ! Use HSRPv2 (recommended)
R1(config-if)# standby 1 ip 192.168.1.254         ! Group 1, virtual IP
R1(config-if)# standby 1 priority 110             ! Default 100; higher = preferred Active
R1(config-if)# standby 1 preempt                  ! Reclaim Active role if it returns

! R2 (lower priority = becomes Standby)
R2(config-if)# standby version 2
R2(config-if)# standby 1 ip 192.168.1.254
R2(config-if)# standby 1 priority 100             ! Default; becomes Standby

! Verify
R1# show standby
R1# show standby brief
```

**Key HSRP Rules:**
- Group number must **match** on all routers in the same subnet
- HSRP versions are NOT cross-compatible — all routers must use same version
- Higher priority = Active; lower = Standby (tie = higher IP wins)

---

### Concept 10: TCP and UDP

**Layer 4 Functions:**
- Identifies application-layer protocol via **port numbers**
- **Session multiplexing** — allows multiple concurrent sessions between same hosts
- Provides (TCP) or omits (UDP) reliability, sequencing, and flow control

**Port Number Ranges:**

| Range | Type | Examples |
|-------|------|---------|
| 0–1023 | Well-Known | HTTP 80, HTTPS 443, SSH 22, Telnet 23, DNS 53, SMTP 25, DHCP 67/68, TFTP 69, SNMP 161/162, FTP 20/21 |
| 1024–49151 | Registered | Application-specific |
| 49152–65535 | Ephemeral/Dynamic | Source ports assigned randomly by client OS |

**TCP (Transmission Control Protocol) — Connection-Oriented:**

| Feature | Detail |
|---------|--------|
| Connection setup | 3-way handshake: SYN → SYN-ACK → ACK |
| Connection teardown | 4-way: FIN → ACK → FIN → ACK |
| Reliability | ACK required for every segment; retransmit if lost |
| Sequencing | Sequence numbers allow correct reassembly out-of-order |
| Flow control | Window size — receiver controls sender's rate |
| Use cases | File transfer, email, web browsing (anything needing reliability) |

**UDP (User Datagram Protocol) — Connectionless:**

| Feature | Detail |
|---------|--------|
| Connection | None — data sent immediately without setup |
| Reliability | No ACKs, no retransmission |
| Sequencing | No sequence numbers |
| Flow control | None |
| Error checking | Checksum only |
| Use cases | VoIP, video streaming, DNS, DHCP, TFTP, SNMP (speed > reliability) |

**TCP vs UDP Header Fields:**

| Field | TCP | UDP |
|-------|-----|-----|
| Source Port | YES | YES |
| Destination Port | YES | YES |
| Sequence Number | YES | NO |
| Acknowledgement Number | YES | NO |
| Window Size | YES | NO |
| Checksum | YES | YES |
| Header size | 20 bytes (minimum) | 8 bytes |

**Key Port Numbers to Memorize:**

| Protocol | Port | Transport |
|---------|------|----------|
| FTP data | 20 | TCP |
| FTP control | 21 | TCP |
| SSH | 22 | TCP |
| Telnet | 23 | TCP |
| SMTP | 25 | TCP |
| DNS | 53 | TCP + UDP |
| DHCP server | 67 | UDP |
| DHCP client | 68 | UDP |
| TFTP | 69 | UDP |
| HTTP | 80 | TCP |
| HTTPS | 443 | TCP |
| POP3 | 110 | TCP |
| SNMP | 161/162 | UDP |
| SYSLOG | 514 | UDP |

---

## SECTION 3: COMMON EXAM TRAPS

| Trap | Correct Answer |
|------|---------------|
| "OSPF Process ID must match between neighbors?" | FALSE — Process ID is locally significant; different IDs can still form adjacency |
| "Which OSPF state triggers DR/BDR election?" | 2-Way state (after both routers see each other's RID in hellos) |
| "DROthers form Full adjacency with all routers?" | FALSE — DROthers form Full adjacency ONLY with DR and BDR, not each other |
| "OSPF Dead timer default on Ethernet?" | 40 seconds (4× hello of 10s) |
| "What multicast does OSPF use to send to DR/BDR?" | 224.0.0.6 (DROthers → DR/BDR); 224.0.0.5 is for all OSPF routers |
| "FastEthernet and GigabitEthernet have same OSPF cost?" | YES (both = 1 with default 100 Mbps reference); fix with `auto-cost reference-bandwidth` |
| "Changing interface bandwidth changes its actual speed?" | FALSE — `bandwidth` only changes the value used in metric calculations; use `speed` to change actual speed |
| "DR/BDR election — is it preemptive?" | NO — non-preemptive; original DR keeps role even if a higher-priority router joins |
| "OSPF neighbor mismatch on MTU — do they become neighbors?" | They may appear as neighbors but OSPF won't function properly (special requirement) |
| "FHRP is preemptive by default?" | NO — must explicitly configure `preempt` (HSRP) for automatic Active role recovery |
| "HSRP versions 1 and 2 are compatible?" | NO — all routers in same group must use same HSRP version |
| "GLBP load balances differently than HSRP?" | YES — GLBP load balances within a single subnet (up to 4 AVFs); HSRP only per-VLAN |
| "VRRP terminology — what is the Active router called?" | Master (not Active — that's HSRP terminology) |
| "TCP uses 3-way handshake — what are the steps?" | SYN → SYN-ACK → ACK |
| "DNS uses TCP or UDP?" | Both (UDP for normal queries; TCP for zone transfers or large responses) |
| "Which port does DHCP server listen on?" | 67 (client sends to server on 67; server responds to client on 68) |

---

## SECTION 4: COMPLETE COMMAND REFERENCE

### OSPF Commands
```
R(config)# router ospf <process-id>
R(config-router)# router-id <A.B.C.D>
R(config-router)# network <network> <wildcard> area <area-id>
R(config-router)# passive-interface <interface>
R(config-router)# passive-interface default
R(config-router)# no passive-interface <interface>
R(config-router)# default-information originate
R(config-router)# auto-cost reference-bandwidth <Mbps>   ! Default 100; set to 1000 or 10000
R(config-router)# distance <1-255>                       ! Change AD (default 110)
R(config-if)# ip ospf <process-id> area <area-id>        ! Activate OSPF directly on interface
R(config-if)# ip ospf cost <1-65535>                     ! Manual cost override
R(config-if)# ip ospf priority <0-255>                   ! DR/BDR election priority (0 = never DR)
R(config-if)# ip ospf network {broadcast | point-to-point | non-broadcast}
R(config-if)# ip ospf hello-interval <seconds>
R(config-if)# ip ospf dead-interval <seconds>
R# show ip ospf                                          ! OSPF process info
R# show ip ospf neighbor                                 ! Neighbor table and states
R# show ip ospf neighbor detail                          ! Detailed neighbor info
R# show ip ospf interface <interface>                    ! OSPF interface details (cost, timers, DR/BDR)
R# show ip ospf database                                 ! LSDB contents
R# show ip protocols                                     ! Routing protocol summary
R# show ip route ospf                                    ! OSPF routes only (marked O or O IA)
```

### HSRP Commands
```
R(config-if)# standby version {1 | 2}
R(config-if)# standby <group> ip <virtual-ip>
R(config-if)# standby <group> priority <0-255>          ! Default 100; higher = Active
R(config-if)# standby <group> preempt                   ! Reclaim Active role automatically
R# show standby                                         ! Detailed HSRP status
R# show standby brief                                   ! Summary table
```

### Serial Interface Commands
```
R# show controllers <interface>                         ! Identify DCE vs DTE side
R(config-if)# clock rate <bps>                         ! DCE side only (sets speed)
R(config-if)# encapsulation {hdlc | ppp}               ! Default: HDLC; must match both ends
```

---

## SECTION 5: EXAM QUICK-REFERENCE TABLES

### OSPF Neighbor States

| State | Key Event | Exchange Type |
|-------|-----------|--------------|
| Down | No hellos received | — |
| Init | Hello received (no my RID in it) | Hello |
| 2-Way | Hello received with my RID; DR/BDR elected | Hello |
| ExStart | Determine master (higher RID) / slave | DBD (empty) |
| Exchange | Share LSDB summaries | DBD (with LSA headers) |
| Loading | Request/send missing LSAs | LSR / LSU / LSAck |
| Full | Identical LSDBs; adjacency complete | — (hellos only) |

### FHRP Quick Reference

| | HSRP v1 | HSRP v2 | VRRP | GLBP |
|-|---------|---------|------|------|
| Standard | Cisco | Cisco | Open | Cisco |
| Active name | Active | Active | Master | AVG/AVF |
| Multicast | 224.0.0.2 | 224.0.0.102 | 224.0.0.18 | 224.0.0.102 |
| Virtual MAC prefix | 0000.0c07.ac | 0000.0c9f.f | 0000.5e00.01 | 0007.b400 |
| LB method | Per-VLAN | Per-VLAN | Per-VLAN | Per-host within subnet |

### TCP vs UDP Summary

| Feature | TCP | UDP |
|---------|-----|-----|
| Connection | Connection-oriented (3-way handshake) | Connectionless |
| Reliability | YES (ACKs + retransmission) | NO |
| Sequencing | YES | NO |
| Flow control | YES (window size) | NO |
| Header size | 20 bytes | 8 bytes |
| Speed | Slower (overhead) | Faster |
| Examples | HTTP, HTTPS, FTP, SSH, Telnet, SMTP | DNS, DHCP, TFTP, VoIP, SNMP, SYSLOG |

### Critical Port Numbers

| Port | Protocol | Transport |
|------|---------|----------|
| 20 | FTP data | TCP |
| 21 | FTP control | TCP |
| 22 | SSH | TCP |
| 23 | Telnet | TCP |
| 25 | SMTP | TCP |
| 53 | DNS | TCP + UDP |
| 67 | DHCP (server) | UDP |
| 68 | DHCP (client) | UDP |
| 69 | TFTP | UDP |
| 80 | HTTP | TCP |
| 110 | POP3 | TCP |
| 161 | SNMP | UDP |
| 162 | SNMP trap | UDP |
| 443 | HTTPS | TCP |
| 514 | Syslog | UDP |

---

## SECTION 6: PRACTICE QUIZ

**1.** A network admin changes the OSPF reference bandwidth to 10,000 Mbps on R1 only. R2 still uses the default 100 Mbps. What is the most likely result?
- A) OSPF adjacency fails completely
- B) OSPF still works but routing may be suboptimal due to inconsistent cost calculations
- C) R1 and R2 cannot exchange LSAs
- D) R1 will not generate Router LSAs

**Answer: B** — The reference bandwidth change affects only cost calculations locally. OSPF adjacency still forms (it's not a neighbor requirement), but routes may be suboptimal because R1 and R2 calculate different costs for the same paths. Always change reference bandwidth on **all** routers.

---

**2.** In OSPF, which state do two routers reach when they have received each other's hello packets and confirmed the neighbor relationship, just before DR/BDR election?
- A) ExStart
- B) Init
- C) 2-Way
- D) Exchange

**Answer: C** — The **2-Way** state is reached when a router sees its own Router ID in a received hello. This confirms the bidirectional relationship. DR/BDR election occurs at the end of this state (on broadcast networks).

---

**3.** An OSPF broadcast network has 5 routers. How many Full adjacencies exist in total?
- A) 10 (full mesh)
- B) 8 (DR + BDR each form Full with 4 DROthers = 4+4; DR-BDR = 1)
- C) 4 (only DR forms Full with others)
- D) 5

**Answer: B** — DR forms Full with BDR + 3 DROthers = 4. BDR forms Full with DR + 3 DROthers = 4. But DR-BDR adjacency is counted once. Total = (4 DROther×DR) + (4 DROther×BDR) + (1 DR×BDR) — but each adjacency counted from both sides means: DR has 4 Full (BDR + 3 others), BDR has 4 Full (DR + 3 others), each DROther has 2 Full (DR + BDR). Unique adjacencies = 4 + 3 = **8** (DR↔BDR, DR↔3DROthers, BDR↔3DROthers; without double counting that's 1+3+3 = **7** unique bidirectional adjacencies). The correct answer for the CCNA is: DROthers form Full only with DR and BDR — so each DROther has 2 Full adjacencies, avoiding n(n-1)/2 = 10 full mesh.

---

**4.** R1's OSPF interface priority is set to 0. What does this mean?
- A) R1 becomes the DR
- B) R1 has the highest priority and will always be elected DR
- C) R1 will never be elected DR or BDR
- D) R1 will not send hello messages

**Answer: C** — Priority 0 disables DR/BDR candidacy for that interface. The router will be a DROther. Priority 255 forces DR election.

---

**5.** R1 is the HSRP Active router with priority 110. R1 fails, and R2 (priority 100) becomes Active. R1 recovers. What happens without `preempt` configured?
- A) R1 immediately becomes Active again
- B) R2 remains Active; R1 becomes Standby
- C) Both routers become Active, causing a conflict
- D) HSRP resets and re-elects based on priority

**Answer: B** — HSRP is **non-preemptive by default**. R2 keeps the Active role until HSRP is reset or another failure occurs. Configure `standby 1 preempt` on R1 to automatically reclaim Active role.

---

**6.** A host is configured with the HSRP virtual IP as its default gateway. The Active HSRP router fails. What does the new Active router send to update the network?
- A) A standard ARP request
- B) A Gratuitous ARP (broadcast ARP reply, unrequested)
- C) An OSPF LSA update
- D) A DHCP offer with the new MAC address

**Answer: B** — The new Active router sends a **Gratuitous ARP** — a broadcast ARP reply sent without a prior request — to update switches' MAC address tables. Hosts don't need to update because they still use the same virtual IP and virtual MAC.

---

**7.** Which statement about TCP's 3-way handshake is correct?
- A) Client sends SYN; server sends SYN; client sends ACK
- B) Client sends SYN; server sends SYN-ACK; client sends ACK
- C) Client sends ACK; server sends SYN; client sends SYN-ACK
- D) Both sides send SYN simultaneously, then exchange ACKs

**Answer: B** — TCP 3-way handshake: **SYN → SYN-ACK → ACK**. The client initiates with SYN, the server responds with SYN-ACK (acknowledging the SYN and sending its own SYN), and the client completes with ACK.

---

**8.** A VoIP application needs to send real-time audio. Which transport protocol is most appropriate and why?
- A) TCP — because it provides error recovery to prevent audio degradation
- B) UDP — because low latency is more important than retransmission of lost packets
- C) TCP — because it supports larger packet sizes for audio data
- D) UDP — because it provides sequencing and flow control

**Answer: B** — VoIP uses **UDP** because real-time applications need low latency. A retransmitted audio packet arriving late is worse than a dropped packet (the audio just "glitches" briefly). TCP's retransmission would cause unacceptable delay. Note: UDP does NOT provide sequencing or flow control — those are TCP features.

---

**9.** Which OSPF LSA type is generated by the DR of a broadcast network segment?
- A) Type 1 (Router LSA)
- B) Type 2 (Network LSA)
- C) Type 3 (Summary LSA)
- D) Type 5 (AS External LSA)

**Answer: B** — **Type 2 (Network LSA)** is generated by the DR of each broadcast segment. It lists the routers attached to that multi-access network. Type 1 = every router's own LSA. Type 5 = external routes from ASBR.

---

**10.** A host uses DHCP to get an IP address. The DHCP Discover message is sent to which port on which transport protocol?
- A) TCP port 67
- B) UDP port 67
- C) UDP port 68
- D) TCP port 68

**Answer: B** — DHCP uses **UDP**. The client sends Discover to destination port **67** (DHCP server port). The server responds to the client on port **68** (DHCP client port). TCP is not used for DHCP.
