#imports
import pandas as pd
import numpy as np
import pickle
import time
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
from recommender import get_recs, get_df_and_dists, get_df

#Get dataframe using function from recommender.py
topic_df = get_df() 
topics = topic_df.columns[8:28]

#initialize app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#Suppressing callback exceptions for implementation of loop breaker
app.config['suppress_callback_exceptions'] = True




#Define graph colors
app_color = {
    "graph_bg": "#082255", 
    "graph_line": "#B4E8FC"
}

colors = {
    'background': '#061E44',
    'text': '#7FDBFF'
}



#Set options for Tab 1: Topic visualizations
current_topic = topics[3]

current_subtopics = list(set(topic_df[topic_df.closest_topic == current_topic].subtopic.values))

dropdown_options = []
for subtopic in current_subtopics:
    if subtopic != '' and subtopic != 'None':
        dropdown_options.append({'label': subtopic, 'value': subtopic})

topic_dropdown_options = []
for topic in topics:
    topic_dropdown_options.append({'label': topic, 'value': topic})

    
    
#Set options for Tab 2: Article recommender
tab2_topics = topic_df.columns[8:28]
tab2_choices = [tab2_topics[15], tab2_topics[2], tab2_topics[16], 
                tab2_topics[5], tab2_topics[0], tab2_topics[8], 
                tab2_topics[11], tab2_topics[13], tab2_topics[14], tab2_topics[3], 
                tab2_topics[4], tab2_topics[9], tab2_topics[6], 
                tab2_topics[12], tab2_topics[17]]

tab2_dropdown_list = []
for selection in tab2_choices:
    choice_subtopic_list = []
    for subtopic in list(set(topic_df[topic_df.closest_topic == selection].subtopic)):
        if subtopic != '' and subtopic != 'None':
            choice_subtopic_list.append({'label': subtopic, 'value': subtopic})
    tab2_dropdown_list.append(choice_subtopic_list)

    
