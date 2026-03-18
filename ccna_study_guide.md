# CCNA 200-301 — Hoc Nhanh Voi AI Claude
## Huong Dan Day Du — Jeremy's IT Lab Course

---

## 1. TONG QUAN KHOA HOC

Jeremy's IT Lab CCNA 200-301 gom 63 "Days", moi Day co lecture + lab (tong ~126 clips).
Da co san course notes tren GitHub: https://github.com/psaumur/CCNA_Course_Notes

### Cau Truc Khoa Hoc Theo CCNA Exam Domains:

| Exam Domain | Ty Trong | Cac Day Lien Quan |
|---|---|---|
| **1. Network Fundamentals (20%)** | ★★★★ | Day 1-15 (Devices, Cables, OSI, IPv4, Subnetting) |
| **2. Network Access (20%)** | ★★★★ | Day 16-23 (VLANs, STP, EtherChannel) |
| **3. IP Connectivity (25%)** | ★★★★★ | Day 11-12, 24-29 (Routing, OSPF, FHRP) |
| **4. IP Services (10%)** | ★★ | Day 30-47 (TCP/UDP, IPv6, NAT, DHCP, DNS, QoS) |
| **5. Security Fundamentals (15%)** | ★★★ | Day 48-51, 55-58 (ACLs, Port Security, Wireless) |
| **6. Automation & Programmability (10%)** | ★★ | Day 59-63 (APIs, SDN, Ansible) |

---

## 2. QUY TRINH HOC NHANH NHAT (3 Buoc)

### Buoc 1: Lay Transcript Tu Dong
Chay script `extract_transcripts.py` tren may tinh ca nhan:
```
pip install youtube-transcript-api pytubefix
python extract_transcripts.py
```
→ Tao thu muc `ccna_transcripts/` chua 126 file .txt

### Buoc 2: Hoc Tung Nhom Voi Claude
Moi lan paste 2-3 transcript vao Claude, dung prompt template ben duoi.

### Buoc 3: On Tap Va Thi Thu
Dung Claude tao quiz, flashcard, va mo phong cau hoi thi.

---

## 3. PROMPT TEMPLATES CHO TUNG GIAI DOAN

### 3.1 — Tom Tat Nhanh (Dung Khi Muon Nám Tong Quan)

```
Toi dang hoc CCNA 200-301 voi Jeremy's IT Lab.
Day la transcript cua [Day X: Ten Bai]:

[PASTE TRANSCRIPT]

Hay:
1. Tom tat 5-7 y chinh quan trong nhat
2. Liet ke cac Cisco IOS commands duoc nhac den (neu co)
3. Giai thich 1 khai niem kho hieu nhat bang vi du thuc te
4. Tao 5 cau hoi True/False de kiem tra
```

### 3.2 — Hoc Sau (Dung Cho Cac Chu De Trong Tam)

```
Toi dang hoc CCNA 200-301, phan [OSPF / STP / Subnetting / ...].
Day la transcript:

[PASTE TRANSCRIPT]

Hay giup toi:
1. Giai thich khai niem nhu dang giai thich cho nguoi chua biet gi ve networking
2. Ve mot kich ban mang thuc te ap dung khai niem nay
3. Liet ke day du cac commands va giai thich tung command
4. So sanh voi cac protocol/technology tuong tu (neu co)
5. 10 cau hoi dang CCNA exam (multiple choice) voi giai thich dap an
```

### 3.3 — Lab Review (Dung Sau Khi Lam Lab)

```
Toi vua hoan thanh lab [Ten Lab] trong CCNA course.
Day la transcript cua lab walkthrough:

[PASTE TRANSCRIPT]

Hay:
1. Tom tat cac buoc chinh cua lab
2. Tao bang "Command Cheat Sheet" cho lab nay
3. Neu 3 loi thuong gap khi lam lab nay va cach khac phuc
4. Tao 1 bai lab tuong tu nhung khac topology de toi tu luyen
```

### 3.4 — On Tap Theo Domain (Dung Truoc Khi Thi)

```
Toi dang on tap CCNA 200-301, domain [Network Fundamentals / Network Access / ...].
Hay:
1. Liet ke TAT CA cac chu de trong domain nay theo exam blueprint
2. Voi moi chu de, cho 1 cau hoi mau dang exam
3. Danh dau chu de nao thuong bi hoi nhieu nhat
4. Tao 20 cau hoi thi thu cho domain nay (4 lua chon, 1 dap an dung)
5. Giai thich chi tiet tai sao moi dap an dung/sai
```

