import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#app = dash.Dash(__name__)

df_SECOP = pd.read_csv('Datos_SECOP_LT.csv', 
                 sep = ',',
                 index_col=0,
                 dtype={
                     'Nit Entidad': str
                 })


df_SECOP_query = df_SECOP[["Entidad","Ciudad Entidad","Adjudicado","Valor Total Adjudicacion"]]

available_ciudades = df_SECOP['Ciudad Entidad'].unique()
available_tipo_contrato = df_SECOP["Tipo de Contrato"].unique()
available_Mod_contrato = df_SECOP["Modalidad de Contratacion"].unique()

  
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
    html.Div([
        html.Div([
            html.H1(children='Gráfico 1'),#
            html.Div(children='''
                Otro ejemplo
            '''),#
            dcc.Dropdown(
                id='crossfilter_ciudad',
                options=[{'label': i, 'value': i} for i in available_ciudades],
                value='Bogotá'
            ),
            dcc.Graph(
                id='example-graph-1'
            ),  
        ], className='six columns'),
        html.Div([
            html.Table([
                html.Thead(
                    html.Tr([html.Th(col) for col in df_SECOP_query.columns])
                ),
                html.Tbody([
                    html.Tr([
                        html.Td(df_SECOP_query.iloc[i][col]) for col in df_SECOP_query.columns
                    ]) for i in range(min(len(df_SECOP_query), 5))
                ])
            ]),
        ], className='six columns'),
    ], className='row'),

    html.H4(children='US Agriculture Exports (2011)'),

    html.Div([
        html.Div([
            html.H1(children='Gráfico 2'),#
            html.Div(children='''
                Otro ejemplo
            '''),#
            dcc.Checklist(id='crossfilter_tipo_contrato1',
                options=[{'label': i, 'value': i} 
                            for i in available_tipo_contrato],
                value = ['Suministros','Consultoría'],
                labelStyle={'display': 'inline-block'}
                ),
            dcc.Graph(
                id='example-graph-2'
            ),  
        ], className='six columns'),
        html.Div([
            html.H1(children='Gráfico 3'),#
            html.Div(children='''
                
                Tipo de Contrato
            
            '''),#
            dcc.Dropdown(
                id='crossfilter_tipo_contrato2',
                 options=[{'label': x, 'value': x} 
                            for x in available_tipo_contrato],
                value = ['Suministros','Consultoría'],
                multi = True
                ),
            html.Div(children='''
                
                Modalidad de contratación
            
            '''),#
            dcc.Dropdown(
                id='crossfilter_mod_contrato',
                 options=[{'label': x, 'value': x} 
                            for x in available_Mod_contrato],
                value = ['Concurso de méritos abierto', 'Licitación pública Obra Publica'],
                multi = True
                ),
            dcc.Graph(
                id='example-graph-3'
            ),  
        ], className='six columns'),
    ], className='row'),#
                 

])

## Viz 1
@app.callback(
    dash.dependencies.Output('example-graph-1', 'figure'),
    [dash.dependencies.Input('crossfilter_ciudad', 'value')]
    )

def update_graph(ciudad_value):
    df_SECOP_ciudad = df_SECOP[df_SECOP['Ciudad Entidad'] == ciudad_value]

    fig = px.treemap(df_SECOP_ciudad, path=['Tipo de Contrato','OrdenEntidad'],
                 values='Valor Total Adjudicacion',
                )

    return fig   

## Viz 2

@app.callback(
    dash.dependencies.Output('example-graph-2', 'figure'),
    [dash.dependencies.Input('crossfilter_tipo_contrato1', 'value')]
    )
def update_graph(tipo_contrato_value):

    query1 = df_SECOP[df_SECOP['Tipo de Contrato'].isin(tipo_contrato_value)]
    query1 = pd.pivot_table(query1, 
                        values='Precio Base', 
                        index=['Tipo de Contrato','OrdenEntidad'],
                        aggfunc=np.sum)
    query1 = query1.reset_index().rename_axis(None, axis=1)
    query1 = query1.sort_values(by=['Precio Base'],ascending=False)

    fig2 = px.bar(query1, x='Precio Base', y='Tipo de Contrato', color = 'OrdenEntidad')

    return fig2

## Viz 3 
@app.callback(
    dash.dependencies.Output('example-graph-3', 'figure'),
    [dash.dependencies.Input('crossfilter_tipo_contrato2', 'value'),
     dash.dependencies.Input('crossfilter_mod_contrato', 'value')]
    )

def update_graph(tipo_contrato_value, tipo_mod_contrato):
    query2 = df_SECOP[df_SECOP['Tipo de Contrato'].isin(tipo_contrato_value)]
    query2 = query2[query2['Modalidad de Contratacion'].isin(tipo_mod_contrato)]
    
    query2 = pd.crosstab(query2["Modalidad de Contratacion"],query2["Tipo de Contrato"])
    query2

    fig3 = px.imshow(query2)

    return fig3


if __name__ == "__main__":
    app.run_server(debug=True)
