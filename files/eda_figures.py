import pandas as pd, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("MQTTEEB-D_cleaned_data.csv", low_memory=False)
d = df.dropna(subset=["label"]).copy()
order = ["legitimate", "dos", "slowite", "malformed", "bruteforce", "flood"]
d["t"] = (d.timestamp - d.timestamp.min()) / 3600

# Fig 1 - class distribution
c = d.label.value_counts().reindex(order)
plt.figure(figsize=(7, 4))
plt.bar(c.index, c.values, color="#4C72B0")
for i, v in enumerate(c.values):
    plt.text(i, v, f"{v/len(d)*100:.1f}%", ha="center", va="bottom", fontsize=9)
plt.title("Figure 1 - Class distribution"); plt.ylabel("Number of packets")
plt.xticks(rotation=30); plt.tight_layout(); plt.savefig("fig1_class_distribution.png", dpi=150); plt.close()

# Fig 2 and 3 - boxplots
for name, col, title in [("fig2_tcp_len", "tcp_len", "Figure 2 - TCP payload length by class (log scale)"),
                         ("fig3_mqtt_msg", "mqtt_msg", "Figure 3 - MQTT message field by class (log scale)")]:
    plt.figure(figsize=(7, 4))
    plt.boxplot([np.log1p(d.loc[d.label == k, col]) for k in order], tick_labels=order, showfliers=False)
    plt.title(title); plt.ylabel(f"log(1 + {col})"); plt.xticks(rotation=30)
    plt.tight_layout(); plt.savefig(f"{name}.png", dpi=150); plt.close()

# Fig 4 - TCP flags per class
ct = pd.crosstab(d.label, d.tcp_flags, normalize="index").reindex(order) * 100
ct.plot(kind="bar", stacked=True, figsize=(7, 4), colormap="Set2")
plt.title("Figure 4 - TCP flags distribution by class"); plt.ylabel("% of packets")
plt.xticks(rotation=30); plt.legend(title="tcp_flags"); plt.tight_layout()
plt.savefig("fig4_tcp_flags.png", dpi=150); plt.close()

# Fig 5 - labels over time
codes = d.label.map({k: i for i, k in enumerate(order)})
plt.figure(figsize=(8, 4))
plt.scatter(d.t, codes, s=1, c=codes, cmap="tab10")
plt.yticks(range(len(order)), order); plt.xlabel("Time since start of capture (hours)")
plt.title("Figure 5 - Attack phases over time"); plt.tight_layout()
plt.savefig("fig5_timeline.png", dpi=150); plt.close()

# Fig 6 - correlation of numeric features
num = ["tcp_len", "mqtt_conflag_cleansess", "mqtt_dupflag", "mqtt_kalive", "mqtt_msg", "mqtt_qos", "timestamp", "tcp_time_delta"]
corr = d[num].corr()
plt.figure(figsize=(7, 6)); plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1); plt.colorbar()
plt.xticks(range(len(num)), num, rotation=45, ha="right"); plt.yticks(range(len(num)), num)
plt.title("Figure 6 - Correlation matrix (numeric features)"); plt.tight_layout()
plt.savefig("fig6_correlation.png", dpi=150); plt.close()
print(corr.round(2).to_string())
