import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app = dash.Dash(__name__)

df_SECOP = pd.read_csv('Datos_SECOP_LT.csv', 
                 sep = ',',
                 index_col=0,
                 dtype={
                     'Nit Entidad': str
                 })
df_SECOP_bog = df_SECOP[(df_SECOP["Ciudad Entidad"] == "Bogotá") & (df_SECOP["Adjudicado"] == "Si") ]

### Visualización 1
fig = px.treemap(df_SECOP_bog, path=['Tipo de Contrato','OrdenEntidad'],
                 values='Valor Total Adjudicacion',
                )

### Visualización 2 #  1  # 

#  1  # query1 = pd.pivot_table(df_SECOP_bog, 
#  1  #                         values='Precio Base', 
#  1  #                         index=['Tipo de Contrato','OrdenEntidad'],
#  1  #                         aggfunc=np.sum)
#  1  # query1 = query1.reset_index().rename_axis(None, axis=1)
#  1  # query1 = query1.sort_values(by=['Precio Base'],ascending=False)
#  1  # query1

#  1  # fig2 = px.bar(query1, x='Precio Base', y='Tipo de Contrato', color = 'OrdenEntidad')

### Visualización 3

#  2  # query2 = pd.crosstab(df_SECOP_bog["Modalidad de Contratacion"],df_SECOP_bog["Tipo de Contrato"])
#  2  # query2

#  2  # fig3 = px.imshow(query2)
  
app.layout = html.Div(
    children=[
        html.H1(children="Hola Dash",
            style = {
                        'textAlign': 'center',
            }),
        html.H2(children="Ejemplo 1 Treemap"),
        html.P(
            children="En ésta visualización se puede observar "
            "la distribución del valor adjudicado de los contratos "
            "para Bogotá (entre los años 2018-2020) desagregado por "
            "tipo de contrato y el orden de la entidad."
            ),
    dcc.Graph(
        id='example-graph-1',
        figure=fig
            ),

### Tabla 1 ###
#    html.H4(children='US Agriculture Exports (2011)'),
#    html.Table([
#        html.Thead(
#            html.Tr([html.Th(col) for col in df_SECOP_bog.columns])
#        ),
#        html.Tbody([
#            html.Tr([
#                html.Td(df_SECOP_bog.iloc[i][col]) for col in df_SECOP_bog.columns
#            ]) for i in range(min(len(df_SECOP_bog), 10))
#        ])
#    ]),

### Viz 2 ###
#    html.Div([
#        html.Div([
#            html.H1(children='Gráfico 2'),#
#            html.Div(children='''
#                Otro ejemplo
#            '''),#
#            dcc.Graph(
#                id='example-graph-2',
#                figure=fig2
#            ),  
#        ], className='six columns'),

### Viz 3 ###
#        html.Div([
#            html.H1(children='Gráfico 3'),#
#            html.Div(children='''
#                Y otro ejemplo más
#            '''),#
#            dcc.Graph(
#                id='example-graph-3',
#                figure=fig3
#            ),  
#        ], className='six columns'),
#    ], className='row'),#
#                 

])

if __name__ == "__main__":
    app.run_server(debug=True)
