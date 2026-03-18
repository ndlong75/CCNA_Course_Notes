# CCNA 200-301 Exam Coach — Section 05 Study Guide
## Days 31–35 | Network Fundamentals + Security Fundamentals: IPv6 Parts 1–3, Standard ACLs, Extended ACLs
### Transcripts 063–072 | Jeremy's IT Lab Complete Course

---

## SECTION 1: EXAM KNOWLEDGE MAP

| # | Video | Day | Topic | CCNA Domain | Exam Weight |
|---|-------|-----|-------|-------------|-------------|
| 063 | IPv6 Part 1 | Day 31 | IPv6 addressing, abbreviation rules, prefix finding, basic config | Network Fundamentals | 20% |
| 064 | IPv6 Part 1 Lab | Day 31 Lab | Configure IPv6 addresses, `ipv6 unicast-routing`, verify with `show` | Network Fundamentals | 20% |
| 065 | IPv6 Part 2 | Day 32 | EUI-64, IPv6 address types (Global Unicast, Unique Local, Link-Local, Multicast, Anycast) | Network Fundamentals | 20% |
| 066 | IPv6 Part 2 Lab | Day 32 Lab | EUI-64 config, address type identification, link-local verification | Network Fundamentals | 20% |
| 067 | IPv6 Part 3 | Day 33 | IPv6 header, NDP, SLAAC, DAD, IPv6 static routing | Network Fundamentals | 20% |
| 068 | IPv6 Part 3 Lab | Day 33 Lab | IPv6 static routes, link-local next hops, neighbor table | Network Fundamentals | 20% |
| 069 | Standard ACLs | Day 34 | ACL concepts, ACEs, implicit deny, standard numbered/named ACLs, placement | Security Fundamentals | 15% |
| 070 | Standard ACLs Lab | Day 34 Lab | Configure and apply standard ACLs, `show ip access-lists` | Security Fundamentals | 15% |
| 071 | Extended ACLs | Day 35 | Extended numbered/named ACLs, protocol/port matching, resequencing, named mode advantages | Security Fundamentals | 15% |
| 072 | Extended ACLs Lab | Day 35 Lab | Configure complex extended ACLs, apply inbound/outbound, verify | Security Fundamentals | 15% |

**Exam Objectives Covered:**
- 1.8 Describe IPv6 address types (Global Unicast, Unique Local, Link-Local, Anycast, Multicast)
- 1.9 Configure and verify IPv6 addressing and prefix
- 1.10 Describe IPv6 address configuration (SLAAC, DHCPv6 stateless/stateful)
- 5.2 Configure and verify access control lists

---

## SECTION 2: MUST-KNOW CONCEPTS

---

### Concept 1: Why IPv6 and Address Basics

**Why IPv6:**
- IPv4 has 2^32 = ~4.3 billion addresses — exhausted by regional registries (ARIN 2015, LACNIC 2020)
- VLSM, Private IPs, and NAT are short-term fixes; IPv6 is the long-term solution
- IPv6 has 2^128 addresses — effectively unlimited

**IPv6 Address Format:**
- **128 bits** = 8 groups of 16 bits (quartets), each group written in **hexadecimal**, separated by `:`
- Example: `2001:0DB8:8B00:0001:FB89:017B:0020:0011`
- Uses **prefix length notation** (no subnet masks): `/64`, `/48`, etc.

**Abbreviation Rules (RFC-required):**
1. Remove **leading zeros** in each group: `0DB8` → `DB8`, `0001` → `1`
2. Use `::` to replace ONE consecutive sequence of all-zero groups — only **once** per address
3. If two equal-length zero runs exist, `::` replaces the **leftmost** one
4. Hex letters `a–f` must be **lowercase**

**Examples:**
```
Full:        2001:0DB8:0000:0000:0000:0000:0000:0001
Abbreviated: 2001:db8::1

Full:        FE80:0000:0000:0000:0A2C:57FF:FE3A:00B1
Abbreviated: fe80::a2c:57ff:fe3a:b1
```

**Finding the Prefix:**
- Enterprises typically receive a **/48 block** from their ISP
- Subnets typically use **/64 prefix length**
- This leaves **16 bits** for subnets and **64 bits** for hosts within each subnet

---

### Concept 2: IPv6 Address Configuration

