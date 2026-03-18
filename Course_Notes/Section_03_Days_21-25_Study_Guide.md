# CCNA 200-301 Exam Coach — Section 03 Study Guide
## Days 21–25 | Network Access (cont.) + IP Connectivity: STP Part 2, Rapid STP, EtherChannel, Dynamic Routing, RIP & EIGRP
### Transcripts 039–050 | Jeremy's IT Lab Complete Course

---

## SECTION 1: EXAM KNOWLEDGE MAP

| # | Video | Day | Topic | CCNA Domain | Exam Weight |
|---|-------|-----|-------|-------------|-------------|
| 039 | STP Part 2 | Day 21 | STP states/timers, BPDU, PortFast, BPDU Guard, STP config | Network Access | 20% |
| 040 | STP Part 2 Lab | Day 21 Lab | Configure root bridge, PortFast, BPDU Guard | Network Access | 20% |
| 041 | Rapid STP | Day 22 | RSTP port roles/states, link types, BPDU differences | Network Access | 20% |
| 042 | Rapid STP Lab | Day 22 Lab | Rapid PVST+ topology analysis, RSTP verification | Network Access | 20% |
| 043 | EtherChannel | Day 23 | PAgP, LACP, static EtherChannel, L2/L3, load balancing | Network Access | 20% |
| 044 | EtherChannel Lab | Day 23 Lab | Configure LACP/PAgP, verify etherchannel summary | Network Access | 20% |
| 045 | Dynamic Routing | Day 24 | IGP/EGP, Distance Vector vs Link State, metrics, AD | IP Connectivity | 25% |
| 046 | Dynamic Routing Lab | Day 24 Lab | Routing table analysis, AD comparison | IP Connectivity | 25% |
| 047 | RIP and EIGRP | Day 25 | RIPv1/v2 config, EIGRP config, EIGRP metric, unequal LB | IP Connectivity | 25% |
| 048 | RIP Lab | Day 25 Lab | RIPv2 configuration, passive-interface, default-information | IP Connectivity | 25% |
| 049 | EIGRP Lab | Day 25 Lab | EIGRP AS config, wildcard masks, variance | IP Connectivity | 25% |

**Exam Objectives Covered:**
- 2.5 Interpret basic operations of Rapid PVST+ Spanning Tree Protocol
- 2.6 Describe Cisco's EtherChannel technology
- 2.7 Describe the need for and basic operations of EtherChannel
- 3.1 Interpret the components of a routing table
- 3.2 Determine how a router makes a forwarding decision by default
- 3.3 Configure and verify IPv4 static routing (floating static routes)
- 3.4 Configure and verify single area OSPFv2 (foundation: dynamic routing concepts)

---

## SECTION 2: MUST-KNOW CONCEPTS

---

### Concept 1: STP States (Classic 802.1D)

**The 4 Port States:**

| State | Type | Sends/Receives Traffic | Learns MACs | Sends/Receives BPDUs |
|-------|------|----------------------|-------------|----------------------|
| Blocking | Stable | NO | NO | Receives only (does NOT forward) |
| Listening | Transitional | NO | NO | YES |
| Learning | Transitional | NO | YES | YES |
| Forwarding | Stable | YES | YES | YES |

**Key Rules:**
- Only **Root Ports** and **Designated Ports** enter Listening → Learning → Forwarding
- **Non-Designated Ports** go directly to Blocking and STAY there
- A Forwarding port can move directly to Blocking (no loop risk)
- A Blocking port CANNOT move directly to Forwarding — must go through Listening and Learning

**Common Exam Trap:** Non-Designated Ports do NOT send BPDUs — they only receive them. BPDUs are only forwarded out **Designated Ports**.

---

### Concept 2: STP Timers