#App layout
app.layout = html.Div(
    #Set app background color
    style={'backgroundColor': colors['background']},
    
    
    children = [
        #App header
        html.H1(
            children='Nature Article Recommender', 
            style = {'textAlign': 'center', 'color': '#fff'}
        ),

    dcc.Tabs(
        #Tab style
        colors={
                "border": "#007ACE",
                "primary": "#007ACE",
                "background": "#007ACE"
        }, 
        children= [

            # Tab 1: Visualizations
            dcc.Tab(
                label='Topic Timelines', 
                children=[
                    html.H3(
                        children='Topic Visualizations', 
                        style = {'textAlign': 'center', 'color':'#fff'}
                    ),
            
                    dcc.Markdown(
                        children='''
                            Choose a topic and subtopic from the dropdown menus below to view a timeline of the frequency of your topic selections in Nature news articles.  Articles were scraped from [Nature](https://www.nature.com/nature/articles) and the timelines consist of content from 1998 to present day.  Each rticle may belong to more than 1 topic.
                            ''',
                        style={'color':'#fff'}
                    ),
            
                    dcc.Markdown(children=' '),
                    
                    #Topic Dropdown menu
                    html.Div(
                        style = {'display':'flex'},
                        children = [
                            html.Div([
                                 html.H6(
                                     """Select your topic:""", 
                                     style={
                                         'color':'#fff',
                                         'margin-right': '2em'
                                     }
                                 )
                            ]),
                            
                            #User-selected value from topic dropdown will dictate values that populate the subtopic dropdown
                            dcc.Dropdown(
                                id='topic_input',
                                options = topic_dropdown_options,
                                style = dict(
                                    width='50%'
                                )
                            )
                        ]
                    ),
                    
                    #Suptopic Dropdown Menu
                    html.Div(
                        style= {'display':'flex'},
                        children = [
                            html.Div([
                                html.H6(
                                    """Select your subtopic:""", 
                                    style = {'margin-right': '2em',
                                            'color':'#fff'}
                                )
                            ]),

                             dcc.Dropdown(
                                id='topic_output',
                                options = dropdown_options,
                                style = dict(
                                    width='50%'
                                )        
                            )
                        ],
                
                    ),

                    html.Div(
                        id="title_output", 
                        children=f'Topic: {topic_df.columns[13]}', 
                        style={'color': '#061E44',
                            'textAlign': 'center'
                        }
                    ),

#                     dcc.Markdown(
#                         children=''
#                     ),

                    html.Div(
                        id = 'topic_graph',
                        children = []

                    ),




                    html.Div(
                        id = 'subtopic_graph',
                        children = []

                    )
            ]),
                
            # Tab 2: Recommender
            dcc.Tab(label='Article Recommender',  children = [

                html.H3(
                    children='Article Recommender', 
                    style = {'color': '#fff', 'textAlign': 'center'}
                ),

                dcc.Markdown(
                    style = {'color':'#fff'},
                    children='''
                    Choose a topic and subtopic from the dropdown menus below to start reading!  If you find the topic fascinating, you can choose to see some similar articles, or else you can explore some other topics.
                    '''
                ),

                html.Br(),

                html.H6(
                    id='choice', 
                    children= 'Select a Topic', 
                    style = {
                        'textAlign': 'center',
                        'color':'#061E44'}
                ),


                html.Div(
                    children = [
                        html.Div(
                            id = 'physical',
                            children = [
                                html.H6(
                                    children='Physical Science', 
                                    style = {'color':'#fff'}
                                ),

                                dcc.RadioItems(
                                    style = {'color':'#fff'},
                                    id='radio1',
                                    options = [
                                        {'label': 'Physics', 'value': 0},
                                        {'label': 'Astronomy/Astrophysics', 'value': 1},
                                        {'label': 'Space Exploration', 'value': 2},
                                        {'label': 'Chemistry/Mathematics/Computing', 'value': 3}
                                    ]
                                ),

                            html.Br()

                            ],
                            style = {'columnCount':1, 'color':'fff'}
                        ),

                        html.Div(
                            id = 'biological',
                            children = [
                                html.H6(
                                    children='Biological Science', 
                                    style={'textAlign': 'left', 'color':'#fff'}),

                                dcc.RadioItems(
                                    id='radio2',
                                    style = {'color':'#fff'},
                                    options = [
                                        {'label': 'Neuroscience/Behavioral Science', 'value': 4},
                                        {'label': 'Genetics/Genomics', 'value': 5},
                                        {'label': 'Stem Cells', 'value': 6},
                                        {'label': 'Molecular Biology/Cell Biology', 'value': 7},
                                        {'label': 'Evolution', 'value': 8}
                                    ]
                                )
                            ],
                            style={'columnCount':1}
                        ),

                        html.Div(
                            id = 'environmental',
                            children = [
                                html.H6(
                                    children='Earth/Health Science', 
                                    style = {'color':'#fff'}),

                                dcc.RadioItems(
                                    id='radio3',
                                    style = {'color': '#fff'},
                                    options = [
                                        {'label': 'Climate Sciences', 'value': 9},
                                        {'label': 'Diseases/Epidemics', 'value': 10},
                                        {'label': 'Geology/Ocean Sciences', 'value': 11},
                                        {'label': 'Drug Discovery/Pharmaceuticals', 'value': 12},
                                        {'label': 'Agriculture/Plant Sciences', 'value': 13},
                                        {'label': 'Ecology/Biodiversity', 'value': 14}

                                    ]
                                )
                            ]
                        ),




                    ],

                    style={
                        'columnCount': 3
                        }

                ),

                html.H6(
                    'Select a Subtopic', 
                    style = {
                        'textAlign': 'center', 
                        'color': '#fff'
                    }
                ),

                html.Div(
                    style = {
                        'width': '50%',
                        'margin':'auto',
                        'alignItems': 'center'
                    },
                    children = [
                        dcc.Dropdown(
                            id='tab2_subtopic_dropdown',
                            options = [{'label': 'First, select a topic', 'value': 0}]
                        )
                    ]
                ),

                html.Div(id='loop_breaker_container', children=[]),

                html.Div(
                    id='recs_output', 
                    style = {'textAlign': 'center'},
                    children=[]
                ),

                html.Div(
                    id='show_more', 
                    children=[], 
                    style={'textAlign': 'center'}
                ),

                html.Br(),


                dcc.Loading(
                    id = 'loading', 
                    type = 'default', 
                    children = [
                        html.Div(
                            id='similar_output',
                            style = {'textAlign': 'center'},
                            children=[])
                    ]
                ),

                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.H6(id='article_index', children=[], style= {'color':'#061E44'})

            ])
    ])
    
])


#callbacks

@app.callback(
    Output(component_id="topic_output", component_property='options'),
    [Input(component_id='topic_input', component_property='value')]
)
def update_topic_output(input_value):
    topic = input_value
    current_subtopics = list(set(topic_df[topic_df.closest_topic == topic].subtopic.values))
    dropdown_options = []
    for subtopic in current_subtopics:
        if subtopic != '' and subtopic != 'None':
            dropdown_options.append({'label': subtopic, 'value': subtopic})
    return dropdown_options