```
! Enable IPv6 routing (REQUIRED — disabled by default)
R1(config)# ipv6 unicast-routing

! Configure an IPv6 address manually
R1(config-if)# ipv6 address 2001:db8:0:1::1/64
R1(config-if)# no shutdown

! Configure with EUI-64 (router generates interface ID from MAC)
R1(config-if)# ipv6 address 2001:db8:0:1::/64 eui-64

! Enable IPv6 on interface (generates link-local only; no global unicast)
R1(config-if)# ipv6 enable

! SLAAC (device auto-generates global unicast from NDP prefix)
R1(config-if)# ipv6 address autoconfig

! Verify
R1# show ipv6 interface brief
R1# show ipv6 interface g0/0
```

**Key Config Rule:** IPv4 routing is enabled by default. IPv6 routing is **disabled by default** — the router can receive/send IPv6 traffic but will NOT forward it between networks without `ipv6 unicast-routing`.

---

### Concept 3: EUI-64 Interface ID Generation

**EUI-64 Process** (converts 48-bit MAC → 64-bit interface ID):
1. Split the 48-bit MAC in half (after the 3rd byte)
2. Insert `FF:FE` in the middle
3. **Invert the 7th bit** (U/L bit) of the first byte

**Example:**
```
MAC:          782B.CBAC.0867
Split:        782B.CB  |  AC.0867
Insert FF:FE: 782B.CBFF.FEAC.0867
Invert 7th bit of 78:
  78 hex = 0111 1000 binary
  7th bit is the second bit: 0111 1000 → 0111 1010 = 7A
Result:       7A2B.CBFF.FEAC.0867
```

**Why invert the 7th bit?**
- MAC addresses: 7th bit (U/L bit) = 0 means UAA (universally administered), 1 means LAA
- In EUI-64 context, the meaning is **reversed**: 1 = UAA, 0 = LAA
- Most real MACs are UAA (7th bit = 0), so after inversion the EUI-64 7th bit = 1

---

### Concept 4: IPv6 Address Types

| Type | Address Block | Description |
|------|--------------|-------------|
| **Global Unicast** | Originally `2000::/3`; now all non-reserved | Public, routable over internet; must register |
| **Unique Local** | `FC00::/7` (must use `FD` prefix) | Private, not internet-routable; like RFC 1918 for IPv6 |
| **Link-Local** | `FE80::/10` (always starts `FE80::`) | Auto-generated on every IPv6 interface; scope = single link; not routed |
| **Multicast** | `FF00::/8` | One-to-many; replaces broadcast |
| **Anycast** | Any unicast range (marked `anycast`) | Same address on multiple routers; traffic sent to nearest |
| **Loopback** | `::1/128` | Local loopback (like 127.0.0.1 in IPv4) |
| **Unspecified** | `::/128` | Used before address is known; IPv6 default route = `::/0` |

**Global Unicast Address Structure:**
- Bits 1-48: **Global Routing Prefix** (assigned by ISP/IANA)
- Bits 49-64: **Subnet ID** (enterprise-defined)
- Bits 65-128: **Interface ID** (host portion)

**Unique Local:**
- Block `FC00::/7`, but 8th bit must = 1 → always starts with `FD`
- `FD + 40-bit random Global ID + 16-bit Subnet ID + 64-bit Interface ID`