| Timer | Default | Purpose |
|-------|---------|---------|
| Hello | 2 seconds | How often root bridge sends BPDUs |
| Forward Delay | 15 seconds | Duration of Listening state AND Learning state (15 sec each) |
| Max Age | 20 seconds | How long a switch waits before re-evaluating STP if no BPDU received |

**Convergence Time:** A blocking port transitioning to forwarding takes up to **50 seconds**:
- Max Age (20s) + Listening (15s) + Learning (15s) = **50 seconds**

**Critical Rule:** The STP timers on the **Root Bridge** determine ALL STP timers for the entire network.

---

### Concept 3: STP Optional Features (Toolkit)

**PortFast:**
- Allows a port to skip Listening/Learning and move immediately to Forwarding
- ONLY enable on ports connected to **end hosts** (never on trunk ports to other switches)
- Per-interface: `spanning-tree portfast`
- Globally on all access ports: `spanning-tree portfast default`

**BPDU Guard:**
- If a PortFast-enabled port receives a BPDU → port is **err-disabled** (shut down)
- Prevents loops if someone accidentally connects a switch to a PortFast port
- Per-interface: `spanning-tree bpduguard enable`
- Globally on all PortFast interfaces: `spanning-tree portfast bpduguard default`

**Exam Rule:** You MUST know PortFast and BPDU Guard for the CCNA. Root Guard and Loop Guard are NOT required knowledge.

---

### Concept 4: STP Configuration Commands

```
! Configure STP mode
SW(config)# spanning-tree mode {pvst | rapid-pvst | mst}

! Configure primary root bridge (sets priority to 24576, or 4096 less than current lowest)
SW(config)# spanning-tree vlan <vlan-id> root primary

! Configure secondary root bridge (sets priority to 28672)
SW(config)# spanning-tree vlan <vlan-id> root secondary

! Manually set priority (must be multiple of 4096)
SW(config)# spanning-tree vlan <vlan-id> priority <0-61440>

! Configure port cost (affects root port selection)
SW(config-if)# spanning-tree vlan <vlan-id> cost <value>

! Configure port priority (affects designated port selection)
SW(config-if)# spanning-tree vlan <vlan-id> port-priority <0-240>
```

**Key Fact:** Modern Cisco switches run **rapid-pvst** by default.
- Primary root priority = **24576**
- Secondary root priority = **28672** (exactly 4096 higher)

**PVST+ vs Regular STP:**
- PVST+ (Cisco) uses multicast MAC: `01:00:0c:cc:cc:cd`
- Regular STP (IEEE) uses multicast MAC: `01:80:c2:00:00:00`
- PVST+ supports 802.1Q; PVST (original) only supported ISL

---

### Concept 5: Rapid Spanning Tree Protocol (RSTP / 802.1w)

**Why RSTP?** Classic STP can take 30–50 seconds to converge. RSTP uses handshake mechanisms to converge in seconds.

**STP Version Comparison:**

| Standard | Name | Cisco Version |
|----------|------|--------------|
| 802.1D | Classic STP | PVST+ |
| 802.1w | Rapid STP | Rapid PVST+ |
| 802.1s | Multiple STP | MSTP |

**RSTP Port States (3, not 4):**

| RSTP State | Equivalent Classic STP States |
|------------|-------------------------------|
| Discarding | Blocking + Listening + Disabled |
| Learning | Learning |
| Forwarding | Forwarding |

**RSTP Port Roles:**
- **Root Port** — same as classic STP (closest to root bridge)
- **Designated Port** — same as classic STP (best BPDU on segment)
- **Alternate Port** — discarding port receiving superior BPDU from another switch (backup to root port — replaces UplinkFast)
- **Backup Port** — discarding port receiving superior BPDU from same switch (only exists with hubs, rare in modern networks)

**RSTP vs Classic STP Key Differences:**