@app.callback(
    Output(component_id="title_output", component_property='children'),
    [Input(component_id='topic_input', component_property='value')]
)
def udpate_title(input_value):
    return f'Topic: {input_value}'

@app.callback(
    Output(component_id='topic_graph', component_property='children'),
    [Input(component_id='topic_input', component_property='value')]
)
def plot_topic(input_value):
    if input_value:
        year_list = []
        article_list = []
        for i in range(1998, 2021):
            year_list.append(i)
            df_date = topic_df[(topic_df['year'] == i)]
            mask = df_date.all_topics.apply(lambda x: any(item for item in [input_value] if item in x))
            df_subset = df_date[mask]
            article_list.append(len(df_subset)/len(df_date))
        df = pd.DataFrame({'x': year_list, 'y': article_list})
        
        trace = dict(
        type="scatter",
        x = df['x'],
        y = df['y'],
        line={'color':'#42C4F7'},
        hoverinfo='skip')
            
        layout = {
            'plot_bgcolor':app_color["graph_bg"],
            'font':dict(family='sans serif',size=18, color='#007ACE'),
            'paper_bgcolor':app_color["graph_bg"],
            'xaxis':{
                'range':[1998,2020],
                'showline': True,
                'zeroline': False,
                'fixedrange':True,
                'title': 'Year'},
            'yaxis':{
                'range':[0, 0.5],
                'showline': True,
                'zeoline': False,
                'fixedrange': True,
                'tickvals': [0, 0.1, 0.2, 0.3, 0.4, 0.5],
                'ticktext': ['0', '10%', '20%', '30%', '40%', '50%']},
            'title': f'Frequency of {input_value} articles over time'}
        fig = dict(data = [trace], layout = layout)
        

        
        topic_graph = dcc.Graph(
                          id='topic_graph_output',
                          figure = fig
                          
                      )
        return [topic_graph]
    else:
        return []

@app.callback(
    Output(component_id='subtopic_graph', component_property='children'),
    [Input(component_id='topic_output', component_property='value')]
)
def plot_subtopic(input_value):
    if input_value:
        year_list = []
        article_list = []
        for i in range(1998, 2021):
            year_list.append(i)
            df_date = topic_df[(topic_df['year'] == i)]
            df_subtopic = df_date[df_date.subtopic == input_value]
            article_list.append(len(df_subtopic)/len(df_date))
        df = pd.DataFrame({'x': year_list, 'y': article_list})
        fig = px.line(df, x='x', y='y', title = f'Frequency of {input_value} articles over time')
        
        trace = dict(
        type="scatter",
        x = df['x'],
        y = df['y'],
        line={'color':'#42C4F7'},
        hoverinfo='skip')
            
        layout = {
            'plot_bgcolor':app_color["graph_bg"],
            'font':dict(family='sans serif',size=18, color='#007ACE'),
            'paper_bgcolor':app_color["graph_bg"],
            'xaxis':{
                'range':[1998,2020],
                'showline': True,
                'zeroline': False,
                'fixedrange':True,
                'title': 'Year'},
            'yaxis':{
                'range':[0, 0.1],
                'showline': True,
                'zeoline': False,
                'fixedrange': True,
                'tickvals': [0, 0.02, 0.04, 0.06, 0.08, 0.1],
                'ticktext': ['0', '2%', '4%', '6%', '8%', '10%']},
            'title': f'Frequency of {input_value} articles over time'}
        fig = dict(data = [trace], layout = layout)


        subtopic_graph = dcc.Graph(
                             id='graph_output',
                             figure = fig
                         )
        return [subtopic_graph]
    else:
        return []
    
@app.callback(
    Output(component_id='choice', component_property='children'),
    [Input(component_id='radio1', component_property='value'),
     Input(component_id='radio2', component_property='value'),
     Input(component_id='radio3', component_property='value')]
)
def reset_choice(radio1, radio2, radio3):
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id']
    if trigger == 'radio1.value':
        if radio1 == None:
            raise PreventUpdate
        else:
            return radio1
    elif trigger == 'radio2.value':
        if radio2 == None:
            raise PreventUpdate
        else:
            return radio2
    elif trigger == 'radio3.value':
        if radio3 == None:
            raise PreventUpdate
        else:
            return radio3
    else:
        return 'Select a Topic'

@app.callback(
    Output('loop_breaker_container', 'children'),
    [Input('choice', 'children')],
    [State('radio1', 'value'), 
     State('radio2', 'value'),
     State('radio3', 'value')])
