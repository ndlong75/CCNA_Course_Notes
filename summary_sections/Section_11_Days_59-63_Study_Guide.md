[< Back to All Sections](../README.md#section-study-guides)

# CCNA 200-301 Exam Coach — Section 11 Study Guide
## Days 59–63 | Network Automation, JSON/XML/YAML, REST APIs, SDN, Ansible/Puppet/Chef
### Transcripts 121–126 | Jeremy's IT Lab Complete Course

---

## SECTION 1: EXAM KNOWLEDGE MAP

| # | Video | Day | Topic | CCNA Domain | Exam Weight |
|---|-------|-----|-------|-------------|-------------|
| 121 | Introduction to Network Automation | Day 59 | Data/control/management planes, SDN overview, SBI/NBI, ASIC/TCAM, benefits of automation | Automation & Programmability | 10% |
| 122 | JSON, XML, and YAML | Day 60 | Data serialization, JSON primitives/objects/arrays, XML tags, YAML whitespace-significant syntax | Automation & Programmability | 10% |
| 123 | REST APIs | Day 61 | CRUD operations, HTTP verbs, HTTP request/response, status codes, REST constraints, Cisco DevNet | Automation & Programmability | 10% |
| 124 | REST API Authentication | Day 61 | API authentication, token-based auth, Postman usage, DNA Center API calls | Automation & Programmability | 10% |
| 125 | Software-Defined Networking | Day 62 | SD-Access, DNA Center, underlay/overlay/fabric, LISP, VXLAN, TrustSec, IBN, greenfield/brownfield | Automation & Programmability | 10% |
| 126 | Ansible, Puppet, and Chef | Day 63 | Configuration drift, provisioning, agent-based vs agentless, push vs pull, playbooks/manifests/cookbooks | Automation & Programmability | 10% |

**Exam Objectives Covered:**
- 6.1 Explain how automation impacts network management
- 6.2 Compare traditional networks with controller-based networking
- 6.3 Describe controller-based and software-defined architectures (overlay, underlay, fabric)
- 6.4 Compare traditional campus device management with Cisco DNA Center enabled device management
- 6.5 Describe characteristics of REST-based APIs (CRUD, HTTP verbs, data encoding)
- 6.6 Recognize the capabilities of configuration management mechanisms Puppet, Chef, and Ansible
- 6.7 Interpret JSON encoded data

---

## SECTION 2: MUST-KNOW CONCEPTS

---

### Concept 1: The Three Logical Planes of Network Functions

**Data Plane (Forwarding Plane):**
- All tasks involved in **forwarding user data** from one interface to another
- Router: looks up routing table, forwards packet, re-encapsulates L2 header
- Switch: looks up MAC address table, forwards/floods frame, adds/removes 802.1Q tags
- Also includes: NAT translation, ACL permit/deny decisions, port security filtering
- Processed by specialized hardware **ASIC** (Application-Specific Integrated Circuit) for speed
- MAC address table stored in **TCAM** (Ternary Content-Addressable Memory), also called CAM table

**Control Plane:**
- Functions that **build the tables** used by the data plane
- OSPF → builds the routing table
- STP → determines which interfaces forward/block
- ARP → builds the ARP table
- The control plane *controls* what the data plane does (overhead work)
- Processed by the **CPU**

**Management Plane:**
- Overhead work that does **NOT directly affect** data plane forwarding
- Protocols for managing devices: SSH/Telnet, Syslog, SNMP, NTP
- Processed by the **CPU**

**Summary Rule:**
- Control/management traffic (destined for the device itself) → processed by **CPU**
- Data traffic (passing through the device) → processed by **ASIC** for maximum speed

---

### Concept 2: Why Network Automation

**Problems with Manual (One-by-One) Configuration:**
- Typos and human errors are common
- Time-consuming and inefficient at scale
- Difficult to ensure all devices comply with organizational standards

**Benefits of Network Automation:**
- **Reduced human error** — fewer typos, consistent configs
- **Scalability** — network-wide changes in a fraction of the time
- **Policy compliance** — standard configurations and software versions enforced
- **Reduced OpEx** — fewer man-hours per task

**Automation Tools:** SDN, Ansible, Puppet, Chef, Python scripts

---

### Concept 3: Software-Defined Networking (SDN) Overview

**What SDN Is:**
- An approach that **centralizes the control plane** into an application called a **controller**
- Also called Software-Defined Architecture (SDA) or Controller-Based Networking
- Traditional networks: distributed control plane (each device runs OSPF independently)
- SDN: centralized controller calculates routes and programs devices via APIs

**Southbound Interface (SBI):**
- Communication between the **controller and network devices**
- Consists of a protocol + API
- Examples: **OpenFlow**, Cisco OpFlex, Cisco OnePK, **NETCONF**, RESTCONF

**Northbound Interface (NBI):**
- Communication between **applications/scripts and the controller**
- Allows interaction with controller, access to network data, programming the network
- Typically uses **REST APIs**
- Data exchanged in serialized formats: **JSON** or **XML**

**SDN vs. Traditional Automation:**
- Traditional: Python scripts push commands via SSH; parse "show" output with regex
- SDN: Controller collects all network data centrally; NBIs provide structured data (JSON/XML); facilitates network-wide analytics
- SDN tools provide automation benefits without requiring scripting expertise

---

### Concept 4: Data Serialization — JSON, XML, YAML

**Data Serialization:**
- Converting data into a standardized format that can be stored, transmitted, and reconstructed
- Allows applications to communicate in a mutually understood format

**JSON (JavaScript Object Notation):**
- Open standard (RFC 8259); language-independent; used by REST APIs
- Whitespace is **insignificant**
- Four primitive types: **string** (`"text"`), **number** (`5`), **boolean** (`true`/`false`), **null**
- Two structured types:
  - **Object:** unordered key-value pairs in `{ }` — keys are strings, values are any type
  - **Array:** ordered list of values in `[ ]` — values can be mixed types

```json
{
  "hostname": "SW1",
  "ip_address": "10.0.0.1",
  "vlans": [10, 20, 30],
  "enabled": true,
  "description": null
}
```

**XML (Extensible Markup Language):**
- Originally a markup language, now used for data serialization
- Less human-readable than JSON
- Whitespace is **insignificant**
- Uses opening and closing tags: `<key>value</key>`

```xml
<device>
  <hostname>SW1</hostname>
  <ip_address>10.0.0.1</ip_address>
  <enabled>true</enabled>
</device>
```

**YAML (YAML Ain't Markup Language):**
- Very human-readable
- Whitespace **IS significant** — indentation matters
- Files start with `---` (three dashes)
- Lists use `-`; key-value pairs use `key: value`
- Used by **Ansible**

```yaml
---
hostname: SW1
ip_address: 10.0.0.1
vlans:
  - 10
  - 20
  - 30
enabled: true
description: null
```

**Format Comparison:**

| Feature | JSON | XML | YAML |
|---------|------|-----|------|
| Readability | Good | Fair | **Best** |
| Whitespace | Insignificant | Insignificant | **Significant** |
| Used by | REST APIs | REST APIs, NETCONF | **Ansible** |
| Data structure | `{ }` objects, `[ ]` arrays | `<tag>` elements | Indentation |
| File extension | `.json` | `.xml` | `.yaml` / `.yml` |

---

### Concept 5: REST APIs

**What REST Is:**
- REST (Representational State Transfer) is a set of **architectural constraints** for APIs
- REST-based APIs / RESTful APIs typically use **HTTP(S)** for communication

**Six REST Constraints:**
1. **Client-Server** — client and server are separate, evolve independently
2. **Stateless** — each request is independent; server does not store previous request state; client must authenticate every request
3. **Cacheable** — cacheable resources must be declared as such
4. **Uniform Interface** — consistent interface between client and server
5. **Layered System** — client doesn't need to know if it's connected directly to the server
6. **Code-on-Demand** (optional) — server can send executable code to client

**CRUD Operations and HTTP Verbs:**

| CRUD Operation | HTTP Verb | Description |
|---------------|-----------|------------|
| **Create** | **POST** | Create a new resource |
| **Read** | **GET** | Retrieve/read a resource |
| **Update** | **PUT** / **PATCH** | Update/modify an existing resource |
| **Delete** | **DELETE** | Delete a resource |

**HTTP Request Components:**
- **HTTP verb** (GET, POST, PUT, DELETE)
- **URI** (Uniform Resource Identifier) — identifies the target resource
- **Headers** — additional information (e.g., `Accept: application/json`)
- **Body** (for POST/PUT) — data to send in JSON or XML format

**HTTP Response Status Codes:**

| Code Class | Meaning | Examples |
|-----------|---------|---------|
| **1xx** | Informational | 102 Processing |
| **2xx** | **Success** | **200 OK**, 201 Created |
| **3xx** | Redirection | 301 Moved Permanently |
| **4xx** | **Client Error** | 401 Unauthorized, **403 Forbidden**, **404 Not Found** |
| **5xx** | **Server Error** | 500 Internal Server Error |

---

### Concept 6: Cisco SD-Access and DNA Center

**Cisco SDN Solutions:**

| Solution | Purpose | Controller |
|----------|---------|-----------|
| **SD-Access** | Campus LAN automation | Cisco DNA Center |
| **ACI** | Data center automation | APIC |
| **SD-WAN** | WAN automation | vManage |

**SD-Access Architecture:**

| Layer | Definition |
|-------|-----------|
| **Underlay** | Physical network (switches, routers, cables) providing IP connectivity. Uses IS-IS routing |
| **Overlay** | Virtual network built on top of the underlay. Uses VXLAN tunnels |
| **Fabric** | Combination of underlay + overlay = the complete network |

**SD-Access Underlay Switch Roles:**

| Role | Function |
|------|---------|
| **Edge Nodes** | Connect to end hosts (access switches) |
| **Border Nodes** | Connect to devices outside SD-Access domain (WAN routers) |
| **Control Nodes** | Use LISP for control plane functions |

**SD-Access Greenfield Deployment (Optimal):**
- All switches are **Layer 3** using **IS-IS** routing protocol
- All links between switches are **routed ports** (no STP needed)
- Edge nodes act as the **default gateway** for end hosts (Routed Access Layer)

**SD-Access Overlay Technologies:**
- **LISP** (Locator ID Separation Protocol) — control plane; maps EIDs to RLOCs
- **VXLAN** — data plane; encapsulates traffic in tunnels
- **Cisco TrustSec (CTS)** — policy control (QoS, security)

**Cisco DNA Center:**
- Two roles: SDN controller for SD-Access + network manager for traditional networks
- Installed on Cisco UCS server hardware
- **REST API** for NBI; **NETCONF/RESTCONF** (+ SSH/SNMP) for SBI
- Enables **Intent-Based Networking (IBN):** engineer communicates intent → DNA Center handles device configurations
- Greenfield = new deployment; Brownfield = existing network with SD-Access added on top

**DNA Center vs. Traditional Management:**

| Feature | Traditional | DNA Center |
|---------|-----------|------------|
| Configuration | One-by-one via SSH | Centralized via GUI or REST API |
| Policy management | Per-device | Centralized, intent-based |
| New deployments | Manual, time-consuming | Automatic, zero-touch provisioning |
| Software updates | Manual per device | Centralized, monitors for new versions |
| Error rate | Higher (manual effort) | Lower (automation) |

---

### Concept 7: Configuration Management — Ansible, Puppet, Chef

**Configuration Drift:**
- Over time, individual changes cause devices to **deviate from standard configurations**
- Changes aren't tracked; engineers forget why changes were made
- Configuration management tools prevent and correct drift

**Configuration Provisioning:**
- How configuration changes are applied to devices
- Traditional: SSH one-by-one (impractical at scale)
- Automation: templates + variables → generate configs → push/pull to devices

**Ansible:**
- Owned by **Red Hat**; written in **Python**
- **Agentless** — no special software needed on managed devices
- Uses **SSH** to connect to devices
- **Push model** — Ansible server pushes configs to devices

| File Type | Purpose | Format |
|-----------|---------|--------|
| **Playbooks** | Blueprints of automation tasks (logic and actions) | **YAML** |
| **Inventory** | Lists managed devices and their characteristics | INI, YAML |
| **Templates** | Device config files with variable placeholders | **Jinja2** |
| **Variables** | Variable names and values (substituted into templates) | **YAML** |

**Puppet:**
- Written in **Ruby**
- Typically **agent-based** (software installed on managed devices)
  - Can run agentless via proxy agent using SSH
- **Pull model** — clients pull configs from the **Puppet Master**
- Clients communicate via **TCP 8140**
- Uses a **proprietary language** (not YAML)

| File Type | Purpose |
|-----------|---------|
| **Manifest** | Defines desired configuration state of a device |
| **Templates** | Used to generate manifests |

**Chef:**
- Written in **Ruby**
- **Agent-based** (software on managed devices)
- **Pull model** — server sends configs via **TCP 10002**
- Uses a **DSL (Domain-Specific Language) based on Ruby**

| File Type | Purpose |
|-----------|---------|
| **Resources** | Configuration objects ("ingredients") |
| **Recipes** | Logic and actions performed on resources |
| **Cookbooks** | Sets of related recipes |
| **Run-list** | Ordered list of recipes to execute |

---

## SECTION 3: COMMON EXAM TRAPS

| Trap | Correct Answer |
|------|---------------|
| "The data plane is processed by the CPU?" | FALSE — The data plane is processed by specialized **ASIC** hardware for maximum speed. The **control plane and management plane** are processed by the CPU. |
| "OSPF and STP are part of the data plane?" | FALSE — OSPF and STP are **control plane** functions. They build tables (routing table, STP topology) that the data plane uses for forwarding decisions. |
| "NAT is part of the control plane?" | FALSE — **NAT** is part of the **data plane**. It modifies packet headers (source/destination addresses) as part of the forwarding process. |
| "SDN eliminates the data plane from network devices?" | FALSE — SDN **centralizes the control plane** into a controller. The **data plane remains on the network devices** — they still forward traffic. |
| "Whitespace is significant in JSON and XML?" | FALSE — Whitespace is insignificant in both JSON and XML. Whitespace **IS significant** only in **YAML** (indentation defines structure). |
| "YAML files start with three asterisks (***) ?" | FALSE — YAML files start with **three dashes** (`---`). |
| "JSON arrays contain key-value pairs?" | FALSE — JSON **objects** contain key-value pairs `{ }`. JSON **arrays** contain **ordered lists of values** `[ ]` without keys. |
| "REST APIs are stateful — the server remembers previous requests?" | FALSE — REST APIs are **stateless**. Each request is independent; the server does not store state from previous requests. The client must authenticate with every request. |
| "HTTP GET is used to create a new resource?" | FALSE — **GET** is used to **read/retrieve** a resource. **POST** is used to **create** a new resource. |
| "HTTP status code 404 means a server error?" | FALSE — **404 (Not Found)** is a **4xx client error** — the requested resource doesn't exist. **5xx** codes are server errors. |
| "Ansible uses a pull model like Puppet and Chef?" | FALSE — **Ansible uses a push model** (server pushes configs via SSH). **Puppet and Chef use a pull model** (clients pull configs from the server). |
| "Ansible requires agent software installed on managed devices?" | FALSE — Ansible is **agentless** — it uses SSH to connect to devices. **Puppet and Chef** are typically agent-based. |
| "Puppet playbooks are written in YAML?" | FALSE — **Ansible** playbooks are written in YAML. **Puppet** uses a **proprietary language**. **Chef** uses a Ruby-based DSL. |
| "In SD-Access, the overlay is the physical network?" | FALSE — The **underlay** is the physical network. The **overlay** is the virtual network built on top. The **fabric** = underlay + overlay combined. |
| "SD-Access greenfield deployments use STP between switches?" | FALSE — In SD-Access greenfield, all links are **routed ports** (Layer 3), so **STP is not needed**. All switches use **IS-IS** routing. |
| "DNA Center's SBI uses REST APIs to communicate with network devices?" | FALSE — The **NBI** uses REST APIs (for apps/engineers to interact with DNA Center). The **SBI** uses protocols like **NETCONF, RESTCONF**, SSH, and SNMP to communicate with devices. |
| "Cisco ACI is used for campus LAN automation?" | FALSE — **SD-Access** is for campus LANs. **ACI** is for **data center** networks. **SD-WAN** is for WANs. |

---

## SECTION 4: COMPLETE COMMAND REFERENCE

### JSON Example — Network Device Data
```json
{
  "device": {
    "hostname": "SW1",
    "ip_address": "10.0.0.1",
    "interfaces": [
      {
        "name": "GigabitEthernet0/0",
        "ip": "10.0.0.1",
        "status": "up"
      },
      {
        "name": "GigabitEthernet0/1",
        "ip": "10.0.1.1",
        "status": "down"
      }
    ],
    "vlans": [10, 20, 30],
    "ospf_enabled": true,
    "description": null
  }
}
```

### XML Example — Same Data
```xml
<device>
  <hostname>SW1</hostname>
  <ip_address>10.0.0.1</ip_address>
  <interfaces>
    <interface>
      <name>GigabitEthernet0/0</name>
      <ip>10.0.0.1</ip>
      <status>up</status>
    </interface>
    <interface>
      <name>GigabitEthernet0/1</name>
      <ip>10.0.1.1</ip>
      <status>down</status>
    </interface>
  </interfaces>
  <vlans>
    <vlan>10</vlan>
    <vlan>20</vlan>
    <vlan>30</vlan>
  </vlans>
  <ospf_enabled>true</ospf_enabled>
  <description/>
</device>
```

### YAML Example — Same Data
```yaml
---
device:
  hostname: SW1
  ip_address: 10.0.0.1
  interfaces:
    - name: GigabitEthernet0/0
      ip: 10.0.0.1
      status: up
    - name: GigabitEthernet0/1
      ip: 10.0.1.1
      status: down
  vlans:
    - 10
    - 20
    - 30
  ospf_enabled: true
  description: null
```

### Ansible Playbook Example
```yaml
---
- name: Configure VLANs on switches
  hosts: access_switches
  gather_facts: no
  tasks:
    - name: Create VLAN 10
      ios_vlans:
        config:
          - vlan_id: 10
            name: DATA
            state: active
    - name: Create VLAN 20
      ios_vlans:
        config:
          - vlan_id: 20
            name: VOICE
            state: active
```

### Ansible Inventory Example (INI format)
```ini
[access_switches]
SW1 ansible_host=10.0.0.1
SW2 ansible_host=10.0.0.2
SW3 ansible_host=10.0.0.3

[core_switches]
CORE1 ansible_host=10.0.0.10

[all:vars]
ansible_network_os=ios
ansible_user=admin
ansible_password=cisco123
ansible_connection=network_cli
```

### REST API Call Examples (Conceptual)
```
# READ all devices (GET request)
GET https://dna-center.example.com/api/v1/network-device
Headers: Accept: application/json
         X-Auth-Token: <authentication_token>

# Response: 200 OK
# Body: JSON list of all network devices

# CREATE a new VLAN (POST request)
POST https://dna-center.example.com/api/v1/vlan
Headers: Content-Type: application/json
         X-Auth-Token: <token>
Body:
{
  "vlan_id": 100,
  "name": "ENGINEERING",
  "status": "active"
}

# Response: 201 Created
```

---

## SECTION 5: EXAM QUICK-REFERENCE TABLES

### Three Logical Planes

| Plane | Function | Processed By | Examples |
|-------|---------|-------------|---------|
| **Data Plane** | Forward user traffic | **ASIC** | Routing/switching, NAT, ACL filtering, 802.1Q tagging |
| **Control Plane** | Build forwarding tables | **CPU** | OSPF, STP, ARP, MAC learning |
| **Management Plane** | Device management (no forwarding impact) | **CPU** | SSH, Syslog, SNMP, NTP |

### SDN Architecture Interfaces

| Interface | Between | Direction | Protocol Examples | Data Format |
|-----------|---------|-----------|-------------------|-------------|
| **SBI** (Southbound) | Controller ↔ Network Devices | Down | OpenFlow, NETCONF, RESTCONF, OpFlex | Varies |
| **NBI** (Northbound) | Applications ↔ Controller | Up | **REST API** | **JSON, XML** |

### CRUD-to-HTTP Mapping

| CRUD | HTTP Verb | Action |
|------|-----------|--------|
| Create | **POST** | Create new resource |
| Read | **GET** | Retrieve resource |
| Update | **PUT/PATCH** | Modify resource |
| Delete | **DELETE** | Remove resource |

### HTTP Status Code Classes

| Class | Meaning | Key Codes |
|-------|---------|-----------|
| 1xx | Informational | 102 Processing |
| **2xx** | **Success** | **200 OK**, 201 Created |
| 3xx | Redirection | 301 Moved Permanently |
| **4xx** | **Client Error** | 401 Unauthorized, 403 Forbidden, **404 Not Found** |
| **5xx** | **Server Error** | **500 Internal Server Error** |

### Data Serialization Format Comparison

| Feature | JSON | XML | YAML |
|---------|------|-----|------|
| Readability | Good | Fair | Best |
| Whitespace | Insignificant | Insignificant | **Significant** |
| Key-value syntax | `"key": "value"` | `<key>value</key>` | `key: value` |
| Arrays/Lists | `[item1, item2]` | Nested tags | `- item` |
| Objects | `{ }` | Nested tags | Indentation |
| Commonly used by | REST APIs | REST APIs, NETCONF | **Ansible** |

### Configuration Management Tool Comparison (MEMORIZE THIS)

| Feature | Ansible | Puppet | Chef |
|---------|---------|--------|------|
| Written in | **Python** | Ruby | Ruby |
| Agent | **Agentless** (SSH) | Agent-based (TCP 8140) | Agent-based (TCP 10002) |
| Model | **Push** | Pull | Pull |
| Config language | **YAML** | Proprietary | Ruby DSL |
| Config files | **Playbooks**, Inventory, Templates (Jinja2), Variables | **Manifests**, Templates | **Recipes**, Cookbooks, Resources, Run-lists |
| Owner | **Red Hat** | Puppet (Perforce) | Progress (Chef) |

### Cisco SDN Solutions

| Solution | Domain | Controller |
|----------|--------|-----------|
| **SD-Access** | Campus LAN | **Cisco DNA Center** |
| **ACI** | Data Center | APIC |
| **SD-WAN** | WAN | vManage |

### SD-Access Terminology

| Term | Definition |
|------|-----------|
| **Underlay** | Physical network providing IP connectivity (IS-IS, L3 routed ports) |
| **Overlay** | Virtual network (VXLAN tunnels) built on top of underlay |
| **Fabric** | Underlay + Overlay combined |
| **Edge Node** | Access switch connecting to end hosts |
| **Border Node** | Connects SD-Access to external networks (WAN) |
| **Control Node** | Runs LISP for control plane functions |
| **LISP** | Control plane protocol (EID-to-RLOC mapping) |
| **VXLAN** | Data plane encapsulation |
| **CTS** | Cisco TrustSec — policy control |
| **IBN** | Intent-Based Networking — engineer states intent, controller implements |

---

## SECTION 6: PRACTICE QUIZ

**1.** A network engineer uses OSPF to build the routing table on a router. The router then uses this routing table to forward a packet from interface G0/0 to G0/1. Which planes are involved in each action?

- A) OSPF = data plane; forwarding = control plane
- B) OSPF = management plane; forwarding = data plane
- C) OSPF = control plane; forwarding = data plane
- D) Both OSPF and forwarding are data plane operations

