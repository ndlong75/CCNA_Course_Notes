[< Back to All Sections](../README.md#section-study-guides)

# CCNA 200-301 Exam Coach — Section 09 Study Guide
## Days 51–55 | Dynamic ARP Inspection, LAN Architectures, WAN Architectures, Virtualization & Cloud, Wireless Fundamentals
### Transcripts 103–114 | Jeremy's IT Lab Complete Course

---

## SECTION 1: EXAM KNOWLEDGE MAP

| # | Video | Day | Topic | CCNA Domain | Exam Weight |
|---|-------|-----|-------|-------------|-------------|
| 103 | Dynamic ARP Inspection | Day 51 | DAI overview, GARP, ARP poisoning, trusted/untrusted ports, DHCP snooping binding table validation, rate-limiting, optional checks | Security Fundamentals | 15% |
| 104 | DAI Lab | Day 51 Lab | Configure DAI, trust ports, ARP ACLs, rate-limiting, show ip arp inspection | Security Fundamentals | 15% |
| 105 | LAN Architectures | Day 52 | Star/full-mesh/partial-mesh topologies, 2-tier (collapsed core), 3-tier campus LAN, spine-leaf (data center), SOHO | Network Fundamentals | 20% |
| 106 | LAN Architectures Lab | Day 52 Lab | Topology analysis, layer identification, design review | Network Fundamentals | 20% |
| 107 | WAN Architectures | Day 53 | Leased lines, MPLS VPNs (L2/L3), Internet connectivity (DSL, cable), site-to-site VPN (IPsec), GRE over IPsec, DMVPN, remote-access VPN (TLS) | Network Fundamentals | 20% |
| 108 | WAN Architectures Lab | Day 53 Lab | GRE tunnel configuration, OSPF over tunnel, default routes to ISP | Network Fundamentals | 20% |
| 109 | Virtualization & Cloud Part 1 | Day 54 | Type 1/Type 2 hypervisors, virtual networks, cloud computing (5 characteristics, 3 service models, 4 deployment models) | Network Fundamentals | 20% |
| 110 | Virtualization Part 2 — Containers | Day 54 | Containers vs VMs, Docker, Kubernetes, container orchestration | Network Fundamentals | 20% |
| 111 | Virtualization Part 3 — VRF | Day 54 | VRF-Lite, multiple routing tables, VRF configuration, VRF leaking | Network Fundamentals | 20% |
| 112 | VRF Lab | Day 54 Lab | ip vrf, vrf forwarding, show ip route vrf, ping vrf | Network Fundamentals | 20% |
| 113 | Wireless Fundamentals | Day 55 | CSMA/CA, RF basics, 2.4/5 GHz bands, channels, 802.11 standards, service sets (IBSS/BSS/ESS/MBSS), AP modes | Network Fundamentals | 20% |
| 114 | Wireless Fundamentals Lab | Day 55 Lab | WLAN configuration basics, SSID identification, channel assignment | Network Fundamentals | 20% |

**Exam Objectives Covered:**
- 5.7 Configure and verify Layer 2 security features (dynamic ARP inspection)
- 1.1 Explain the role and function of network components (routers, Layer 2/3 switches, firewalls)
- 1.2 Describe characteristics of network topology architectures (two-tier, three-tier, spine-leaf, WAN, SOHO)
- 1.3 Compare physical interface and cabling types (single-mode/multimode fiber, copper, WAN serial)
- 1.11 Describe wireless principles (nonoverlapping Wi-Fi channels, SSID, RF, encryption)
- 1.12 Explain virtualization fundamentals (server virtualization, containers, VRFs)
- 1.13 Describe switching concepts (MAC learning, frame switching, MAC table, collision/broadcast domains)

---

## SECTION 2: MUST-KNOW CONCEPTS

---

### Concept 1: Dynamic ARP Inspection (DAI)

**ARP Review:**
- ARP resolves a known IP address to a MAC address using a two-message exchange: **ARP Request** (broadcast) and **ARP Reply** (unicast)
- **Gratuitous ARP (GARP):** An ARP Reply sent without a preceding ARP Request, sent to the broadcast MAC address
  - Allows devices to learn the sender's MAC without requesting it
  - Automatically sent when an interface comes up, IP/MAC changes, etc.

**ARP Poisoning Attack:**
- Attacker sends crafted **Gratuitous ARP messages** using another device's IP address
- Victims update their ARP cache with the attacker's MAC → traffic is redirected to the attacker
- This is a **Man-in-the-Middle (MITM)** attack

**What DAI Does:**
- A **Layer 2 switch security feature** that filters ARP messages on **untrusted ports**
- Only inspects ARP messages — all other traffic passes normally
- All ports are **untrusted by default** — uplinks to switches/routers should be trusted
- DAI validates ARP messages against the **DHCP snooping binding table**
  - Checks: sender MAC and sender IP in the ARP message must match a binding table entry
  - Match → forward; no match → discard
- Messages on **trusted ports** are forwarded without inspection

**DAI Dependency on DHCP Snooping:**
- DAI uses the DHCP snooping binding table for validation
- **DHCP snooping must be enabled** for DAI to function (unless using ARP ACLs)
- For hosts with static IPs (no DHCP), configure **ARP ACLs** to manually map IP-to-MAC

**DAI Rate-Limiting:**
- Prevents attackers from overwhelming the switch CPU with ARP messages
- Default: **15 ARP messages per second** on untrusted ports
- Exceeding the rate limit causes the port to be **err-disabled**
- Trusted ports have **no rate limit** by default
- `errdisable recovery cause arp-inspection` enables automatic recovery

**DAI Optional Checks:**
- Beyond basic sender MAC/IP validation, DAI can perform additional checks:
  - **dst-mac:** Validates the destination MAC in the Ethernet header matches the target MAC in the ARP body
  - **src-mac:** Validates the source MAC in the Ethernet header matches the sender MAC in the ARP body
  - **ip:** Validates against invalid/unexpected IP addresses (e.g., 0.0.0.0, 255.255.255.255, multicast)

**DAI Configuration:**
```
! DHCP snooping must be enabled first (DAI depends on the binding table)
SW(config)# ip dhcp snooping
SW(config)# ip dhcp snooping vlan 10

! Enable DAI on the VLAN
SW(config)# ip arp inspection vlan 10

! Trust uplink ports (toward other switches/routers)
SW(config)# interface g0/1
SW(config-if)# ip arp inspection trust

! Configure rate-limiting on untrusted ports (default is 15 pps)
SW(config)# interface range fa0/1 - 24
SW(config-if-range)# ip arp inspection limit rate 25

! Enable optional validation checks
SW(config)# ip arp inspection validate dst-mac src-mac ip

! ARP ACL for static IP hosts
SW(config)# arp access-list DAI-ACL
SW(config-arp-nacl)# permit ip host 10.0.0.100 mac host aaaa.bbbb.cccc
SW(config)# ip arp inspection filter DAI-ACL vlan 10

! Err-disable auto-recovery
SW(config)# errdisable recovery cause arp-inspection

! Verification
SW# show ip arp inspection                    ! Global DAI config and statistics
SW# show ip arp inspection interfaces         ! Per-interface trust state and rate limits
SW# show ip arp inspection vlan 10            ! DAI status for a specific VLAN
SW# show ip dhcp snooping binding             ! Binding table (used by DAI)
```

---

### Concept 2: LAN Architectures — Network Topologies

**Common Topology Types:**

| Topology | Description |
|----------|------------|
| **Star** | All devices connect to one central device (most common LAN topology) |
| **Full Mesh** | Every device is directly connected to every other device |
| **Partial Mesh** | Some devices are directly interconnected, but not all |

**Two-Tier (Collapsed Core) LAN Design:**
- Consists of two hierarchical layers: **Access Layer** and **Distribution Layer**
- Called "collapsed core" because it omits the core layer found in three-tier designs
- Suitable for **small-to-medium** enterprise networks

| Layer | Function |
|-------|---------|
| **Access Layer** | End hosts connect here (PCs, phones, cameras). Many ports. QoS marking, port security, DAI, PoE for APs/phones |
| **Distribution Layer** | Aggregates access layer connections. L2/L3 boundary. Connects to WAN/Internet. Also called **aggregation layer** |

**Three-Tier Campus LAN Design:**
- Adds a **Core Layer** above the distribution layer
- Cisco recommends adding a core layer when there are **more than 3 distribution layer switches** in a single location
- Used in **large enterprise/campus** networks

| Layer | Function |
|-------|---------|
| **Core Layer** | Connects distribution layers. Focus: **speed** ("fast transport"). All L3, no STP. Avoid CPU-intensive operations (QoS, security). Must maintain connectivity if devices fail |
| **Distribution Layer** | Policy-based connectivity. Routing, filtering, QoS, aggregation |
| **Access Layer** | End-host connectivity. Security services, PoE, QoS marking |

**Spine-Leaf Architecture (Data Center):**
- Also called **Clos architecture**; used in Cisco ACI (Application Centric Infrastructure)
- Designed for **east-west traffic** (server-to-server) dominant in modern data centers with virtualization
- Traditional three-tier designs caused bottlenecks and variable latency for east-west traffic

**Spine-Leaf Rules:**
1. Every **leaf switch** connects to every **spine switch**
2. Every **spine switch** connects to every **leaf switch**
3. Leaf switches do **NOT** connect to other leaf switches
4. Spine switches do **NOT** connect to other spine switches
5. End hosts (servers) **ONLY** connect to leaf switches

- Traffic path is randomly chosen to balance load across spine switches
- Every server is the same number of hops apart (except on the same leaf) → **consistent latency**

**SOHO (Small Office / Home Office):**
- A single "home router" or "wireless router" serves all functions: router, switch, firewall, wireless AP, modem
- No complex design needed; all-in-one device

---

### Concept 3: WAN Architectures — Connecting Sites

**WAN Overview:**
- WANs connect geographically separate LANs
- "WAN" typically refers to an enterprise's **private connections** between offices, data centers, and sites
- Many WAN technologies exist; availability varies by location

**Leased Lines:**
- Dedicated **physical link** between two sites
- Uses **serial connections** with PPP or HDLC encapsulation
- Higher cost, longer installation time, slower speeds → being replaced by Ethernet WAN technologies

**MPLS VPNs (Multi-Protocol Label Switching):**
- Shared service provider infrastructure using **labels** for forwarding (not destination IP)
- Key terminology:
  - **CE Router** = Customer Edge — the customer's router connecting to the SP
  - **PE Router** = Provider Edge — the SP's router connecting to the customer
  - **P Router** = Provider Core — internal SP routers

| MPLS VPN Type | CE-PE Relationship | Effect |
|---------------|-------------------|--------|
| **Layer 3 MPLS VPN** | CE and PE peer via routing protocol (e.g., OSPF) | CE learns remote site routes through PE |
| **Layer 2 MPLS VPN** | CE and PE do NOT form peerings; SP is transparent | CEs appear directly connected; peer with each other |

**Internet Connectivity Technologies:**

| Technology | Medium | Notes |
|-----------|--------|-------|
| **DSL** | Phone lines | DSL modem required; shares existing phone line |
| **Cable (CATV)** | Coaxial cable TV lines | Cable modem required; shares TV infrastructure |
| **Fiber Optic Ethernet** | Fiber | Growing in popularity; high speed over long distances |

**Redundant Internet Connections:**
- **Single-homed:** One connection to one ISP
- **Dual-homed:** Two connections to one ISP
- **Multi-homed:** One connection each to two ISPs
- **Dual multi-homed:** Two connections each to two ISPs (most redundant)

---

### Concept 4: Internet VPNs — Site-to-Site and Remote-Access

**Site-to-Site VPNs (IPsec):**
- Connects **two sites** over the Internet via a VPN tunnel between two routers/firewalls
- Process: original packet → encrypted with session key → encapsulated with VPN header + new IP header → sent through tunnel → decrypted at destination
- Only the **tunnel endpoints** (routers) need VPN configuration; end devices send unencrypted traffic to their local router

**IPsec Limitations:**
1. Does NOT support **broadcast or multicast** → routing protocols like OSPF cannot run over pure IPsec tunnels
2. Configuring a **full mesh** of tunnels is labor-intensive

**GRE over IPsec (solves limitation 1):**
- **GRE** (Generic Routing Encapsulation) supports broadcast/multicast but does NOT encrypt
- **GRE over IPsec** combines GRE flexibility with IPsec security
- Encapsulation order: Original packet → GRE header + new IP → IPsec encryption → VPN header + new IP

**DMVPN (solves limitation 2):**
- **Dynamic Multipoint VPN** — Cisco-developed solution
- Spoke routers configure only one tunnel to the **hub**
- Hub provides information for spokes to dynamically form **direct spoke-to-spoke tunnels**
- Result: configuration simplicity of hub-and-spoke + efficiency of full mesh

**Remote-Access VPNs (TLS):**
- For **individual end devices** (laptops, phones) connecting to company resources over the Internet
- Uses **TLS** (Transport Layer Security), formerly SSL
- Requires VPN client software (e.g., Cisco AnyConnect) on end devices
- End device forms a secure tunnel to the company's router/firewall

**Site-to-Site vs. Remote-Access VPN:**

| Feature | Site-to-Site | Remote-Access |
|---------|-------------|--------------|
| Protocol | Typically **IPsec** | Typically **TLS** |
| Serves | Many devices at both sites | One end device per tunnel |
| Connection | Permanent between two sites | On-demand for individual users |
| Use Case | Connect branch offices | Remote workers accessing company network |

---

### Concept 5: Virtualization — Hypervisors, Containers, VRF

**Servers Before Virtualization:**
- One physical server = one OS = one application
- Inefficient: expensive, space/power-consuming, resources under-utilized

**Type 1 Hypervisor (Bare-Metal / Native):**
- Runs **directly on hardware** — no host OS
- Used in **data center environments**
- Examples: VMware ESXi, Microsoft Hyper-V
- Manages and allocates hardware resources (CPU, RAM, storage) to each VM

**Type 2 Hypervisor (Hosted):**
- Runs **as a program on a host OS** (like a regular application)
- Used on **personal devices** (running CML, testing different OSes)
- Examples: VMware Workstation, Oracle VirtualBox
- Host OS = OS on the hardware; Guest OS = OS inside the VM

**Benefits of Virtualization:**
- **Partitioning** — multiple OSes on one physical machine
- **Isolation** — fault and security isolation between VMs
- **Encapsulation** — entire VM state saved to files; easy to move/copy
- **Hardware Independence** — migrate VMs between physical servers

**Virtual Networks:**
- VMs connect via a **virtual switch (vSwitch)** on the hypervisor
- vSwitch interfaces operate as access or trunk ports with VLANs
- vSwitch connects to the physical NIC(s) for external network access

**Containers vs. Virtual Machines:**

| Feature | Virtual Machines | Containers |
|---------|-----------------|-----------|
| Boot time | Minutes | Milliseconds |
| Disk space | Gigabytes | Megabytes |
| CPU/RAM usage | More (each has own OS) | Less (shared OS) |
| Portability | Portable (same hypervisor required) | More portable (run on any container engine) |
| Isolation | Stronger (separate OS per VM) | Weaker (shared OS — OS crash affects all) |
| Engine | Hypervisor | Container Engine (e.g., Docker) |
| Orchestration | N/A | Kubernetes, Docker Swarm |

**VRF (Virtual Routing and Forwarding):**
- Divides a single router into **multiple virtual routers** with separate routing tables
- Similar concept to VLANs dividing a switch into multiple virtual switches
- Traffic in one VRF **cannot** be forwarded to interfaces in another VRF (unless VRF leaking is configured)
- **VRF-Lite** = VRF without MPLS
- Commonly used by service providers to carry traffic from multiple customers on one device
- Customer IP address spaces can **overlap** without conflict

**VRF Configuration:**
```
! Create VRFs
R1(config)# ip vrf CUSTOMER_A
R1(config)# ip vrf CUSTOMER_B

! Assign interfaces to VRFs (removes existing IP when applied)
R1(config)# interface g0/0
R1(config-if)# ip vrf forwarding CUSTOMER_A
R1(config-if)# ip address 10.0.0.1 255.255.255.0

R1(config)# interface g0/1
R1(config-if)# ip vrf forwarding CUSTOMER_B
R1(config-if)# ip address 10.0.0.1 255.255.255.0    ! Same IP — no conflict, different VRFs

! Verification
R1# show ip route vrf CUSTOMER_A           ! Routing table for VRF
R1# show ip vrf                             ! All configured VRFs
R1# ping vrf CUSTOMER_A 10.0.0.2           ! Ping within a specific VRF
```

---

### Concept 6: Cloud Computing Models

**Five Essential Characteristics (NIST SP 800-145):**

| Characteristic | Meaning |
|---------------|---------|
| **On-Demand Self-Service** | Customer provisions/de-provisions services freely via web portal without contacting the provider |
| **Broad Network Access** | Service available via standard network connections (Internet/WAN); accessible from many device types |
| **Resource Pooling** | Provider maintains a shared pool of resources; allocated dynamically per customer request |
| **Rapid Elasticity** | Customers can quickly scale up or down; resources appear infinite |
| **Measured Service** | Usage is measured and billed (e.g., $/GB/day); both provider and customer can monitor |

**Three Service Models:**

| Model | What Customer Manages | What Provider Manages | Example |
|-------|----------------------|----------------------|---------|
| **SaaS** (Software as a Service) | Just use the application | Everything (infrastructure + platform + application) | Microsoft 365, Gmail |
| **PaaS** (Platform as a Service) | Application code and data | Infrastructure + OS + runtime | AWS Lambda, Google App Engine |
| **IaaS** (Infrastructure as a Service) | OS, applications, data | Hardware, networking, storage, virtualization | Amazon EC2, Google Compute Engine |

**Four Deployment Models:**

| Model | Description |
|-------|------------|
| **Private Cloud** | Infrastructure reserved for a single organization. Can be on/off premises. May be owned by a third party (e.g., AWS for US DoD) |
| **Community Cloud** | Infrastructure shared by a specific group of organizations with common concerns. Least common model |
| **Public Cloud** | Open to the general public. Most common. Examples: AWS, Azure, GCP, OCI, IBM Cloud, Alibaba Cloud |
| **Hybrid Cloud** | Any combination of private, community, and public clouds (e.g., private cloud that bursts to public cloud) |

**Traditional Deployment Comparison:**

| Model | Equipment Location | Equipment Owner | Space/Power/Cooling |
|-------|-------------------|----------------|---------------------|
| **On-Premises** | Company property | Company | Company |
| **Co-Location** | Third-party data center | Company | Data center provider |
| **Cloud** | Provider's data center | Provider | Provider |

---

### Concept 7: Wireless Fundamentals — RF, Bands, and Channels

**Wireless Network Challenges:**
1. All devices within range receive all frames (like an Ethernet hub) → **privacy concern**
2. Uses **CSMA/CA** (Collision Avoidance) for half-duplex communication — devices wait before transmitting
3. Wireless signal regulated by international/national bodies
4. Signal coverage affected by: **absorption**, **reflection**, **refraction**, **diffraction**, **scattering**
5. Other devices on the same channel cause **interference**

**Signal Behavior:**

| Effect | Cause | Example |
|--------|-------|---------|
| **Absorption** | Signal passes through material, converted to heat | Walls weakening signal |
| **Reflection** | Signal bounces off material | Metal surfaces, elevators |
| **Refraction** | Signal bends entering medium with different speed | Glass, water |
| **Diffraction** | Signal travels around an obstacle | Creates blind spots behind obstacle |
| **Scattering** | Signal scatters in all directions | Dust, smog, uneven surfaces |

**Radio Frequency Basics:**
- Sender applies alternating current to antenna → electromagnetic waves propagate
- **Amplitude** = maximum strength of the signal
- **Frequency** = number of cycles per second (measured in Hertz)
- **Period** = time of one cycle (inverse of frequency)

**Wi-Fi Frequency Bands:**

| Band | Range | Characteristics |
|------|-------|----------------|
| **2.4 GHz** | 2.400–2.4835 GHz | Longer range, better wall penetration; more interference (crowded) |
| **5 GHz** | 5.150–5.825 GHz (4 sub-bands) | Shorter range; less interference (more channels, non-overlapping) |
| **6 GHz** | Wi-Fi 6E (802.11ax) extension | Even more channels and bandwidth |

**Channels:**
- Each band divided into channels; devices transmit/receive on specific channels
- **2.4 GHz:** 22 MHz wide channels; recommended non-overlapping: **channels 1, 6, and 11**
- **5 GHz:** All channels are non-overlapping — easier to avoid interference
- Multiple APs should use different channels to avoid interference ("honeycomb" pattern)

---

### Concept 8: Wi-Fi Standards and Service Sets

**802.11 Wi-Fi Standards (Exam Must-Know):**

| Standard | Wi-Fi Alliance Name | Frequency | Max Speed | Notes |
|----------|-------------------|-----------|-----------|-------|
| 802.11 | — | 2.4 GHz | 2 Mbps | Original standard |
| 802.11b | — | 2.4 GHz | 11 Mbps | — |
| 802.11a | — | 5 GHz | 54 Mbps | — |
| 802.11g | — | 2.4 GHz | 54 Mbps | Backward compatible with 802.11b |
| 802.11n | **Wi-Fi 4** | 2.4 / 5 GHz | 600 Mbps | MIMO; first dual-band standard |
| 802.11ac | **Wi-Fi 5** | 5 GHz | 6.93 Gbps | MU-MIMO; 5 GHz only |
| 802.11ax | **Wi-Fi 6 / 6E** | 2.4 / 5 / 6 GHz | 9.6 Gbps | OFDMA; includes 6 GHz band |

**Service Sets:**

| Type | Full Name | Description |
|------|-----------|------------|
| **IBSS** | Independent BSS | Ad hoc — devices connect directly, no AP. Not scalable |
| **BSS** | Basic Service Set | Clients connect through a single AP. BSSID = AP's radio MAC address. Coverage area = BSA |
| **ESS** | Extended Service Set | Multiple APs with same SSID, unique BSSIDs, different channels. Supports roaming. BSAs overlap 10–15% |
| **MBSS** | Mesh BSS | Mesh APs with two radios: one for clients, one for backhaul. RAP (Root AP) connects to wired network; MAPs (Mesh APs) form the mesh |

**Key Service Set Terms:**
- **SSID** (Service Set Identifier): Human-readable network name; does NOT have to be unique
- **BSSID** (Basic Service Set ID): AP's radio MAC address; must be unique per BSS
- **BSA** (Basic Service Area): Coverage area of a single AP's signal
- **Roaming**: Client moves between APs in an ESS without disconnecting

**Distribution System:**
- The upstream wired network that wireless clients ultimately connect to
- Each BSS/ESS maps to a **VLAN** in the wired network
- An AP can provide **multiple WLANs** (multiple SSIDs), each mapped to a different VLAN via a **trunk** connection
- Each WLAN uses a unique BSSID (typically incrementing the last digit)

**Additional AP Modes:**

| Mode | Function |
|------|---------|
| **Repeater** | Extends BSS range by retransmitting AP signals. Single radio = same channel (reduces throughput). Dual radio = different channels |
| **Workgroup Bridge (WGB)** | Connects wired devices to the wireless network (wireless client of another AP) |
| **Outdoor Bridge** | Connects remote networks over long distances using directional antennas. Point-to-point or point-to-multipoint |

---

## SECTION 3: COMMON EXAM TRAPS

| Trap | Correct Answer |
|------|---------------|
| "DAI inspects all traffic on untrusted ports?" | FALSE — DAI **only inspects ARP messages**. All non-ARP traffic passes through untrusted ports normally. |
| "DAI works independently without DHCP snooping?" | FALSE — DAI validates ARP messages against the **DHCP snooping binding table**. DHCP snooping must be enabled first (unless using ARP ACLs for static hosts). |
| "All ports are trusted by default for DAI?" | FALSE — All ports are **untrusted by default**. Uplink ports to switches/routers must be manually configured as trusted. |
| "DAI rate-limiting applies to trusted ports by default?" | FALSE — Trusted ports have **no rate limit** by default. Rate-limiting is applied to **untrusted ports** (default 15 pps). |
| "In a two-tier LAN design, the core layer connects the distribution switches?" | FALSE — A two-tier design has **no core layer** (that's why it's called "collapsed core"). Only three-tier designs have a core layer. |
| "Cisco recommends adding a core layer when you have 2 distribution switches?" | FALSE — Cisco recommends a core layer when there are **more than 3 distribution layer switches** in a single location. |
| "In spine-leaf architecture, leaf switches connect to other leaf switches for redundancy?" | FALSE — Leaf-to-leaf connections are **NOT allowed**. Every leaf connects to every spine, and traffic between leaves always traverses exactly one spine switch. |
| "MPLS labels are used by CE routers to forward traffic?" | FALSE — **CE routers do NOT use MPLS**. Only **PE and P routers** (service provider equipment) use MPLS labels. |
| "IPsec natively supports OSPF over VPN tunnels?" | FALSE — Standard IPsec only supports **unicast** traffic. OSPF uses multicast and cannot run over pure IPsec. **GRE over IPsec** solves this. |
| "Remote-access VPNs typically use IPsec?" | FALSE — Remote-access VPNs typically use **TLS** (not IPsec). **Site-to-site** VPNs use IPsec. |
| "Type 2 hypervisors are used in data center environments?" | FALSE — Data centers use **Type 1 (bare-metal/native)** hypervisors. Type 2 (hosted) hypervisors run on personal devices. |
| "Containers provide stronger isolation than VMs?" | FALSE — **VMs** provide stronger isolation (each has its own OS). Containers share the host OS — if the OS crashes, all containers are affected. |
| "VRF allows traffic to pass freely between virtual routing instances?" | FALSE — Traffic in one VRF **cannot** reach interfaces in another VRF by default. **VRF leaking** must be explicitly configured to allow inter-VRF traffic. |
| "Assigning an interface to a VRF preserves its existing IP address?" | FALSE — Assigning an interface to a VRF with `ip vrf forwarding` **removes the existing IP address**. You must reconfigure the IP after the VRF assignment. |
| "The 2.4 GHz band has more non-overlapping channels than 5 GHz?" | FALSE — The 2.4 GHz band has only **3 non-overlapping channels** (1, 6, 11). The 5 GHz band has **many more** non-overlapping channels. |
| "CSMA/CA detects collisions after they occur?" | FALSE — **CSMA/CA avoids** collisions (devices wait before transmitting). **CSMA/CD** (wired) detects collisions. |
| "In an ESS, all APs use the same BSSID?" | FALSE — Each AP in an ESS has a **unique BSSID** (its radio MAC). They share the same **SSID**, but BSSIDs must differ. |
| "Private cloud always means on-premises infrastructure?" | FALSE — Private clouds can be **on or off premises** and may even be owned by a third party (e.g., AWS GovCloud). |

---

## SECTION 4: COMPLETE COMMAND REFERENCE

### Dynamic ARP Inspection Commands
```
! Enable DHCP snooping (prerequisite for DAI)
SW(config)# ip dhcp snooping
SW(config)# ip dhcp snooping vlan 10

! Enable DAI on a VLAN
SW(config)# ip arp inspection vlan 10
SW(config)# ip arp inspection vlan 10,20,30         ! Multiple VLANs

! Configure trusted ports (uplinks to switches/routers)
SW(config-if)# ip arp inspection trust

! Rate-limiting on untrusted ports
SW(config-if)# ip arp inspection limit rate 25       ! Max 25 ARP msgs/sec (default 15)
SW(config-if)# ip arp inspection limit rate 25 burst interval 2  ! 25 per 2 seconds

! Enable optional validation checks
SW(config)# ip arp inspection validate dst-mac       ! Check dst MAC in Ethernet header
SW(config)# ip arp inspection validate src-mac       ! Check src MAC in Ethernet header
SW(config)# ip arp inspection validate ip            ! Check for invalid IPs
SW(config)# ip arp inspection validate dst-mac src-mac ip   ! All checks (must be one line)

! ARP ACL for static IP hosts (no DHCP)
SW(config)# arp access-list STATIC-HOSTS
SW(config-arp-nacl)# permit ip host 10.0.0.100 mac host aaaa.bbbb.cccc
SW(config)# ip arp inspection filter STATIC-HOSTS vlan 10

! Err-disable auto-recovery for DAI
SW(config)# errdisable recovery cause arp-inspection

! Verification
SW# show ip arp inspection                           ! Global DAI statistics
SW# show ip arp inspection interfaces                ! Per-interface trust/rate config
SW# show ip arp inspection vlan 10                   ! DAI status per VLAN
SW# show ip dhcp snooping binding                    ! DHCP binding table (used by DAI)
```

### WAN / GRE Tunnel Commands
```
! Create a GRE tunnel interface
R1(config)# interface tunnel 0
R1(config-if)# tunnel source g0/0                    ! Physical exit interface
R1(config-if)# tunnel destination 203.0.113.2        ! Remote tunnel endpoint IP
R1(config-if)# ip address 10.0.0.1 255.255.255.252   ! Tunnel interface IP

! Default route to ISP
R1(config)# ip route 0.0.0.0 0.0.0.0 203.0.113.1

! OSPF over GRE tunnel
R1(config)# router ospf 1
R1(config-router)# network 10.0.0.0 0.0.0.3 area 0         ! Tunnel network
R1(config-router)# network 192.168.1.0 0.0.0.255 area 0     ! LAN network
R1(config-router)# passive-interface g0/1                     ! LAN interface
```

### VRF Commands
```
! Create VRFs
R1(config)# ip vrf CUSTOMER_A
R1(config-vrf)# exit
R1(config)# ip vrf CUSTOMER_B

! Assign interface to VRF (WARNING: removes existing IP!)
R1(config)# interface g0/0
R1(config-if)# ip vrf forwarding CUSTOMER_A
R1(config-if)# ip address 10.0.0.1 255.255.255.0    ! Re-apply IP after VRF assignment

! Verification
R1# show ip vrf                              ! List all VRFs and their interfaces
R1# show ip route vrf CUSTOMER_A             ! Routing table for specific VRF
R1# ping vrf CUSTOMER_A 10.0.0.2            ! Ping within a VRF
```

---

## SECTION 5: EXAM QUICK-REFERENCE TABLES

### Layer 2 Security Feature Comparison

| Feature | What It Filters | Validation Source | Default Port State | Err-Disable Trigger |
|---------|----------------|-------------------|-------------------|---------------------|
| **DHCP Snooping** | DHCP messages | CHADDR vs source MAC; binding table | Untrusted | Rate-limit exceeded |
| **Dynamic ARP Inspection** | ARP messages | DHCP snooping binding table (or ARP ACL) | Untrusted | Rate-limit exceeded |
| **Port Security** | Source MAC addresses | Configured allowed MACs (static/dynamic/sticky) | N/A (must enable) | Violation (default: shutdown) |

### LAN Architecture Comparison

| Design | Layers | When to Use | Key Characteristic |
|--------|--------|------------|-------------------|
| **Two-Tier (Collapsed Core)** | Access + Distribution | Small-to-medium networks | No dedicated core layer |
| **Three-Tier Campus** | Access + Distribution + Core | Large campus (>3 distribution switches) | Core = speed, L3 only, no STP |
| **Spine-Leaf (Data Center)** | Leaf + Spine | Modern data centers (east-west traffic) | Every leaf connects to every spine; consistent latency |
| **SOHO** | Single device | Home/small office | All-in-one router/switch/AP/firewall |

### WAN Technology Comparison

| Technology | Type | Encryption | Broadcast/Multicast? | Use Case |
|-----------|------|-----------|---------------------|---------|
| **Leased Line** | Dedicated | N/A (private) | Yes | Legacy point-to-point WAN |
| **MPLS VPN** | Shared (SP) | N/A (label-separated) | Depends on type | Enterprise multi-site WAN |
| **IPsec VPN** | Internet-based | Yes (encrypted) | No (unicast only) | Site-to-site over Internet |
| **GRE over IPsec** | Internet-based | Yes | Yes | Site-to-site needing routing protocols |
| **DMVPN** | Internet-based | Yes | Yes | Multi-site with dynamic full mesh |
| **TLS VPN** | Internet-based | Yes | N/A | Remote-access for individual users |

### Hypervisor Comparison

| Feature | Type 1 (Bare-Metal) | Type 2 (Hosted) |
|---------|---------------------|-----------------|
| Runs on | Directly on hardware | On top of a host OS |
| Use case | Data centers | Personal devices |
| Examples | VMware ESXi, Hyper-V | VMware Workstation, VirtualBox |
| Performance | Higher (direct hardware access) | Lower (OS overhead) |
| Also called | Native hypervisor | Hosted hypervisor |

### Cloud Service Model — "Who Manages What"

| Component | On-Prem | IaaS | PaaS | SaaS |
|-----------|---------|------|------|------|
| Applications | Customer | Customer | Customer | **Provider** |
| Data | Customer | Customer | Customer | **Provider** |
| Runtime | Customer | Customer | **Provider** | **Provider** |
| OS | Customer | Customer | **Provider** | **Provider** |
| Virtualization | Customer | **Provider** | **Provider** | **Provider** |
| Servers | Customer | **Provider** | **Provider** | **Provider** |
| Storage | Customer | **Provider** | **Provider** | **Provider** |
| Networking | Customer | **Provider** | **Provider** | **Provider** |

### Wi-Fi Band Comparison

| Feature | 2.4 GHz | 5 GHz |
|---------|---------|-------|
| Range | Longer | Shorter |
| Wall penetration | Better | Worse |
| Interference | More (crowded) | Less |
| Non-overlapping channels | 3 (1, 6, 11) | Many (all non-overlapping) |
| Channel width | 22 MHz | 20/40/80/160 MHz |

---

## SECTION 6: PRACTICE QUIZ

**1.** A switch has DHCP snooping and DAI enabled on VLAN 10. An attacker on an untrusted port (fa0/5) sends a Gratuitous ARP claiming to be the default gateway (10.0.0.1) with the attacker's MAC. The DHCP snooping binding table has no entry for the attacker's MAC/IP. What happens?

- A) The ARP message is forwarded because GARP messages are always allowed
- B) The ARP message is discarded because the sender MAC/IP does not match any entry in the DHCP snooping binding table
- C) The ARP message is forwarded but the switch generates a syslog alert
- D) The switch err-disables port fa0/5 immediately

