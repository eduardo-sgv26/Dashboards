from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# Crear una aplicación Dash
app = Dash(__name__)

# Leer los datos
df = pd.read_csv('titanic.csv')

# Calcular estadísticas
media = df["Age"].mean()
moda = df["Age"].mode()[0]

# Diseño de la aplicación
app.layout = html.Div([
    html.H1("Dashboard Interactivo"),

    # Selector de categorías
    html.Label("Selecciona una categoría:"),
    dcc.Dropdown(
        id="categoria-dropdown",
        options=[{"label": cat, "value": cat} for cat in df["Sex"].unique()],
        value="male",
        clearable=False
    ),

    # Estadísticas
    html.Div([
        html.H3("Estadísticas"),
        html.P(f"Media de la edad de pasajeros: {media:.2f}"),
        html.P(f"Moda de la edad de pasajeros: {moda:.2f}"),
        html.P(f"Sobrevivientes: {df['Survived'].value_counts().to_dict()}")
    ]),

    # Gráficas
    dcc.Graph(id="bar-chart"),
    dcc.Graph(id="pie-chart"),
    dcc.Graph(id="scatter-plot")
])

# Callback para actualizar las gráficas en función de la categoría seleccionada
@app.callback(
    [
        Output("bar-chart", "figure"),
        Output("pie-chart", "figure"),
        Output("scatter-plot", "figure")
    ],
    [Input("categoria-dropdown", "value")]
)
def update_graphs(selected_category):
    filtered_df = df[df["Sex"] == selected_category]

    # Gráfico de barras
    bar_fig = px.bar(filtered_df, x="Pclass", y="Age", color="Survived", 
                     title="Edades por Clase y Supervivencia")

    # Gráfico de pastel
    pie_fig = px.pie(filtered_df, names="Survived", title="Distribución de Supervivencia", color_discrete_map={0: "No sobrevivió", 1: "Sobrevivió"})


    # Gráfico de dispersión
    scatter_fig = px.scatter(filtered_df, x="Age", y="Fare", color="Pclass", 
                              title="Edad vs Tarifa por Clase")

    return bar_fig, pie_fig, scatter_fig

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run_server(debug=True)

