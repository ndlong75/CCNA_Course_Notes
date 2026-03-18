# CCNA 200-301 Exam Coach — Section 02 Study Guide
## Days 16–20 | Network Access: VLANs, DTP/VTP, Spanning Tree Protocol (Part 1)
### Transcripts 028–038 | Jeremy's IT Lab Complete Course

---

## SECTION 1: EXAM KNOWLEDGE MAP

| # | Video | Day | Topic | CCNA Domain | Exam Weight |
|---|-------|-----|-------|-------------|-------------|
| 028 | Subnetting VLSM Lab | Day 15 Lab | VLSM practice: 5 subnets, static routes | Network Fundamentals | 20% |
| 029 | VLANs Part 1 | Day 16 | Broadcast domains, VLAN concept, access ports | Network Access | 20% |
| 030 | VLANs Part 1 Lab | Day 16 Lab | Access port config, VLAN naming | Network Access | 20% |
| 031 | VLANs Part 2 | Day 17 | Trunk ports, 802.1Q, native VLAN, ROAS | Network Access | 20% |
| 032 | VLANs Part 2 Lab | Day 17 Lab | Trunk + ROAS configuration | Network Access | 20% |
| 033 | VLANs Part 3 | Day 18 | Native VLAN on router, L3 switching, SVIs | Network Access | 20% |
| 034 | VLANs Part 3 Lab | Day 18 Lab | Multi-layer switch, SVI, routed ports | Network Access | 20% |
| 035 | DTP/VTP | Day 19 | Dynamic Trunking Protocol, VLAN Trunking Protocol | Network Access | 20% |
| 036 | DTP/VTP Lab | Day 19 Lab | DTP modes, VTP configuration | Network Access | 20% |
| 037 | STP Part 1 | Day 20 | Broadcast storms, STP process, port roles | Network Access | 20% |
| 038 | STP Lab | Day 20 Lab | STP topology analysis, show spanning-tree | Network Access | 20% |

**Exam Objectives Covered:**
- 2.1 Configure and verify VLANs (normal range) spanning multiple switches
- 2.2 Configure and verify interswitch connectivity (trunk ports, native VLAN)
- 2.3 Configure and verify Layer 2 discovery protocols (DTP, VTP context)
- 2.4 Configure and verify EtherChannel (upcoming — foundation built here)
- 2.5 Interpret basic operations of Rapid PVST+ (foundation: classic STP)

---

## SECTION 2: MUST-KNOW CONCEPTS

### Concept 1: Broadcast Domain vs LAN

**Definition:** A broadcast domain is the group of devices that will receive a broadcast frame (destination MAC = FF:FF:FF:FF:FF:FF) sent by any one member. A LAN = a single broadcast domain.

**How It Works:**
- Switches FLOOD broadcast frames out all interfaces except the receiving one
- Routers DO NOT forward broadcast frames — they stop at the router
- Each router interface creates a boundary between broadcast domains

**Key Facts:**
- A network with 3 router interfaces = at least 3 broadcast domains (plus point-to-point links)
- Without VLANs, all hosts on the same switch are in the same broadcast domain regardless of subnets

**Common Exam Trap:** Subnetting creates separate Layer 3 networks but does NOT create separate Layer 2 broadcast domains without VLANs. The switch only sees MAC addresses, not IP addresses.

**Why VLANs Exist:**
1. **Performance**: Excessive broadcasts from a large flat L2 network slow the network
2. **Security**: Without VLANs, hosts communicate directly at L2 — router security policies are bypassed for same-subnet traffic

---

### Concept 2: VLANs — Virtual Local Area Networks

**Definition:** A VLAN logically divides a single physical switch into multiple separate Layer 2 broadcast domains.

**How It Works:**
- Configured on a per-interface basis on the switch
- The switch treats each VLAN as a completely separate LAN
- Broadcasts in VLAN 10 NEVER reach VLAN 20, even on the same switch
- Traffic between VLANs MUST pass through a router (or Layer 3 switch)

**Key Facts:**
- Default VLAN is VLAN 1 — all interfaces belong to VLAN 1 until configured otherwise
- VLANs 1 and 1002–1005 exist by default and CANNOT be deleted
- Normal VLAN range: 1–1005 | Extended VLAN range: 1006–4094
- Assigning an interface to a non-existent VLAN AUTOMATICALLY creates that VLAN

**Access Port:**
- Belongs to exactly ONE VLAN
- Typically connects to end hosts (PCs, servers, printers)
- Frames sent/received without VLAN tags (untagged)
- Also called: "untagged port"

**Trunk Port:**
- Carries traffic from MULTIPLE VLANs over a single physical link
- Typically connects switch-to-switch or switch-to-router
- Frames are tagged with 802.1Q to identify which VLAN they belong to
- Also called: "tagged port"