**Answer: B** — DAI checks the sender MAC and sender IP of ARP messages on untrusted ports against the **DHCP snooping binding table**. Since the attacker's MAC/IP combination has no matching entry, the ARP message is **discarded**. The port is not immediately err-disabled unless the rate limit is exceeded.

---

**2.** A network architect is designing a campus LAN with 5 distribution layer switches across 3 buildings. Which LAN design does Cisco recommend?

- A) Two-tier (collapsed core) design
- B) Three-tier design with a dedicated core layer
- C) Spine-leaf architecture
- D) SOHO design with all-in-one devices

**Answer: B** — Cisco recommends adding a **core layer** when there are more than **3 distribution layer switches** in a single location. With 5 distribution switches, a three-tier design provides fast transport between distribution layers and maintains connectivity even if devices fail.

---

**3.** In a spine-leaf data center architecture, Server A is connected to Leaf 1 and Server B is connected to Leaf 3. How many hops does traffic between them traverse?

- A) 1 hop (leaf-to-leaf directly)
- B) 2 hops (leaf → spine → leaf)
- C) 3 hops (leaf → spine → core → leaf)
- D) Variable depending on network load

**Answer: B** — In spine-leaf architecture, traffic between servers on different leaf switches always traverses exactly **2 hops**: source leaf → one spine switch → destination leaf. Leaf switches never connect directly to other leaf switches. This ensures **consistent latency**.

