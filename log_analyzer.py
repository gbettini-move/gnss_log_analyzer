from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import logging

# ---------------------------
# CONFIGURATION
# ---------------------------
CONFIG = {
    "csv_file": "7_enu_log.csv",
    "columns": ["E[cm]", "N[cm]", "U[cm]", "TTSF[s]"],
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------
# LOAD CSV
# ---------------------------
def load_data(filepath):
    """Load and preprocess CSV data."""
    if not Path(filepath).exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    df = pd.read_csv(filepath, skipinitialspace=True)
    df.columns = df.columns.str.strip()
    
    # Validate required columns
    required_cols = ["date", "UTC", "cycle"] + CONFIG["columns"]
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"Missing required columns. Expected: {required_cols}")
    
    df["datetime"] = pd.to_datetime(df["date"] + " " + df["UTC"], dayfirst=True)
    logger.info(f"Loaded {len(df)} records from {filepath}")
    return df

# ---------------------------
# COMPUTE METRICS
# ---------------------------
def add_horizontal_distance(df):
    """Add horizontal distance column."""
    e_centered = df["E[cm]"] - df["E[cm]"].mean() 
    n_centered = df["N[cm]"] - df["N[cm]"].mean()
    df["r"] = np.sqrt(e_centered**2 + n_centered**2)
    return df

def compute_cycle_metrics(group):
    """Compute metrics for a single cycle."""
    e = group["E[cm]"] - group["E[cm]"].mean()
    n = group["N[cm]"] - group["N[cm]"].mean()
    u = group["U[cm]"] - group["U[cm]"].mean()
    r = np.sqrt(e**2 + n**2)
    
    return pd.Series({
        "samples": len(group),
        "mean_E": group["E[cm]"].mean(),
        "mean_N": group["N[cm]"].mean(),
        "mean_U": group["U[cm]"].mean(),
        "CEP50": np.percentile(r, 50),
        "CEP95": np.percentile(r, 95),
        "RMS_H": np.sqrt(np.mean(r**2)),
        "STD_U": np.std(u)
    })

def compute_global_metrics(df):
    """Compute overall metrics."""
    mean_E = df["E[cm]"].mean()
    mean_N = df["N[cm]"].mean()
    mean_U = df["U[cm]"].mean()
    u_all = df["U[cm]"] - mean_U
    mean_TTSF = df["TTSF[s]"].mean()
    
    return {
        "samples": len(df),
        "mean_E": mean_E,
        "mean_N": mean_N,
        "mean_U": mean_U,
        "CEP50": np.percentile(df["r"], 50),
        "CEP95": np.percentile(df["r"], 95),
        "RMS_H": np.sqrt(np.mean(df["r"]**2)),
        "STD_U": np.std(u_all),
        "mean_TTSF": mean_TTSF
    }

# ---------------------------
# MAIN EXECUTION
# ---------------------------
if __name__ == "__main__":
    try:
        df = load_data(CONFIG["csv_file"])
        df = add_horizontal_distance(df)
        
        # Cycle metrics
        cycle_metrics = df.groupby("cycle").apply(compute_cycle_metrics)
        print("\nMetriche per ciclo")
        print(cycle_metrics)
        
        # Global metrics
        global_metrics = compute_global_metrics(df)
        print("\nMetriche globali")
        for k, v in global_metrics.items():
            print(f"{k}: {round(v, 3)}")

        # ---------------------------
        # SCATTER EN
        # ---------------------------
        fig_scatter = px.scatter(
            df,
            x="E[cm]",
            y="N[cm]",
            color="cycle",
            title="Dispersione EN per ciclo"
        )

        fig_scatter.update_layout(
            xaxis_title="East [cm]",
            yaxis_title="North [cm]"
        )

        fig_scatter.show()

        # ---------------------------
        # CONVERGENZA RMS
        # ---------------------------
        df["r_cum_rms"] = np.sqrt(
            (df["r"]**2).expanding().mean()
        )

        fig_conv = px.line(
            df,
            x="datetime",
            y="r_cum_rms",
            title="Convergenza RMS orizzontale"
        )

        fig_conv.show()

        # ---------------------------
        # ANDAMENTO TEMPORALE ENU
        # ---------------------------
        fig_time = px.line(
            df,
            x="datetime",
            y=["E[cm]", "N[cm]", "U[cm]"],
            title="Andamento ENU nel tempo"
        )

        fig_time.show()

        # ---------------------------
        # TTFF E TTSF PER CICLO
        # ---------------------------
        ttff_ttsf = df.groupby("cycle")[["TTFF[s]", "TTSF[s]"]].first().reset_index()

        fig_ttff_ttsf = px.line(
            ttff_ttsf,
            x="cycle",
            y=["TTFF[s]", "TTSF[s]"],
            title="Andamento TTFF e TTSF per ciclo",
            markers=True
        )

        fig_ttff_ttsf.update_layout(
            xaxis_title="Cycle",
            yaxis_title="Time [s]"
        )

        fig_ttff_ttsf.show()

    except Exception as e:
        logger.error(f"Error: {e}")
        raise