**Common Exam Trap:** `show vlan brief` shows ACCESS port assignments — it does NOT show trunk ports. Use `show interfaces trunk` for trunk port information.

---

### Concept 3: 802.1Q (dot1Q) Encapsulation

**Definition:** IEEE standard for VLAN tagging on trunk links. A 4-byte tag inserted into the Ethernet frame to identify the VLAN.

**Tag Location:** Inserted between Source MAC address and the Type/Length field of the Ethernet header.

**802.1Q Tag Structure (4 bytes = 32 bits):**

| Field | Bits | Value/Purpose |
|-------|------|---------------|
| TPID (Tag Protocol ID) | 16 | Always 0x8100 — identifies frame as 802.1Q tagged |
| PCP (Priority Code Point) | 3 | Class of Service (CoS) — traffic priority |
| DEI (Drop Eligible Indicator) | 1 | Frame can be dropped during congestion |
| VID (VLAN ID) | 12 | Identifies the VLAN (0–4095; usable 1–4094) |

**Why 12-bit VID:** 2^12 = 4096 total values; 0 and 4095 reserved → 1–4094 usable

**ISL vs 802.1Q:**

| Feature | ISL | 802.1Q |
|---------|-----|--------|
| Origin | Cisco proprietary | IEEE standard |
| Status | Obsolete | Current standard |
| Modern support | Rarely (old Cisco only) | Universal |
| Native VLAN | No | Yes |

**Native VLAN:**
- Frames in the native VLAN are sent UNTAGGED over a trunk
- Receiving switch assumes untagged frames belong to the native VLAN
- Default native VLAN = VLAN 1
- **MUST match on both ends** of a trunk link — mismatch causes frame misclassification
- Best practice: change native VLAN to an unused VLAN for security

---

### Concept 4: Inter-VLAN Routing Methods

**Method 1 — Separate Router Interfaces (Day 16):**
- One physical router interface per VLAN
- Simple but wastes router interfaces
- Not scalable with many VLANs

**Method 2 — Router on a Stick (ROAS) (Day 17):**
- Single trunk link between switch and router
- Router uses sub-interfaces (G0/0.10, G0/0.20, G0/0.30)
- Each sub-interface configured with: `encapsulation dot1q <vlan-id>` and an IP address
- Sub-interface number does NOT have to match VLAN ID, but it's best practice to match
- Problem: all inter-VLAN traffic goes through single physical link — potential bottleneck

**Method 3 — Layer 3 Switch with SVIs (Day 18):**
- Most efficient method for large networks
- SVI = Switch Virtual Interface — virtual L3 interface per VLAN on a multi-layer switch
- Switch routes inter-VLAN traffic internally — no need to send to external router
- Requires: `ip routing` global command to enable routing
- A routed port (`no switchport`) connects the switch to an external router for outside traffic

**SVI Requirements for Up/Up state:**
1. VLAN must exist on the switch
2. At least one access port in VLAN is up/up OR one trunk port allowing the VLAN is up/up
3. The VLAN itself must not be shutdown
4. The SVI must not be shutdown (`no shutdown` required — SVIs are shutdown by default)

---

### Concept 5: DTP — Dynamic Trunking Protocol

**Definition:** Cisco proprietary protocol that allows switches to automatically negotiate trunk/access port status without manual configuration.

**DTP Modes:**

| Mode | Behavior |
|------|----------|
| `switchport mode access` | Always access port; DTP disabled |
| `switchport mode trunk` | Always trunk; still sends DTP frames |
| `switchport mode dynamic desirable` | Actively tries to form a trunk |
| `switchport mode dynamic auto` | Passive; forms trunk only if other end initiates |

**DTP Negotiation Results Table:**

| SW1 Mode | SW2 Mode | Result |
|----------|----------|--------|
| access | access | access |
| access | dynamic auto | access |
| access | dynamic desirable | access |
| access | trunk | **MISCONFIG** (do not do this) |
| dynamic auto | dynamic auto | access |
| dynamic auto | dynamic desirable | **trunk** |
| dynamic auto | trunk | **trunk** |
| dynamic desirable | dynamic desirable | **trunk** |
| dynamic desirable | trunk | **trunk** |
| trunk | trunk | **trunk** |

**Key Facts:**
- Older switches default to `dynamic desirable` | Newer switches default to `dynamic auto`
- DTP will NOT form a trunk with a router, PC, or non-Cisco device
- Disable DTP for security: `switchport nonegotiate` (also: `switchport mode access` disables DTP)
- Trunk encapsulation negotiation: ISL favored over dot1Q if both supported; disable negotiate with `switchport trunk encapsulation dot1q`
- Best practice: always manually configure ports, disable DTP