| Feature | Classic STP | RSTP |
|---------|-------------|------|
| BPDU origin | Only root bridge sends; others forward | ALL switches send their own BPDUs |
| BPDU interval | 2 sec (hello); 20 sec max age | Every 2 sec; missed 3 BPDUs (6 sec) = neighbor lost |
| Convergence | Up to 50 seconds | Near-instant (seconds) |
| UplinkFast | Optional feature, must configure | Built-in (Alternate Port) |
| BackboneFast | Optional feature, must configure | Built-in |
| Port states | 4 (Blocking/Listening/Learning/Forwarding) | 3 (Discarding/Learning/Forwarding) |

**RSTP Link Types:**

| Type | Description | Duplex | Configured by |
|------|-------------|--------|---------------|
| Edge | Connected to end host; moves straight to Forwarding | N/A | `spanning-tree portfast` |
| Point-to-Point | Switch-to-switch; full-duplex | Full | Auto-detected (or `spanning-tree link-type point-to-point`) |
| Shared | Switch connected via hub; half-duplex | Half | Auto-detected (or `spanning-tree link-type shared`) |

**RSTP Port Costs (different from classic STP):**

| Speed | Classic STP Cost | RSTP Cost |
|-------|------------------|-----------|
| 10 Mbps | 100 | 2,000,000 |
| 100 Mbps | 19 | 200,000 |
| 1 Gbps | 4 | 20,000 |
| 10 Gbps | 2 | 2,000 |

**Compatibility:** RSTP is backward-compatible with classic STP. An RSTP switch connected to a classic STP switch will operate in classic STP mode on that interface.

---

### Concept 6: EtherChannel

**What It Is:** Groups multiple physical interfaces into a single logical interface. STP sees the group as ONE interface, preventing ports from being blocked.

**Why Use It:**
- Without EtherChannel: STP blocks all but one link between two switches (prevents loops)
- With EtherChannel: All physical links are active, STP sees one logical link

**Other Names:** Port Channel, LAG (Link Aggregation Group)

**EtherChannel Protocols:**

| Protocol | Standard | Modes | Notes |
|----------|----------|-------|-------|
| PAgP | Cisco proprietary | `desirable` (active) / `auto` (passive) | Two "auto" = NO channel |
| LACP | IEEE 802.3ad (industry standard) | `active` (active) / `passive` (passive) | Two "passive" = NO channel |
| Static | None | `on` | Both sides must be `on`; does not negotiate |

**Mode Compatibility:**

| Side A | Side B | Result |
|--------|--------|--------|
| desirable | desirable | EtherChannel forms (PAgP) |
| desirable | auto | EtherChannel forms (PAgP) |
| auto | auto | NO EtherChannel |
| active | active | EtherChannel forms (LACP) |
| active | passive | EtherChannel forms (LACP) |
| passive | passive | NO EtherChannel |
| on | on | EtherChannel forms (Static) |
| on | desirable/active | NO EtherChannel |

**Load Balancing:**
- EtherChannel load balances based on **flows** (communication between two nodes)
- All frames in the same flow use the SAME physical interface (prevents out-of-order delivery)
- Load-balance inputs: src-mac, dst-mac, src-dst-mac, src-ip, dst-ip, src-dst-ip

**Important Config Rule:** All member interfaces must have MATCHING configuration:
- Same duplex, same speed
- Same switchport mode (access or trunk)
- Same allowed VLANs / native VLAN (for trunks)
- Mismatched interface → excluded from EtherChannel (shows as "suspended")

**Channel Group Number:**
- Must match on all member interfaces of the **same switch**
- Does NOT need to match on the other switch (`channel-group 1` on SW1 can connect to `channel-group 2` on SW2)

**Layer 2 vs Layer 3 EtherChannel:**
- L2: `switchport` interfaces; acts as a trunk or access port
- L3: `no switchport` interfaces; assign IP address directly to port-channel interface (show as "RU" in summary: R=Layer3, U=in use)

---

### Concept 7: Dynamic Routing Overview

**Static vs Dynamic Routing:**