**Link-Local Rules:**
- Auto-generated when `ipv6 enable` or any IPv6 address is configured
- Always starts with `FE80` (standard requires bits 11-64 = all zeros — so FE9x, FEAx, FEBx won't appear)
- Interface ID generated using EUI-64
- Used for: routing protocol peerings (OSPFv3), NDP, next-hop for static routes
- Routers do NOT forward packets destined to link-local addresses

---

### Concept 5: IPv6 Multicast Addresses

**IPv6 has NO broadcast** — multicast replaces it.

**Key Multicast Groups (must memorize):**

| Address | Group | Used By |
|---------|-------|---------|
| `FF02::1` | All IPv6 nodes | Equivalent to broadcast within subnet |
| `FF02::2` | All IPv6 routers | Sent by hosts using RS; received by routers |
| `FF02::5` | All OSPF routers | OSPFv3 (same as IPv4 224.0.0.5) |
| `FF02::6` | OSPF DR/BDR | OSPFv3 (same as IPv4 224.0.0.6) |
| `FF02::9` | All RIP routers | RIPng |
| `FF02::A` | All EIGRP routers | EIGRPv6 |

**Multicast Scope (first nibble after FF):**

| Scope | Code | Boundary |
|-------|------|---------|
| Interface-local | FF**01** | Stays on local device |
| Link-local | FF**02** | Stays on local subnet; most common |
| Site-local | FF**05** | Single physical site |
| Organization-local | FF**08** | Entire company |
| Global | FF**0E** | Internet-routable |

---

### Concept 6: IPv6 Header

**Fixed size: 40 bytes** (no fragmentation at routers — simpler than IPv4)

| Field | Bits | Purpose |
|-------|------|---------|
| Version | 4 | Always `6` (0b0110) |
| Traffic Class | 8 | QoS — marks high-priority traffic |
| Flow Label | 20 | Identifies traffic flows (src→dst) |
| Payload Length | 16 | Length of payload in bytes (IPv6 header itself NOT included) |
| Next Header | 8 | Type of next header (TCP=6, UDP=17, ICMPv6=58) — same as IPv4 Protocol field |
| Hop Limit | 8 | Decrements by 1 per router hop; packet dropped at 0 (same as IPv4 TTL) |
| Source Address | 128 | Source IPv6 address |
| Destination Address | 128 | Destination IPv6 address |

**vs IPv4 Header:** IPv4 = variable 20–60 bytes; IPv6 = fixed 40 bytes. IPv6 removed fragmentation, checksum, and options fields (moved to extension headers).

---

### Concept 7: Neighbor Discovery Protocol (NDP)

**NDP replaces ARP in IPv6.** Uses ICMPv6 and solicited-node multicast (not broadcast).

**NDP Functions:**
1. **Layer 2 address resolution** (like ARP) — using NS/NA
2. **Router discovery** — using RS/RA
3. **SLAAC** — automatic address configuration
4. **DAD** — duplicate address detection

**NDP Message Types:**

| Message | ICMPv6 Type | Sent To | Purpose |
|---------|-------------|---------|---------|
| NS (Neighbor Solicitation) | 135 | Solicited-node multicast | "What's your MAC?" (like ARP request) |
| NA (Neighbor Advertisement) | 136 | Unicast (or all-nodes) | "Here's my MAC" (like ARP reply) |
| RS (Router Solicitation) | 133 | `FF02::2` (all routers) | Host asks routers to identify themselves |
| RA (Router Advertisement) | 134 | `FF02::1` (all nodes) | Router announces prefix + other info |

**Solicited-Node Multicast Address:**
- Format: `FF02::1:FF` + last 24 bits of the unicast address
- Example: unicast `2001:db8::1` → solicited-node = `FF02::1:FF00:0001`
- More targeted than broadcast — only the host(s) with matching last 24 bits receive it

**IPv6 Neighbor Table** (equivalent of ARP cache):
```
R1# show ipv6 neighbors
```

---

### Concept 8: SLAAC and DAD

**SLAAC (Stateless Address Auto-Configuration):**
- Host sends RS to `FF02::2`; router replies with RA containing the local prefix
- Host uses the prefix + EUI-64 (or random) to generate its own global unicast address
- No DHCP server needed — "stateless"
- Command: `R1(config-if)# ipv6 address autoconfig`

**DAD (Duplicate Address Detection):**
- Performed **every time** an IPv6 address is assigned (manual, EUI-64, SLAAC) or an interface initializes
- Host sends NS to its own solicited-node multicast address asking "is anyone using this IP?"
  - No reply = address is unique → use it
  - Reply received = duplicate detected → address not used

---

### Concept 9: IPv6 Static Routing

**Static route types** (same as IPv4, but no directly attached on Ethernet):

| Type | Command | Notes |
|------|---------|-------|
| Recursive | `ipv6 route dest/prefix next-hop-IPv6` | Most common; specifies next-hop only |
| Fully Specified | `ipv6 route dest/prefix exit-int next-hop-IPv6` | Required for link-local next-hops |
| Directly Attached | `ipv6 route dest/prefix exit-int` | **NOT valid on Ethernet** in IPv6 |

```
! Enable IPv6 routing first!
R1(config)# ipv6 unicast-routing

! Network route (recursive)
R1(config)# ipv6 route 2001:db8:0:3::/64 2001:db8:0:12::2

! Default route
R1(config)# ipv6 route ::/0 2001:db8:0:12::2

! Host route (/128 = specific host)
R2(config)# ipv6 route 2001:db8:0:1::100/128 2001:db8:0:12::1

! Floating static (increase AD above IGP's AD)
R1(config)# ipv6 route ::/0 2001:db8:0:12::2 111

! Link-local next-hop (MUST specify exit interface)
R1(config)# ipv6 route 2001:db8:0:3::/64 g0/0 fe80::a2c:57ff:fe3a:b1

! Verify
R1# show ipv6 route
R1# show ipv6 route static
```

**Key Difference from IPv4:** Directly attached static routes using exit-interface only **do NOT work on Ethernet** in IPv6 (NDP requires knowing the next-hop address).

---

### Concept 10: ACL Fundamentals

**ACL (Access Control List):** Ordered list of ACEs (Access Control Entries) that a router processes top-to-bottom to permit or deny packets.

**How ACLs Work:**
1. Router checks each ACE in order from **top to bottom**
2. **First match** → take action (permit/deny) and **stop** processing
3. If no ACE matches → **Implicit Deny** (deny all) — applied automatically at the end of every ACL
4. An ACL configured in global config has **no effect** until applied to an interface with `in` or `out`

**ACL Application Direction:**
- **Inbound (`in`):** ACL checked before routing decision — can stop traffic before it consumes router resources
- **Outbound (`out`):** ACL checked after routing decision, before sending out interface

**Maximum per interface:** One ACL per direction per interface (1 in, 1 out)

---

### Concept 11: Standard ACLs

**Standard ACLs match only on SOURCE IP address.**

| Feature | Detail |
|---------|--------|
| Match field | Source IP only |
| Numbered range | **1–99** and **1300–1999** |
| Placement rule | Apply **as close to the destination as possible** (to avoid blocking too much traffic) |

**Standard Numbered ACL:**
```
! Deny a specific host
R1(config)# access-list 1 deny 1.1.1.1                    ! host shorthand
R1(config)# access-list 1 deny host 1.1.1.1               ! same
R1(config)# access-list 1 deny 1.1.1.1 0.0.0.0            ! with wildcard

! Permit any source
R1(config)# access-list 1 permit any
R1(config)# access-list 1 permit 0.0.0.0 255.255.255.255  ! same

! Add a remark
R1(config)# access-list 1 remark ## BLOCK BOB FROM ACCOUNTING ##

! Apply to interface
R1(config-if)# ip access-group 1 {in | out}
```

**Standard Named ACL:**
```
R1(config)# ip access-list standard BLOCK_BOB
R1(config-std-nacl)# 10 deny 192.168.1.1
R1(config-std-nacl)# 20 permit any

R1(config-if)# ip access-group BLOCK_BOB out
```

**Note:** IOS may reorder ACEs within a named ACL (more specific entries first). Cisco Packet Tracer does **not** reorder.

---

### Concept 12: Extended ACLs

**Extended ACLs can match on:** Source IP, Destination IP, Protocol (IP/TCP/UDP/ICMP/etc.), Source Port, Destination Port.

| Feature | Detail |
|---------|--------|
| Match fields | Src IP, Dst IP, Protocol, Src Port, Dst Port |
| Numbered range | **100–199** and **2000–2699** |
| Placement rule | Apply **as close to the SOURCE as possible** (filter early to save bandwidth) |

**Extended Numbered ACL syntax:**
```
R1(config)# access-list number {permit|deny} protocol src-ip src-wildcard [src-port] dst-ip dst-wildcard [dst-port]
```

**Extended Named ACL syntax:**
```
R1(config)# ip access-list extended ACL_NAME
R1(config-ext-nacl)# {seq-num} {permit|deny} protocol src-ip [src-port] dst-ip [dst-port]
```

**Protocol Keywords:**
- `ip` = match ALL IP traffic (any protocol)
- `tcp` = TCP only
- `udp` = UDP only
- `icmp` = ICMP only
- Number (e.g., `89`) = specific IP protocol number (OSPF=89, EIGRP=88)

**Port Matching Operators:**
- `eq 80` = equal to port 80
- `gt 1023` = greater than port 1023
- `lt 1024` = less than port 1024
- `neq 23` = not equal to port 23
- `range 20000 30000` = port range 20000 to 30000

**Practice Examples:**
```
! Deny all TCP from 10.0.0.0/24 to any
R1(config-ext-nacl)# deny tcp 10.0.0.0 0.0.0.255 any

! Permit HTTPS from 10.0.0.0/16 to server 2.2.2.2
R1(config-ext-nacl)# permit tcp 10.0.0.0 0.0.255.255 host 2.2.2.2 eq 443

! Block UDP source ports 20000-30000 to server 3.3.3.3
R1(config-ext-nacl)# deny udp any range 20000 30000 host 3.3.3.3

! Block pings from 172.16.1.1 to 192.168.0.0/24
R1(config-ext-nacl)# deny icmp host 172.16.1.1 192.168.0.0 0.0.0.255

! Permit everything else
R1(config-ext-nacl)# permit ip any any
```

---

### Concept 13: Named ACL Mode Advantages + Resequencing

**Named ACL config mode advantages over numbered global config mode:**
1. **Delete individual entries:** `no 10` (removes sequence 10 only) — impossible with global numbered ACL (deleting deletes entire ACL)
2. **Insert entries between existing ones:** specify a sequence number between existing entries (e.g., `15 deny ...` between entries 10 and 20)

**Modern IOS:** Numbered ACLs can also be configured in named ACL style:
```
R1(config)# ip access-list standard 1
R1(config-std-nacl)# 10 deny 192.168.1.0 0.0.0.255
R1(config-std-nacl)# 20 permit any
```

**Resequencing:**
```
! Resequence ACL 1: start at 10, increment by 10
R1(config)# ip access-list resequence 1 10 10

! Same for named ACL
R1(config)# ip access-list resequence BLOCK_BOB 10 10
```

---

## SECTION 3: COMMON EXAM TRAPS

| Trap | Correct Answer |
|------|---------------|
| "IPv6 uses broadcast like IPv4?" | FALSE — IPv6 has NO broadcast; multicast replaces it (FF02::1 is closest equivalent) |
| "Can `::` be used more than once in an IPv6 address?" | NO — `::` can only appear **once** per address |
| "Leading zeros must be removed in IPv6?" | YES — RFC requires removing leading zeros (0db8 → db8) |
| "IPv6 routing is enabled by default?" | FALSE — must enable with `ipv6 unicast-routing` |
| "Can you use a directly attached static route on an Ethernet IPv6 interface?" | NO — Ethernet requires a known next-hop address in IPv6 (NDP needs it) |
| "Unique Local addresses start with FC or FD?" | Only **FD** — the 8th bit must be 1, so FC00::/7 always uses FD in practice |
| "Link-local addresses can start with FE9, FEA, or FEB?" | NO — standard requires bits 11-64 all zero; only **FE80** is used |
| "NDP uses broadcast to find MAC addresses?" | FALSE — NDP uses **solicited-node multicast** (not broadcast like ARP) |
| "DAD only happens at initial configuration?" | FALSE — DAD runs every time an IPv6 interface initializes OR any address is configured |
| "Standard ACL should be placed close to source?" | FALSE — Standard ACLs go **close to destination** (to avoid over-blocking); Extended ACLs go close to source |
| "An ACL takes effect as soon as it's configured?" | FALSE — ACL must be **applied to an interface** with `ip access-group` |
| "What happens if no ACE matches a packet?" | **Implicit deny** — packet is dropped (every ACL has invisible deny all at the end) |
| "Standard ACL numbers vs Extended ACL numbers?" | Standard: 1–99, 1300–1999 / Extended: 100–199, 2000–2699 |
| "Can you delete one entry from a numbered ACL using global config mode?" | NO — deletes the entire ACL; use **named ACL config mode** (or configure numbered in named style) |
| "Extended ACLs match only source IP like standard?" | FALSE — Extended ACLs match source IP, destination IP, protocol, AND port numbers |
| "EUI-64: which bit is inverted?" | The **7th bit** (U/L bit) of the first byte of the MAC address |

---

## SECTION 4: COMPLETE COMMAND REFERENCE

### IPv6 Configuration Commands
```
R(config)# ipv6 unicast-routing                          ! REQUIRED to route IPv6 (disabled by default)
R(config-if)# ipv6 address <addr/prefix>                 ! Manual IPv6 address
R(config-if)# ipv6 address <prefix/prefix-len> eui-64   ! EUI-64 auto interface ID
R(config-if)# ipv6 address autoconfig                   ! SLAAC — learn prefix via NDP
R(config-if)# ipv6 enable                               ! Enable IPv6 on interface (link-local only)
R# show ipv6 interface brief                            ! Summary of IPv6 interfaces and addresses
R# show ipv6 interface <int>                            ! Detailed IPv6 interface info (joined groups)
R# show ipv6 neighbors                                  ! IPv6 neighbor table (like show arp)
```

### IPv6 Static Routing Commands
```
R(config)# ipv6 route <dest/prefix> <next-hop>                    ! Recursive static route
R(config)# ipv6 route <dest/prefix> <exit-int> <next-hop>         ! Fully specified static route
R(config)# ipv6 route <dest/prefix> <exit-int>                    ! Directly attached (Ethernet: NOT valid)
R(config)# ipv6 route ::/0 <next-hop>                             ! Default route
R(config)# ipv6 route <dest/prefix> <next-hop> <AD>               ! Floating static route
R(config)# ipv6 route <dest/prefix> <exit-int> <link-local-addr>  ! Link-local next-hop (must specify int)
R# show ipv6 route                                                ! Full IPv6 routing table
R# show ipv6 route static                                         ! IPv6 static routes only
```

### Standard ACL Commands
```
! Numbered (global config mode)
R(config)# access-list <1-99|1300-1999> {permit|deny} <src-ip> [wildcard]
R(config)# access-list <num> {permit|deny} host <ip>
R(config)# access-list <num> {permit|deny} any
R(config)# access-list <num> remark <text>

! Named (named config mode)
R(config)# ip access-list standard <name|number>
R(config-std-nacl)# [seq-num] {permit|deny} <src-ip> [wildcard]

! Apply to interface
R(config-if)# ip access-group <name|number> {in|out}

! Verify
R# show ip access-lists                           ! All ACLs with hit counts
R# show ip access-lists <name|number>             ! Specific ACL
R# show ip interface <int>                        ! Shows applied ACLs on interface
```

### Extended ACL Commands
```
! Numbered (global config mode)
R(config)# access-list <100-199|2000-2699> {permit|deny} <protocol> <src-ip> [src-wildcard] [src-port] <dst-ip> [dst-wildcard] [dst-port]

! Named (named config mode)
R(config)# ip access-list extended <name|number>
R(config-ext-nacl)# [seq-num] {permit|deny} <protocol> <src-ip> [src-wildcard] [src-port] <dst-ip> [dst-wildcard] [dst-port]

! Delete a single entry (named/numbered in named mode only)
R(config-std-nacl)# no <seq-num>

! Resequence
R(config)# ip access-list resequence <acl-id> <start> <increment>

! Apply to interface
R(config-if)# ip access-group <name|number> {in|out}
```

---

## SECTION 5: EXAM QUICK-REFERENCE TABLES

### IPv6 Address Type Summary

| Type | Prefix | Routable? | Scope | IPv4 Equivalent |
|------|--------|-----------|-------|-----------------|
| Global Unicast | `2000::/3` (all non-reserved) | Yes (internet) | Global | Public IP |
| Unique Local | `FD00::/8` | No | Organization | Private (RFC 1918) |
| Link-Local | `FE80::/10` | No | Single link | 169.254.x.x (APIPA) |
| Multicast | `FF00::/8` | Depends on scope | Varies | 224.0.0.0/4 |
| Anycast | Any unicast range | Yes | Global | (no equivalent) |
| Loopback | `::1/128` | No | Local device | 127.0.0.1 |
| Unspecified | `::/128` | No | Local | 0.0.0.0 |

### NDP Message Summary

| Message | Type | Direction | Purpose |
|---------|------|-----------|---------|
| NS (Neighbor Solicitation) | ICMPv6 135 | Host → solicited-node multicast | Find MAC of neighbor |
| NA (Neighbor Advertisement) | ICMPv6 136 | Host → requester | Reply with MAC |
| RS (Router Solicitation) | ICMPv6 133 | Host → FF02::2 | Find routers on link |
| RA (Router Advertisement) | ICMPv6 134 | Router → FF02::1 | Announce prefix + info |

### ACL Type Comparison

| Feature | Standard ACL | Extended ACL |
|---------|-------------|-------------|
| Match | Source IP only | Src IP, Dst IP, Protocol, Src/Dst Port |
| Numbered range | 1–99, 1300–1999 | 100–199, 2000–2699 |
| Placement | Close to **destination** | Close to **source** |
| Complexity | Simple | More precise (and complex) |
| `ip access-list` keyword | `standard` | `extended` |

### ACL Wildcard Mask Quick Reference

| Mask | Meaning | Example |
|------|---------|---------|
| `0.0.0.0` | Match exact host | `10.1.1.1 0.0.0.0` = host 10.1.1.1 |
| `0.0.0.255` | Match /24 network | `192.168.1.0 0.0.0.255` = 192.168.1.0/24 |
| `0.0.255.255` | Match /16 network | `172.16.0.0 0.0.255.255` = 172.16.0.0/16 |
| `255.255.255.255` | Match any | Same as keyword `any` |
| `host <ip>` | Match exact host | Shorthand for `0.0.0.0` wildcard |
| `any` | Match all | Shorthand for `0.0.0.0 255.255.255.255` |

---

## SECTION 6: PRACTICE QUIZ

**1.** An IPv6 address is written as `2001:0DB8:0000:0000:00AB:0000:0000:0001`. Which of the following is the correct abbreviated form?

- A) `2001:db8::ab::1`
- B) `2001:db8:0:0:ab::1`
- C) `2001:DB8::AB:0:0:1`
- D) `2001:db8::ab:0:0:1`