---

### Concept 6: VTP — VLAN Trunking Protocol

**Definition:** Cisco proprietary protocol allowing a central switch (server) to advertise VLAN configuration to other switches (clients) so VLANs don't need to be manually configured on every switch.

**VTP Modes:**

| Mode | Add/Modify/Delete VLANs | Stores in NVRAM | Syncs to Server | Forwards Advertisements |
|------|------------------------|------------------|-----------------|------------------------|
| Server (default) | YES | YES | YES (also a client) | YES |
| Client | NO | NO (v1/v2), YES (v3) | YES | YES |
| Transparent | YES (locally only) | YES | NO | YES (if same domain) |

**Revision Number:**
- Incremented every time a VLAN is added, modified, or deleted on a server
- Switches sync to the device with the HIGHEST revision number
- **DANGER:** Connecting an old switch with a high revision number overwrites the entire VLAN database → all hosts lose connectivity

**Resetting Revision Number to 0:**
1. Change VTP domain to an unused name
2. Change switch to transparent mode

**VTP Versions:**
- v1 (default): Normal VLANs only (1–1005)
- v2: Adds Token Ring VLAN support (no practical difference)
- v3: Supports extended VLANs (1–4094), clients store NVRAM

**Key Facts:**
- VTP domain null → switch automatically joins first domain it hears
- VTP only syncs the VLAN database — it does NOT configure interface assignments
- VTP advertisements sent only on trunk ports, not access ports
- Best practice: Do NOT use VTP in modern networks — too risky

---

### Concept 7: STP — Spanning Tree Protocol

**Definition:** IEEE 802.1D protocol that prevents Layer 2 loops in redundant networks by selectively blocking ports.

**The Problem Without STP:**
1. **Broadcast Storm**: Broadcast frames loop indefinitely (no TTL in Ethernet frames). Network becomes unusable.
2. **MAC Address Flapping**: Same MAC appears on different interfaces; MAC table constantly updates.

**STP Port States:**

| State | Sends/Receives Regular Traffic | Sends/Receives BPDUs |
|-------|-------------------------------|----------------------|
| Forwarding | YES | YES |
| Blocking | NO | YES |

**BPDU (Bridge Protocol Data Unit):**
- Hello BPDUs sent every 2 seconds by default
- Used to elect root bridge and detect topology
- Only the root bridge generates original BPDUs; other switches forward them

**PVST (Per-VLAN Spanning Tree):** Cisco runs a separate STP instance per VLAN. Different ports can be forwarding/blocking in different VLANs.

---

### Concept 8: STP Bridge ID and Root Bridge Election

**Bridge ID Structure:**
```
[Bridge Priority (4 bits)] + [Extended System ID/VLAN ID (12 bits)] + [MAC Address (48 bits)]
```

**Bridge Priority:**
- Default = 32768 (bit 15 set to 1)
- With VLAN 1: total priority = 32768 + 1 = **32769**
- Can only be changed in multiples of **4096**
- Valid values: 0, 4096, 8192, 12288, 16384, 20480, 24576, 28672, 32768, 36864, 40960, 45056, 49152, 53248, 57344, 61440

**Root Bridge Election:**
- Switch with LOWEST bridge ID wins
- Tiebreaker: lowest priority → lowest MAC address
- All ports on root bridge = **Designated Ports (Forwarding)**
- When powered on, each switch thinks it IS the root bridge until it receives a superior BPDU

---

### Concept 9: STP Port Role Selection Process

**Step 1 — Elect Root Bridge:**
- Lowest bridge ID becomes root bridge
- All root bridge ports → Designated (Forwarding)

**Step 2 — Select Root Port on each non-root switch:**
- One root port per non-root switch
- Root port = best path to root bridge
- Selection criteria (in order):
  1. Lowest **root cost** (cumulative cost of outgoing interfaces to root)
  2. Lowest neighbor **bridge ID**
  3. Lowest neighbor **port ID**
- Root ports → Forwarding state

**STP Interface Cost Values (Classic 802.1D):**

| Speed | STP Cost |
|-------|----------|
| 10 Mbps | 100 |
| 100 Mbps (FastEthernet) | 19 |
| 1 Gbps (GigabitEthernet) | 4 |
| 10 Gbps | 2 |

**Step 3 — Select Designated/Non-Designated per collision domain:**
- Each link has exactly ONE designated port
- Designated port = on the switch with the LOWEST root cost
- Tiebreaker: lowest bridge ID
- The OTHER port becomes **Non-Designated (Blocking)**

**Port Roles Summary:**

