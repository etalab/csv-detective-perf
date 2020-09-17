import dash
import dash_auth
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table

import pandas as pd
import random
import json
import numpy as np
import csv

from secrets import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)


df = pd.read_csv("full.csv")
savedf = pd.read_csv("results.csv")

df = df[~df[df.columns[0]].isin(savedf.index)]

df = df[df['shuffle_serie'].notna()]

ct = ['adresse','booleen','code_commune_insee','code_csp_insee',
        'code_departement','code_fantoir','code_postal','code_region','code_rna',
        'code_waldec','commune','csp_insee','date','date_fr','datetime_iso',
        'departement','email','insee_ape700','insee_canton','iso_country_code',
        'jour_de_la_semaine','json_geojson','latitude_l93','latitude_wgs',
        'latitude_wgs_fr_metropole','latlon_wgs','longitude_l93','longitude_wgs',
        'longitude_wgs_fr_metropole','money','pays','region','sexe','siren','siret',
        'tel_fr','uai','url','year']

GLOBAL_LOC = -1



ct = np.insert(ct, 0, "Ne sais pas",axis=0)


app.layout = html.Div([

    html.Div([
        html.H1("Labellisation des types de colonnes CSV"),
        dcc.Markdown('''
            Vous trouverez ci-dessous un extrait d'une colonne d'un csv issu de data.gouv. 
            Le but du jeu est que vous déterminiez manuellement le type de cette colonne en sélectionnant le type parmi la liste ci-dessous.  
              
            Si vous ne trouvez pas de type correspondant, sélectionnez "Ne sais pas".  
              
            Une fois que vous aurez sélectionné et validé un type, une autre colonne vous sera proposée.
        ''')
    ], style={'float': 'left', 'width': '100%','height':'200px'}),


    html.Div(id="dropdowndiv",children=[
            dcc.Dropdown(
                id='dropdown',
                options=[
                    {'label': i, 'value': i} for i in ct
                ],
                value='empty'
            ),
            html.Br(),
            html.Div(id="result-dropdown",
                children='')

    ], style={'float': 'left', 'width': '20%','marginRight':'30px'}),

    html.Div([
        html.Div(id="mytable",children=[])
    ], style={'float': 'left', 'width': '75%'}),




],style={'width':'1200px','margin':'auto','backgroundColor':'green'})

@app.callback(
    dash.dependencies.Output(component_id='mytable',component_property='children'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_table(value):

    global GLOBAL_LOC
    global df 

    if((value != "empty") & (GLOBAL_LOC != -1)):
        arr = []
        for el in df[df[df.columns[0]] == GLOBAL_LOC]:
            arr.append(df[df[df.columns[0]] == GLOBAL_LOC][el].values[0])
        arr.append(value)
        with open('results.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(arr)

        df = df[df[df.columns[0]] != GLOBAL_LOC]


        df = df.reset_index(drop=True)

        print(df.shape[0])


    loc = df.sample()[df.columns[0]].values[0]


    GLOBAL_LOC = loc


    df2 = pd.DataFrame(json.loads(df[df[df.columns[0]] == loc]['shuffle_serie'].values[0]))
    df2 = df2.rename(columns={ df2.columns[0]:  df[df[df.columns[0]] == loc]['header'].values[0]})
    
    headers = df[df[df.columns[0]] == loc]['headers'].values[0].replace("[","").replace("]","").replace("'","").replace('"',"").split(",")


    df3 = pd.DataFrame(headers)
    df3 = df3.rename(columns={ df3.columns[0]: 'headers'})

    return html.Div([
        
        html.Div([
            html.P(html.B("Titre du dataset :")),
            html.Div(children=[df[df[df.columns[0]] == loc]['dataset_title'].values[0]],style={'height':'50px'}),
            html.Br(),
            html.P(html.B("Colonne et son contenu :")),
            html.Br(),
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
        ], style={'float': 'left', 'width': '45%','marginRight':'20px'}),
        html.Div([
            html.P(html.B("Titre de la ressource :")),
            html.Div(children=[df[df[df.columns[0]] == loc]['resource_title'].values[0]],style={'height':'50px'}),
            html.Br(),
            html.P(html.B("Headers du fichier csv")),
            html.Br(),
            dash_table.DataTable(
                id='table2',
                columns=[{"name": i, "id": i} for i in df3.columns],
                data=df3.to_dict('records'),
                style_table={
                'maxWidth':'100%',
                'overflowY': 'scroll',
                'overflowX': 'scroll',
                }
            ),
        ], style={'float': 'left', 'width': '45%'})
    ])


@app.callback(
    dash.dependencies.Output(component_id='dropdowndiv',component_property='children'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_dropdown(value):
    return html.Div([
            dcc.Dropdown(
                id='dropdown',
                options=[
                    {'label': i, 'value': i} for i in ct
                ],
                value='empty'
            ),
            html.Br(),
            html.Div(id="result-dropdown",
                children='')
    ])


if __name__ == '__main__':
    app.run_server(debug=True,port=8051)
