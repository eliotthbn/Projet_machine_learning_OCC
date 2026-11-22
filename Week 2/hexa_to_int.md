# Hexa to int
 
## 1. TCP — `tcp_flags`
 
| Hex | Int | Flags | Rows |
|---|---|---|---|
| 0x0018 | 24 | ACK + PSH | 204,477 |
| 0x0019 | 25 | ACK + PSH + FIN | 17,818 |
| 0x0010 | 16 | ACK | 518 |
 
---
 
## 2. MQTT — `mqtt_hdrflags` (Fixed header)
 
| Hex | Int | Type | Flags |
|---|---|---|---|
| 0x10 | 16 | CONNECT | — | 
| 0x34 | 52 | PUBLISH | QoS 2 |
| 0x30 | 48 | PUBLISH | QoS 0 |
| 0x35 | 53 | PUBLISH | QoS 2 + RETAIN |
| 0xe0 | 224 | DISCONNECT | — |
| 0x3c | 60 | PUBLISH | DUP + QoS 2 |
| 0x20 | 32 | CONNACK | — |
 
---
 
## 3. MQTT — `mqtt_conflags` (Connect flags)
 
| Hex | Int | Flags |
|---|---|---|
| 0x82 | 130 | USER + CLEAN_SESS |
| 0 | 0 | NONE (not a CONNECT) |
| 0x02 | 2 | CLEAN_SESS |
| 0xf2 | 242 | USER + PASS + WILL_RET + WILL_QOS 2 + CLEAN_SESS |
 
---
 
## 4. MQTT — `mqtt_conack_flags` (Connect Acknowledge flags)
 
| Hex | Int | Meaning |
|---|---|---|
| 0 | 0 | No session present / not a CONNACK |
| 0x20, 0x4a, 0x57, 0x59, 0x61 … 0x79 | 32 – 121 | Invalid values |
 
> ⚠️ The 143 non-zero values are also ASCII codes (`u`, `o`, `a`, `h`, space…), so they are probably parsing errors. They set reserved bits and should be treated as anomalies.
 