| Role | State | Location |
|------|-------|----------|
| Root Port (RP) | Forwarding | Non-root switch — best path to root |
| Designated Port (DP) | Forwarding | One per collision domain |
| Non-Designated Port | Blocking | Prevents loops |

---

## SECTION 3: CISCO IOS COMMAND REFERENCE

### VLAN Commands

| Command | Mode | Purpose | Example |
|---------|------|---------|---------|
| `show vlan brief` | Privileged EXEC | Show VLANs and ACCESS port assignments | `show vlan brief` |
| `vlan <id>` | Global Config | Create VLAN or enter VLAN config mode | `vlan 10` |
| `name <name>` | VLAN Config | Name a VLAN | `name Engineering` |
| `interface range <range>` | Global Config | Configure multiple interfaces at once | `interface range g0/1 - 3` |
| `switchport mode access` | Interface Config | Set port as access port (disables DTP) | `switchport mode access` |
| `switchport access vlan <id>` | Interface Config | Assign access port to VLAN | `switchport access vlan 10` |

### Trunk Commands

| Command | Mode | Purpose | Example |
|---------|------|---------|---------|
| `switchport trunk encapsulation dot1q` | Interface Config | Set trunk encapsulation to 802.1Q (required on switches supporting both ISL and dot1Q) | `switchport trunk encapsulation dot1q` |
| `switchport mode trunk` | Interface Config | Manually configure as trunk port | `switchport mode trunk` |
| `show interfaces trunk` | Privileged EXEC | Show trunk ports and allowed VLANs | `show interfaces trunk` |
| `switchport trunk allowed vlan <list>` | Interface Config | Set allowed VLANs on trunk | `switchport trunk allowed vlan 10,20,30` |
| `switchport trunk allowed vlan add <id>` | Interface Config | Add VLAN to allowed list | `switchport trunk allowed vlan add 20` |
| `switchport trunk allowed vlan remove <id>` | Interface Config | Remove VLAN from allowed list | `switchport trunk allowed vlan remove 20` |
| `switchport trunk allowed vlan all` | Interface Config | Allow all VLANs (restore default) | `switchport trunk allowed vlan all` |
| `switchport trunk allowed vlan except <list>` | Interface Config | Allow all except specified VLANs | `switchport trunk allowed vlan except 1-5` |
| `switchport trunk allowed vlan none` | Interface Config | Block all VLANs on trunk | `switchport trunk allowed vlan none` |
| `switchport trunk native vlan <id>` | Interface Config | Change native VLAN on trunk | `switchport trunk native vlan 1001` |
| `switchport nonegotiate` | Interface Config | Disable DTP on interface | `switchport nonegotiate` |

### Router on a Stick (ROAS) Commands

| Command | Mode | Purpose | Example |
|---------|------|---------|---------|
| `interface g0/0.<num>` | Global Config | Create sub-interface | `interface g0/0.10` |
| `encapsulation dot1q <vlan-id>` | Sub-interface Config | Assign VLAN to sub-interface | `encapsulation dot1q 10` |
| `encapsulation dot1q <vlan-id> native` | Sub-interface Config | Assign native VLAN to sub-interface | `encapsulation dot1q 10 native` |
| `no interface g0/0.<num>` | Global Config | Delete a sub-interface | `no interface g0/0.10` |

### Layer 3 Switch / SVI Commands

| Command | Mode | Purpose | Example |
|---------|------|---------|---------|
| `ip routing` | Global Config | Enable L3 routing on switch | `ip routing` |
| `no switchport` | Interface Config | Convert L2 port to L3 routed port | `no switchport` |
| `interface vlan <id>` | Global Config | Create SVI for VLAN | `interface vlan 10` |
| `ip address <ip> <mask>` | Interface Config | Assign IP to SVI or routed port | `ip address 10.0.0.1 255.255.255.0` |
| `no shutdown` | Interface Config | Enable SVI (SVIs are shutdown by default) | `no shutdown` |
| `show interfaces status` | Privileged EXEC | Show port status; "routed" in VLAN column = L3 port | `show interfaces status` |

### DTP Commands

| Command | Mode | Purpose | Example |
|---------|------|---------|---------|
| `switchport mode dynamic desirable` | Interface Config | Actively try to form trunk | `switchport mode dynamic desirable` |
| `switchport mode dynamic auto` | Interface Config | Passively allow trunk formation | `switchport mode dynamic auto` |
| `show interfaces g0/0 switchport` | Privileged EXEC | Show DTP administrative and operational mode | `show interfaces g0/0 switchport` |

### VTP Commands

