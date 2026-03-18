# CCNA 200-301 Exam Coach — Section 10 Study Guide
## Days 56–58 | Wireless Architectures, Wireless Security, Wireless Configuration
### Transcripts 115–120 | Jeremy's IT Lab Complete Course

---

## SECTION 1: EXAM KNOWLEDGE MAP

| # | Video | Day | Topic | CCNA Domain | Exam Weight |
|---|-------|-----|-------|-------------|-------------|
| 115 | Wireless Architectures | Day 56 | 802.11 frame format, association process, message types, autonomous APs, lightweight APs, split-MAC, CAPWAP, WLC deployments, cloud-based APs | Network Fundamentals | 20% |
| 116 | Wireless Architectures Lab | Day 56 Lab | AP mode configuration, WLC connectivity verification | Network Fundamentals | 20% |
| 117 | Wireless Security | Day 57 | Authentication/encryption/integrity, WEP, EAP methods (LEAP/EAP-FAST/PEAP/EAP-TLS), 802.1X, TKIP/CCMP/GCMP, WPA/WPA2/WPA3, personal vs enterprise mode | Security Fundamentals | 15% |
| 118 | Wireless Security Lab | Day 57 Lab | WPA2/WPA3 configuration, PSK vs enterprise mode setup | Security Fundamentals | 15% |
| 119 | Wireless Configuration | Day 58 | WLC ports/interfaces, dynamic interfaces, WLAN-to-VLAN mapping, WLAN creation via GUI, Layer 2/3 security, QoS, ACLs on WLC | Security Fundamentals | 15% |
| 120 | Wireless Configuration Lab | Day 58 Lab | WLC GUI walkthrough, WLAN creation, security policy, interface mapping, ACL creation | Security Fundamentals | 15% |

**Exam Objectives Covered:**
- 1.11 Describe wireless principles (nonoverlapping Wi-Fi channels, SSID, RF, encryption, 802.11a/b/g/n/ac)
- 1.12 Explain virtualization fundamentals (in the context of cloud-based WLC)
- 2.6 Compare Cisco Wireless Architectures and AP modes
- 2.7 Describe physical infrastructure connections of WLAN components (AP, WLC, access/trunk ports)
- 2.8 Describe AP and WLC management access connections (Telnet, SSH, HTTP, HTTPS, console, TACACS+/RADIUS)
- 5.4 Describe wireless security protocols (WPA, WPA2, WPA3)
- 5.9 Describe wireless security protocols and authentication methods

---

## SECTION 2: MUST-KNOW CONCEPTS

---

### Concept 1: 802.11 Frame Format and Association

**802.11 Frame vs. 802.3 Ethernet Frame:**
- 802.11 frames have a **different format** than Ethernet frames
- Up to **4 address fields** (not all always present, depends on message type):
  - **DA** (Destination Address) — final recipient
  - **SA** (Source Address) — original sender
  - **RA** (Receiver Address) — immediate recipient
  - **TA** (Transmitter Address) — immediate sender

**Key 802.11 Frame Fields:**

| Field | Purpose |
|-------|---------|
| **Frame Control** | Message type/subtype (management, control, data) |
| **Duration/ID** | Channel dedication time (μs) or association ID |
| **Addresses** | Up to 4 MAC addresses (DA, SA, RA, TA) |
| **Sequence Control** | Fragment reassembly and duplicate elimination |
| **QoS Control** | Traffic prioritization |
| **HT Control** | High Throughput operations (added in 802.11n) |
| **FCS** | Frame Check Sequence — error detection |

**802.11 Connection States:**
1. **Not authenticated, not associated**
2. **Authenticated, not associated**
3. **Authenticated and associated** — only this state allows data transmission

**802.11 Message Types:**

| Type | Purpose | Examples |
|------|---------|---------|
| **Management** | Manage the BSS | Beacon, Probe Request/Response, Authentication, Association Request/Response |
| **Control** | Control access to the RF medium | RTS (Request to Send), CTS (Clear to Send), ACK |
| **Data** | Carry actual data packets | User data frames |

---

### Concept 2: Autonomous APs

**Characteristics:**
- **Self-contained** systems — do NOT rely on a WLC
- Configured **individually** via console, Telnet/SSH, or HTTP/HTTPS (GUI)
- Each AP independently manages: RF parameters, security policies, QoS rules
- No central monitoring or management

