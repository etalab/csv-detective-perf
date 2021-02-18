import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table

import pandas as pd
import numpy as np

import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


df_rb = pd.read_csv("res_rb.csv")
df_indic_rb = pd.read_csv("analysis_rb.csv")
df_ml = pd.read_csv("res_ml.csv")
df_indic_ml = pd.read_csv("analysis_ml.csv")

list_ct = ['booleen', 'longitude_l93', 'latitude_wgs', 'latitude_wgs_fr_metropole', 'longitude_wgs', 'code_postal', 'code_commune_insee', 'sexe', 'tel_fr', 'adresse', 'code_departement', 'commune', 'iso_country_code', 'year', 'departement', 'csp_insee', 'insee_ape700', 'insee_canton', 'region', 'url', 'code_fantoir', 'siren', 'code_region', 'date', 'longitude_wgs_fr_metropole', 'latlon_wgs', 'datetime_iso', 'code_waldec', 'email', 'uai', 'json_geojson', 'jour_de_la_semaine', 'siret', 'pays', 'date_fr', 'latitude_l93']

vnrb = 'NA'
vprb = 'NA'
fnrb = 'NA'
fprb = 'NA'

vnml = 'NA'
vpml = 'NA'
fnml = 'NA'
fpml = 'NA'

prrb = 'NA'
prml = 'NA'
rerb = 'NA'
reml = 'NA'


app.layout = html.Div([

    html.Div([
        html.H1("Etude sur la performance de CSV Detective"),
        dcc.Markdown('''
            Résultats des tests.
        ''')
    ], style={'float': 'left', 'width': '100%','height':'200px'}),

    html.Div(id="dropdowntypes",children=[
            dcc.Dropdown(
                id='dropdown',
                options=[
                    {'label': i, 'value': i } for i in list_ct
                ],
                value='empty'
            )

    ], style={'float': 'left', 'width': '50%'}),
    html.Br(),
    html.Button('Visualiser nouveau', id='reload-val', n_clicks=0),
    html.Br(),
    html.Div(id='matrix',children=[
        html.Div(id='rbmatrix',children=[
            html.Div(id='VPRB',children=[
                html.P('Vrai Positif : '+vprb)
            ], style={'float': 'left', 'width': '50%','background-color':'#99FE98'}),
            html.Div(id='FPRB',children=[
                html.P('Faux Positif : '+fprb)
            ], style={'float': 'left', 'width': '50%','background-color':'#FF9999'}),
            html.Div(id='FNRB',children=[
                html.P('Faux Négatif : '+fnrb)
            ], style={'float': 'left', 'width': '50%','background-color':'#FF9999'}),
            html.Div(id='VNRB',children=[
                html.P('Vrai Négatif : '+vnrb)
            ], style={'float': 'left', 'width': '50%','background-color':'#99FE98'}),

            html.Div(id='precisionRB',children=[
                html.P('Précision : '+prrb)
            ], style={'float': 'left', 'width': '50%'}),

            html.Div(id='recallRB',children=[
                html.P('Recall : '+rerb)
            ], style={'float': 'left', 'width': '50%'}),


            html.Div([
                dcc.Tabs(id='tabs-example-rb', value='tab-1', children=[
                    dcc.Tab(label='(VN) Bien détecté', value='tab-1-rb'),
                    dcc.Tab(label='(FP) Mal détecté', value='tab-2-rb'),
                    dcc.Tab(label='(FN) Mal exclu', value='tab-3-rb'),
                    dcc.Tab(label='(VN) Bien exclu', value='tab-4-rb'),
                ])
            ], style={'float': 'left', 'width': '100%','margin-top':'30px'}),
            html.Div(id='tabs-example-content-rb')

        ], style={'float': 'left', 'width': '45%'}),


        html.Div(id='mlmatrix',children=[
            html.Div(id='VPML',children=[
                html.P('Vrai Positif : '+vpml)
            ], style={'float': 'left', 'width': '50%','background-color':'#99FE98'}),
            html.Div(id='FPML',children=[
                html.P('Faux Positif : '+fpml)
            ], style={'float': 'left', 'width': '50%','background-color':'#FF9999'}),
            html.Div(id='FNML',children=[
                html.P('Faux Négatif : '+fnml)
            ], style={'float': 'left', 'width': '50%','background-color':'#FF9999'}),
            html.Div(id='VNML',children=[
                html.P('Vrai Négatif : '+vnml)
            ], style={'float': 'left', 'width': '50%','background-color':'#99FE98'}),

            html.Div(id='precisionML',children=[
                html.P('Précision : '+prml)
            ], style={'float': 'left', 'width': '50%'}),

            html.Div(id='recallML',children=[
                html.P('Recall : '+reml)
            ], style={'float': 'left', 'width': '50%'}),


            html.Div([
                dcc.Tabs(id='tabs-example-ml', value='tab-1', children=[
                    dcc.Tab(label='(VN) Bien détecté', value='tab-1-ml'),
                    dcc.Tab(label='(FP) Mal détecté', value='tab-2-ml'),
                    dcc.Tab(label='(FN) Mal exclu', value='tab-3-ml'),
                    dcc.Tab(label='(VN) Bien exclu', value='tab-4-ml'),
                ])
            ], style={'float': 'left', 'width': '100%','margin-top':'30px'}),
            html.Div(id='tabs-example-content-ml')

        ], style={'float': 'left', 'width': '45%','margin-left':'10%'}),
       html.Br(),
       html.Br(),

    ], style={'float': 'left', 'width': '100%', 'margin-top':'30px'}),


    
],style={'width':'1200px','margin':'auto'})