| Command | Mode | Purpose | Example |
|---------|------|---------|---------|
| `vtp mode server` | Global Config | Set switch as VTP server (default) | `vtp mode server` |
| `vtp mode client` | Global Config | Set switch as VTP client | `vtp mode client` |
| `vtp mode transparent` | Global Config | Set switch to transparent mode | `vtp mode transparent` |
| `vtp domain <name>` | Global Config | Set VTP domain name | `vtp domain Cisco` |
| `vtp version <1-3>` | Global Config | Set VTP version | `vtp version 2` |
| `show vtp status` | Privileged EXEC | Show VTP mode, domain, revision, VLAN count | `show vtp status` |

### STP Commands

| Command | Mode | Purpose | Example |
|---------|------|---------|---------|
| `show spanning-tree` | Privileged EXEC | Show STP topology, port roles, states | `show spanning-tree` |
| `show spanning-tree vlan <id>` | Privileged EXEC | Show STP for specific VLAN | `show spanning-tree vlan 1` |
| `spanning-tree vlan <id> priority <value>` | Global Config | Set STP priority for a VLAN (multiples of 4096) | `spanning-tree vlan 1 priority 4096` |
| `spanning-tree vlan <id> root primary` | Global Config | Set switch as root bridge (sets priority to 24576) | `spanning-tree vlan 1 root primary` |
| `spanning-tree vlan <id> root secondary` | Global Config | Set switch as backup root (sets priority to 28672) | `spanning-tree vlan 1 root secondary` |

---

## SECTION 4: DAILY PRACTICE CHECKLIST

### Packet Tracer Lab Sequence

**Lab 1 — Basic VLAN Configuration (Day 16)**
- [ ] Build topology: 1 switch, 1 router, 6 PCs in 3 departments
- [ ] Configure three /26 subnets from 10.0.0.0/24 for VLANs 10, 20, 30
- [ ] Create VLANs 10, 20, 30 and name them Engineering, HR, Sales
- [ ] Configure access ports and assign to correct VLANs
- [ ] Configure three router interfaces (one per VLAN) as default gateways
- [ ] Verify: `show vlan brief` shows correct VLAN-port assignments
- [ ] Test: ping between VLANs (should work via router); ping subnet broadcast (stays in VLAN)

**Lab 2 — Trunk Ports and ROAS (Day 17)**
- [ ] Build topology: 2 switches, 1 router, hosts in VLANs 10, 20, 30
- [ ] Configure trunk link between switches: `switchport trunk encapsulation dot1q`, `switchport mode trunk`
- [ ] Restrict allowed VLANs on trunk appropriately
- [ ] Change native VLAN to unused VLAN 1001 on both ends
- [ ] Configure ROAS on router: G0/0.10, G0/0.20, G0/0.30 with correct encapsulation and IPs
- [ ] Verify: `show interfaces trunk` shows correct allowed VLANs and native VLAN
- [ ] Test: inter-VLAN ping; verify traffic path using simulation mode

**Lab 3 — Layer 3 Switch Inter-VLAN Routing (Day 18)**
- [ ] Add a Layer 3 switch to topology
- [ ] Enable routing: `ip routing`
- [ ] Configure SVIs for each VLAN with last-usable IP
- [ ] Configure routed port (`no switchport`) connecting L3 switch to router
- [ ] Configure default route on L3 switch pointing to router
- [ ] Verify: `show ip route` shows connected routes for each SVI
- [ ] Test: inter-VLAN routing via SVIs (traffic should NOT go to router); external routing goes to router

**Lab 4 — DTP/VTP (Day 19)**
- [ ] Configure one switch as VTP server, one as VTP client, one as transparent
- [ ] Set VTP domain name on all
- [ ] Add VLANs on server, verify client syncs but transparent does not
- [ ] Reset a switch's revision number (domain change or transparent mode)
- [ ] Practice DTP mode combinations: verify operational mode with `show interfaces switchport`
- [ ] Disable DTP on access ports: `switchport nonegotiate`

**Lab 5 — STP Analysis (Day 20)**
- [ ] Build topology: 4 switches with redundant links
- [ ] Manually determine: root bridge, root ports, designated ports, non-designated ports
- [ ] Verify with: `show spanning-tree` and `show spanning-tree vlan 1`
- [ ] Observe port states (forwarding/blocking)
- [ ] Influence root bridge election by changing priority: `spanning-tree vlan 1 priority 4096`
- [ ] Disconnect a forwarding link, observe STP reconvergence

### Daily Real-World Application Drill
- Can you explain to a junior engineer WHY we need both VLANs and subnets?
- Can you draw the traffic path for inter-VLAN routing in each of the 3 methods?
- Can you explain why native VLAN mismatch causes problems?
- Can you trace STP port role selection step by step on a 3-switch topology?
- Can you explain the DTP broadcast storm risk to a security team?

---