def call_loop_breaker(choice, state1, state2, state3):
    states = dash.callback_context.states
    s1 = states['radio1.value']
    s2 = states['radio2.value']
    s3 = states['radio3.value']
    if (s1 != None and s2 != None):
        if choice <=3:
            return [html.Div(id='loop_breaker', children=2)]
        else:
            return [html.Div(id='loop_breaker', children=1)]
                    
    elif (s2 != None and s3 != None):
        if choice >8:
            return [html.Div(id='loop_breaker', children=2)]
        else:
            return [html.Div(id='loop_breaker', children=3)]      
    elif (s1 != None and s3 != None):
        if choice <= 3:
            return [html.Div(id='loop_breaker', children=3)]
        else:
            return [html.Div(id='loop_breaker', children=1)]
    else:
        return []
        
@app.callback(
    Output('radio1', 'value'),
    [Input('loop_breaker', 'children')],
    [State('radio1', 'value')])
def clear_radio1(deselect, _):
    if deselect == 1:
        return None
    else:
        return dash.callback_context.states['radio1.value']
                    
@app.callback(
    Output('radio2', 'value'),
    [Input('loop_breaker', 'children')],
    [State('radio2', 'value')])
def clear_radio2(deselect, _):
    if deselect == 2:
        return None
    else:
        return dash.callback_context.states['radio2.value']

@app.callback(
    Output('radio3', 'value'),
    [Input('loop_breaker', 'children')],
    [State('radio3', 'value')])
def clear_radio3(deselect, _):
    if deselect == 3:
        return None
    else:
        return dash.callback_context.states['radio3.value']


@app.callback(
    Output('tab2_subtopic_dropdown', 'value'),
    Input('tab2_subtopic_dropdown', 'options')
)
def reset_articles(options):
    return []


@app.callback(
    Output('tab2_subtopic_dropdown', 'options'),
    Input('choice', 'children')
)
def populate_tab2_subtopic_dropdown(subtopic_index):
    if subtopic_index == 'Select a Topic':
        return [{'label': 'First, select a topic', 'value': 0}]
    else:
        return tab2_dropdown_list[subtopic_index]


    

@app.callback(
    Output('recs_output', 'children'),
    Input('tab2_subtopic_dropdown', 'value')
)
def get_recent_articles(input_topic):
    if input_topic:
        subset = topic_df[topic_df.subtopic == input_topic].head(5)
        titles = list(subset.title)
        urls = list(subset.url)
        indices = list(subset.index)

        element_list = []
        element_list.append(html.Br())
        element_list.append(html.H6(dcc.Markdown(
            children = f'Recent articles related to **{input_topic}**',
            style = {'color': '#fff'})))
        element_list.append(html.Br())
        for i in range(len(titles)):
            element = html.Form(
                children=[
                    html.Button(
                        children=f'{titles[i]}',
                        id=f'btn{i}', 
                        type='submit',
                        formAction = f'https://www.nature.com{urls[i]}',
                        formTarget= '_blank',
                        n_clicks=0,
                        style={
                            'backgroundColor':'#fff',
                            'border':'none',
                            'color':'black',
                            'fontSize':'14px'

                             
                            
                        }
                    )
            ])
            element_list.append(element)
            element_list.append(html.Br())
            
            
            
        return element_list
    else:
        return []

@app.callback(
    Output('btn0', 'style'),
    [Input('btn0', 'n_clicks'),
     Input('btn1', 'n_clicks'),
     Input('btn2', 'n_clicks'),
     Input('btn3', 'n_clicks'),
     Input('btn4', 'n_clicks')]
)
def change_button_color0(btn0, btn1, btn2, btn3, btn4):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn0' in changed_id:
        style = {'backgroundColor':'#034f84',
                 'color': 'white',
                 'fontSize':'16px'}
    else:
        style={
            'backgroundColor':'#fff',
            'border':'none',
            'color':'black',
            'fontSize':'14px'
}
    return style

@app.callback(
    Output('btn1', 'style'),
    [Input('btn0', 'n_clicks'),
     Input('btn1', 'n_clicks'),
     Input('btn2', 'n_clicks'),
     Input('btn3', 'n_clicks'),
     Input('btn4', 'n_clicks')]
)
def change_button_color1(btn0, btn1, btn2, btn3, btn4):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn1' in changed_id:
        style = {'backgroundColor':'#034f84',
                 'color': 'white',
                 'fontSize':'16px'}
    else:
        style={
            'backgroundColor':'#fff',
            'border':'none',
            'color':'black',
            'fontSize':'14px'
}
    return style