**Answer: B** — `::` replaces the longest consecutive run of all-zero groups. The second run (groups 7-8) is also two groups but the LEFT occurrence (groups 3-4) is used first — wait, here the first zero run is groups 3-4 (two groups) and the second is groups 6-7 (two groups). Per RFC, when equal, use `::` for the leftmost. BUT group 5 is `00AB` (not all zeros), so the two runs are: `0000:0000` (positions 3-4) and `0000:0000` (positions 6-7). Leftmost wins: `2001:db8::ab:0:0:1`. Hex must be lowercase. Answer **D** — `2001:db8::ab:0:0:1` is correct (the leftmost two-zero-group run gets `::`, giving groups 3-4 replaced; remaining zeros in groups 6-7 stay as `0:0`).

---

**2.** A router's interface MAC address is `AA:BB:CC:DD:EE:FF`. What is the EUI-64 interface ID?

- A) `AABB:CCFF:FEDD:EEFF`
- B) `A8BB:CCFF:FEDD:EEFF`
- C) `AABB:CCDD:EEFF:0000`
- D) `A8BB:CC00:00DD:EEFF`

**Answer: B** — Split MAC: `AABB:CC | DD:EEFF`. Insert FF:FE: `AABB:CCFF:FEDD:EEFF`. Invert 7th bit of `AA` (0xAA = 1010 1010; 7th bit is bit 1 from left in second nibble = 1010 1010; 7th bit = index 6 from left = 1; flip to 0: 1010 1000 = 0xA8). Result: `A8BB:CCFF:FEDD:EEFF`.

