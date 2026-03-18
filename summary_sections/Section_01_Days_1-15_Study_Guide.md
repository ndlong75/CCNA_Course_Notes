[< Back to All Sections](../README.md#section-study-guides)

# CCNA 200-301 Study Guide — Section 1: Days 1–15
### Jeremy's IT Lab | Videos 001–027

> **Scope:** Network Devices · Interfaces & Cables · OSI/TCP-IP Models · Cisco IOS CLI ·
> Ethernet LAN Switching · IPv4 Addressing · Switch Interfaces · IPv4 Header ·
> Routing Fundamentals · Static Routing · Life of a Packet · Subnetting (Parts 1–3) · VLSM

---

## Table of Contents

1. [Network Devices (Day 1)](#1-network-devices-day-1)
2. [Interfaces and Cables (Day 2)](#2-interfaces-and-cables-day-2)
3. [OSI Model and TCP/IP Suite (Day 3)](#3-osi-model-and-tcpip-suite-day-3)
4. [Cisco IOS CLI (Day 4)](#4-cisco-ios-cli-day-4)
5. [Ethernet LAN Switching (Days 5–6)](#5-ethernet-lan-switching-days-5-6)
6. [IPv4 Addressing (Days 7–8)](#6-ipv4-addressing-days-7-8)
7. [Switch Interfaces (Day 9)](#7-switch-interfaces-day-9)
8. [The IPv4 Header (Day 10)](#8-the-ipv4-header-day-10)
9. [Routing Fundamentals and Static Routing (Days 11–12)](#9-routing-fundamentals-and-static-routing-days-11-12)
10. [Life of a Packet (Day 12 continued)](#10-life-of-a-packet-day-12-continued)
11. [Subnetting Parts 1–3 and VLSM (Days 13–15)](#11-subnetting-parts-13-and-vlsm-days-13-15)
12. [Complete Command Reference](#12-complete-command-reference)
13. [Exam Quick-Reference Tables](#13-exam-quick-reference-tables)

---

## 1. Network Devices (Day 1)

### What Is a Network?

A computer network is a digital telecommunications network that allows **nodes** to share **resources**.

- **Client:** a device that accesses a service made available by a server.
- **Server:** a device that provides functions or services for clients.
- The same physical device can be both a client and a server simultaneously (e.g., peer-to-peer networks).

---

### Switches

- Operate at **Layer 2** (Data Link layer).
- Provide connectivity to hosts **within the same LAN** (Local Area Network).
- Have **many network interfaces/ports** — typically 24 or 48.
- **DO NOT** provide connectivity between separate LANs or over the Internet.
- Forward traffic based on **MAC addresses**.

---

### Routers

- Operate at **Layer 3** (Network layer).
- Used to provide connectivity **between LANs** and to send data over the Internet.
- Have **fewer interfaces** than switches (typically 2–8 on enterprise routers).
- Forward traffic based on **IP addresses**.
- Each interface connects to a different network/subnet.

> **Key distinction:** Switches connect hosts *within* a LAN. Routers connect *separate* LANs together.

---

### Firewalls

- Can operate at **Layers 3, 4, and 7**.
- Specialty hardware (or software) **network security devices**.
- Control network traffic **entering and exiting** your network based on configured rules.
- Can be placed **inside** or **outside** the network (or both — layered security).
- Monitor and control traffic based on configured **access rules/policies**.

**Hardware firewall examples:** Cisco ASA5500-X series, Cisco Firepower 2100 series.

**Next-Generation Firewalls (NGFW):**

- Include **IPS** (Intrusion Prevention System).
- Perform **deep packet inspection** — inspect application-layer data, not just port/IP.
- Can identify and block malicious traffic patterns, not just known bad IP/port combinations.
- Also called "application-aware" firewalls.

**Host-Based Firewalls:**

- Software applications running **on a PC or server**.
- Filter traffic **entering and exiting that specific host**.
- Separate and independent from a network firewall.
- Examples: Windows Defender Firewall, iptables (Linux).

---

### Hubs (Legacy — Layer 1)

- Operate at **Layer 1** (Physical layer).
- Simply **repeat** all received traffic out **every other port** (flooding).
- Create a **collision domain** — only one device can send at a time.
- No intelligence — cannot distinguish between frames.
- **Replaced by switches** in modern networks.

---

### Summary Table

| Device | Layer | Key Function | Identifier Used |
|--------|-------|--------------|-----------------|
| Hub | L1 | Repeats all traffic out all ports | None |
| Switch | L2 | Connects hosts in a LAN | MAC address |
| Router | L3 | Connects LANs / Internet routing | IP address |
| Firewall | L3/4/7 | Controls traffic by security rules | IP, port, application |

---

## 2. Interfaces and Cables (Day 2)

### What Is Ethernet?

Ethernet is a collection of **network protocols and standards** that define:

- Common communication standards over networks.
- Common hardware standards to allow connectivity between devices.

Standards are defined by **IEEE 802.3** (first standardised 1983).

**Speed is measured in bits per second (bps) — NOT bytes.**

| Unit | Bits |
|------|------|
| 1 Kilobit (Kb) | 1,000 |
| 1 Megabit (Mb) | 1,000,000 |
| 1 Gigabit (Gb) | 1,000,000,000 |
| 1 Terabit (Tb) | 1,000,000,000,000 |

---

### Copper Ethernet Standards (UTP)

UTP = **Unshielded Twisted Pair**

- 4 pairs (8 wires total), RJ-45 connector.
- Twisting protects against **EMI** (Electromagnetic Interference).
- Maximum distance: **100 meters**.
- No metallic shielding.

| Speed | Common Name | IEEE Standard | Cable Standard | Pairs Used |
|-------|-------------|---------------|----------------|------------|
| 10 Mbps | Ethernet | 802.3i | 10BASE-T | 2 pairs (pins 1,2 and 3,6) |
| 100 Mbps | Fast Ethernet | 802.3u | 100BASE-T | 2 pairs (pins 1,2 and 3,6) |
| 1 Gbps | Gigabit Ethernet | 802.3ab | 1000BASE-T | 4 pairs (bidirectional) |
| 10 Gbps | 10 Gigabit Ethernet | 802.3an | 10GBASE-T | 4 pairs (bidirectional) |

- **BASE** = Baseband Signaling (one signal on the wire at a time).
- **T** = Twisted Pair.

---

### Pin Assignments and Cable Types

**Transmit/Receive pin layout:**

| Device Type | Transmit (TX) Pins | Receive (RX) Pins |
|-------------|--------------------|-------------------|
| PC | 1, 2 | 3, 6 |
| Router | 1, 2 | 3, 6 |
| Firewall | 1, 2 | 3, 6 |
| Switch | 3, 6 | 1, 2 |

**Straight-Through Cable:**

- Pin 1 → Pin 1, Pin 2 → Pin 2, Pin 3 → Pin 3 ... (straight through, no crossover).
- Connects **DIFFERENT** device types: PC–Switch, Router–Switch, Firewall–Switch.
- Works because one end TXs on 1,2 and the other RXs on 1,2.

**Crossover Cable:**

- Pin 1 → Pin 3, Pin 2 → Pin 6, Pin 3 → Pin 1, Pin 6 → Pin 2.
- Connects **SAME** device types: Switch–Switch, Router–Router, PC–PC, PC–Router.
- Works because both devices TX on the same pins — crossover swaps them.

**Auto MDI-X:**

- Modern devices automatically **detect** which pins their neighbour is transmitting on and adjust accordingly.
- Eliminates the need to worry about straight-through vs. crossover for most modern connections.

**Rollover Cable (Console Cable):**

- Completely reversed: Pin 1 ↔ Pin 8, Pin 2 ↔ Pin 7, Pin 3 ↔ Pin 6, Pin 4 ↔ Pin 5.
- Used to **connect a PC to a Cisco device's console port** for out-of-band management.
- NOT used for network data traffic.

---

### Fiber Optic Connections

Fiber optic sends **light** over glass fibers instead of electrical signals over copper.

- Requires **SFP Transceiver** (Small Form-Factor Pluggable) to connect to switches/routers.
- Uses **separate cables** for Transmit (TX) and Receive (RX) — two fibers per connection.
- Immune to **EMI**.
- Does **NOT** emit signal outside the cable (more secure than UTP).

**Four physical parts of a fiber optic cable:**

1. Fiberglass core (carries light)
2. Cladding (reflects light back into core)
3. Buffer (protective coating)
4. Outer jacket

#### Single-Mode Fiber (SMF)

- **Narrow core** — light enters at a single angle (one "mode").
- Uses **laser-based** transmitter (more expensive).
- Supports **longer distances** — up to 10km or 30km depending on standard.
- **More expensive** than multimode.

#### Multimode Fiber (MMF)

- **Wider core** — allows multiple angles of light ("modes").
- Uses **LED-based** transmitter (cheaper).
- Supports **shorter distances** than single-mode (up to ~550m).
- **Less expensive** than single-mode.

#### Fiber Optic Standards

| Standard | IEEE | Speed | Mode | Max Distance |
|----------|------|-------|------|--------------|
| 1000BASE-LX | 802.3z | 1 Gbps | Multimode | 550 m |
| 1000BASE-LX | 802.3z | 1 Gbps | Single-mode | 5 km |
| 10GBASE-SR | 802.3ae | 10 Gbps | Multimode | 400 m |
| 10GBASE-LR | 802.3ae | 10 Gbps | Single-mode | 10 km |
| 10GBASE-ER | 802.3ae | 10 Gbps | Single-mode | 30 km |

---

### UTP vs. Fiber Optic Comparison

| Characteristic | UTP (Copper) | Fiber Optic |
|----------------|-------------|-------------|
| Cost | Lower | Higher |
| Max Distance | 100 m | Up to 30+ km |
| EMI Vulnerability | YES (susceptible) | NO (immune) |
| Signal Leakage | YES (security risk) | NO (secure) |
| Connector | RJ-45 (cheap) | SFP port (expensive) |
| Use Case | LAN (within building) | Long-haul, backbone, inter-building |

---

## 3. OSI Model and TCP/IP Suite (Day 3)

### Why Networking Standards Matter

Without standards, devices from different vendors could not communicate. Standards are defined by:

- **IEEE** (Institute of Electrical and Electronics Engineers) — hardware standards (e.g., 802.3 Ethernet, 802.11 Wi-Fi).
- **IETF** (Internet Engineering Task Force) — software/protocol standards via **RFCs** (e.g., TCP, IP, UDP, HTTP).

---

### The OSI Model (7 Layers)

The **Open Systems Interconnection** model — a conceptual framework. Not directly implemented but used as a reference.

| Layer # | Layer Name | PDU | Key Protocols/Functions |
|---------|------------|-----|-------------------------|
| 7 | Application | Data | HTTP, FTP, SSH, DNS, DHCP |
| 6 | Presentation | Data | Data translation, encryption, compression |
| 5 | Session | Data | Session management, dialog control |
| 4 | Transport | Segment (TCP) / Datagram (UDP) | Port numbers, reliability (TCP), speed (UDP) |
| 3 | Network | Packet | IP addressing, routing (IP, ICMP, OSPF) |
| 2 | Data Link | Frame | MAC addressing, hop-to-hop delivery (Ethernet, Wi-Fi) |
| 1 | Physical | Bit | Physical transmission (cables, signals, voltage) |

**Mnemonic (top-down):** "All People Seem To Need Data Processing"
**Mnemonic (bottom-up):** "Please Do Not Throw Sausage Pizza Away"

---

### The TCP/IP Model (5 Layers — used in practice)

| Layer # | Name | OSI Equivalent | Key Function |
|---------|------|----------------|--------------|
| 5 | Application | OSI L5–L7 | HTTP, FTP, DNS, DHCP, SMTP |
| 4 | Transport | OSI L4 | TCP, UDP — port-to-port delivery |
| 3 | Network / Internet | OSI L3 | IP — end-to-end delivery |
| 2 | Data Link / Network Access | OSI L2 | Ethernet, Wi-Fi — hop-to-hop delivery |
| 1 | Physical | OSI L1 | Cables, signals, bits |

> **Exam tip:** The CCNA commonly references both models. Know that TCP/IP is what is actually used. OSI is the reference model for troubleshooting and terminology.

---

### Encapsulation and Decapsulation

**Encapsulation** (sender — data travels DOWN the stack):

1. Application layer creates **data**.
2. Transport layer adds **L4 header** (port numbers) → becomes **Segment** (TCP) or **Datagram** (UDP).
3. Network layer adds **L3 header** (IP addresses) → becomes **Packet**.
4. Data Link layer adds **L2 header** (MAC addresses) AND **L2 trailer** (FCS) → becomes **Frame**.
5. Physical layer converts to **Bits** and transmits.

**Decapsulation** (receiver — data travels UP the stack):

- Each layer **strips** its corresponding header/trailer and passes the payload up.

> **Important:** Layer 2 is the ONLY layer that adds BOTH a header AND a trailer (the FCS at the end).

---

### Key Addressing Per Layer

| Layer | Address Type | Scope | Purpose |
|-------|-------------|-------|---------|
| L2 Data Link | MAC address (48-bit) | Hop-to-hop (one link at a time) | Identify device on local network segment |
| L3 Network | IP address (32-bit IPv4) | End-to-end (source to destination) | Route packets across networks |
| L4 Transport | Port number (16-bit) | Process-to-process | Identify which application/process |

---

### Same-Layer vs. Adjacent-Layer Interaction

- **Adjacent-layer interaction:** Layers on the **same device** work together (e.g., L3 passes packet to L2 for framing).
- **Same-layer interaction:** The same layer on **different devices** communicate **logically** (e.g., TCP on PC1 "talks to" TCP on PC2, even though physically the data passes through many devices).

---

### Switches vs. Routers in the OSI Model

- **Switches** operate at **Layer 2** — they read frames, use MAC addresses, but do NOT count as network hops.
- **Routers** operate at **Layer 3** — they read packets, use IP addresses, and count as **hops** (each router decrements TTL).

---

### Common Port Numbers (Layer 4)

| Port | Protocol | Application |
|------|----------|-------------|
| 20 | TCP | FTP (data) |
| 21 | TCP | FTP (control) |
| 22 | TCP | SSH |
| 23 | TCP | Telnet |
| 25 | TCP | SMTP (email) |
| 53 | TCP/UDP | DNS |
| 67/68 | UDP | DHCP |
| 80 | TCP | HTTP |
| 110 | TCP | POP3 (email) |
| 443 | TCP | HTTPS |

---

## 4. Cisco IOS CLI (Day 4)

### What Is Cisco IOS?

- **IOS** = Internetwork Operating System — the OS running on **Cisco routers and switches**.
- Completely unrelated to Apple iOS.
- Network engineers primarily use the **CLI** (Command Line Interface), not a GUI.

---

### Connecting via Console

1. Use an **RJ-45 rollover cable** from the device's Console port.
2. Connect to a **DB-9** serial port on your PC (or use a USB-to-serial adapter).
3. Open a **terminal emulator** (e.g., **PuTTY** from putty.org).
4. Select **Serial** connection type with these settings:
   - Speed: **9600 baud**
   - Data bits: **8**
   - Stop bits: **1**
   - Parity: **None**
   - Flow control: **None**

---

### IOS CLI Modes

```
Router>              ← User EXEC mode (view only, very limited)
Router#              ← Privileged EXEC mode (full view access)
Router(config)#      ← Global Configuration mode (make changes)
Router(config-if)#   ← Interface Configuration mode
Router(config-line)# ← Line Configuration mode
```

**Entering modes:**

```
Router> enable                  → enters Privileged EXEC
Router# configure terminal      → enters Global Config (shortcut: conf t)
Router(config)# interface g0/0  → enters Interface Config (shortcut: int g0/0)
```

**Exiting modes:**

```
exit     → go back ONE level
end      → jump directly back to Privileged EXEC from anywhere
Ctrl+Z   → same as 'end'
```

---

### CLI Navigation Tips

- **`?`** — shows all available commands at the current mode, or completes a partial command.
- **Tab key** — auto-completes a command (as long as the partial input is unambiguous).
- **Shortcuts:** Commands can be abbreviated as long as they are unambiguous:
  - `en` = `enable`
  - `conf t` = `configure terminal`
  - `sh run` = `show running-config`
  - `sh ip int br` = `show ip interface brief`
- **`do <command>`** — run Privileged EXEC commands from within any config mode (e.g., `do show run`).
- **`no <command>`** — removes/negates a configuration (e.g., `no shutdown`).

---

### Password Security

**Enable Password (weak — avoid in production):**

```
Router(config)# enable password CCNA
```

- Protects entry into Privileged EXEC mode.
- Stored as **plain text** in the running config (insecure).
- Can be encrypted with `service password-encryption` → Type 7 (weak, easily cracked).

**Enable Secret (preferred):**

```
Router(config)# enable secret Cisco
```

- Stored as **MD5 hash** (Type 5) in the config — always encrypted.
- **Takes priority** over `enable password` if both are configured.
- Cannot be recovered, only reset.

**Service Password Encryption:**

```
Router(config)# service password-encryption
```

- Encrypts ALL plain-text passwords in the config with **Type 7** encryption.
- Type 7 is weak — free online tools can decrypt it.
- Does NOT affect `enable secret` (already encrypted with MD5).
- If removed with `no service password-encryption`, previously encrypted passwords **remain** encrypted.

> **Rule:** If both `enable password` and `enable secret` are configured, the **`enable secret` ALWAYS wins**. The `enable password` is completely ignored.

---

### Configuration Files

| File | Location | Description |
|------|----------|-------------|
| Running-config | RAM | Currently active configuration. Lost on reload if not saved. |
| Startup-config | NVRAM | Loaded on boot. Persists through power cycles. |

**Saving the running config (three equivalent methods):**

```
Router# write
Router# write memory
Router# copy running-config startup-config
```

**Viewing configs:**

```
Router# show running-config
Router# show startup-config
```

> **Important:** If you make changes and do NOT save, they are lost when the device reloads. Always save after making changes.

---

### Basic Device Configuration

```
Router(config)# hostname R1                     ← set device name
Router(config)# enable password CCNA            ← set enable password (plain-text)
Router(config)# enable secret Cisco             ← set enable secret (MD5 hash)
Router(config)# service password-encryption     ← encrypt all plain-text passwords
Router(config)# no service password-encryption  ← disable (existing encrypted stay encrypted)
```

---

## 5. Ethernet LAN Switching (Days 5–6)

### Ethernet Frame Structure

A complete Ethernet frame (with Preamble/SFD):

```
| Preamble | SFD | Destination MAC | Source MAC | Type/Length | Payload | FCS |
|  7 bytes | 1B  |    6 bytes      |  6 bytes   |   2 bytes   |46-1500B | 4B  |
```

**Field details:**

| Field | Size | Description |
|-------|------|-------------|
| Preamble | 7 bytes | Alternating 10101010 pattern — clock synchronization |
| SFD (Start Frame Delimiter) | 1 byte | 10101011 — marks end of preamble, start of frame |
| Destination MAC | 6 bytes | MAC address of intended recipient |
| Source MAC | 6 bytes | MAC address of sender |
| Type / Length | 2 bytes | ≥ 1536 (0x0600) = EtherType (0x0800=IPv4, 0x86DD=IPv6); < 1500 = Length |
| Payload / Data | 46–1500 bytes | Encapsulated data (minimum 46 bytes — padding added if needed) |
| FCS (Frame Check Sequence) | 4 bytes | CRC error detection — in the **trailer** |

> **Note on Preamble/SFD:** These are often NOT counted as part of the Ethernet "header" in many references, including CCNA materials. When the exam says "Ethernet header," it usually means the 14-byte portion: Dst MAC + Src MAC + Type/Length.

**Size calculations:**

- Ethernet header (no Preamble/SFD) = 6 + 6 + 2 = **14 bytes**
- Ethernet trailer (FCS) = **4 bytes**
- Minimum payload = **46 bytes** (zeros padded if actual data < 46 bytes)
- Minimum frame size = 14 + 46 + 4 = **64 bytes** (not counting Preamble/SFD)
- Maximum payload = **1500 bytes** (MTU — Maximum Transmission Unit)

---

### MAC Addresses

- **48 bits** long — represented as **12 hexadecimal characters**.
- Also called **BIA** (Burned-In Address) — permanently assigned by manufacturer (burned into ROM).
- Written in multiple formats:
  - `AA:BB:CC:DD:EE:FF` (Linux/macOS style)
  - `AABB.CCDD.EEFF` (Cisco style)
  - `AA-BB-CC-DD-EE-FF` (Windows style)

**MAC Address Structure:**

```
OUI (3 bytes / 24 bits)         |  Device Identifier (3 bytes / 24 bits)
Organizationally Unique Identifier  Unique to this specific device
(Identifies manufacturer)
```

- OUI is assigned by **IEEE** to manufacturers (e.g., Cisco has multiple OUIs).
- Globally unique (for factory-assigned addresses).
- **Locally administered** MACs can override the BIA (used in virtualization, security testing).

---

### Hexadecimal Refresher

| Decimal | Binary | Hex |
|---------|--------|-----|
| 0 | 0000 | 0 |
| 1 | 0001 | 1 |
| 5 | 0101 | 5 |
| 9 | 1001 | 9 |
| 10 | 1010 | A |
| 11 | 1011 | B |
| 12 | 1100 | C |
| 13 | 1101 | D |
| 14 | 1110 | E |
| 15 | 1111 | F |

Each hex digit represents exactly **4 bits** (one nibble).

---

### Switch MAC Address Learning and Forwarding

**How a switch builds its MAC address table:**

1. A frame arrives on a switch port.
2. Switch reads the **SOURCE MAC address** → records it in the **MAC address table** with the incoming interface.
3. Switch checks the **DESTINATION MAC address**:
   - **Unknown** (not in table) → **Unknown Unicast Flood** — frame is sent out ALL ports EXCEPT the incoming port.
   - **Known** (in table) → **Known Unicast Forward** — frame is sent out ONLY the matching port.

**MAC address table aging:**

- Dynamic MAC entries **age out after 5 minutes** (Cisco default) if no frames are received from that MAC.
- `clear mac address-table dynamic` — manually clears all dynamic entries.

**Broadcast frames:**

- Destination MAC = `FF:FF:FF:FF:FF:FF`.
- Always **flooded** out all ports except the incoming port (like an unknown unicast).
- Switches cannot "learn" where to send broadcasts selectively — by definition they go everywhere.

> **Key rule:** Switches use **SOURCE MAC** to *learn* (build the table). Switches use **DESTINATION MAC** to *forward* (decide where to send).

---

### Useful Switch Verification Commands

```
Switch# show mac address-table
Switch# show mac address-table dynamic
Switch# clear mac address-table dynamic
Switch# show interfaces
Switch# show ip interface brief
```

---

### ARP — Address Resolution Protocol

Purpose: resolve a **known IP address** to an **unknown MAC address**.

**Why ARP is needed:**

- When PC1 wants to send data to PC2, it knows PC2's IP address.
- But to create a frame, PC1 needs PC2's **MAC address**.
- ARP bridges this gap.

**ARP Process:**

1. **ARP Request** (broadcast):
   - Sent to `FF:FF:FF:FF:FF:FF` (all devices on the LAN receive it).
   - Message: *"Who has IP 192.168.1.2? Tell 192.168.1.1"*
   - Contains sender's IP and MAC, target IP, target MAC = 00:00:00:00:00:00 (unknown).

2. **ARP Reply** (unicast):
   - Only the device with the matching IP responds.
   - Sent directly to the requester's MAC address.
   - Message: *"192.168.1.2 is at MAC AA:BB:CC:DD:EE:FF"*

3. **ARP Table:**
   - Each device maintains an ARP table (IP → MAC mapping).
   - Entries age out after a timeout period.
   - View with: `arp -a` (Windows) or `arp -n` (Linux).

> **Layer note:** ARP is technically a Layer 3 protocol (resolves L3 addresses) but uses Layer 2 broadcasts (Ethernet). It is sometimes called a "Layer 2.5" protocol.

---

## 6. IPv4 Addressing (Days 7–8)

### Binary and Dotted Decimal

- IPv4 address = **32 bits** = **4 octets** (groups of 8 bits).
- Written in **dotted decimal** notation: `192.168.1.100`.
- Each octet ranges from **0 to 255**.

**Bit values per octet (left to right):**

```
Bit position:  8    7    6    5    4    3    2    1
Bit value:    128   64   32   16   8    4    2    1
```

**Binary to Decimal conversion:**

Add up the values of all positions where the bit = 1.

```
Example: 1100 1010
= 128 + 64 + 0 + 0 + 8 + 0 + 2 + 0 = 202
```

**Decimal to Binary conversion:**

Work left to right — subtract the largest bit value that fits, write 1; if it does not fit, write 0.

```
Example: 173
173 ≥ 128? YES → 1, remainder 45
45 ≥ 64?  NO  → 0
45 ≥ 32?  YES → 1, remainder 13
13 ≥ 16?  NO  → 0
13 ≥ 8?   YES → 1, remainder 5
5 ≥ 4?    YES → 1, remainder 1
1 ≥ 2?    NO  → 0
1 ≥ 1?    YES → 1
Result: 1010 1101
```

---

### IPv4 Address Classes

| Class | First Octet Range | Default Prefix Length | Leading Bits | Network Bits | Host Bits |
|-------|------------------|-----------------------|--------------|--------------|-----------|
| A | 1–126 | /8 | 0xxxxxxx | 8 | 24 |
| B | 128–191 | /16 | 10xxxxxx | 16 | 16 |
| C | 192–223 | /24 | 110xxxxx | 24 | 8 |
| D | 224–239 | N/A | Multicast | — | — |
| E | 240–255 | N/A | Experimental | — | — |

> **Special address: 127.0.0.0/8 (Loopback)** — the entire 127.x.x.x range is reserved for loopback. `127.0.0.1` is the standard loopback address used to test a device's TCP/IP stack. NOT assignable to hosts.

---

### Private IPv4 Address Ranges (RFC 1918)

| Range | Class | CIDR |
|-------|-------|------|
| 10.0.0.0 – 10.255.255.255 | A | 10.0.0.0/8 |
| 172.16.0.0 – 172.31.255.255 | B | 172.16.0.0/12 |
| 192.168.0.0 – 192.168.255.255 | C | 192.168.0.0/16 |

- Private addresses are **NOT routed on the Internet**.
- Used internally in organisations.
- Require **NAT** (Network Address Translation) to communicate with the Internet.

---

### Network Address, Broadcast Address, and Usable Hosts

Every subnet has three special addresses:

| Address | Host Bits | Assignable? | Purpose |
|---------|-----------|-------------|---------|
| **Network address** | All 0s | NO | Identifies the network/subnet itself |
| **Broadcast address** | All 1s | NO | Sends to all hosts on the subnet |
| **Usable host range** | Anything else | YES | Assigned to devices |

**Formulas:**

```
Number of host addresses = 2^n
Usable hosts = 2^n - 2   (subtract network and broadcast)
where n = number of host bits
```

**Example — 192.168.1.0/24:**

```
Network address:  192.168.1.0   (host bits = 00000000)
First usable:     192.168.1.1
Last usable:      192.168.1.254
Broadcast:        192.168.1.255 (host bits = 11111111)
Usable hosts: 2^8 - 2 = 254
```

---

### Subnet Masks

A subnet mask tells you which bits are **network bits** (1s) and which are **host bits** (0s).

| CIDR Notation | Dotted Decimal Mask | Binary |
|---------------|--------------------|----|
| /8 | 255.0.0.0 | 11111111.00000000.00000000.00000000 |
| /16 | 255.255.0.0 | 11111111.11111111.00000000.00000000 |
| /24 | 255.255.255.0 | 11111111.11111111.11111111.00000000 |
| /25 | 255.255.255.128 | 11111111.11111111.11111111.10000000 |
| /26 | 255.255.255.192 | 11111111.11111111.11111111.11000000 |
| /30 | 255.255.255.252 | 11111111.11111111.11111111.11111100 |

> **Cisco IOS requires dotted decimal subnet masks.** CIDR slash notation (/24) is used in documentation and study but IOS commands require `255.255.255.0` format (when configuring interfaces).

---

### IP Interface Configuration

```
Router(config)# interface GigabitEthernet0/0
Router(config-if)# ip address 192.168.1.1 255.255.255.0
Router(config-if)# no shutdown
```

**Verification:**

```
Router# show ip interface brief
Router# show interfaces GigabitEthernet0/0
```

---

## 7. Switch Interfaces (Day 9)

### Interface Speed and Duplex

**Speed:**

- Switch interfaces support multiple speeds: **10 / 100 / 1000 Mbps** (or higher).
- Speed is **auto-negotiated** by default — devices agree on the highest common speed.
- Can be manually set: `speed 100` (in interface config mode).

**Duplex:**

| Mode | Description | Where Used |
|------|-------------|------------|
| Half-duplex | One direction at a time (send OR receive) | Hubs, legacy devices |
| Full-duplex | Both directions simultaneously | Modern switches and end devices |

- Full-duplex is used on **all modern switch-to-device connections**.
- Manually set with: `duplex full` (in interface config mode).

**Duplex Mismatch:**

- One side set to full-duplex, other side set to half-duplex.
- Results in: **collisions, late collisions, poor performance, CRC errors**.
- Common cause: manually setting one side while leaving the other on auto-negotiate.
- Both sides should be **either both auto, or both manually set to the same value**.

---

### Auto MDI/MDIX

- Automatically detects the cable type and adjusts pin assignment accordingly.
- Eliminates the need for crossover cables on modern equipment.
- Enabled by default on Cisco switches.

---

### Useful Show Commands for Interfaces

```
Switch# show interfaces status
Switch# show interfaces
Switch# show ip interface brief
```

**`show interfaces status` output columns:**

| Column | Meaning |
|--------|---------|
| Port | Interface name |
| Name | Description (if configured) |
| Status | connected / notconnect / disabled |
| Vlan | VLAN assigned to port |
| Duplex | a-full (auto-negotiated full) or half/full |
| Speed | a-100 (auto-negotiated 100Mbps) or manual speed |
| Type | Physical media type (e.g., 10/100/1000BaseTX) |

---

## 8. The IPv4 Header (Day 10)

The IPv4 header is **20 bytes minimum** (without options). Maximum with options: 60 bytes.

### IPv4 Header Fields

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|  IHL  |   DSCP  | ECN |          Total Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Identification        |Flags|     Fragment Offset     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Time to Live |    Protocol   |       Header Checksum         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                         Source IP Address                     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      Destination IP Address                   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options (if IHL > 5)                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

| Field | Size | Value/Notes |
|-------|------|-------------|
| **Version** | 4 bits | Always **4** for IPv4 (6 for IPv6) |
| **IHL** (Internet Header Length) | 4 bits | Header length in **32-bit words**. Min = 5 (= 20 bytes). Max = 15 (= 60 bytes). |
| **DSCP** (Differentiated Services Code Point) | 6 bits | **QoS** marking — used for traffic prioritisation |
| **ECN** (Explicit Congestion Notification) | 2 bits | End-to-end congestion notification without dropping packets |
| **Total Length** | 16 bits | Total packet size (header + data) in bytes. Max = **65,535 bytes** |
| **Identification** | 16 bits | Identifies which fragments belong to the same original packet |
| **Flags** | 3 bits | Bit 0: Reserved (0). Bit 1: **DF** (Don't Fragment). Bit 2: **MF** (More Fragments) |
| **Fragment Offset** | 13 bits | Position of this fragment in the original unfragmented packet |
| **TTL** (Time to Live) | 8 bits | Decremented by **1 at each router**. Packet dropped when TTL = 0. Prevents loops. |
| **Protocol** | 8 bits | Identifies upper-layer protocol: **6**=TCP, **17**=UDP, **1**=ICMP, **89**=OSPF |
| **Header Checksum** | 16 bits | Error-checking for the header **only** (not the data payload) |
| **Source IP** | 32 bits | Sender's IP address |
| **Destination IP** | 32 bits | Receiver's IP address |
| **Options** | 0–40 bytes | Variable length; present only if IHL > 5 |

---

### Key IPv4 Header Facts for the Exam

- **TTL:** Windows default = 128; Linux/macOS default = 64; Cisco IOS default = 255.
- **TTL purpose:** Prevents packets from looping forever. Each router (L3 hop) decrements TTL by 1. When TTL reaches 0, the router drops the packet and sends an **ICMP Time Exceeded** message back to the source.
- **Protocol field** is how the router/receiving device knows which upper-layer protocol to hand the payload to.
- **Fragmentation:** If a packet is too large for a link's MTU, it can be fragmented (unless DF bit is set). Reassembly happens at the destination, not intermediate routers.
- **Header Checksum:** Recalculated at every router (because TTL changes each hop).

---

## 9. Routing Fundamentals and Static Routing (Days 11–12)

### What Is Routing?

Routing is the **process routers use to determine the path** that IP packets should take to reach their destination.

- Routers forward packets between **different networks/subnets**.
- Switches forward frames **within a single network/subnet**.
- A router must have a **route** to the destination network, or the packet is **dropped** (unlike switches, which flood unknown destinations).

---

### The Routing Table

Each router maintains a **routing table** — a database of known networks and how to reach them.

```
Router# show ip route
```

**Routing table route codes:**

| Code | Meaning | Administrative Distance |
|------|---------|------------------------|
| **C** | Connected (interface configured + up/up) | 0 |
| **L** | Local (the router's own interface IP, /32) | 0 |
| **S** | Static (manually configured) | 1 |
| **O** | OSPF (learned via OSPF protocol) | 110 |
| **R** | RIP (learned via RIP protocol) | 120 |
| **D** | EIGRP (learned via EIGRP protocol) | 90 |
| **\*** | Candidate default route | — |

**Connected (C) and Local (L) routes:**

- Added **automatically** when you configure an IP address on an interface AND the interface is **up/up** (`no shutdown`).
- **C route:** the network the interface belongs to (uses the actual prefix length, e.g., /24).
- **L route:** the exact IP address configured on the interface — always with a **/32** mask.

```
Example:
C   192.168.1.0/24 is directly connected, GigabitEthernet0/0
L   192.168.1.1/32 is directly connected, GigabitEthernet0/0
```

---

### Administrative Distance (AD)

AD is the **trustworthiness** of a routing source. Lower AD = more trusted = preferred.

| Source | AD |
|--------|----|
| Connected | 0 |
| Static | 1 |
| EIGRP summary | 5 |
| External BGP | 20 |
| EIGRP | 90 |
| IGRP | 100 |
| OSPF | 110 |
| IS-IS | 115 |
| RIP | 120 |
| External EIGRP | 170 |
| Internal BGP | 200 |
| Unknown/Unreachable | 255 |

> **AD is used to choose between routes to the same destination learned from DIFFERENT sources.** If two routing protocols both know a route to 192.168.1.0/24, the one with the lower AD wins.

---

### Longest Prefix Match

When multiple routes match a destination IP, the router always picks the **most specific route** (longest prefix length).

```
Routing table contains:
192.168.1.0/24   via 10.0.0.1
192.168.1.64/26  via 10.0.0.2
0.0.0.0/0        via 10.0.0.3

Packet destination: 192.168.1.100

Match 1: 192.168.1.0/24    (/24 — matches)
Match 2: 192.168.1.64/26   (/26 — also matches: 192.168.1.64–192.168.1.127 includes .100)
Match 3: 0.0.0.0/0         (matches everything)

Router picks: 192.168.1.64/26 (longest prefix = most specific)
```

**Prefix length hierarchy: /32 > /30 > /24 > /16 > /8 > /0**

---

### Static Routes

Manually configured by a network administrator. Useful for:

- Small networks.
- Stub networks (networks with only one exit path).
- Providing a backup route (floating static route).

**Configuration syntax:**

```
ip route <destination-network> <subnet-mask> <next-hop-IP>
ip route <destination-network> <subnet-mask> <exit-interface>
ip route <destination-network> <subnet-mask> <exit-interface> <next-hop-IP>
```

**Examples:**

```
R1(config)# ip route 192.168.3.0 255.255.255.0 192.168.12.2
R1(config)# ip route 192.168.3.0 255.255.255.0 GigabitEthernet0/1
R1(config)# ip route 192.168.3.0 255.255.255.0 GigabitEthernet0/1 192.168.12.2
```

> **Recommendation:** Use next-hop IP (not just exit interface) for Ethernet interfaces. For point-to-point serial links, exit interface alone is sufficient.

---

### Default Route (Gateway of Last Resort)

A **catch-all** route that matches any destination not matched by a more specific route.

```
Router(config)# ip route 0.0.0.0 0.0.0.0 <next-hop-IP>
```

- Appears in the routing table as: `S*  0.0.0.0/0`
- Also called the **"gateway of last resort"**.
- Typically configured on routers connecting to the Internet (points toward the ISP).
- Hosts also have a default gateway (their router's IP) — same concept, different level.

---

### Floating Static Routes (Backup Routes)

A static route with a **higher AD than the primary route**, so it only activates if the primary fails.

```
R1(config)# ip route 192.168.3.0 255.255.255.0 10.0.0.1 1    ← primary (AD=1)
R1(config)# ip route 192.168.3.0 255.255.255.0 10.0.0.2 5    ← floating backup (AD=5)
```

- The backup route with AD=5 stays in the routing table but is **NOT preferred** as long as the AD=1 route is present.
- If the primary route disappears (link down), the backup "floats" into use.

---

### Removing Static Routes

```
Router(config)# no ip route 192.168.3.0 255.255.255.0 192.168.12.2
```

---

### Verification Commands

```
Router# show ip route
Router# show ip route static
Router# show ip route connected
Router# ping 192.168.3.1
```

---

## 10. Life of a Packet (Day 12 continued)

### End-to-End Packet Journey

**Scenario:** PC1 (192.168.1.1) sends a packet to PC4 (192.168.4.1) through R1 and R2.

**Step 1 — PC1 determines if destination is local or remote:**

- PC1 compares destination IP to its own subnet using its subnet mask.
- 192.168.4.1 is NOT in 192.168.1.0/24 → **different network** → must go to default gateway.

**Step 2 — PC1 resolves default gateway's MAC via ARP:**

- PC1 checks its ARP table for R1's interface IP (e.g., 192.168.1.254).
- If not found → PC1 sends ARP broadcast → R1 replies with its MAC.

**Step 3 — PC1 creates the frame:**

```
Layer 3 (Packet):  Src IP = 192.168.1.1  |  Dst IP = 192.168.4.1
Layer 2 (Frame):   Src MAC = PC1's MAC   |  Dst MAC = R1's MAC
```

**Step 4 — R1 receives and processes:**

- R1 receives the frame on its G0/0 interface.
- R1 **de-encapsulates** the L2 frame (removes the Ethernet header/trailer).
- R1 reads the L3 packet — destination IP = 192.168.4.1.
- R1 checks its routing table → longest prefix match → next hop = R2.
- R1 checks ARP table for R2's IP → if needed, sends ARP request.

**Step 5 — R1 creates a NEW frame for the next hop:**

```
Layer 3 (Packet):  Src IP = 192.168.1.1  |  Dst IP = 192.168.4.1  ← UNCHANGED
Layer 2 (Frame):   Src MAC = R1's G0/1 MAC | Dst MAC = R2's MAC   ← NEW
```

**Step 6 — R2 receives and processes (same as Step 4):**

- R2 de-encapsulates, reads destination IP.
- R2's routing table: 192.168.4.0/24 is directly connected on G0/1.
- R2 checks ARP for PC4's MAC → creates final frame.

**Step 7 — PC4 receives the frame:**

- PC4 de-encapsulates all layers and passes data to the application.

---

### The Critical Rule

> **IP addresses (Layer 3) REMAIN THE SAME** from source to destination across the entire path.
>
> **MAC addresses (Layer 2) CHANGE at every router hop** — each router creates a brand-new L2 header for the next link.

This is the fundamental concept behind the separation of Layer 2 and Layer 3 addressing.

---

### Summary of Address Changes

| Hop | Src IP | Dst IP | Src MAC | Dst MAC |
|-----|--------|--------|---------|---------|
| PC1 → R1 | PC1's IP | PC4's IP | PC1's MAC | R1 G0/0 MAC |
| R1 → R2 | PC1's IP | PC4's IP | R1 G0/1 MAC | R2 G0/0 MAC |
| R2 → PC4 | PC1's IP | PC4's IP | R2 G0/1 MAC | PC4's MAC |

---

## 11. Subnetting Parts 1–3 and VLSM (Days 13–15)

### Why Subnetting? The Problem with Classful Addressing

Before CIDR (Classless Inter-Domain Routing), the Internet used **classful** addressing:

- A company needing 5,000 addresses would receive a **Class B** (/16 = 65,534 hosts).
- 60,000+ addresses were **wasted** — not usable by anyone else.

**CIDR** (introduced by IETF in 1993) solved this by allowing any prefix length — not just /8, /16, /24.

---

### Subnetting Fundamentals

**What subnetting does:**

- Takes a larger network and **divides it into smaller subnetworks** (subnets).
- "Borrows" bits from the host portion and adds them to the network portion.

**Key formulas:**

```
Number of subnets = 2^x
  where x = number of borrowed bits (bits moved from host to network)

Hosts per subnet = 2^n - 2
  where n = remaining host bits
  (subtract 2 for network address and broadcast address)
```

---

### Subnetting a /24 Network

Starting with a Class C /24 (e.g., 192.168.1.0/24), borrowing bits from the last octet:

| New Prefix | Mask | Subnets | Hosts/Subnet | Block Size |
|------------|------|---------|--------------|------------|
| /24 | 255.255.255.0 | 1 | 254 | 256 |
| /25 | 255.255.255.128 | 2 | 126 | 128 |
| /26 | 255.255.255.192 | 4 | 62 | 64 |
| /27 | 255.255.255.224 | 8 | 30 | 32 |
| /28 | 255.255.255.240 | 16 | 14 | 16 |
| /29 | 255.255.255.248 | 32 | 6 | 8 |
| /30 | 255.255.255.252 | 64 | 2 | 4 |
| /31 | 255.255.255.254 | 128 | 2* | 2 |
| /32 | 255.255.255.255 | 256 | 1** | 1 |

**/31:** Only 2 addresses — no traditional network/broadcast (RFC 3021). Used for **point-to-point links** between routers.
**/32:** Identifies a **single specific host**. Used in routing tables (local routes, loopback interfaces).

---

### The "Magic Number" Method

The fastest way to find subnet boundaries without converting to binary.

**Rule:** The **block size** (subnet increment) = **256 minus the subnet mask value** of the interesting octet.

```
/26 mask = 255.255.255.192
Interesting octet (4th) mask value = 192
Block size = 256 - 192 = 64

Subnets for 192.168.1.0/26:
Subnet 1: 192.168.1.0   → 192.168.1.63  (broadcast)
Subnet 2: 192.168.1.64  → 192.168.1.127 (broadcast)
Subnet 3: 192.168.1.128 → 192.168.1.191 (broadcast)
Subnet 4: 192.168.1.192 → 192.168.1.255 (broadcast)
```

**Alternative "magic number" from bit value:**

The magic number = the value of the **last 1-bit in the network portion** of the mask.

```
/26 binary mask: 11111111.11111111.11111111.11000000
                                              ^ last network bit = 64 (2^6)
Block size = 64
```

---

### Finding Which Subnet an IP Belongs To

**Method:**

1. Identify the block size.
2. Count up in multiples of the block size until you **pass** the host IP.
3. The subnet **before** where you passed is the **network address**.
4. The next multiple **after** the network address minus 1 is the **broadcast address**.

**Example:** Find the subnet for 192.168.1.100/26

```
Block size = 64
Count: 0, 64, 128...
100 is between 64 and 128.

Network address:  192.168.1.64
Broadcast:        192.168.1.127
First usable:     192.168.1.65
Last usable:      192.168.1.126
```

---

### Subnetting Class B Networks (/16)

The same process applies, but the "interesting" octet may be the **3rd octet**.

**Example:** 172.16.0.0/20

```
Mask: 255.255.240.0
Interesting octet: 3rd
Block size: 256 - 240 = 16 (applied to 3rd octet)

Subnets:
172.16.0.0/20   → 172.16.15.255
172.16.16.0/20  → 172.16.31.255
172.16.32.0/20  → 172.16.47.255
... etc.

Subnets: 2^(20-16) = 2^4 = 16 subnets
Hosts: 2^12 - 2 = 4,094 per subnet
```

---

### Subnetting Class A Networks (/8)

**Example:** 10.0.0.0/18

```
Mask: 255.255.192.0
Interesting octet: 3rd
Block size: 256 - 192 = 64 (applied to 3rd octet)

Subnets: 2^(18-8) = 2^10 = 1,024 subnets
Hosts: 2^14 - 2 = 16,382 per subnet
```

---

### The Subnetting Cheat Sheet

| Group Size | 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |
|------------|-----|----|----|----|----|---|---|---|
| Last-octet mask | 128 | 192 | 224 | 240 | 248 | 252 | 254 | 255 |
| 4th Octet CIDR | /25 | /26 | /27 | /28 | /29 | /30 | /31 | /32 |
| 3rd Octet CIDR | /17 | /18 | /19 | /20 | /21 | /22 | /23 | /24 |
| 2nd Octet CIDR | /9 | /10 | /11 | /12 | /13 | /14 | /15 | /16 |
| 1st Octet CIDR | /1 | /2 | /3 | /4 | /5 | /6 | /7 | /8 |

**To use:**

1. Locate your CIDR in the table → read off the block size.
2. Find your "magic octet" (the one where the prefix boundary falls).
3. Count up in block-size increments until you pass the target IP.
4. The previous block start = Network; add block size - 1 for Broadcast.

---

### VLSM — Variable Length Subnet Masks

**VLSM** allows assigning **different prefix lengths** to different subnets within the same network — maximising address efficiency.

Without VLSM (Fixed Length Subnet Masks — FLSM): every subnet gets the same size.
With VLSM: each subnet is sized to fit its actual requirement.

**VLSM Process:**

1. List all subnets ordered by **size (largest first)**.
2. Assign the **largest** subnet first, starting at the beginning of the address space.
3. The **next subnet starts immediately after** the previous one ends.
4. Choose the **smallest prefix that still fits** all required hosts.
5. Continue until all subnets are assigned.

**Example — Assign from 192.168.1.0/24:**

Requirements:
- LAN A: 60 hosts
- LAN B: 30 hosts
- LAN C: 10 hosts
- WAN link: 2 hosts (point-to-point)

**Step 1 — Sort by size:** LAN A (60) → LAN B (30) → LAN C (10) → WAN (2)

**Step 2 — Assign:**

| Subnet | Hosts Needed | Prefix | Mask | Range | Usable Hosts |
|--------|-------------|--------|------|-------|--------------|
| LAN A | 60 | /26 | .192 | 192.168.1.0–.63 | 62 |
| LAN B | 30 | /27 | .224 | 192.168.1.64–.95 | 30 |
| LAN C | 10 | /28 | .240 | 192.168.1.96–.111 | 14 |
| WAN | 2 | /30 | .252 | 192.168.1.112–.115 | 2 |

> **Rule for choosing prefix:** Always use the **smallest prefix** (most hosts) that **still accommodates** the required number. For LAN A needing 60 hosts: /26 gives 62 (fits); /27 gives only 30 (does not fit).

**Remaining unused space:** 192.168.1.116–192.168.1.255 (140 addresses saved for future use).

---

### Subnetting Practice — Quick Method Summary

**Finding network address, broadcast, first/last usable:**

```
Given: 172.25.217.192/21

Step 1: /21 falls in 3rd octet (CIDR 17-24 = 3rd octet magic)
Step 2: Block size = 256 - 248 = 8 (mask value at /21 3rd octet position = 248)
Step 3: 3rd octet of IP = 217. Count in 8s: 208, 216, 224...
        217 is between 216 and 224 → network base = 216

Network:      172.25.216.0
Broadcast:    172.25.223.255
First usable: 172.25.216.1
Last usable:  172.25.223.254
Hosts: 2^11 - 2 = 2,046
```

---

## 12. Complete Command Reference

### CLI Navigation

| Command | Description |
|---------|-------------|
| `enable` | Enter Privileged EXEC mode from User EXEC |
| `disable` | Return to User EXEC from Privileged EXEC |
| `configure terminal` | Enter Global Configuration mode |
| `exit` | Exit current mode (go up one level) |
| `end` | Exit directly to Privileged EXEC from any mode |
| `Ctrl+Z` | Same as `end` |
| `do <command>` | Run privileged commands from config mode |
| `?` | Show available commands or completions |
| `Tab` | Auto-complete command |

---

### Basic Configuration

| Command | Description |
|---------|-------------|
| `hostname <name>` | Set device hostname |
| `enable password <password>` | Set plain-text enable password |
| `enable secret <password>` | Set MD5-hashed enable secret (preferred) |
| `service password-encryption` | Encrypt all plain-text passwords (Type 7) |
| `no service password-encryption` | Disable; previously encrypted passwords stay encrypted |
| `no <command>` | Remove/negate a configuration command |

---

### Saving Configuration

| Command | Description |
|---------|-------------|
| `write` | Save running-config to startup-config |
| `write memory` | Same as `write` |
| `copy running-config startup-config` | Same as `write` (explicit copy) |

---

### Show / Verification Commands

| Command | Description |
|---------|-------------|
| `show running-config` | Show current active configuration (RAM) |
| `show startup-config` | Show saved configuration (NVRAM) |
| `show version` | IOS version, uptime, hardware info |
| `show ip interface brief` | Summary of all interfaces (IP, status) |
| `show interfaces` | Detailed interface stats, counters, errors |
| `show interfaces status` | Interface status table (speed, duplex, VLAN) |
| `show ip route` | Display full routing table |
| `show ip route static` | Display only static routes |
| `show ip route connected` | Display only connected/local routes |
| `show mac address-table` | Display MAC address table (switch) |
| `show mac address-table dynamic` | Display only dynamically learned MACs |
| `ping <ip-address>` | Send ICMP echo requests to test connectivity |

---

### Interface Configuration

| Command | Description |
|---------|-------------|
| `interface <type/number>` | Enter interface config mode (e.g., `int g0/0`) |
| `ip address <ip> <mask>` | Assign IP address and subnet mask |
| `no shutdown` | Enable interface (bring up) |
| `shutdown` | Disable interface (bring down) |
| `speed <10|100|1000>` | Manually set interface speed |
| `duplex <half|full|auto>` | Manually set duplex mode |
| `description <text>` | Add interface description |

---

### Static Routing

| Command | Description |
|---------|-------------|
| `ip route <network> <mask> <next-hop>` | Static route via next-hop IP |
| `ip route <network> <mask> <interface>` | Static route via exit interface |
| `ip route <network> <mask> <interface> <next-hop>` | Static route with both (recommended for Ethernet) |
| `ip route 0.0.0.0 0.0.0.0 <next-hop>` | Default route (gateway of last resort) |
| `ip route <network> <mask> <next-hop> <AD>` | Floating static (backup) with higher AD |
| `no ip route <network> <mask> <next-hop>` | Remove a static route |

---

### MAC Address Table (Switch)

| Command | Description |
|---------|-------------|
| `show mac address-table` | Show full MAC address table |
| `show mac address-table dynamic` | Show only dynamically learned entries |
| `clear mac address-table dynamic` | Remove all dynamic MAC entries |

---

## 13. Exam Quick-Reference Tables

### OSI vs. TCP/IP Layer Comparison

| OSI Layer | OSI Name | TCP/IP Layer | PDU | Key Protocols |
|-----------|----------|-------------|-----|---------------|
| 7 | Application | Application (5) | Data | HTTP, FTP, DNS, DHCP, SMTP |
| 6 | Presentation | Application (5) | Data | SSL/TLS, JPEG, ASCII |
| 5 | Session | Application (5) | Data | NetBIOS, RPC |
| 4 | Transport | Transport (4) | Segment/Datagram | TCP, UDP |
| 3 | Network | Internet (3) | Packet | IP, ICMP, OSPF, EIGRP |
| 2 | Data Link | Network Access (2) | Frame | Ethernet, Wi-Fi, ARP |
| 1 | Physical | Physical (1) | Bit | UTP, fiber, signals |

---

### Ethernet Standards Summary

| Standard | Speed | Media | Distance | IEEE |
|----------|-------|-------|----------|------|
| 10BASE-T | 10 Mbps | UTP (2 pairs) | 100 m | 802.3i |
| 100BASE-T | 100 Mbps | UTP (2 pairs) | 100 m | 802.3u |
| 1000BASE-T | 1 Gbps | UTP (4 pairs) | 100 m | 802.3ab |
| 10GBASE-T | 10 Gbps | UTP (4 pairs) | 100 m | 802.3an |
| 1000BASE-LX | 1 Gbps | SMF/MMF | 5 km / 550 m | 802.3z |
| 10GBASE-SR | 10 Gbps | MMF | 400 m | 802.3ae |
| 10GBASE-LR | 10 Gbps | SMF | 10 km | 802.3ae |
| 10GBASE-ER | 10 Gbps | SMF | 30 km | 802.3ae |

---

### IPv4 Address Classes

| Class | Range | Default Mask | Private Range | Networks | Hosts/Network |
|-------|-------|-------------|---------------|----------|---------------|
| A | 1–126 | /8 | 10.0.0.0/8 | 126 | 16,777,214 |
| B | 128–191 | /16 | 172.16.0.0/12 | 16,384 | 65,534 |
| C | 192–223 | /24 | 192.168.0.0/16 | 2,097,152 | 254 |
| D | 224–239 | — | — | Multicast | — |
| E | 240–255 | — | — | Experimental | — |

---

### Subnet Mask Quick Reference

| CIDR | Mask | Hosts/Subnet | Block Size | Subnets from /24 |
|------|------|-------------|------------|-------------------|
| /24 | 255.255.255.0 | 254 | 256 | 1 |
| /25 | 255.255.255.128 | 126 | 128 | 2 |
| /26 | 255.255.255.192 | 62 | 64 | 4 |
| /27 | 255.255.255.224 | 30 | 32 | 8 |
| /28 | 255.255.255.240 | 14 | 16 | 16 |
| /29 | 255.255.255.248 | 6 | 8 | 32 |
| /30 | 255.255.255.252 | 2 | 4 | 64 |
| /31 | 255.255.255.254 | 2* | 2 | 128 |
| /32 | 255.255.255.255 | 1** | 1 | 256 |

---

### IPv4 Header Protocol Field Values

| Value | Protocol |
|-------|----------|
| 1 | ICMP |
| 6 | TCP |
| 17 | UDP |
| 89 | OSPF |

---

### Administrative Distance Reference

| Routing Source | AD |
|---------------|----|
| Connected | 0 |
| Static | 1 |
| EIGRP | 90 |
| OSPF | 110 |
| RIP | 120 |
| Unusable | 255 |

---

### Cable Type Selection Guide

| Connection | Cable Type |
|-----------|------------|
| PC → Switch | Straight-through |
| Router → Switch | Straight-through |
| PC → Router | Crossover |
| Switch → Switch | Crossover |
| Router → Router | Crossover |
| PC → Console port | Rollover |

> Modern devices with **Auto MDI-X** automatically handle straight-through vs. crossover — cable type matters less on new equipment.

---

### Common Misconceptions and Exam Traps

| Misconception | Correct Understanding |
|--------------|----------------------|
| Switches connect different LANs | Switches connect hosts WITHIN one LAN. Routers connect different LANs. |
| IP addresses change at each hop | IP addresses stay constant end-to-end. MAC addresses change at every router. |
| /32 cannot be used | /32 is used for host-specific routes (local routes, loopbacks, null routes) |
| Hub and switch work the same | Hub floods ALL ports (L1). Switch forwards based on MAC address table (L2). |
| Enable password and enable secret are equivalent | Enable secret uses MD5 and ALWAYS overrides enable password if both are set. |
| 127.0.0.1 is the only loopback address | 127.0.0.0/8 is the entire loopback range — none of it is assignable to hosts. |
| TTL is decremented by switches | Only ROUTERS (Layer 3 devices) decrement TTL — switches do not. |
| Broadcast stays /32 in routing table | Broadcast address is NOT in the routing table. Network (all 0s) and local (/32) routes are added automatically. |

---

*Study guide based on Jeremy's IT Lab CCNA 200-301 course — Days 1 through 15 (Videos 001–027).*