## SECTION 5: EXAM-STYLE PRACTICE QUESTIONS

### Single-Answer Multiple Choice

**Q1.** A PC in VLAN 10 sends an ARP broadcast. Which devices will receive the broadcast?

A) All devices on the switch
B) Only devices in VLAN 10
C) Only the default gateway router
D) All devices in the same IP subnet

**Answer: B** — VLANs create separate L2 broadcast domains. The switch only floods the frame to interfaces in VLAN 10.

---

**Q2.** You configure `switchport access vlan 25` on an interface, but VLAN 25 does not yet exist. What happens?

A) The command is rejected
B) The interface is disabled until VLAN 25 is created
C) VLAN 25 is automatically created
D) The interface is placed in VLAN 1

**Answer: C** — The switch automatically creates a VLAN when you assign an interface to a non-existent VLAN.

---

**Q3.** You configure `switchport trunk allowed vlan 10,30` on a trunk, then issue `switchport trunk allowed vlan add 20`. What VLANs are now allowed?

A) 20 only
B) 10, 20
C) 10, 20, 30
D) 1, 10, 20, 30

**Answer: C** — The `add` keyword appends to the existing allowed list without replacing it.

---

**Q4.** Which command changes the native VLAN on a trunk port to VLAN 99?

A) `vlan 99 native`
B) `switchport trunk native vlan 99`
C) `switchport trunk allowed vlan native 99`
D) `encapsulation dot1q 99 native`

**Answer: B** — `switchport trunk native vlan 99` sets the native VLAN on a switch trunk port.

---

**Q5.** Switch A is configured with `switchport mode dynamic auto`. Switch B is configured with `switchport mode dynamic auto`. What will be the operational mode of the connected interfaces?

A) Trunk
B) Access
C) Dynamic
D) The command is rejected

**Answer: B** — Two dynamic auto ports are both passive. Neither initiates trunk formation, so both remain in access mode.

---

**Q6.** A network administrator connects an old spare switch to a production network running VTP. The old switch has VTP domain "Corp" and revision number 85. The production switches have domain "Corp" and revision number 12. What will happen?

A) The old switch will sync its VLAN database to the production network
B) The production switches will sync their VLAN database to the old switch
C) VTP negotiation fails because of revision number mismatch
D) Nothing — VTP only syncs when changes are made

**Answer: B** — VTP syncs to the highest revision number. All production switches will overwrite their VLAN database with the old switch's database, potentially causing a network outage.

---

**Q7.** In a network with 4 switches running STP, Switch D has bridge priority 4096, Switch B has 8192, Switch A has 32769, and Switch C has 32769. Which switch becomes the root bridge?

A) Switch A
B) Switch B
C) Switch C
D) Switch D

**Answer: D** — Switch D has the lowest bridge priority (4096). Lowest bridge ID wins root bridge election.

---

**Q8.** Which STP cost is assigned to a 100 Mbps FastEthernet interface?

A) 2
B) 4
C) 19
D) 100

**Answer: C** — FastEthernet (100 Mbps) has an STP cost of 19 in classic 802.1D.

---

### Multi-Answer Multiple Choice

**Q9.** Which TWO conditions must be met for an SVI to be in up/up state? (Choose 2)

A) The SVI must be configured with an IP address
B) The VLAN must exist on the switch
C) At least one interface in the VLAN must be in up/up state
D) The `ip routing` command must be configured
E) The SVI must be configured as a trunk port

**Answer: B and C** — An SVI requires: (1) VLAN exists on switch, (2) at least one access port in VLAN up/up OR one trunk allowing VLAN up/up. The SVI must also not be shutdown and the VLAN must not be shutdown.

---

**Q10.** Which TWO methods can reset a switch's VTP revision number to 0? (Choose 2)

A) Reloading the switch
B) Changing the VTP domain to an unused name
C) Deleting all VLANs on the switch
D) Changing the VTP mode to transparent
E) Upgrading to VTP version 3

**Answer: B and D** — Changing VTP domain name OR changing to transparent mode resets revision number to 0.

---

**Q11.** Which TWO commands are required to configure a Layer 3 switch interface as a routed port with IP address 10.1.1.1/30? (Choose 2)

A) `ip routing`
B) `no switchport`
C) `switchport mode routed`
D) `ip address 10.1.1.1 255.255.255.252`
E) `encapsulation dot1q 1`

**Answer: B and D** — `no switchport` converts the interface to a routed port, then `ip address` assigns the IP. (`ip routing` is needed on the switch globally but not on the individual interface.)

---

### Scenario-Based Questions