---

**3.** Which IPv6 address type is automatically generated on every IPv6-enabled interface and is NOT routed between subnets?

- A) Global Unicast
- B) Unique Local
- C) Link-Local
- D) Anycast

**Answer: C** — **Link-Local** addresses (`FE80::/10`) are automatically generated and are only valid within a single link/subnet. Routers do not forward packets with a link-local destination address.

---

**4.** A host sends an ICMPv6 Type 133 message to `FF02::2`. What is this message and what is its purpose?

- A) Neighbor Advertisement — replies to a MAC address request
- B) Router Solicitation — asks routers on the local link to identify themselves
- C) Neighbor Solicitation — checks for duplicate addresses
- D) Router Advertisement — announces the local prefix to hosts

**Answer: B** — ICMPv6 Type 133 = **Router Solicitation (RS)**. Sent to `FF02::2` (all routers multicast). The host is asking routers to send an RA so the host can learn the local prefix for SLAAC or other configuration.

---

**5.** Which of the following IPv6 static route commands is INVALID on an Ethernet interface?

- A) `ipv6 route 2001:db8::/64 2001:db8:0:12::2`
- B) `ipv6 route 2001:db8::/64 g0/0 2001:db8:0:12::2`
- C) `ipv6 route 2001:db8::/64 g0/0`
- D) `ipv6 route 2001:db8::/64 g0/0 fe80::1`