---

**4.** A company uses MPLS Layer 3 VPN to connect Office A and Office B. Which statement is correct about the CE and PE router relationship?

- A) CE routers use MPLS labels to forward traffic across the service provider network
- B) CE and PE routers form routing protocol peerings (e.g., OSPF); CE learns remote routes through PE
- C) The service provider network is transparent; CE routers peer directly with each other
- D) PE routers are owned and managed by the customer

**Answer: B** — In a **Layer 3 MPLS VPN**, CE and PE routers form routing protocol peerings (e.g., OSPF). The CE router learns about remote site routes through the PE router. In a **Layer 2** MPLS VPN, the SP network is transparent and CEs peer directly — but that's not what this question describes.

---

**5.** An engineer needs to run OSPF between two sites connected over the Internet via VPN. Standard IPsec tunnels are currently configured. What is the problem and the recommended solution?

- A) IPsec does not support encryption; use TLS instead
- B) IPsec only supports unicast; use GRE over IPsec to support OSPF multicast
- C) OSPF cannot run over any VPN tunnel; use static routes instead
- D) IPsec tunnels are too slow for OSPF; upgrade to DMVPN

**Answer: B** — Standard IPsec only supports **unicast** traffic. OSPF relies on **multicast** (224.0.0.5 and 224.0.0.6) and cannot operate over pure IPsec tunnels. **GRE over IPsec** encapsulates traffic with GRE first (supporting broadcast/multicast), then encrypts with IPsec.