**Network Connectivity:**
- Connect to the wired network via a **trunk link** (carries multiple VLANs)
- Data traffic flows **directly** from wireless clients to the wired network

**Limitations:**
- Every VLAN must **stretch across the entire network** (bad practice)
  - Large broadcast domains
  - STP disables links
  - Adding/deleting VLANs is labor-intensive
- Not viable for medium-to-large networks (thousands of APs)
- Suitable only for **small networks**

**Additional Modes:** Repeater, outdoor bridge, workgroup bridge

---

### Concept 3: Lightweight APs and Split-MAC Architecture

**Split-MAC Architecture:**
- AP functions are **split** between the lightweight AP and a WLC

| Lightweight AP Handles (Real-Time) | WLC Handles (Not Time-Dependent) |
|-----------------------------------|--------------------------------|
| Transmitting/receiving RF traffic | RF management |
| Encryption/decryption of traffic | Security/QoS management |
| Sending beacons/probes | Client authentication |
| Packet prioritization | Client association/roaming management |
| | Centralized AP configuration |

**CAPWAP (Control And Provisioning of Wireless Access Points):**
- Protocol used for communication between lightweight APs and WLC
- Based on older LWAPP protocol
- Creates **two tunnels** between each AP and the WLC:

| Tunnel | UDP Port | Purpose | Encrypted by Default? |
|--------|----------|---------|----------------------|
| **Control Tunnel** | 5246 | AP configuration, management, control | **Yes** |
| **Data Tunnel** | 5247 | All wireless client traffic → WLC | **No** (can enable DTLS) |

**Critical Detail:** Because all wireless client traffic is tunneled via CAPWAP to the WLC, lightweight APs connect to switches via **access ports** (NOT trunk ports).

**WLC-AP Authentication:** Mutual authentication using **X.509 digital certificates**

**Benefits of Split-MAC:**
- **Scalability** — manage thousands of APs from a central WLC
- **Dynamic channel assignment** — WLC auto-selects channels
- **Transmit power optimization** — WLC auto-adjusts power
- **Self-healing coverage** — if an AP fails, WLC increases power of nearby APs
- **Seamless roaming** — no noticeable delay between APs
- **Client load balancing** — WLC distributes clients to least-used AP

---

### Concept 4: Lightweight AP Modes

| Mode | Offers BSS? | Function |
|------|------------|---------|
| **Local** (default) | Yes | Standard mode — one or more BSSs for client association |
| **FlexConnect** | Yes | Like Local, but can locally switch traffic if WLC tunnel goes down |
| **Sniffer** | No | Captures 802.11 frames, sends to Wireshark |
| **Monitor** | No | Receives 802.11 frames to detect rogue devices; can send de-auth messages |
| **Rogue Detector** | No (radio off) | Listens to wired network ARP traffic; correlates with WLC rogue list to detect rogues |
| **SE-Connect** | No | RF spectrum analysis on all channels; sends data to Cisco Spectrum Expert |
| **Bridge/Mesh** | Varies | Dedicated bridge between sites or mesh AP network |
| **Flex Plus Bridge** | Yes | Adds FlexConnect to Bridge/Mesh mode |

---

### Concept 5: Cloud-Based APs and WLC Deployments

**Cloud-Based APs (Cisco Meraki):**
- A hybrid between autonomous and split-MAC
- APs are **centrally managed from the cloud** (Meraki dashboard)
- Cloud manages: configuration, channel selection, transmit power, monitoring, reporting
- **Data traffic goes directly to the wired network** (NOT to the cloud)
- Only management/control traffic goes to the cloud

**WLC Deployment Modes (Split-MAC):**

| Deployment | Where WLC Lives | Max APs (approx.) |
|-----------|----------------|-------------------|
| **Unified** | Dedicated hardware appliance in central location | ~6,000 |
| **Cloud-Based** | VM on a server (usually private cloud data center) | ~3,000 |
| **Embedded** | Integrated within a switch | ~200 |
| **Mobility Express** | Integrated within an AP | ~100 |

---

### Concept 6: Wireless Security — Authentication Methods

**Why Wireless Security is Critical:**
- Wireless signals are not contained in a wire — any device in range can receive traffic
- Three security pillars: **Authentication**, **Encryption**, **Integrity**