| Feature | Static Routing | Dynamic Routing |
|---------|----------------|-----------------|
| Configuration | Manual by admin | Automatic via protocol |
| Adaptability | Fixed; won't react to failures | Automatically reroutes |
| Resource use | Low (no protocol overhead) | Higher (CPU/memory/bandwidth) |
| Use case | Small networks, stub routes | Medium-large networks |

**Routing Protocol Categories:**

```
Routing Protocols
├── IGP (Interior Gateway Protocol) — within one AS (company)
│   ├── Distance Vector: RIP, EIGRP
│   └── Link State: OSPF, IS-IS
└── EGP (Exterior Gateway Protocol) — between AS (internet)
    └── Path Vector: BGP
```

**Distance Vector ("Routing by Rumor"):**
- Routers share their routing table with directly connected neighbors
- Each router only knows what neighbors tell it (doesn't see full network map)
- Slower to react to topology changes

**Link State:**
- Each router advertises its connected interfaces to ALL routers in the network
- All routers build an identical map of the network
- Each router independently calculates best path (Dijkstra's algorithm)
- Uses more CPU but reacts faster to changes

---

### Concept 8: Metrics and Administrative Distance

**Metric** = used to compare routes learned by the **same** routing protocol (lower = better)

| Protocol | Metric Used | Notes |
|----------|-------------|-------|
| RIP | Hop count | Max 15 hops; bandwidth irrelevant |
| OSPF | Cost (based on bandwidth) | Cost = 100 Mbps / interface bandwidth |
| EIGRP | Bandwidth + Delay | Complex formula; very large numbers |
| IS-IS | Cost | Similar to OSPF |

**ECMP (Equal-Cost Multi-Path):** When two routes have the same metric via the same protocol, both are installed and traffic is load-balanced.

**Administrative Distance (AD)** = used to compare routes learned by **different** routing protocols (lower = more trusted/preferred)

| Route Source | AD Value |
|-------------|----------|
| Connected interface | 0 |
| Static route | 1 |
| EIGRP (internal) | 90 |
| OSPF | 110 |
| RIP | 120 |
| EIGRP (external) | 170 |
| Unknown / untrusted | 255 (not installed) |

**Selection Order:** First compare AD (prefer lower AD) → then compare Metric (prefer lower metric)

**Floating Static Route:**
- A static route with a manually increased AD (higher than the dynamic protocol's AD)
- Stays inactive while the dynamic route exists; activates only if the dynamic route is lost
- Example: `ip route 0.0.0.0 0.0.0.0 10.0.0.1 5` (AD 5 — still beats OSPF/RIP)
- To make it a backup to OSPF: `ip route 192.168.1.0 255.255.255.0 10.0.0.1 111` (AD 111 > OSPF 110)

---

### Concept 9: RIP (Routing Information Protocol)

**RIP Versions:**

| Feature | RIPv1 | RIPv2 |
|---------|-------|-------|
| Address support | Classful only | VLSM/CIDR support |
| Subnet mask in updates | NO | YES |
| Update destination | Broadcast 255.255.255.255 | Multicast **224.0.0.9** |
| Authentication | NO | YES (MD5) |

**Key RIP Facts:**
- Distance Vector IGP
- Metric = **hop count** (bandwidth is irrelevant)
- Maximum hop count = **15** (16 = unreachable)
- AD = **120**
- Sends full routing table updates every **30 seconds**
- Three versions: RIPv1, RIPv2 (IPv4), RIPng (IPv6)

**RIP Configuration:**
```
R1(config)# router rip
R1(config-router)# version 2
R1(config-router)# no auto-summary           ! Disable classful auto-summarization
R1(config-router)# network 10.0.0.0          ! Classful — activates RIP on matching interfaces
R1(config-router)# network 172.16.0.0
R1(config-router)# passive-interface g2/0    ! Stop sending RIP updates out this interface
R1(config-router)# default-information originate  ! Advertise default route to RIP neighbors

! Change max paths (ECMP)
R1(config-router)# maximum-paths <1-16>

! Change AD
R1(config-router)# distance <1-255>
```

**`network` command behavior:**
- The `network` command is **classful** — `network 10.0.0.1` becomes `network 10.0.0.0/8`
- Activates RIP on all interfaces whose IP falls in that classful range
- Advertises the actual network prefix of the interface (not the classful summary)

**`passive-interface` command:**
- Stops sending RIP advertisements out the specified interface
- Still advertises that interface's network prefix to other RIP neighbors
- Use on interfaces with no RIP neighbors (LAN-facing interfaces)

---

### Concept 10: EIGRP (Enhanced Interior Gateway Routing Protocol)

**Key EIGRP Facts:**
- Distance Vector (advanced/hybrid) IGP
- Originally Cisco proprietary; now open standard
- No 15-hop limit
- Multicast address: **224.0.0.10** (memorize!)
- AD: **90** (internal), **170** (external)
- Only IGP supporting **unequal-cost load balancing**
- Metric = **Bandwidth (slowest link) + Delay (all links)**

**EIGRP Configuration:**
```
R1(config)# router eigrp 100                 ! AS number MUST match on all routers
R1(config-router)# no auto-summary
R1(config-router)# network 10.0.0.0 0.0.255.255  ! Wildcard mask (inverted subnet mask)
R1(config-router)# network 172.16.1.0 0.0.0.15
R1(config-router)# passive-interface g2/0

! Configure variance for unequal-cost LB
R1(config-router)# variance 2               ! Allow routes up to 2x successor FD
```

**Wildcard Mask:**
- Inverted subnet mask: 1s and 0s are flipped
- `255.255.255.0` → wildcard = `0.0.0.255`
- `255.255.255.240` → wildcard = `0.0.0.15`
- `0` in wildcard = bits MUST match; `1` = don't care

**Router ID (same priority order for EIGRP and OSPF):**
1. Manually configured router-id
2. Highest IP on a loopback interface
3. Highest IP on a physical interface

**EIGRP Terminology:**

| Term | Definition |
|------|-----------|
| Feasible Distance (FD) | This router's metric to the destination |
| Reported/Advertised Distance (RD/AD) | Neighbor's metric to the destination |
| Successor | Best route to destination (lowest FD) — installed in routing table |
| Feasible Successor | Backup route meeting feasibility condition |
| Feasibility Condition | RD of backup route < FD of successor route |

**Unequal-Cost Load Balancing (EIGRP only):**
- `variance 1` (default) = ECMP only
- `variance 2` = routes with FD ≤ 2× successor's FD can be used
- Only Feasible Successors qualify for unequal load balancing (NOT just any backup route)

---

## SECTION 3: COMMON EXAM TRAPS

| Trap | Correct Answer |
|------|---------------|
| "Which ports send BPDUs in classic STP?" | Only Designated Ports forward BPDUs (root and non-designated do NOT forward) |
| "What is the total STP convergence time from blocking?" | 50 seconds (20 Max Age + 15 Listening + 15 Learning) |
| "What does PortFast do?" | Skips Listening/Learning; goes directly to Forwarding — end hosts ONLY |
| "What happens if a PortFast port receives a BPDU?" | BPDU Guard err-disables the port (if enabled) |
| "What's the default STP mode on modern Cisco switches?" | rapid-pvst (Rapid PVST+) |
| "Two LACP passive interfaces — do they form EtherChannel?" | NO — at least one side must be active |
| "Two PAgP auto interfaces — do they form EtherChannel?" | NO — at least one side must be desirable |
| "Static EtherChannel (`on`) with LACP `active`?" | NO — `on` only works with `on` |
| "Does channel-group number need to match on both switches?" | NO — only needs to match on interfaces of the same switch |
| "What metric does RIP use?" | Hop count (bandwidth is irrelevant) |
| "Max RIP hop count?" | 15 (16 = unreachable) |
| "RIPv1 vs RIPv2 — multicast?" | RIPv1 uses broadcast; RIPv2 uses multicast 224.0.0.9 |
| "EIGRP multicast address?" | 224.0.0.10 |
| "OSPF AD vs EIGRP AD?" | EIGRP internal = 90, OSPF = 110; EIGRP preferred |
| "Floating static route — what makes it float?" | Its AD is set higher than the dynamic protocol's AD |
| "RSTP equivalent of classic STP Blocking + Listening + Disabled?" | All three map to RSTP Discarding state |
| "RSTP Alternate Port function?" | Backup to root port; immediately takes over if root port fails (UplinkFast equivalent) |

---

## SECTION 4: COMPLETE COMMAND REFERENCE

### STP Commands
```
SW# show spanning-tree [vlan <id>]          ! View STP topology
SW# show spanning-tree detail               ! Detailed STP info including timers
SW(config)# spanning-tree mode rapid-pvst  ! Set STP mode
SW(config)# spanning-tree vlan 1 root primary    ! Become primary root (priority 24576)
SW(config)# spanning-tree vlan 1 root secondary  ! Become secondary root (priority 28672)
SW(config)# spanning-tree vlan 1 priority 4096   ! Manual priority (multiple of 4096)
SW(config-if)# spanning-tree portfast             ! Enable PortFast on interface
SW(config)# spanning-tree portfast default        ! Enable PortFast on all access ports
SW(config-if)# spanning-tree bpduguard enable     ! Enable BPDU Guard on interface
SW(config)# spanning-tree portfast bpduguard default  ! BPDU Guard on all PortFast ports
SW(config-if)# spanning-tree vlan 1 cost <value>       ! Set port cost
SW(config-if)# spanning-tree vlan 1 port-priority <0-240>  ! Set port priority
SW(config-if)# spanning-tree link-type point-to-point  ! RSTP link type
SW(config-if)# spanning-tree link-type shared          ! RSTP link type
```

### EtherChannel Commands
```
SW(config)# port-channel load-balance {src-mac | dst-mac | src-dst-mac | src-ip | dst-ip | src-dst-ip}
SW# show etherchannel load-balance
SW(config-if-range)# channel-group <1-48> mode {desirable | auto | active | passive | on}
SW(config-if-range)# channel-protocol {lacp | pagp}   ! Force a specific protocol
SW# show etherchannel summary               ! Flags: S=L2, R=L3, U=in-use, P=bundled, s=suspended, D=down
SW# show etherchannel port-channel          ! Detailed port-channel info
SW# show interfaces port-channel <id>       ! Interface status
SW# show spanning-tree                      ! Confirms EtherChannel appears as single interface
```

### RIP Commands
```
R(config)# router rip
R(config-router)# version 2
R(config-router)# no auto-summary
R(config-router)# network <classful-network>
R(config-router)# passive-interface <interface>
R(config-router)# passive-interface default      ! All interfaces passive (then enable specific ones)
R(config-router)# no passive-interface <int>     ! Un-passive a specific interface
R(config-router)# default-information originate  ! Advertise default route
R(config-router)# maximum-paths <1-16>           ! Default: 4
R(config-router)# distance <1-255>               ! Change AD (default 120)
R# show ip protocols                             ! View RIP config, neighbors, networks
R# show ip route rip                             ! Show only RIP routes (marked R)
```

### EIGRP Commands
```
R(config)# router eigrp <AS-number>
R(config-router)# no auto-summary
R(config-router)# network <network> <wildcard-mask>
R(config-router)# passive-interface <interface>
R(config-router)# variance <1-128>              ! Unequal-cost LB (default: 1 = ECMP only)
R(config-router)# maximum-paths <1-32>          ! Default: 4
R(config-router)# eigrp router-id <A.B.C.D>    ! Manual router-id
R# show ip protocols                            ! View EIGRP config
R# show ip route eigrp                         ! Show only EIGRP routes (marked D)
R# show ip eigrp neighbors                     ! View EIGRP neighbor table
R# show ip eigrp topology                      ! View EIGRP topology table (successors, feasible successors)
```

### General Routing Commands
```
R# show ip route                    ! Full routing table
R# show ip route <network>          ! Route for specific destination
R(config)# ip route <net> <mask> <next-hop> <AD>  ! Static route with custom AD (floating)
```

---

## SECTION 5: EXAM QUICK-REFERENCE TABLES

### STP Port States Comparison

| Classic STP | RSTP Equivalent | Sends Traffic | Learns MACs |
|-------------|-----------------|---------------|-------------|
| Disabled | Discarding | NO | NO |
| Blocking | Discarding | NO | NO |
| Listening | Discarding | NO | NO |
| Learning | Learning | NO | YES |
| Forwarding | Forwarding | YES | YES |

### EtherChannel Protocol Mode Combinations

| Protocol | Mode A | Mode B | Forms Channel? |
|----------|--------|--------|----------------|
| PAgP | desirable | desirable | YES |
| PAgP | desirable | auto | YES |
| PAgP | auto | auto | NO |
| LACP | active | active | YES |
| LACP | active | passive | YES |
| LACP | passive | passive | NO |
| Static | on | on | YES |
| Mixed | on | active/desirable | NO |

### Administrative Distance Quick Reference

| Source | AD | Memory Aid |
|--------|----|-----------|
| Connected | 0 | "I'm directly connected — trust me completely" |
| Static | 1 | "Admin configured it — almost as good" |
| EIGRP internal | 90 | "90 = E for EIGRP" |
| OSPF | 110 | "110 = O for OSPF" |
| RIP | 120 | "120 = R for RIP (worst IGP)" |
| EIGRP external | 170 | "redistributed = less trusted" |
| Unknown | 255 | "255 = rejected" |

### Dynamic Routing Protocol Summary

| Protocol | Type | Algorithm | Metric | AD | Multicast | Standard |
|----------|------|-----------|--------|----|-----------|---------|
| RIPv2 | Distance Vector IGP | Bellman-Ford | Hop count (max 15) | 120 | 224.0.0.9 | Industry |
| EIGRP | Distance Vector IGP | DUAL | BW + Delay | 90/170 | 224.0.0.10 | Cisco (now open) |
| OSPF | Link State IGP | Dijkstra (SPF) | Cost (BW-based) | 110 | 224.0.0.5/6 | Industry |
| IS-IS | Link State IGP | Dijkstra (SPF) | Cost | 115 | N/A | Industry |
| BGP | Path Vector EGP | Best Path | AS-PATH | 20/200 | N/A | Industry |

---

## SECTION 6: PRACTICE QUIZ

**1.** A switch port is in the STP Listening state. Which of the following is TRUE?
- A) It forwards regular network traffic
- B) It learns MAC addresses from arriving frames
- C) It sends and receives BPDUs only
- D) It is in a stable state