**Answer: C** — **Directly attached static routes** (exit interface only, no next-hop) are **NOT valid on Ethernet interfaces** in IPv6. NDP cannot resolve the next-hop without knowing the actual address. A or B (recursive or fully specified) are valid. D (link-local next-hop with interface) is also valid.

---

**6.** An ACL is applied outbound on R1's G0/2 interface. The ACL has two entries: `deny 192.168.2.0 0.0.0.255` and `permit any`. A packet from 192.168.2.5 arrives on G0/0 destined for 10.0.1.50 (reachable via G0/2). What happens?

- A) Packet is permitted because ACL is inbound on G0/0
- B) Packet is denied when it reaches G0/2 outbound
- C) Packet is permitted because source IP doesn't match destination
- D) Packet is denied immediately at G0/0

**Answer: B** — The ACL is **outbound on G0/2**. The router accepts the packet on G0/0, makes a routing decision, then checks the ACL before forwarding out G0/2. Source is 192.168.2.5 → matches `deny 192.168.2.0 0.0.0.255` → packet denied.

---

**7.** What is the key difference in placement between Standard and Extended ACLs?

- A) Standard close to source; Extended close to destination
- B) Standard close to destination; Extended close to source
- C) Both should be placed close to the source
- D) Both should be placed close to the destination

