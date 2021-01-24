import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#from jupyter_dash import JupyterDash
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import os 

data_path = os.getcwd() + '/'
data_df = pd.read_csv(data_path+'Dataset.csv')

type_mappings = pd.read_csv(data_path+'Type_mappings.csv')

sort_order_mappings = pd.read_csv(data_path+'Sort_Order_Mappings.csv')
sort_order_mappings = sort_order_mappings.set_index('Attribute').squeeze()

metrics = list(data_df.columns.values)
metrics.remove('Id')

dropdown_2 = list(type_mappings[type_mappings['Type'] == 'Numeric']['Measure'])

def num_conv(input):
    try:
        return float(input)
    except:
        return 0

app = dash.Dash(__name__)
#app = JupyterDash(__name__)

#---------------------------------------------------------------
app.layout = html.Div([

    html.Div([dcc.Graph(id='our_graph')
    ],className='nine columns'),
    html.Div([
        html.Br(),
        html.Label(['Input Settings:'],style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(id='measure_1',
            options=[{'label':x, 'value':x} for x in metrics],
            value='OverallQual',
            multi=False,
            disabled=False,
            clearable=False,
            searchable=True,
            placeholder='Select Measure',
            className='form-dropdown',
            style={'width':"90%"},
            persistence='string',
            persistence_type='memory'),
        dcc.Dropdown(id='measure_2',
            options=[{'label':x, 'value':x} for x in dropdown_2],
            value='SalePrice',
            multi=False,
            disabled=False,
            clearable=False,
            searchable=True,
            placeholder='Select Measure',
            className='form-dropdown',
            style={'width':"90%"},
            persistence='string',
            persistence_type='memory')
    ],className='three columns'),

])

#---------------------------------------------------------------

@app.callback(
    Output('our_graph','figure'),
    [Input('measure_1','value'),
    Input('measure_2','value')]
)

def build_graph(measure_sel_1,measure_sel_2):
    df = data_df[[measure_sel_1,measure_sel_2]].copy()
    df[measure_sel_1] = df[measure_sel_1].astype('str')
    df['sort_order'] = df[measure_sel_1].replace(sort_order_mappings)
    df['sort_order'] = df['sort_order'].apply(num_conv)
    df = df.sort_values('sort_order')
    df = df.drop(['sort_order'],axis=1)
    Final_fig = make_subplots()
    Final_fig = px.scatter(x=df[measure_sel_1], y=df[measure_sel_2])
    Final_fig.update_layout(
    yaxis={'title':measure_sel_2},
    title={'text':measure_sel_2+' against '+ measure_sel_1,'font':{'size':28},'x':0.5,'xanchor':'center'},
    xaxis={'title':measure_sel_1})
    return Final_fig

#---------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=False)
    #app.run_server(mode='inline')