---

**6.** A data center runs 50 application servers across 10 physical servers using VMware ESXi. What type of hypervisor is ESXi, and where does it run?

- A) Type 2 hypervisor; runs on top of Windows Server
- B) Type 1 hypervisor; runs directly on the server hardware (bare-metal)
- C) Type 1 hypervisor; runs inside a container on the server
- D) Type 2 hypervisor; runs as a program on Linux

**Answer: B** — VMware ESXi is a **Type 1 (bare-metal/native)** hypervisor that runs **directly on the server hardware** without a host OS underneath. This is the standard for data center environments, providing direct hardware access for better performance.

---

**7.** An engineer configures `ip vrf forwarding CUSTOMER_A` on interface g0/0 which currently has IP 10.0.0.1/24. What happens immediately?

- A) The interface is added to the VRF and retains its IP address
- B) The interface is added to the VRF and its IP address is removed — it must be reconfigured
- C) The VRF is created automatically and the IP is preserved
- D) The command fails because the IP address must be removed first

**Answer: B** — Assigning an interface to a VRF with `ip vrf forwarding` **automatically removes the existing IP address**. The engineer must reconfigure the IP address after the VRF assignment. This is a common gotcha on the exam.

---

**8.** A wireless network uses three APs in an ESS deployment. Which statement is TRUE?