**Q12.** A network has Switch1 connected to Switch2 via G0/1 on each switch. Switch1 has VLAN 10 and 30 hosts; Switch2 has VLAN 20 and 30 hosts. A router connects to Switch2 G0/0 for inter-VLAN routing using ROAS. After configuring trunks, hosts in VLAN 10 cannot reach hosts in VLAN 20. What is the MOST likely cause?

A) The native VLAN is misconfigured
B) VLAN 20 is not allowed on the trunk between Switch1 and Switch2
C) ROAS sub-interfaces are not configured
D) Switch1 does not have VLAN 20 created

**Answer: B** — VLAN 20 hosts are only on Switch2, but traffic from VLAN 10 (on Switch1) must travel through the Switch1-Switch2 trunk, then to the router for inter-VLAN routing. If VLAN 20 is not in the trunk's allowed VLAN list between the switches, the router cannot send the reply back.

*Explanation:* The router routes VLAN 10 → VLAN 20 traffic and sends the reply tagged as VLAN 20 back to Switch2. Switch2 then needs to forward that to Switch1 if the VLAN 10 PC is on Switch1. The trunk must allow both VLANs 10 AND 20.

---

**Q13.** In an STP topology, Switch1 (priority 32769, MAC AA:AA:AA) is connected to Switch2 (priority 32769, MAC BB:BB:BB). Switch2 is also connected to Switch3 (priority 32769, MAC CC:CC:CC), and Switch3 is connected back to Switch1. All links are GigabitEthernet. Which port will be in blocking state?

A) Switch1 G0/1 (connecting to Switch3)
B) Switch2 G0/1 (connecting to Switch3)
C) Switch3 G0/0 (connecting to Switch1)
D) Switch3 G0/1 (connecting to Switch2)

**Answer: D** — Switch1 has the lowest MAC → root bridge (all ports designated). Switch2's root port is toward Switch1 (cost 4); Switch3's root port is toward Switch1 (cost 4). The remaining link between Switch2 and Switch3: Switch2 has lower root cost (4) vs Switch3 (4 — tie). Tiebreaker: Switch2 has lower bridge ID (MAC BB < CC). Switch2's port toward Switch3 = Designated. Switch3's port toward Switch2 = Non-Designated (Blocking).

---

**Q14.** You are configuring ROAS and issue `encapsulation dot1q 10` on interface G0/0.10, but frames from VLAN 10 are arriving untagged at the router. What is the most likely explanation and fix?

A) The trunk native VLAN on the switch is set to VLAN 10; use `encapsulation dot1q 10 native` on the sub-interface
B) VLAN 10 is not allowed on the trunk; add VLAN 10 to the allowed list
C) The sub-interface number must match the VLAN ID exactly
D) Use ISL instead of dot1Q

**Answer: A** — If the switch trunk's native VLAN is VLAN 10, it sends VLAN 10 frames untagged. The router's sub-interface expects tagged frames with VLAN 10. The fix is to either (1) add `native` to the encapsulation command on the sub-interface, or (2) change the switch's native VLAN to an unused VLAN.

---

**Q15.** A VTP transparent mode switch has VTP domain "Corp". Switch A (server) in domain "Corp" creates VLAN 50. Will the transparent switch forward VTP advertisements to switches behind it? Will it add VLAN 50 to its own database?

A) Yes it forwards; Yes it adds VLAN 50
B) Yes it forwards; No it does not add VLAN 50
C) No it does not forward; No it does not add VLAN 50
D) No it does not forward; Yes it adds VLAN 50

**Answer: B** — A transparent switch in the same VTP domain FORWARDS advertisements (passes them through to downstream switches) but does NOT synchronize its own VLAN database to the server.

---

## SECTION 6: QUICK REFERENCE CARD

### 802.1Q Tag — Memory Aid
```
[TPID: 0x8100][PCP: 3b][DEI: 1b][VID: 12b]
      |            |       |        |
  "Tagged!"    Priority  Drop?   VLAN#
```
Mnemonic: **"The Party Doesn't Vary"** = TPID, PCP, DEI, VID

### VLAN Default Values

| Setting | Default |
|---------|---------|
| Default VLAN | 1 |
| Native VLAN | 1 |
| VLANs that cannot be deleted | 1, 1002–1005 |
| Normal VLAN range | 1–1005 |
| Extended VLAN range | 1006–4094 |
| Total usable VLANs | 1–4094 |
| show vlan brief after creating VLANs 10, 20, 30 | 8 total (1, 10, 20, 30, 1002–1005) |

### STP Cost Cheat Sheet
```
10M  = 100  (remember: slowest = highest cost)
100M = 19   (FastEthernet)
1G   = 4    (GigabitEthernet — most common)
10G  = 2    (10 Gigabit)
```
Mnemonic: **"100, 19, 4, 2"** — memorize this exactly for the exam