**Original 802.11 Authentication (Both Insecure):**

| Method | Description | Security |
|--------|------------|---------|
| **Open Authentication** | AP accepts any authentication request. May require web-based auth afterward (e.g., Starbucks Wi-Fi) | NOT secure |
| **WEP** (Wired Equivalent Privacy) | Shared-key using RC4 encryption. Keys: 40-bit or 104-bit + 24-bit IV = 64 or 128-bit total | **Broken** — easily cracked |

**802.1X and EAP:**
- **802.1X** provides **port-based network access control** — limits access until authentication
- Three entities in 802.1X:
  - **Supplicant:** Device wanting to connect
  - **Authenticator:** Device providing network access (AP/WLC)
  - **Authentication Server (AS):** Verifies credentials, permits/denies access (RADIUS server)

**EAP Methods Comparison:**

| Method | Developer | Authentication | Certificate Required? | Security Level |
|--------|----------|---------------|----------------------|---------------|
| **LEAP** | Cisco | Username/password + mutual challenge | No | **Vulnerable** — do not use |
| **EAP-FAST** | Cisco | PAC → TLS tunnel → auth inside tunnel | No (PAC instead) | Good |
| **PEAP** | Cisco/Microsoft/RSA | Server cert → TLS tunnel → MS-CHAPv2 inside | Server only | Good |
| **EAP-TLS** | Standard | Mutual certificate authentication | **Both** client and server | **Most secure** (but hardest to deploy) |

---

### Concept 7: Wireless Encryption and Integrity

**Encryption/Integrity Protocols:**

| Protocol | Encryption Algorithm | Integrity (MIC) | Used In | Security |
|----------|---------------------|-----------------|---------|---------|
| **TKIP** | RC4 (enhanced) | MIC with sender MAC + timestamp | WPA | Legacy — improved WEP but still weak |
| **CCMP** | **AES** Counter Mode | CBC-MAC | WPA2 | **Strong** — current standard |
| **GCMP** | **AES** Counter Mode | GMAC | WPA3 | **Strongest** — more efficient than CCMP |

**TKIP Enhancements Over WEP:**
- MIC (Message Integrity Check) added
- Key mixing algorithm — unique WEP key per frame
- IV doubled from 24 to 48 bits
- MIC includes sender MAC address
- Timestamp to prevent replay attacks
- Sequence number per source MAC

---

### Concept 8: WPA Certifications

**Wi-Fi Protected Access (WPA) Versions:**

| Feature | WPA | WPA2 | WPA3 |
|---------|-----|------|------|
| Released | ~2003 | 2004 | 2018 |
| Encryption/MIC | TKIP | **CCMP (AES)** | **GCMP (AES)** |
| Auth Modes | Personal (PSK) or Enterprise (802.1X) | Personal (PSK) or Enterprise (802.1X) | Personal (PSK) or Enterprise (802.1X) |

**Authentication Modes:**

| Mode | Authentication Method | Use Case |
|------|----------------------|---------|
| **Personal (PSK)** | Pre-Shared Key; 4-way handshake generates encryption keys | Home/small networks |
| **Enterprise** | 802.1X with RADIUS server; supports all EAP methods | Corporate networks |

**WPA3 Additional Security Features:**
- **PMF (Protected Management Frames):** Protects 802.11 management frames from eavesdropping/forging
- **SAE (Simultaneous Authentication of Equals):** Protects the 4-way handshake in personal mode
- **Forward Secrecy:** Prevents captured wireless frames from being decrypted later

**Important:** The PSK itself is **never sent over the air**. It is used to generate encryption keys during the 4-way handshake.

---

### Concept 9: WLC Ports and Interfaces

**WLC Physical Ports:**

| Port | Function |
|------|---------|
| **Service Port** | Dedicated out-of-band management. Connects to **access port** (one VLAN only). Used for boot/recovery |
| **Distribution System Port** | Standard data ports connecting to the wired network. Connect to **trunk ports**. Multiple ports can form a LAG |
| **Console Port** | Standard console (RJ45 or USB) |
| **Redundancy Port** | Connects to another WLC for HA (High Availability) pair |

**WLC Logical Interfaces:**

