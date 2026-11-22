# MQTT Intrusion Detection with Machine Learning

Can a model tell if an MQTT packet is normal traffic or an attack? That's what we try to answer here, using real traffic from a healthcare IoT network.

This is an academic project, the time given to realise it was 4 weeks.

**Team (A4 ESILV, OCC):** Eliott H., Maxence M., Regis S., Mayeul D.

---

## 1. The dataset

We use MQTTEEB-D, published on Mendeley Data. It was captured in a real lab (EEB lab, International University of Rabat) where health sensors send data through a Raspberry Pi 4 to a ThingsBoard server. Attacks were launched on this setup while PyShark recorded every packet.

We work with `MQTTEEB-D_cleaned_data.csv`:

- 222,813 packets, 13 columns
- 12 features from the TCP and MQTT headers (`tcp_len`, `tcp_flags`, `mqtt_msg`, `mqtt_qos`, ...)
- 1 `label` column: legitimate traffic or one of 5 attacks

| Class | Share | What it is |
|---|---|---|
| malformed | 47.4% | Corrupted packets sent to break the broker |
| dos | 18.8% | Flood of connections and messages |
| bruteforce | 12.3% | Guessing usernames and passwords |
| slowite | 9.0% | Slow DoS: many connections, very little data |
| legitimate | 7.9% | Normal traffic |
| flood | 4.6% | Huge payloads to overload the broker |

 note : The data is very imbalanced, and attacks are the majority. 

**What we did to the data (Week 2):**

- Removed 246 rows with no label.
- Removed `timestamp` and `tcp_time_delta` so the model can't learn when attacks happened (data leakage).
- Removed duplicates. Once the time columns are gone, 85% of rows are duplicates. We kept **33,107 rows**.
- Converted the hexadecimal columns to integers.
- Made the target binary: `0` = legitimate, `1` = attack.

The result is saved in `Dataset/MQTTEEB-D_int.csv`.

---

## 2. Install and run the project

Using Python 3 and these libraries:

```bash
git clone https://github.com/eliotthbn/Projet_machine_learning_OCC.git
cd Projet_machine_learning_OCC

python -m venv .venv
source .venv/bin/activate        

pip install pandas matplotlib scikit-learn notebook
jupyter notebook
```

Run in order :

1. `Week 1/EDA.ipynb`
2. `Week 2/Week2.ipynb` 

---
 
## 3. Repository structure
 
```
Projet_machine_learning_OCC/
├── Dataset/
│   ├── MQTTEEB-D_cleaned_data.csv   # original cleaned data (222,813 rows)
│   └── MQTTEEB-D_int.csv            # our prepared data (33,107 rows, numeric)
├── Week 1/
│   ├── EDA.ipynb                    # first exploration
│   ├── fig1_class_distribution.png
│   ├── goals.md
│   └── Projet_Machine_Learning_A4_OCC_Week-1.pdf
├── Week 2/
│   ├── Week2.ipynb                  # cleaning, split, baseline
│   ├── goals.md
│   └── week2.pdf
├── Week 3/
│   ├── Week3.ipynb                  # models and experiments
│   └── goals.md
├── Week 4/
│   └── goals.md                     # final evaluation and presentation
└── README.md
```
 
---
 
## 4. Summary of the 4 weeks
 
**Week 1: Project definition and data.**
We picked the topic (intrusion detection on MQTT), wrote the research question, downloaded MQTTEEB-D and ran a first exploration: structure, missing values, class distribution.
 
**Week 2: Data preparation and baseline.**
We cleaned the data as described above, split it 75% train / 25% test (stratified, `random_state=42`), and scaled it with `StandardScaler` fitted on the train set only. Our baseline is a **logistic regression** with balanced class weights. We only use a train/test split for now, since a baseline doesn't need a validation set.
 
| Metric | Baseline |
|---|---|
| Accuracy | 0.798 |
| Balanced accuracy | 0.716 |
| Precision | 0.924 |
| Recall | 0.832 |
| F1-score | 0.876 |
 
On the test set, 1185 attacks were missed and 484 legitimate packets were flagged as attacks.
 
**Week 3: Model development and experimentation (not done yet).**
Goals: implement and train one or more models, try feature selection and hyperparameter tuning, compare with the baseline, and analyse errors and limits.
 
**Week 4: Evaluation and final presentation (not done yet).**
Goals: finish the experiments, compare and interpret the models, discuss limits and improvements, then write the final report and present the project.
 
---
 
## 5. References
 
- **Dataset:** MQTTEEB-D, Aqachtoul et al., Mendeley Data. https://data.mendeley.com/datasets/jfttfjn6tr/2
- **Scientific article:** https://pmc.ncbi.nlm.nih.gov/articles/PMC12332880/