- A) All three APs share the same SSID and the same BSSID
- B) All three APs share the same SSID but each has a unique BSSID; they use different channels
- C) Each AP has a unique SSID and a unique BSSID
- D) The APs use the same channel to ensure seamless roaming

**Answer: B** — In an ESS, all APs share the **same SSID** so clients see one seamless network. Each AP has a **unique BSSID** (its radio MAC address) and uses a **different channel** to avoid interference. BSAs should overlap 10–15% to enable roaming.

---

**9.** Which cloud deployment model describes infrastructure reserved for a single organization but potentially hosted off-premises by a third-party provider?

- A) Public Cloud
- B) Community Cloud
- C) Private Cloud
- D) Hybrid Cloud

**Answer: C** — A **Private Cloud** is infrastructure reserved for a single organization. It can be located **on or off premises** and may even be owned/operated by a third party (e.g., AWS GovCloud for the US DoD). The key distinction is that it serves only one organization.

---

**10.** An AP operates in repeater mode with a single radio. What is the primary disadvantage compared to an AP in normal BSS mode?

- A) The repeater cannot extend the signal range
- B) The repeater must operate on the same channel as the AP, reducing overall throughput
- C) The repeater requires a wired backhaul connection
- D) Clients cannot associate with the repeater

**Answer: B** — A single-radio repeater must operate on the **same channel** as the AP it extends. Since it receives and retransmits on the same channel, it effectively **halves the throughput** on that channel. A dual-radio repeater solves this by using different channels for receiving and retransmitting.