**Answer: C** — Listening state only processes BPDUs. No traffic forwarding, no MAC learning. It is a **transitional** state (not stable).

---

**2.** How long does it take for a blocking port to transition to forwarding in classic STP (worst case)?
- A) 15 seconds
- B) 30 seconds
- C) 50 seconds
- D) 20 seconds

**Answer: C** — Max Age (20s) + Listening (15s) + Learning (15s) = **50 seconds**.

---

**3.** Which STP feature, when enabled globally, allows ALL access ports to skip the Listening and Learning states?
- A) BPDU Guard
- B) Root Guard
- C) `spanning-tree portfast default`
- D) `spanning-tree mode rapid-pvst`

**Answer: C** — `spanning-tree portfast default` enables PortFast on all access ports globally. BPDU Guard protects against rogue switches. Root Guard prevents unauthorized root bridges.

---

**4.** In RSTP, what is the function of the Alternate Port?
- A) It connects to end hosts and skips the learning state
- B) It acts as a backup Designated Port on a shared segment
- C) It is a backup Root Port that can immediately transition to Forwarding if the Root Port fails
- D) It connects to a hub in half-duplex mode

**Answer: C** — The Alternate Port is a discarding port that receives a superior BPDU from another switch. If the Root Port fails, the Alternate Port immediately becomes the Root Port (no delay). This is equivalent to the classic STP optional feature UplinkFast.