**Answer: C** — **OSPF** is a **control plane** function — it builds the routing table that the data plane uses. The actual **forwarding** of the packet from one interface to another is a **data plane** operation processed by the ASIC.

---

**2.** An engineer needs to read the current configuration of a network device using a REST API. Which HTTP verb should they use?

- A) POST
- B) PUT
- C) GET
- D) DELETE

**Answer: C** — **GET** maps to the **Read** CRUD operation. It retrieves/reads a resource from the server without modifying it. POST creates, PUT updates, and DELETE removes resources.

---

**3.** A REST API call returns HTTP status code 404. What does this mean?

- A) The request was successful
- B) The server encountered an internal error
- C) The client's request was unauthorized
- D) The requested resource was not found

**Answer: D** — **404 Not Found** is a **4xx client error** indicating the requested resource does not exist on the server. 200 = success, 500 = server error, 401 = unauthorized.

---

**4.** Which data serialization format uses significant whitespace and is used by Ansible for playbooks?

- A) JSON
- B) XML
- C) YAML
- D) HTML

**Answer: C** — **YAML** is the only format where **whitespace is significant** (indentation defines structure). Ansible uses YAML for playbooks and variable files. JSON and XML both treat whitespace as insignificant.

---

**5.** Look at the following JSON data. What is the value associated with the key "enabled"?
```json
{"hostname": "R1", "enabled": true, "interfaces": ["G0/0", "G0/1"]}
```

