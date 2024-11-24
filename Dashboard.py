import dash
from dash import dcc, html
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from flask import Flask
from pyngrok import ngrok, conf

# Charger et parser les données
hover_file = "/content/output/hover_output.txt"
purchase_file = "/content/output/purchase_output.txt"

NGROK_AUTH_TOKEN = "2admtTw8QXIn1bwsHm1fSZB6aIV_54CFAgXPusqebsoX4Zpxq"  # Remplacez par votre authtoken

# Configurer pyngrok avec votre authtoken
conf.get_default().auth_token = NGROK_AUTH_TOKEN


def parse_hover_data(file):
    hover_data = []
    with open(file, 'r') as f:
        for line in f.readlines():
            parts = line.strip().split(" | ")
            timestamp, action, product, count = parts
            hover_data.append({
                "Timestamp": timestamp,
                "Product": product,
                "HoverCount": int(count)
            })
    return pd.DataFrame(hover_data)

def parse_purchase_data(file):
    purchase_data = []
    with open(file, 'r') as f:
        for line in f.readlines():
            parts = line.strip().split(" | ")
            timestamp, action, product, quantity, revenue = parts
            purchase_data.append({
                "Timestamp": timestamp,
                "Product": product,
                "Quantity": int(quantity),
                "Revenue": int(revenue)
            })
    return pd.DataFrame(purchase_data)

hover_df = parse_hover_data(hover_file)
purchase_df = parse_purchase_data(purchase_file)

# Fusionner les DataFrames
merged_df = pd.merge(hover_df, purchase_df, on="Product", how="outer").fillna(0)
merged_df["ConversionRate"] = (merged_df["Quantity"] / merged_df["HoverCount"]).fillna(0) * 100
merged_df["RevenuePerHover"] = (merged_df["Revenue"] / merged_df["HoverCount"]).fillna(0)

# Créer un Flask app
server = Flask(__name__)

# Initialiser l'application Dash
app = dash.Dash(__name__, server=server, url_base_pathname='/')

# Fonction pour convertir un graphique matplotlib en image utilisable par Dash
def fig_to_base64(fig):
    img_buf = BytesIO()
    fig.savefig(img_buf, format="png")
    img_buf.seek(0)
    return base64.b64encode(img_buf.read()).decode()

# Création des graphiques
def create_figures(df):
    fig1, ax1 = plt.subplots(figsize=(7, 5))
    sns.barplot(data=df.sort_values(by="HoverCount", ascending=False), x="HoverCount", y="Product", palette="Blues_d", ax=ax1)
    ax1.set_title("Nombre de Hovers par Produit")
    ax1.set_xlabel("Nombre de Hovers")
    ax1.set_ylabel("Produit")
    
    fig2, ax2 = plt.subplots(figsize=(7, 5))
    sns.barplot(data=df.sort_values(by="Revenue", ascending=False), x="Revenue", y="Product", palette="Greens_d", ax=ax2)
    ax2.set_title("Revenus par Produit")
    ax2.set_xlabel("Revenus")
    ax2.set_ylabel("Produit")
    
    fig3, ax3 = plt.subplots(figsize=(7, 5))
    sns.barplot(data=df.sort_values(by="ConversionRate", ascending=False), x="ConversionRate", y="Product", palette="Oranges_d", ax=ax3)
    ax3.set_title("Taux de Conversion par Produit (%)")
    ax3.set_xlabel("Taux de Conversion (%)")
    ax3.set_ylabel("Produit")
    
    fig4, ax4 = plt.subplots(figsize=(7, 5))
    sns.barplot(data=df.sort_values(by="RevenuePerHover", ascending=False), x="RevenuePerHover", y="Product", palette="Purples_d", ax=ax4)
    ax4.set_title("Revenu par Hover")
    ax4.set_xlabel("Revenu par Hover")
    ax4.set_ylabel("Produit")

    return [
        fig_to_base64(fig1),
        fig_to_base64(fig2),
        fig_to_base64(fig3),
        fig_to_base64(fig4)
    ]

# Créer les graphiques sous forme d'images
figures = create_figures(merged_df)

# Layout de l'application Dash
app.layout = html.Div([
    html.H1("Tableau de Bord des Hovers et Achats", style={"text-align": "center"}),

    # Graphiques
    html.Div([
        html.Div([html.Img(src=f"data:image/png;base64,{figures[0]}")], style={'width': '40%', 'display': 'inline-block'}),
        html.Div([html.Img(src=f"data:image/png;base64,{figures[1]}")], style={'width': '40%', 'display': 'inline-block'})
    ], style={'display': 'flex', 'justify-content': 'center'}),

    html.Div([
        html.Div([html.Img(src=f"data:image/png;base64,{figures[2]}")], style={'width': '40%', 'display': 'inline-block'}),
        html.Div([html.Img(src=f"data:image/png;base64,{figures[3]}")], style={'width': '40%', 'display': 'inline-block'})
    ], style={'display': 'flex', 'justify-content': 'center'})
])

# Ouvrir le tunnel ngrok
public_url = ngrok.connect(8050)
print(' * Tunnel ouvert à %s' % public_url)

# Lancer l'application
if __name__ == "__main__":
    app.run_server(debug=True)