---

**5.** SW1 and SW2 are connected by four links. SW1 interfaces are configured `channel-group 1 mode passive` and SW2 interfaces are configured `channel-group 1 mode passive`. What happens?
- A) A LACP EtherChannel forms between the switches
- B) STP blocks three of the four links
- C) No EtherChannel forms; at least one side must be `active`
- D) A PAgP EtherChannel forms

**Answer: C** — Two LACP `passive` interfaces will NOT negotiate an EtherChannel. At least one side must be `active`. STP would then block 3 of the 4 redundant links.

---

**6.** A router has two routes to 10.1.1.0/24: one via OSPF (metric 20) and one via EIGRP internal (metric 5000). Which route is installed in the routing table?
- A) OSPF route, because it has a lower metric
- B) EIGRP route, because it has a lower metric
- C) EIGRP route, because it has a lower Administrative Distance (90 vs 110)
- D) Both routes are installed via ECMP

**Answer: C** — AD is compared FIRST, before metric. EIGRP internal AD = 90, OSPF AD = 110. The EIGRP route wins regardless of metric values.

---

**7.** Which of the following is TRUE about RIPv2 versus RIPv1? (Choose TWO)
- A) RIPv2 supports VLSM; RIPv1 does not
- B) RIPv1 uses multicast 224.0.0.9; RIPv2 uses broadcast
- C) Both RIPv1 and RIPv2 have a maximum hop count of 15
- D) RIPv2 includes subnet mask information in updates; RIPv1 does not
- E) RIPv2 uses hop count as metric; RIPv1 uses bandwidth