**Answer: B** — **Standard ACLs** match only source IP and should be placed **close to the destination** (to avoid accidentally blocking traffic to other networks). **Extended ACLs** can match both source and destination precisely, so they are placed **close to the source** to filter traffic as early as possible and save bandwidth.

---

**8.** A network admin wants to permit only HTTPS traffic from 172.16.0.0/16 to server 10.0.1.100, and deny everything else. Which extended ACL correctly implements this?

- A) `permit tcp 172.16.0.0 0.0.255.255 host 10.0.1.100 eq 80` then `deny ip any any`
- B) `permit tcp 172.16.0.0 0.0.255.255 host 10.0.1.100 eq 443` then `permit ip any any`
- C) `permit tcp 172.16.0.0 0.0.255.255 host 10.0.1.100 eq 443` then `deny ip any any`
- D) `permit ip 172.16.0.0 0.0.255.255 host 10.0.1.100` then `deny ip any any`

**Answer: C** — HTTPS = TCP port **443** (not 80 which is HTTP). After permitting the HTTPS traffic, adding `deny ip any any` is explicit (same as relying on implicit deny). Answer B would also permit other traffic via `permit ip any any`. Answer D uses `ip` (all protocols) instead of `tcp` with port 443.

---

**9.** An admin configures: `R1(config)# access-list 50 deny 10.0.0.0 0.255.255.255`. What is the effect before applying to an interface?

- A) All traffic from 10.0.0.0/8 is immediately denied
- B) The ACL exists but has NO effect until applied to an interface
- C) The router warns that a permit statement is needed
- D) The ACL automatically applies to all interfaces

**Answer: B** — Configuring an ACL in global config mode **does not activate it**. The ACL must be explicitly applied to an interface using `ip access-group 50 {in|out}`. Until then, no traffic is filtered by this ACL.

---

**10.** An admin wants to delete only the second entry (sequence 20) from named ACL "FILTER_HOSTS" without affecting other entries. Which command accomplishes this?

- A) `no access-list FILTER_HOSTS 20`
- B) `R1(config)# no ip access-list standard FILTER_HOSTS`
- C) `R1(config-std-nacl)# no 20`
- D) `R1(config)# no access-list 20`

**Answer: C** — Enter named ACL config mode with `ip access-list standard FILTER_HOSTS`, then use `no 20` to delete sequence number 20 only. Option B deletes the entire ACL. Options A and D are incorrect syntax. This is one of the key advantages of named ACL config mode over global numbered ACL configuration.