@app.callback(
    Output('btn2', 'style'),
    [Input('btn0', 'n_clicks'),
     Input('btn1', 'n_clicks'),
     Input('btn2', 'n_clicks'),
     Input('btn3', 'n_clicks'),
     Input('btn4', 'n_clicks')]
)
def change_button_color2(btn0, btn1, btn2, btn3, btn4):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn2' in changed_id:
        style = {'backgroundColor':'#034f84',
                 'color': 'white',
                 'fontSize':'16px'}
    else:
        style={
            'backgroundColor':'#fff',
            'border':'none',
            'color':'black',
            'fontSize':'14px'
}
    return style
    
@app.callback(
    Output('btn3', 'style'),
    [Input('btn0', 'n_clicks'),
     Input('btn1', 'n_clicks'),
     Input('btn2', 'n_clicks'),
     Input('btn3', 'n_clicks'),
     Input('btn4', 'n_clicks')]
)
def change_button_color3(btn0, btn1, btn2, btn3, btn4):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn3' in changed_id:
        style = {'backgroundColor':'#034f84',
                 'color': 'white',
                 'fontSize':'16px'}
    else:
        style={
            'backgroundColor':'#fff',
            'border':'none',
            'color':'black',
            'fontSize':'14px'}
    return style

@app.callback(
    Output('btn4', 'style'),
    [Input('btn0', 'n_clicks'),
     Input('btn1', 'n_clicks'),
     Input('btn2', 'n_clicks'),
     Input('btn3', 'n_clicks'),
     Input('btn4', 'n_clicks')]
)
def change_button_color4(btn0, btn1, btn2, btn3, btn4):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn4' in changed_id:
        style = {'backgroundColor':'#034f84',
                 'color': 'white',
                 'fontSize':'16px'}
    else:
        style={
            'backgroundColor':'#fff',
            'border':'none',
            'color':'black',
            'fontSize':'14px'}
    return style


@app.callback(
    Output('article_index', 'children'),
    [Input('btn0', 'n_clicks'),
     Input('btn1', 'n_clicks'),
     Input('btn2', 'n_clicks'),
     Input('btn3', 'n_clicks'),
     Input('btn4', 'n_clicks'),
     Input('btn0', 'children'),
     Input('btn1', 'children'),
     Input('btn2', 'children'),
     Input('btn3', 'children'),
     Input('btn4', 'children')]
)
def show_me_more(btn0, btn1, btn2, btn3, btn4, title0, title1, title2, title3, title4):
    changed_id = dash.callback_context.triggered[0]
    button = changed_id['prop_id'].split('.')[0]
    if changed_id['value'] == 0:
        return []
    if button == 'btn0':
        title = title0
    elif button == 'btn1':
        title = title1
    elif button == 'btn2':
        title = title2
    elif button == 'btn3':
        title = title3
    elif button == 'btn4':
        title = title4
    if title:
        article_index = topic_df[topic_df.title == title].index[0]
        print(article_index)
        return article_index

@app.callback(
    Output('show_more', 'children'),
    [Input('article_index', 'children')]
)
def show_more_button(article_index):
    if article_index == []:
        return []
    else:
        show_more = html.Button(children='Show similar articles?',
                                        id='show_similar_button',
                                        n_clicks=0,
                                        style = {
                                            'backgroundColor':'#034f84',
                                            'color': 'white'}
                                        )
        

            
        return [html.Hr(style={'width':'50%', 'borderStyle':'inset', 'borderWidth':'4px'}), show_more]
    


@app.callback(
    Output('similar_output', 'children'),
    [Input('show_similar_button', 'n_clicks')],
    State('article_index', 'children')
)
def get_similar_articles(n_clicks, _):
    if n_clicks == []:
        return []

    elif n_clicks > 0:
        article_index = int(dash.callback_context.states['article_index.children'])
        article_title = topic_df.loc[article_index, 'title']
        recs, title_list, url_list = get_recs(article_index, n=5, topic_df=topic_df)
        element_list = []
        element_list.append(html.Br())
        element_list.append(html.H6(dcc.Markdown(
            children='Articles similar to your selection:',
            style={'color':'#fff'})))
        element_list.append(html.Br())
        for i, rec in enumerate(recs):
            element = html.Form(children=[
                html.Button(children=f'{title_list[i]}',
                id = f'rec{i}',
                type = 'submit',
                formAction = f'https://www.nature.com{url_list[i]}',
                formTarget = '_blank',
                n_clicks=0,
                style={
                    'backgroundColor':'#fff',
                    'border':'none',
                    'color':'black',
                    'fontSize':'14px'})
                
            ])
            element_list.append(element)
            element_list.append(html.Br())
        return element_list
    else:
        return []

    
    


if __name__ == '__main__':
    app.run_server(debug=True)