| Interface | Purpose |
|-----------|---------|
| **Management** | Management traffic (Telnet, SSH, HTTP/S, RADIUS, NTP, Syslog). **CAPWAP tunnels** form to/from this interface |
| **Redundancy Management** | Manage the standby WLC in an HA pair |
| **Virtual** | Communicates with wireless clients for DHCP relay and web authentication |
| **Service Port** | Bound to the physical service port for out-of-band management |
| **Dynamic** | Maps a **WLAN to a VLAN**. Traffic from a WLAN exits the WLC through its mapped dynamic interface |

---

### Concept 10: WLAN Configuration via WLC GUI

**WLAN-to-VLAN Mapping:**
- Each WLAN (identified by SSID) is mapped to a **dynamic interface** on the WLC
- Each dynamic interface is associated with a **VLAN** on the wired network
- Example: "Internal" WLAN → Internal dynamic interface → VLAN 100

**WLAN Creation Steps (WLC GUI):**
1. Create a **dynamic interface** (specify VLAN, IP, netmask, gateway)
2. Create a **WLAN** (specify SSID and profile name)
3. Map the WLAN to the correct **dynamic interface**
4. Configure **security** (WPA2/WPA3, PSK or Enterprise)
5. **Enable** the WLAN (Status: Enabled)

**Layer 3 Security Options (Guest Networks):**
- **Web Authentication:** Client must enter username/password on a web page
- **Web Passthrough:** Client agrees to terms (no credentials required)
- **Conditional/Splash Page Redirect:** Requires 802.1X Layer 2 auth first

**QoS Settings on WLC:**
- Default: **Silver** (Best Effort)
- Options: Platinum (Voice), Gold (Video), Silver (Best Effort), Bronze (Background)

**DHCP Option 43:**
- Used to inform lightweight APs of the WLC's IP address
- Configured on the DHCP server so APs can auto-discover and join the WLC

---

## SECTION 3: COMMON EXAM TRAPS

| Trap | Correct Answer |
|------|---------------|
| "Autonomous APs connect to switch trunk ports; lightweight APs also connect to trunk ports?" | FALSE — Autonomous APs connect to **trunk** ports. Lightweight APs connect to **access** ports because all client traffic is tunneled via CAPWAP to the WLC. |
| "The CAPWAP data tunnel is encrypted by default?" | FALSE — The **control** tunnel (UDP 5246) is encrypted by default. The **data** tunnel (UDP 5247) is **NOT** encrypted by default. DTLS can be enabled to encrypt it. |
| "Cloud-based APs (Meraki) send all data traffic to the cloud?" | FALSE — Only **management/control** traffic is sent to the cloud. **Data traffic** goes directly to the wired network, like autonomous APs. |
| "WEP provides adequate security for modern wireless networks?" | FALSE — WEP is **broken** and easily cracked. It should never be used. Even TKIP/WPA is considered legacy. WPA2 (CCMP/AES) is the current minimum standard. |
| "PEAP requires certificates on both the client and server?" | FALSE — **PEAP** requires a certificate only on the **server**. The client authenticates inside the TLS tunnel (e.g., MS-CHAPv2). **EAP-TLS** requires certificates on both client and server. |
| "EAP-TLS is the easiest EAP method to deploy?" | FALSE — EAP-TLS is the **most secure** but also the **hardest to deploy** because every client device needs a certificate. PEAP is easier (only server needs a cert). |
| "WPA3 uses CCMP for encryption?" | FALSE — **WPA2** uses CCMP. **WPA3** uses **GCMP**, which is more secure and efficient than CCMP. Both use AES, but with different modes. |
| "In WPA Personal mode, the PSK is sent over the air during authentication?" | FALSE — The PSK is **never sent over the air**. It is used to generate encryption keys during a **4-way handshake**. |
| "The WLC management interface handles data traffic from wireless clients?" | FALSE — The management interface handles **management traffic** (SSH, RADIUS, CAPWAP). Data traffic from WLANs flows through **dynamic interfaces** mapped to specific VLANs. |
| "A Unified WLC is a virtual machine running in a data center?" | FALSE — A **Unified** WLC is a **hardware appliance**. A **Cloud-Based** WLC is a VM running on a server in a private cloud/data center. |
| "FlexConnect mode is only useful when the WLC is operational?" | FALSE — FlexConnect's key feature is that it can **locally switch traffic** between wired and wireless networks **even if the CAPWAP tunnel to the WLC goes down**. |
| "A rogue detector AP uses its radio to detect rogue devices?" | FALSE — A rogue detector AP does **NOT use its radio**. It listens to **wired network ARP traffic** and correlates it with the WLC's suspected rogue list. |
| "802.1X authentication involves only two entities: client and server?" | FALSE — 802.1X involves **three entities**: **Supplicant** (client), **Authenticator** (AP/WLC), and **Authentication Server** (RADIUS). |
| "WPA3 Forward Secrecy means the data is encrypted more strongly?" | FALSE — Forward secrecy means that even if encryption keys are compromised later, **previously captured traffic cannot be decrypted**. It protects past sessions, not current encryption strength. |