### 3.5 — Subnetting Drill (Phan Nhieu Nguoi Thay Kho Nhat)

```
Hay tao 10 bai tap subnetting tu de den kho cho CCNA:
- 3 bai Class A/B/C co ban
- 3 bai VLSM
- 2 bai tim subnet, broadcast, host range
- 2 bai troubleshooting (cho IP va mask, hoi loi o dau)

Cho toi lam tung bai, doi toi tra loi roi moi cham va giai thich.
```

### 3.6 — So Sanh Concepts (Cuc Ky Hieu Qua Cho CCNA)

```
Hay tao bang so sanh chi tiet giua:
[Chon 1 trong cac cap duoi]
- OSPF vs EIGRP vs RIP
- TCP vs UDP
- Static NAT vs Dynamic NAT vs PAT
- Standard ACL vs Extended ACL
- RADIUS vs TACACS+
- Trunk vs Access port
- HSRP vs VRRP vs GLBP
- WPA vs WPA2 vs WPA3
- Traditional vs Controller-based networking
- JSON vs XML vs YAML

Bao gom: dinh nghia, use case, uu/nhuoc diem, commands, va cau hoi exam mau.
```

---

## 4. LICH HOC DE XUAT (8-12 Tuan)

### Tuan 1-2: Network Fundamentals (Day 1-10)
- Muc tieu: Hieu OSI model, IPv4, Subnetting co ban
- Trong tam: Day 3 (OSI), Day 7-8 (IPv4), Day 13-15 (Subnetting)
- Bai tap: Subnetting drill moi ngay

### Tuan 3-4: Network Access (Day 16-23)
- Muc tieu: VLANs, STP, EtherChannel
- Trong tam: Day 16-18 (VLANs), Day 20-22 (STP)
- Bai tap: Lab tren Packet Tracer

### Tuan 5-6: IP Connectivity (Day 24-29)
- Muc tieu: Dynamic Routing, OSPF
- Trong tam: Day 26-28 (OSPF) — QUAN TRONG NHAT
- Bai tap: Cau hinh OSPF multi-area

### Tuan 7-8: IP Services + IPv6 (Day 30-47)
- Muc tieu: TCP/UDP, IPv6, NAT, DHCP, QoS
- Trong tam: Day 31-33 (IPv6), Day 44-45 (NAT)
- Bai tap: NAT configuration labs

### Tuan 9-10: Security + Wireless (Day 48-58)
- Muc tieu: ACLs, Port Security, Wireless
- Trong tam: Day 34-35 (ACLs), Day 55-57 (Wireless)
- Bai tap: ACL troubleshooting scenarios

### Tuan 11-12: Automation + Review (Day 59-63)
- Muc tieu: REST APIs, SDN, Ansible + Tong on
- Trong tam: On lai OSPF, Subnetting, STP
- Bai tap: Full practice exams

---

## 5. TAI NGUYEN BO SUNG

### Mien Phi:
- **Course Notes GitHub**: https://github.com/psaumur/CCNA_Course_Notes
  (Clone ve doc offline: git clone https://github.com/psaumur/CCNA_Course_Notes.git)
- **Packet Tracer**: Download tu Cisco NetAcad (mien phi) de lam lab
- **Subnetting Practice**: https://subnetipv4.com
- **Jeremy's Flashcards**: Co trong moi video description

### Dung Claude Hieu Qua:
- Paste transcript + hoi cau hoi cu the → tot hon la hoi chung chung
- Yeu cau Claude tao quiz SAU moi buoi hoc
- Dung Claude de giai thich lai nhung gi chua hieu trong video
- Tao flashcard Anki bang cach yeu cau Claude format san

---

## 6. MEO THI CCNA 200-301

1. **Subnetting** xuat hien o HAU HET cac cau hoi — luyen moi ngay
2. **OSPF** chiem ty trong lon nhat trong IP Connectivity
3. Doc ky **moi tu** trong cau hoi thi — Cisco hay dat bay o chi tiet nho
4. Thoi gian thi: 120 phut, ~100 cau — trung binh 1.2 phut/cau
5. Cac dang cau hoi: Multiple choice, Drag-and-drop, Lab simulation
6. Diem pass: ~825/1000 (khong co thong bao chinh thuc)

---

*Tao boi Claude cho Mike — CCNA 200-301 Study Plan*
*Cap nhat: March 2026*
