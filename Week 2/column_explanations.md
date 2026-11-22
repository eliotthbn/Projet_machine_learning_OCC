# Column explanations
 
One row = one captured network packet. After removing the 246 rows with no label, the dataset has **222,567 rows and no missing values**.
 
The table below lists the columns of `df`, the dataframe given to the model. All of them are numeric.

## TCP part
 
| Column | What it is |
|---|---|
| `tcp_len` | Size of the data carried by the TCP packet, in bytes (TCP header excluded), i.e. the size of the MQTT message. Legitimate PUBLISH packets are around 610 bytes; the DoS CONNECT packets are 39 bytes |
| `tcp_flags_int` | TCP flags byte, converted from hex to decimal. Each flag adds its weight: FIN 1, SYN 2, RST 4, PSH 8, ACK 16. Examples: `24` = ACK + PSH (data sent), `25` = ACK + PSH + FIN (data + connection close), `16` = ACK only (plain acknowledgment) |
 
## MQTT part: message header
 
| Column | What it is |
|---|---|
| `mqtt_hdrflags_int` | First byte of every MQTT packet, converted to decimal. Left 4 bits = message type, right 4 bits = options (DUP, QoS, RETAIN). Example: `53` = PUBLISH with QoS 2, `16` = CONNECT |
| `mqtt_msg_type` | Message type, extracted from the byte above: `mqtt_hdrflags_int // 16`. 1 = CONNECT, 2 = CONNACK, 3 = PUBLISH, 4 = PUBACK, 8 = SUBSCRIBE, 9 = SUBACK, 12 = PINGREQ, 13 = PINGRESP, 14 = DISCONNECT |
| `mqtt_dupflag` | 1 = the message is a resend of a previous one, 0 otherwise |
| `mqtt_qos` | Delivery guarantee level: 0 = at most once, 1 = at least once, 2 = exactly once. The value 3 is forbidden by the MQTT standard → malformed packet |
 
## MQTT part: connection
 
These columns only carry information on connection packets (CONNECT / CONNACK); they are 0 on all other packets.
 
| Column | What it is |
|---|---|
| `mqtt_conflags_int` | Connection options sent by the client in a CONNECT, converted to decimal: username 128, password 64, will retain 32, will QoS 16 and 8, will flag 4, clean session 2. Example: `130` = username + clean session |
| `mqtt_conflag_cleansess` | 1 = the client asks for a fresh session (bit "clean session" of the byte above) |
| `mqtt_kalive` | Keep alive, in seconds: maximum time the client may stay silent before the broker closes the connection. Only set in CONNECT packets; 60 s in the observed DoS connections |
| `mqtt_conack_flags_int` | Broker's answer to a connection (CONNACK). Only bit 0 is used: 1 = the broker already had a session for this client |
 
## Other columns
 
| Column | What it is |
|---|---|
| `mqtt_msg` | Numeric value linked to the message. It increases by 1 from one packet to the next (37372, 37373, 37374…) and is 0 on CONNECT packets, so it looks like a counter or ID. **Its exact meaning is still to be checked**, and if it follows packet order it may leak time information like `timestamp` |
| `target` | Value to predict: 0 = legitimate traffic, 1 = attack (dos, flood, bruteforce, slowite or malformed). Built from the original `label` column | 
 

# `df_bis`: columns for human reading
 
`df_bis` has the same 222,567 rows as `df`, in the same order, and no missing values. It is **never given to the model**: it keeps the columns that would cause leakage, and readable versions of the protocol fields, so a human can check what each packet is.
 
| Column | What it is | Why it is not in `df` |
|---|---|---|
| `timestamp` | Packet capture time (Unix time, in seconds) | Time leakage: attacks were injected during specific time windows, so the model could learn *when* instead of *how* |
| `tcp_time_delta` | Supposed to be the time since the previous packet, but contains exactly the same value as `timestamp` | Same leakage as `timestamp`, and useless as is |
| `mqtt_msg_type_str` | Message type as text: CONNECT, CONNACK, PUBLISH, PUBACK, SUBSCRIBE, SUBACK, PINGREQ, PINGRESP, DISCONNECT, or OTHER for any other value | Text version of `mqtt_msg_type`, for reading only |
| `tcp_flags_strings` | TCP flags as text, e.g. `ACK PSH` for 24 | Text version of `tcp_flags_int`, for reading only |
| `mqtt_conflags_strings` | Connection options as text, e.g. `USER CLEAN_SESS` for 130, `NONE` when no option is set (all non-CONNECT packets) | Text version of `mqtt_conflags_int`, for reading only. Will QoS bits are not decoded |
| `label` | Original label: legitimate, dos, flood, bruteforce, slowite or malformed | Replaced in `df` by the binary `target`; kept to analyse errors per attack type later |
 
The raw hex columns (`tcp_flags`, `mqtt_hdrflags`, `mqtt_conflags`, `mqtt_conack_flags`) are in neither dataframe: they were replaced by their `_int` version in `df`.
 