**Answer: A and D** — RIPv2 supports VLSM and includes subnet masks in updates. Both versions use hop count (max 15). RIPv2 uses multicast 224.0.0.9 (not RIPv1 which uses broadcast). Both use hop count.

---

**8.** An EIGRP router has a Feasible Successor route. The Successor route's Feasible Distance is 100. Which Reported Distance for the Feasible Successor satisfies the Feasibility Condition?
- A) 110
- B) 100
- C) 95
- D) 105

**Answer: C** — Feasibility Condition: the Feasible Successor's Reported Distance must be LESS THAN the Successor's Feasible Distance (100). Only 95 qualifies.

---

**9.** A network admin configures: `ip route 0.0.0.0 0.0.0.0 203.0.113.1 121`. The router also learns a default route via OSPF. Which route is used?
- A) The static route, because static routes always win
- B) The OSPF route, because it has a lower AD (110 < 121)
- C) Both routes are used via ECMP
- D) The static route because it was configured first

**Answer: B** — The static route has been configured with AD 121 (a floating static route). OSPF AD = 110, which is lower. The OSPF route is preferred. The static only activates if the OSPF route is lost.

---

**10.** What is the EIGRP multicast address, and what is EIGRP's Administrative Distance for internal routes?
- A) 224.0.0.5, AD 90
- B) 224.0.0.9, AD 120
- C) 224.0.0.10, AD 90
- D) 224.0.0.10, AD 110

**Answer: C** — EIGRP uses multicast **224.0.0.10** and has an internal AD of **90**. (224.0.0.5/6 = OSPF; 224.0.0.9 = RIPv2; AD 120 = RIP; AD 110 = OSPF.)