- A) "true" (string)
- B) true (boolean)
- C) 1 (number)
- D) null

**Answer: B** — The value `true` (without quotes) is a JSON **boolean**. If it were `"true"` (with quotes), it would be a string. JSON booleans are lowercase: `true` or `false`.

---

**6.** In Cisco SD-Access, what is the term for the combination of the physical underlay network and the virtual overlay network?

- A) The controller
- B) The fabric
- C) The VXLAN
- D) The LISP domain

**Answer: B** — The **fabric** is the combination of the **underlay** (physical network) and the **overlay** (virtual network). VXLAN provides the data plane for the overlay; LISP provides the control plane.

---

**7.** A company wants to use a configuration management tool that is agentless, uses SSH, and pushes configurations to devices. Which tool should they choose?

- A) Puppet
- B) Chef
- C) Ansible
- D) Cisco DNA Center

**Answer: C** — **Ansible** is the only tool that is **agentless** (uses SSH), uses a **push model**, and is written in Python. Puppet and Chef are agent-based and use a pull model.

---

**8.** An engineer configures Puppet to manage network devices. How do managed devices receive their configurations?

- A) The Puppet Master pushes configs via SSH
- B) Managed devices pull configs from the Puppet Master via TCP 8140
- C) Managed devices pull configs via TCP 10002
- D) The Puppet Master pushes configs via NETCONF