---

## SECTION 4: COMPLETE COMMAND REFERENCE

### Switch Configuration for Lightweight APs
```
! Lightweight APs connect to ACCESS ports (not trunks — traffic is CAPWAP tunneled)
SW(config)# interface fa0/1
SW(config-if)# switchport mode access
SW(config-if)# switchport access vlan 10            ! AP management VLAN

! WLC connects to a TRUNK port (carries multiple VLAN traffic)
SW(config)# interface g0/1
SW(config-if)# switchport mode trunk
SW(config-if)# switchport trunk allowed vlan 10,100,200   ! Management + WLAN VLANs
```

### Switch Configuration for Autonomous APs
```
! Autonomous APs connect to TRUNK ports
SW(config)# interface fa0/1
SW(config-if)# switchport mode trunk
SW(config-if)# switchport trunk native vlan 10
SW(config-if)# switchport trunk allowed vlan 10,100,200
```

### Layer 3 Switch Configuration (WLC Deployment)
```
! Create VLANs for management and WLANs
SW(config)# vlan 10
SW(config-vlan)# name MANAGEMENT
SW(config)# vlan 100
SW(config-vlan)# name INTERNAL-WLAN
SW(config)# vlan 200
SW(config-vlan)# name GUEST-WLAN

! Create SVIs for each VLAN
SW(config)# interface vlan 10
SW(config-if)# ip address 10.0.10.1 255.255.255.0
SW(config)# interface vlan 100
SW(config-if)# ip address 10.0.100.1 255.255.255.0
SW(config)# interface vlan 200
SW(config-if)# ip address 10.0.200.1 255.255.255.0

! DHCP pool with Option 43 (WLC IP for AP discovery)
SW(config)# ip dhcp pool AP-POOL
SW(dhcp-config)# network 10.0.10.0 255.255.255.0
SW(dhcp-config)# default-router 10.0.10.1
SW(dhcp-config)# option 43 hex f104.0a00.0a02        ! WLC IP in hex (10.0.10.2)
```

### WLC GUI Configuration Steps
```
! WLC GUI accessed via HTTPS: https://<WLC-management-IP>

! 1. Create Dynamic Interfaces (Controller > Interfaces > New)
!    - Interface Name: INTERNAL
!    - VLAN ID: 100
!    - IP Address, Netmask, Gateway
!    - DHCP server address

! 2. Create WLAN (WLANs > Create New)
!    - Profile Name: Internal
!    - SSID: CompanyWiFi
!    - Status: Enabled
!    - Interface: INTERNAL (dynamic interface created above)

! 3. Security Tab:
!    - Layer 2: WPA+WPA2
!    - WPA2 Policy: Enabled
!    - WPA2 Encryption: AES
!    - Auth Key Mgmt: PSK or 802.1X
!    - PSK Format: ASCII, enter passphrase (min 8 chars)

! 4. QoS Tab:
!    - Quality of Service: Silver (default Best Effort)
!    - Options: Platinum (Voice), Gold (Video), Silver (Best Effort), Bronze (Background)
```

---

## SECTION 5: EXAM QUICK-REFERENCE TABLES

### Wireless Architecture Comparison

| Feature | Autonomous AP | Lightweight AP (Split-MAC) | Cloud-Based AP (Meraki) |
|---------|--------------|--------------------------|------------------------|
| Management | Individual (CLI/GUI) | Centralized via WLC | Centralized via cloud dashboard |
| Switch Connection | **Trunk** port | **Access** port | **Trunk** port |
| Data Path | Direct to wired network | Tunneled to WLC via CAPWAP | Direct to wired network |
| Control Path | Local on AP | WLC via CAPWAP | Cloud |
| Scalability | Small networks only | Large networks (thousands of APs) | Medium-large networks |
| Protocol | N/A | CAPWAP | Proprietary |

