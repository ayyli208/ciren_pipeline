import pandas as pd
from pathlib import Path

# change this to the folder containing the CSVs files from the simulations you ran
folder = Path("./umtri_behavioral_safety_assessment/lane_departure_same")

# optional: set masses (kg)
m_av = 1500        # AV mass
m_ch = 1500        # challenger mass (change if needed)

results = []

for i in range(46):
    csv_path = folder / f"{i}.csv"
    
    df = pd.read_csv(csv_path)
    last = df.iloc[-1]   # last row
    
    # extract speeds
    v_av = last["AV sp"]
    v_ch = last["challenger sp"]
    timestamp = last["timestamp"]
    
    # conservation of momentum
    v_final = (m_av * v_av + m_ch * v_ch) / (m_av + m_ch)
    delta_v_av = v_final - v_av
    delta_v_ch = v_final - v_ch
    
    results.append({
        "case": i,
        "timestamp": timestamp,
        "AV_sp": v_av,
        "challenger_sp": v_ch,
        "v_final": v_final,
        "delta_v_AV": delta_v_av,
        "delta_v_challenger": delta_v_ch
    })

# combine all cases into one dataframe
results_df = pd.DataFrame(results)

# save if needed
results_df.to_csv("delta_v_results.csv", index=False)