### STP Bridge Priority — Valid Values
```
0, 4096, 8192, 12288, 16384, 20480, 24576, 28672,
32768, 36864, 40960, 45056, 49152, 53248, 57344, 61440
```
- `root primary` sets priority to **24576**
- `root secondary` sets priority to **28672**
- Default = **32768** (+ VLAN ID for PVST)

### DTP Quick Table (Results)
```
Auto + Auto       = ACCESS
Auto + Desirable  = TRUNK
Auto + Trunk      = TRUNK
Desirable + Des.  = TRUNK
Desirable + Trunk = TRUNK
Access + Trunk    = MISCONFIG
```

### VTP Mode Quick Comparison
```
Server      = Add/Modify/Delete VLANs + Syncs + NVRAM + Forwards
Client      = Read only + Syncs (no NVRAM v1/v2) + Forwards
Transparent = Add/Modify/Delete (local only) + NO Sync + NVRAM + Forwards*
              * only forwards if same domain
```

### Inter-VLAN Routing Methods at a Glance
```
Method 1: One interface per VLAN — Simple but wastes ports
Method 2: ROAS — One trunk + sub-interfaces — OK for small networks
Method 3: L3 Switch SVIs — Best for large networks — routes internally
```

### Key show Commands for This Section
```
show vlan brief               -> access port VLAN assignments
show interfaces trunk         -> trunk ports, allowed VLANs, native VLAN
show interfaces <int> switchport -> DTP admin/operational mode
show vtp status               -> VTP mode, domain, revision number
show spanning-tree            -> STP topology, root bridge, port roles
show ip route                 -> routing table (L3 switch or router)
show interfaces status        -> port speed/duplex + "routed" for L3 ports
```

---

## SECTION 7: KNOWLEDGE GAPS FLAG

### Topics Needing Deeper Study

**1. STP Timers (Covered in Part 2 — Day 21)**
- Hello timer (2s), Forward delay (15s), Max age (20s)
- Port transition states: Blocking → Listening → Learning → Forwarding
- These are high-frequency exam topics — study in Part 2

**2. Rapid PVST+ (RSTP — Future Day)**
- Much faster convergence than classic STP
- This is the version on the CCNA exam topics list
- Classic STP is foundational knowledge only

**3. PortFast and BPDU Guard (Day 21)**
- PortFast: immediately move access ports to forwarding state
- `spanning-tree portfast default` — enables on all access ports globally
- BPDU Guard: shutdown port if BPDU received (prevents rogue switches)
- These will appear on exam — do not skip

**4. STP Configuration Commands (Day 21)**
- `spanning-tree vlan <id> root primary/secondary`
- Port cost and priority manipulation

**5. EtherChannel (Future)**
- Aggregates multiple physical links into one logical link
- Solves STP blocking redundant paths
- Very high exam weight — prepare thoroughly

**6. InterVLAN Routing Security**
- VLAN hopping attacks (exploit native VLAN)
- Why native VLAN should always be changed to unused VLAN
- Double-tagging attack concept

**7. Wireless VLANs**
- SSIDs mapped to VLANs
- Wireless infrastructure connects to trunk ports
- Part of Network Access domain

### Cross-Domain Connections
- **VLANs and ACLs (Security)**: VLANs separate traffic; ACLs on SVIs or router interfaces control what crosses VLAN boundaries
- **VLANs and DHCP**: Each VLAN typically needs its own DHCP scope; IP helper-address for DHCP relay
- **STP and EtherChannel**: EtherChannel prevents STP from blocking redundant links between switches
- **L3 Switching and OSPF**: Multi-layer switches can run OSPF just like routers

### Exam Traps to Remember
1. `show vlan brief` does NOT show trunk ports — use `show interfaces trunk`
2. SVIs are **shutdown by default** — always `no shutdown`
3. STP priority increments are **4096**, not any number
4. DTP forms a trunk only between **Cisco switches** — not with routers or PCs
5. VTP syncs the VLAN **database only** — does NOT configure interface assignments
6. Native VLAN must **match on both ends** of a trunk
7. When counting VLANs in `show vlan brief`: default VLANs 1 + 1002–1005 = 5 always exist
8. STP root cost counts **outgoing** interface cost only, not receiving interface
9. `switchport trunk encapsulation dot1q` is required **only** on switches that support both ISL and dot1Q (not all switches need it)
10. PVST uses bridge priority = **32768 + VLAN ID** by default, not 32768

---

*Study Guide generated from Jeremy's IT Lab CCNA 200-301 Complete Course — Transcripts 028-038 (Days 16-20)*
*Next section: Days 21-25 — STP Part 2, Rapid STP, EtherChannel*