### CAPWAP Tunnel Details

| Tunnel | UDP Port | Default Encryption | Content |
|--------|----------|-------------------|---------|
| Control | 5246 | **Encrypted** | AP config, management, control messages |
| Data | 5247 | **NOT encrypted** (enable DTLS) | All wireless client data traffic |

### WPA Version Comparison

| Feature | WPA | WPA2 | WPA3 |
|---------|-----|------|------|
| Encryption/MIC Protocol | TKIP (RC4) | **CCMP (AES)** | **GCMP (AES)** |
| Integrity Method | MIC | CBC-MAC | GMAC |
| Personal Mode | PSK | PSK | PSK + **SAE** |
| Enterprise Mode | 802.1X | 802.1X | 802.1X |
| Management Frame Protection | No | Optional | **Required (PMF)** |
| Forward Secrecy | No | No | **Yes** |
| Security Rating | Legacy/weak | Current standard | Next-generation |

### EAP Method Comparison

| Method | Server Cert? | Client Cert? | Tunnel? | Security |
|--------|-------------|-------------|---------|---------|
| LEAP | No | No | No | Vulnerable |
| EAP-FAST | No (uses PAC) | No | TLS | Good |
| PEAP | **Yes** | No | TLS | Good |
| EAP-TLS | **Yes** | **Yes** | TLS | **Best** |

### WLC Deployment Comparison

| Deployment | Form Factor | Location | Max APs |
|-----------|------------|---------|---------|
| Unified | Hardware appliance | Central network location | ~6,000 |
| Cloud-Based | VM on server | Private cloud / data center | ~3,000 |
| Embedded | Inside a switch | Network closet | ~200 |
| Mobility Express | Inside an AP | Wherever the AP is | ~100 |

### 802.1X Entities

| Entity | Role | Example |
|--------|------|---------|
| **Supplicant** | Device wanting network access | Laptop, phone |
| **Authenticator** | Provides network access; relays auth | AP or WLC |
| **Authentication Server** | Verifies credentials; permits/denies | RADIUS server (e.g., Cisco ISE) |

---

## SECTION 6: PRACTICE QUIZ

**1.** A company deploys 500 lightweight APs managed by a single WLC. An engineer connects a new lightweight AP to the network switch. What type of switch port should the AP connect to, and why?

- A) Trunk port — the AP needs to carry multiple VLANs for different WLANs
- B) Access port — all wireless client traffic is tunneled via CAPWAP to the WLC, so the AP only needs one VLAN
- C) EtherChannel — for redundancy between the AP and switch
- D) Trunk port — CAPWAP requires 802.1Q tagging

**Answer: B** — Lightweight APs connect to **access ports**. All wireless client data traffic is tunneled through the **CAPWAP data tunnel** to the WLC, so the AP itself only needs to be in one VLAN (its management VLAN). The WLC handles VLAN mapping through its dynamic interfaces.

---

**2.** Which CAPWAP tunnel carries wireless client data, and is it encrypted by default?

- A) Control tunnel (UDP 5246); encrypted by default
- B) Data tunnel (UDP 5247); encrypted by default
- C) Data tunnel (UDP 5247); NOT encrypted by default — DTLS can be enabled
- D) Control tunnel (UDP 5246); NOT encrypted by default

**Answer: C** — The **data tunnel** (UDP 5247) carries all wireless client traffic to the WLC. It is **NOT encrypted by default**, but **DTLS** (Datagram Transport Layer Security) can be enabled to encrypt it. The control tunnel (UDP 5246) is encrypted by default.

---

**3.** A hospital needs the most secure wireless authentication method. They have the infrastructure to deploy certificates on every device. Which EAP method should they use?

- A) LEAP — provides mutual authentication
- B) EAP-FAST — uses a PAC for authentication
- C) PEAP — requires only a server certificate
- D) EAP-TLS — mutual certificate authentication on both client and server

**Answer: D** — **EAP-TLS** is the **most secure** wireless authentication method. It requires digital certificates on both the authentication server AND every client device, providing mutual certificate-based authentication. Since the hospital can deploy certificates on every device, EAP-TLS is the best choice.