@app.callback(dash.dependencies.Output('VPRB', 'children'),
dash.dependencies.Input('dropdown','value'))
def render_matrixes_vprb(value):
    try:
        out = df_indic_rb[df_indic_rb['column_type'] == value]['vrai_positif'].iloc[0]
    except:
        out = 'NA'
    return html.P('Vrai Positif : '+str(out))


@app.callback(dash.dependencies.Output('FNRB', 'children'),
dash.dependencies.Input('dropdown','value'))
def render_matrixes_fnrb(value):
    try:
        out = df_indic_rb[df_indic_rb['column_type'] == value]['faux_negatif'].iloc[0]
    except:
        out = 'NA'
    return html.P('Faux Négatif : '+str(out))


@app.callback(dash.dependencies.Output('VNRB', 'children'),
dash.dependencies.Input('dropdown','value'))
def render_matrixes_vnrb(value):
    try:
        out = df_indic_rb[df_indic_rb['column_type'] == value]['vrai_negatif'].iloc[0]
    except:
        out = 'NA'
    return html.P('Vrai Négatif : '+str(out))


@app.callback(dash.dependencies.Output('FPRB', 'children'),
dash.dependencies.Input('dropdown','value'))
def render_matrixes_fprb(value):
    try:
        out = df_indic_rb[df_indic_rb['column_type'] == value]['faux_positif'].iloc[0]
    except:
        out = 'NA'
    return html.P('Faux Positif : '+str(out))



@app.callback(dash.dependencies.Output('precisionRB', 'children'),
dash.dependencies.Input('dropdown','value'))
def render_matrixes_precisionrb(value):
    try:
        out = round(df_indic_rb[df_indic_rb['column_type'] == value]['precision'].iloc[0]*100,2)
    except:
        out = 'NA'
    return html.P('Précision : '+str(out))


@app.callback(dash.dependencies.Output('recallRB', 'children'),
dash.dependencies.Input('dropdown','value'))
def render_matrixes_recallrb(value):
    try:
        out = round(df_indic_rb[df_indic_rb['column_type'] == value]['rappel'].iloc[0]*100,2)
    except:
        out = 'NA'
    return html.P('Recall : '+str(out))






@app.callback(dash.dependencies.Output('VPML', 'children'),
dash.dependencies.Input('dropdown','value'))
def render_matrixes_vpml(value):
    try:
        out = df_indic_ml[df_indic_ml['column_type'] == value]['vrai_positif'].iloc[0]
    except:
        out = 'NA'
    return html.P('Vrai Positif : '+str(out))


@app.callback(dash.dependencies.Output('FNML', 'children'),
dash.dependencies.Input('dropdown','value'))
def render_matrixes_fnml(value):
    try:
        out = df_indic_ml[df_indic_ml['column_type'] == value]['faux_negatif'].iloc[0]
    except:
        out = 'NA'
    return html.P('Faux Négatif : '+str(out))


@app.callback(dash.dependencies.Output('VNML', 'children'),
dash.dependencies.Input('dropdown','value'))
def render_matrixes_vnml(value):
    try:
        out = df_indic_ml[df_indic_ml['column_type'] == value]['vrai_negatif'].iloc[0]
    except:
        out = 'NA'
    return html.P('Vrai Négatif : '+str(out))


@app.callback(dash.dependencies.Output('FPML', 'children'),
dash.dependencies.Input('dropdown','value'))
def render_matrixes_fpml(value):
    try:
        out = df_indic_ml[df_indic_ml['column_type'] == value]['faux_positif'].iloc[0]
    except:
        out = 'NA'
    return html.P('Faux Positif : '+str(out))



