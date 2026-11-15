"""Quick EDA - MQTTEEB-D cleaned data (run as a script or paste cells into a notebook)."""
import pandas as pd, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PATH = "MQTTEEB-D_cleaned_data.csv"
df = pd.read_csv(PATH, low_memory=False)

# ---- 1. Structure --------------------------------------------------------
print(df.shape); print(df.dtypes); print(df.isna().sum())
print("duplicates:", df.duplicated().sum())
print("timestamp == tcp_time_delta:", (df.timestamp == df.tcp_time_delta).all())
print("sorted by time:", df.timestamp.is_monotonic_increasing)

# ---- 2. Target -----------------------------------------------------------
print(df.label.value_counts(dropna=False))
print((df.label.value_counts(normalize=True) * 100).round(2))

# ---- 3. Features per class ----------------------------------------------
num = ["tcp_len", "mqtt_msg", "mqtt_kalive", "mqtt_qos", "mqtt_conflag_cleansess"]
print(df.groupby("label")[num].agg(["mean", "median"]).round(2))
for c in ["tcp_flags", "mqtt_conflags", "mqtt_hdrflags", "mqtt_qos"]:
    print(pd.crosstab(df.label, df[c]))

# ---- 4. Temporal structure ----------------------------------------------
df["t"] = df.timestamp - df.timestamp.min()
df["segment"] = (df.label != df.label.shift()).cumsum()
print("number of contiguous label segments:", df.segment.nunique())

# ---- 5. Figures ----------------------------------------------------------
order = ["legitimate", "dos", "slowite", "malformed", "bruteforce", "flood"]
fig, ax = plt.subplots(2, 2, figsize=(13, 9))

counts = df.label.value_counts().reindex(order)
ax[0, 0].bar(counts.index, counts.values, color="#4C72B0")
ax[0, 0].set_title("Class distribution"); ax[0, 0].set_ylabel("packets")
for i, v in enumerate(counts.values):
    ax[0, 0].text(i, v, f"{v/len(df)*100:.1f}%", ha="center", va="bottom", fontsize=9)
ax[0, 0].tick_params(axis="x", rotation=30)

for col, a, title in [("tcp_len", ax[0, 1], "tcp_len by class (log)"),
                      ("mqtt_msg", ax[1, 0], "mqtt_msg by class (log1p)")]:
    data = [np.log1p(df.loc[df.label == k, col]) for k in order]
    a.boxplot(data, tick_labels=order, showfliers=False)
    a.set_title(title); a.tick_params(axis="x", rotation=30)

d = df.dropna(subset=["label"])
codes = d.label.map({k: i for i, k in enumerate(order)})
ax[1, 1].scatter(d.t / 3600, codes, s=1, c=codes, cmap="tab10")
ax[1, 1].set_yticks(range(len(order))); ax[1, 1].set_yticklabels(order)
ax[1, 1].set_xlabel("time (hours since start)"); ax[1, 1].set_title("Label over time")

plt.tight_layout(); plt.savefig("eda_mqtteeb.png", dpi=130)