---

**4.** A company currently uses WPA2 with CCMP. They want to upgrade to the latest standard for better security. What encryption/integrity protocol will WPA3 use?

- A) TKIP for encryption, MIC for integrity
- B) CCMP for encryption, CBC-MAC for integrity
- C) GCMP for encryption, GMAC for integrity
- D) AES-256 for encryption, SHA-256 for integrity

**Answer: C** — WPA3 uses **GCMP** (Galois/Counter Mode Protocol), which provides AES Counter Mode encryption and **GMAC** (Galois Message Authentication Code) for integrity. GCMP is more secure and efficient than CCMP used in WPA2.

---

**5.** An engineer notices that when a remote office's WAN link to the WLC fails, all wireless clients lose connectivity even though the local wired network is functional. Which lightweight AP mode would solve this problem?

- A) Local mode
- B) Monitor mode
- C) FlexConnect mode
- D) Sniffer mode

**Answer: C** — **FlexConnect** mode allows a lightweight AP to **locally switch traffic** between the wired and wireless networks if the CAPWAP tunnel to the WLC goes down. In standard Local mode, all traffic must tunnel to the WLC — so a WAN failure means total wireless outage.

---

**6.** A network admin is comparing WLC deployment options for a network with 150 APs. Which deployment modes could support this? (Select TWO)

- A) Mobility Express (~100 AP limit)
- B) Embedded (~200 AP limit)
- C) Unified (~6,000 AP limit)
- D) A single autonomous AP

**Answer: B and C** — An **Embedded** WLC (inside a switch) supports ~200 APs, and a **Unified** WLC (hardware appliance) supports ~6,000 APs. Both can handle 150 APs. Mobility Express only supports ~100, which is insufficient.

---

**7.** In 802.1X wireless authentication, a laptop running Cisco AnyConnect connects to a corporate WLAN. The traffic flow involves three entities. Which entity acts as the authenticator?

- A) The laptop (supplicant)
- B) The RADIUS server (authentication server)
- C) The AP or WLC (authenticator)
- D) The DNS server

**Answer: C** — In 802.1X, the **authenticator** is the device that provides network access and relays authentication between the supplicant and the authentication server. In wireless networks, this is the **AP or WLC**. The laptop is the supplicant; the RADIUS server is the authentication server.

---

**8.** What is the key difference between PEAP and EAP-TLS?

- A) PEAP uses AES; EAP-TLS uses RC4
- B) PEAP requires a certificate only on the server; EAP-TLS requires certificates on BOTH the client and server
- C) EAP-TLS does not use a TLS tunnel; PEAP does
- D) PEAP is Cisco proprietary; EAP-TLS is open standard

**Answer: B** — The key difference: **PEAP** requires a digital certificate only on the **authentication server** (client authenticates inside the TLS tunnel using MS-CHAPv2 or similar). **EAP-TLS** requires certificates on **both the client and server** for mutual certificate-based authentication, making it more secure but harder to deploy.

---

**9.** An administrator configures a guest WLAN on the WLC. Guests should be able to access the Internet after agreeing to a terms-of-use page without entering any credentials. Which Layer 3 security method should be configured?

- A) Web Authentication
- B) Web Passthrough
- C) WPA2-Enterprise with RADIUS
- D) Conditional Web Redirect

**Answer: B** — **Web Passthrough** displays a warning or terms-of-use statement, and the client simply agrees to gain Internet access — no username or password required. **Web Authentication** requires credentials. Conditional Web Redirect requires 802.1X Layer 2 auth first.

---

**10.** A Cisco Meraki cloud-based AP deployment is configured. Where does wireless client data traffic flow?

- A) All traffic is sent to the Meraki cloud for processing and then forwarded
- B) Data traffic goes directly to the wired network; only management/control traffic goes to the cloud
- C) All traffic is tunneled to an on-premises WLC via CAPWAP
- D) Data traffic is split between the cloud and the local network based on QoS policies

**Answer: B** — In a Meraki **cloud-based AP** deployment, **data traffic flows directly to the wired network** (like autonomous APs). Only **management and control traffic** (configuration, monitoring, channel/power adjustments) is sent to the Meraki cloud dashboard.