@app.callback(dash.dependencies.Output('precisionML', 'children'),
dash.dependencies.Input('dropdown','value'))
def render_matrixes_precisionml(value):
    try:
        out = round(df_indic_ml[df_indic_ml['column_type'] == value]['precision'].iloc[0]*100,2)
    except:
        out = 'NA'
    return html.P('Précision : '+str(out))


@app.callback(dash.dependencies.Output('recallML', 'children'),
dash.dependencies.Input('dropdown','value'))
def render_matrixes_recallml(value):
    try:
        out = round(df_indic_ml[df_indic_ml['column_type'] == value]['rappel'].iloc[0]*100,2)
    except:
        out = 'NA'
    return html.P('Recall : '+str(out))






@app.callback(dash.dependencies.Output('tabs-example-content-rb', 'children'),
              [dash.dependencies.Input('tabs-example-rb', 'value'),
              dash.dependencies.Input('dropdown', 'value'),
              dash.dependencies.Input('reload-val','n_clicks')])
def render_content(tab,value,n_clicks):
    if tab == 'tab-1-rb':
        df2 = pd.DataFrame(np.array([]), columns=[''])
        
        try:      
            out = df_rb[(df_rb['column_type'] == value) & (df_rb['score_rb'] > 0.5) & (df_rb['value'].str.contains(value))][['resource_id', 'header','shuffle_serie']].sample(frac=1)[:1]
            header = out.header.iloc[0]
            rid = out.resource_id.iloc[0]
            df2 = pd.DataFrame(json.loads(out.shuffle_serie.iloc[0]))
            df2 = df2.rename(columns={0:header})
        except:
            out = 'NA',
            rid = 'NA',
            header = '',
            content = []

        return html.Div([
            html.H3(value),
            html.P("CSV Detective a bien détecté le type "+value+" sur la colonne suivante : "),
            html.P(rid),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df2.columns],
                data=df2.to_dict('records'),
                style_table={
                'maxWidth':'100%',
                'overflowY': 'scroll',
                'overflowX': 'scroll',
                }
            )
        ])

    elif tab == 'tab-2-rb':
        df2 = pd.DataFrame(np.array([]), columns=[''])
        
        try:      
            out = df_rb[(df_rb['column_type'] == value) & (~df_rb['value'].str.contains(value))][['resource_id','header','shuffle_serie']].sample(frac=1)[:1]
            header = out.header.iloc[0]
            rid = out.resource_id.iloc[0]
            df2 = pd.DataFrame(json.loads(out.shuffle_serie.iloc[0]))
            df2 = df2.rename(columns={0:header})
        except:
            out = 'NA',
            rid = 'NA',
            header = '',
            content = []

        return html.Div([
            html.H3(value),
            html.P("CSV Detective a détecté le type "+value+" alors qu'il ne s'agit pas de "+value+" : "),
            html.P(rid),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df2.columns],
                data=df2.to_dict('records'),
                style_table={
                'maxWidth':'100%',
                'overflowY': 'scroll',
                'overflowX': 'scroll',
                }
            )
        ])
        
    
    elif tab == 'tab-3-rb':
        df2 = pd.DataFrame(np.array([]), columns=[''])
        
        try:      
            out = df_rb[(df_rb['column_type'] != value) & (df_rb['score_rb'] > 0.5) & (df_rb['value'].str.contains(value))][['resource_id','header','shuffle_serie']].sample(frac=1)[:1]
            header = out.header.iloc[0]
            rid = out.resource_id.iloc[0]
            df2 = pd.DataFrame(json.loads(out.shuffle_serie.iloc[0]))
            df2 = df2.rename(columns={0:header})
        except:
            out = 'NA',
            rid = 'NA',
            header = '',
            content = []

        return html.Div([
            html.H3(value),
            html.P("CSV Detective n'a pas détecté le type "+value+" alors qu'il s'agit pourtant d'un type "+value+" : "),
            html.P(rid),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df2.columns],
                data=df2.to_dict('records'),
                style_table={
                'maxWidth':'100%',
                'overflowY': 'scroll',
                'overflowX': 'scroll',
                }
            )
        ])
        
    
    elif tab == 'tab-4-rb':
        df2 = pd.DataFrame(np.array([]), columns=[''])
        
        try:      
            out = df_rb[(df_rb['column_type'] != value) & (~df_rb['value'].str.contains(value))][['resource_id','header','shuffle_serie']].sample(frac=1)[:1]
            header = out.header.iloc[0]
            rid = out.resource_id.iloc[0]
            df2 = pd.DataFrame(json.loads(out.shuffle_serie.iloc[0]))
            df2 = df2.rename(columns={0:header})
        except:
            out = 'NA',
            rid = 'NA',
            header = '',
            content = []

        return html.Div([
            html.H3(value),
            html.P("CSV Detective n'a pas détecté le type "+value+" et effectivement, ce n'est pas le cas : "),
            html.P(rid),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df2.columns],
                data=df2.to_dict('records'),
                style_table={
                'maxWidth':'100%',
                'overflowY': 'scroll',
                'overflowX': 'scroll',
                }
            )
        ])
        




