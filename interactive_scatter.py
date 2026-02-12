from pathlib import Path
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback_context
import logging

# ---------------------------
# CONFIGURATION
# ---------------------------
CONFIG = {
    "csv_file": "7_enu_log.csv",
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------
# LOAD DATA
# ---------------------------
def load_data(filepath):
    """Load and preprocess CSV data."""
    if not Path(filepath).exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    df = pd.read_csv(filepath, skipinitialspace=True)
    df.columns = df.columns.str.strip()
    
    logger.info(f"Loaded {len(df)} records from {filepath}")
    return df

# Load data
df = load_data(CONFIG["csv_file"])
cycles = sorted(df["cycle"].unique())

# ---------------------------
# DASH APP
# ---------------------------
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Dispersione EN per Ciclo - Vista Interattiva", 
            style={'textAlign': 'center'}),
    
    html.Div([
        html.Label("Seleziona i cicli da visualizzare:", 
                   style={'fontWeight': 'bold', 'marginBottom': '10px'}),
        
        html.Div([
            html.Button("Seleziona Tutti", id="select-all", 
                       style={'marginRight': '10px'}),
            html.Button("Deseleziona Tutti", id="deselect-all"),
        ], style={'marginBottom': '15px'}),
        
        dcc.Checklist(
            id='cycle-checklist',
            options=[{'label': f' Ciclo {cycle}', 'value': cycle} for cycle in cycles],
            value=cycles,  # All selected by default
            inline=True,
            style={'columnCount': 4}
        ),
    ], style={'padding': '20px', 'backgroundColor': '#f0f0f0', 'marginBottom': '20px'}),
    
    dcc.Graph(id='scatter-plot', style={'height': '70vh'}),
    
    html.Div(id='info-box', style={
        'padding': '15px', 
        'backgroundColor': '#e8f4f8',
        'marginTop': '20px',
        'borderRadius': '5px'
    })
])

@app.callback(
    Output('cycle-checklist', 'value'),
    [Input('select-all', 'n_clicks'),
     Input('deselect-all', 'n_clicks')],
    prevent_initial_call=True
)
def update_checklist(select_all_clicks, deselect_all_clicks):
    """Handle select all / deselect all buttons."""
    ctx = callback_context
    if not ctx.triggered:
        return cycles
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'select-all':
        return cycles
    elif button_id == 'deselect-all':
        return []
    
    return cycles

@app.callback(
    [Output('scatter-plot', 'figure'),
     Output('info-box', 'children')],
    [Input('cycle-checklist', 'value')]
)
def update_graph(selected_cycles):
    """Update scatter plot based on selected cycles."""
    if not selected_cycles:
        # Empty plot if no cycles selected
        fig = go.Figure()
        fig.update_layout(
            title="Dispersione EN per ciclo",
            xaxis_title="East [cm]",
            yaxis_title="North [cm]",
            annotations=[{
                'text': 'Seleziona almeno un ciclo per visualizzare i dati',
                'xref': 'paper',
                'yref': 'paper',
                'x': 0.5,
                'y': 0.5,
                'showarrow': False,
                'font': {'size': 16}
            }]
        )
        info_text = "Nessun ciclo selezionato"
        return fig, info_text
    
    # Filter data
    df_filtered = df[df['cycle'].isin(selected_cycles)]
    
    # Create figure
    fig = go.Figure()
    
    # Define color palette
    colors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
    ]
    
    for i, cycle in enumerate(selected_cycles):
        df_cycle = df_filtered[df_filtered['cycle'] == cycle]
        
        fig.add_trace(go.Scatter(
            x=df_cycle['E[cm]'],
            y=df_cycle['N[cm]'],
            mode='markers',
            name=f'Ciclo {cycle}',
            marker=dict(
                size=6,
                color=colors[i % len(colors)],
                opacity=0.6
            ),
            hovertemplate='<b>Ciclo %{text}</b><br>E: %{x:.2f} cm<br>N: %{y:.2f} cm<extra></extra>',
            text=[cycle] * len(df_cycle)
        ))
    
    fig.update_layout(
        title=f"Dispersione EN per ciclo ({len(selected_cycles)} cicli selezionati)",
        xaxis_title="East [cm]",
        yaxis_title="North [cm]",
        hovermode='closest',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    # Calculate info for selected cycles
    total_points = len(df_filtered)
    e_range = df_filtered['E[cm]'].max() - df_filtered['E[cm]'].min()
    n_range = df_filtered['N[cm]'].max() - df_filtered['N[cm]'].min()
    
    info_text = html.Div([
        html.Strong(f"Cicli selezionati: "),
        html.Span(f"{', '.join(map(str, selected_cycles))}"),
        html.Br(),
        html.Strong(f"Punti totali: "),
        html.Span(f"{total_points}"),
        html.Br(),
        html.Strong(f"Range E: "),
        html.Span(f"{e_range:.2f} cm"),
        html.Span(" | "),
        html.Strong(f"Range N: "),
        html.Span(f"{n_range:.2f} cm"),
    ])
    
    return fig, info_text

# ---------------------------
# RUN APP
# ---------------------------
if __name__ == '__main__':
    logger.info("Starting interactive scatter plot...")
    logger.info("Open http://127.0.0.1:8050 in your browser")
    app.run(debug=True, port=8050)
