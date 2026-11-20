import pandas as pd

df = pd.read_csv("./Dataset/MQTTEEB-D_cleaned_data.csv", low_memory=False)

hex_cols = ["tcp_flags", "mqtt_hdrflags", "mqtt_conflags", "mqtt_conack_flags"]

for col in hex_cols:
    df[col] = df[col].astype(str).apply(lambda x: int(x, 16))

print(df[hex_cols].dtypes)   # -> int64 partout

OUT_PATH = "./Dataset/MQTTEEB-D_int.csv"
df.to_csv(OUT_PATH, index=False)
print(f"Fichier enregistré : {OUT_PATH}")