@app.callback(dash.dependencies.Output('tabs-example-content-ml', 'children'),
              [dash.dependencies.Input('tabs-example-ml', 'value'),
              dash.dependencies.Input('dropdown', 'value'),
              dash.dependencies.Input('reload-val','n_clicks')])
def render_content(tab,value,n_clicks):
    if tab == 'tab-1-ml':
        df2 = pd.DataFrame(np.array([]), columns=[''])
        
        try:      
            out = df_ml[(df_ml['column_type'] == value) & (df_ml['score_ml'] > 0.5) & (df_ml['value'].str.contains(value))][['resource_id', 'header','shuffle_serie']].sample(frac=1)[:1]
            header = out.header.iloc[0]
            rid = out.resource_id.iloc[0]
            df2 = pd.DataFrame(json.loads(out.shuffle_serie.iloc[0]))
            df2 = df2.rename(columns={0:header})
        except:
            out = 'NA',
            rid = 'NA',
            header = '',
            content = []

        return html.Div([
            html.H3(value),
            html.P("CSV Detective a bien détecté le type "+value+" sur la colonne suivante : "),
            html.P(rid),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df2.columns],
                data=df2.to_dict('records'),
                style_table={
                'maxWidth':'100%',
                'overflowY': 'scroll',
                'overflowX': 'scroll',
                }
            )
        ])

    elif tab == 'tab-2-ml':
        df2 = pd.DataFrame(np.array([]), columns=[''])
        
        try:      
            out = df_ml[(df_ml['column_type'] == value) & (~df_ml['value'].str.contains(value))][['resource_id','header','shuffle_serie']].sample(frac=1)[:1]
            header = out.header.iloc[0]
            rid = out.resource_id.iloc[0]
            df2 = pd.DataFrame(json.loads(out.shuffle_serie.iloc[0]))
            df2 = df2.rename(columns={0:header})
        except:
            out = 'NA',
            rid = 'NA',
            header = '',
            content = []

        return html.Div([
            html.H3(value),
            html.P("CSV Detective a détecté le type "+value+" alors qu'il ne s'agit pas de "+value+" : "),
            html.P(rid),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df2.columns],
                data=df2.to_dict('records'),
                style_table={
                'maxWidth':'100%',
                'overflowY': 'scroll',
                'overflowX': 'scroll',
                }
            )
        ])
        
    
    elif tab == 'tab-3-ml':
        df2 = pd.DataFrame(np.array([]), columns=[''])
        
        try:      
            out = df_ml[(df_ml['column_type'] != value) & (df_ml['score_ml'] > 0.5) & (df_ml['value'].str.contains(value))][['resource_id','header','shuffle_serie']].sample(frac=1)[:1]
            header = out.header.iloc[0]
            rid = out.resource_id.iloc[0]
            df2 = pd.DataFrame(json.loads(out.shuffle_serie.iloc[0]))
            df2 = df2.rename(columns={0:header})
        except:
            out = 'NA',
            rid = 'NA',
            header = '',
            content = []

        return html.Div([
            html.H3(value),
            html.P("CSV Detective n'a pas détecté le type "+value+" alors qu'il s'agit pourtant d'un type "+value+" : "),
            html.P(rid),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df2.columns],
                data=df2.to_dict('records'),
                style_table={
                'maxWidth':'100%',
                'overflowY': 'scroll',
                'overflowX': 'scroll',
                }
            )
        ])
        
    
    elif tab == 'tab-4-ml':
        df2 = pd.DataFrame(np.array([]), columns=[''])
        
        try:      
            out = df_ml[(df_ml['column_type'] != value) & (~df_ml['value'].str.contains(value))][['resource_id','header','shuffle_serie']].sample(frac=1)[:1]
            header = out.header.iloc[0]
            rid = out.resource_id.iloc[0]
            df2 = pd.DataFrame(json.loads(out.shuffle_serie.iloc[0]))
            df2 = df2.rename(columns={0:header})
        except:
            out = 'NA',
            rid = 'NA',
            header = '',
            content = []

        return html.Div([
            html.H3(value),
            html.P("CSV Detective n'a pas détecté le type "+value+" et effectivement, ce n'est pas le cas : "),
            html.P(rid),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df2.columns],
                data=df2.to_dict('records'),
                style_table={
                'maxWidth':'100%',
                'overflowY': 'scroll',
                'overflowX': 'scroll',
                }
            )
        ])



if __name__ == '__main__':
    app.run_server(debug=True,port=8051)