**Answer: B** — Puppet uses a **pull model**. Managed devices (with Puppet agent software installed) pull their configurations from the **Puppet Master** via **TCP port 8140**. TCP 10002 is used by Chef.

---

**9.** In a traditional network, an engineer communicates with network devices using SSH to configure them individually. In an SDN architecture with DNA Center, how does the engineer communicate their desired network behavior?

- A) SSH to each device individually
- B) Through the DNA Center GUI or REST API (NBI); DNA Center configures devices via the SBI
- C) Through the SBI using OSPF messages
- D) By directly modifying the ASIC firmware on each device

**Answer: B** — In SDN with DNA Center, the engineer communicates their **intent** through the **NBI** (GUI or REST API). DNA Center then translates this intent into device configurations and pushes them to devices via the **SBI** (NETCONF, RESTCONF, SSH). This is Intent-Based Networking (IBN).

---

**10.** Which of the following correctly describes the relationship between Ansible file types? (Select the BEST answer)

- A) Playbooks define the automation logic (YAML); templates provide config structure (Jinja2); variables provide specific values (YAML); inventory lists managed devices
- B) Playbooks list managed devices; templates define automation logic; variables are written in Ruby
- C) Manifests define automation logic; cookbooks provide templates; run-lists list devices
- D) Recipes define automation logic; playbooks list variables; inventory uses XML

**Answer: A** — In Ansible: **Playbooks** (YAML) define the automation tasks and logic. **Templates** (Jinja2) are config files with variable placeholders. **Variables** (YAML) provide specific values substituted into templates. **Inventory** files list the managed devices. Options C and D mix Puppet/Chef terminology with Ansible.
