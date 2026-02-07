import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------- LOAD CSV ----------
df = pd.read_csv("6_enu_log.csv", skipinitialspace=True)

# pulizia nomi colonne
df.columns = df.columns.str.strip()

# tempo
df["datetime"] = pd.to_datetime(df["date"] + " " + df["UTC"],
                                 dayfirst=True)

# ---------- FUNZIONI ----------
def compute_metrics(group):
    # rimuove offset medio (errore relativo)
    e = group["E[cm]"] - group["E[cm]"].mean()
    n = group["N[cm]"] - group["N[cm]"].mean()
    u = group["U[cm]"] - group["U[cm]"].mean()

    r = np.sqrt(e**2 + n**2)

    metrics = {
        "CEP50": np.percentile(r, 50),
        "CEP95": np.percentile(r, 95),
        "RMS_H": np.sqrt(np.mean(r**2)),
        "STD_U": np.std(u),
        "samples": len(group),
    }
    return pd.Series(metrics)

metrics = df.groupby("cycle").apply(compute_metrics)
print(metrics)

# ---------- PLOT SCATTER EN ----------
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

# ---------- CONVERGENZA ----------
df["r"] = np.sqrt(
    (df["E[cm]"] - df["E[cm]"].mean())**2 +
    (df["N[cm]"] - df["N[cm]"].mean())**2
)

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
