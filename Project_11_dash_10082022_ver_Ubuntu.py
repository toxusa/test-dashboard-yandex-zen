import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime
import time
import pandas as pd
from sqlalchemy import create_engine


db_config = {'user': 'praktikum_student', # имя пользователя
            'pwd': 'Sdf4$2;d-d30pp', # пароль
            'host': 'rc1b-wcoijxj3yxfsf3fs.mdb.yandexcloud.net',
            'port': 6432, # порт подключения
            'db': 'data-analyst-zen-project-db'} # название базы данных

connection_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_config['user'],
                                                db_config['pwd'],
                                                db_config['host'],
                                                db_config['port'],
                                                db_config['db'])
# создаем движок
engine = create_engine(connection_string)

# выбираем все данные из соответствующей таблицы
query = 'SELECT * FROM dash_visits'

# читаем все данные в объект pandas 
dash_visits = pd.io.sql.read_sql(query, con = engine)

#### ! ниже код в комментах для отладки и локальной работы ! ###
# сохраняем сsv в том же каталоге, чтобы читать из него
#dash_visits.to_csv('dash_visits.csv', index=False)
# читаем csv в dash_visits
#dash_visits = pd.read_csv('dash_visits.csv') # раскомментить для работы с локальным файлом csv в том же каталоге

#external_stylesheets = ['bWLwgP.css'] # раскомментить для работы локально со скаченной CSS

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=
    [
        
        html.Div(
            children=
            [
            html.Div(
                [
                    html.Div(
                        [
                            # формируем заголовок тегом HTML
                            html.H1(children = 'Дашборд Яндекс.Дзен'),
                            html.P(
                                'Анализ пользовательского взаимодействия с карточками статей по темам, источникам и возрастным категориям', 
                                style={'fontSize': 20}
                            ),
                            dcc.Markdown('[**Ссылка на этот же проект в Tablue**](https://public.tableau.com/views/Project_11_16599720184690/_?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link)'),
                        ], className='six columns',
                    ),
                    # добавление временной шкалы
                    html.Div(
                        [
                            html.Label(
                                'Временной период: ',
                            ),
                            dcc.RangeSlider(
                                min = int(datetime.strptime(str(dash_visits['dt'].min()), '%Y-%m-%d %H:%M:%S').strftime('%s')), #int(time.mktime(datetime.strptime(str(dash_visits['dt'].min()), '%Y-%m-%d %H:%M:%S').timetuple())),
                                max = int(datetime.strptime(str(dash_visits['dt'].max()), '%Y-%m-%d %H:%M:%S').strftime('%s')), #int(time.mktime(datetime.strptime(str(dash_visits['dt'].max()), '%Y-%m-%d %H:%M:%S').timetuple())),
                                marks = {
                                    int(datetime.strptime(str(dash_visits['dt'].min()), '%Y-%m-%d %H:%M:%S').strftime('%s')): {'label': '18:28'},
                                    int(datetime.strptime(str(dash_visits['dt'].max()), '%Y-%m-%d %H:%M:%S').strftime('%s')): {'label': '19:00'},
                                    int(datetime.strptime('2019-09-24 18:44:00', '%Y-%m-%d %H:%M:%S').strftime('%s')): {'label': '18:44'},
                                    int(datetime.strptime('2019-09-24 18:31:00', '%Y-%m-%d %H:%M:%S').strftime('%s')): {'label': '18:31'},
                                    int(datetime.strptime('2019-09-24 18:34:00', '%Y-%m-%d %H:%M:%S').strftime('%s')): {'label': '18:34'},
                                    int(datetime.strptime('2019-09-24 18:37:00', '%Y-%m-%d %H:%M:%S').strftime('%s')): {'label': '18:37'},
                                    int(datetime.strptime('2019-09-24 18:40:00', '%Y-%m-%d %H:%M:%S').strftime('%s')): {'label': '18:40'},
                                    int(datetime.strptime('2019-09-24 18:47:00', '%Y-%m-%d %H:%M:%S').strftime('%s')): {'label': '18:47'},
                                    int(datetime.strptime('2019-09-24 18:50:00', '%Y-%m-%d %H:%M:%S').strftime('%s')): {'label': '18:50'},
                                    int(datetime.strptime('2019-09-24 18:53:00', '%Y-%m-%d %H:%M:%S').strftime('%s')): {'label': '18:53'},
                                    int(datetime.strptime('2019-09-24 18:56:00', '%Y-%m-%d %H:%M:%S').strftime('%s')): {'label': '18:56'},
                                    1569339072: {'label': '18:31'},
                                    1569339264: {'label': '18:34'},
                                    1569339456: {'label': '18:37'},
                                    1569339648: {'label': '18:40'},
                                    1569339840: {'label': '18:44'},
                                    1569340032: {'label': '18:47'},
                                    1569340224: {'label': '18:50'},
                                    1569340416: {'label': '18:53'},
                                    1569340608: {'label': '18:56'},
                                    1569340800: {'label': '19:00'},  
                                    },
                                value=[int(datetime.strptime(str(dash_visits['dt'].min()), '%Y-%m-%d %H:%M:%S').strftime('%s')), int(datetime.strptime(str(dash_visits['dt'].max()), '%Y-%m-%d %H:%M:%S').strftime('%s'))],
                                allowCross=False,
                                #tooltip={"placement": "bottom", "always_visible": True},
                                id = 'dt_selector',
                            ),
                            html.Label('Выбор карточек тем:'),
                            dcc.Dropdown(
                                options=[{'label': x, 'value': x} for x in dash_visits['item_topic'].unique()],
                                value=dash_visits['item_topic'].unique().tolist(),
                                multi=True,
                                id = 'item_topic_selector',
                            ),
                            html.Br(),
                            # добавление чек-листа возрастного сегмента
                            html.Label('Выбор возрастных сегментов:'),
                            dcc.Checklist(
                                options=[{'label': x, 'value': x} for x in dash_visits['age_segment'].unique()],
                                value=dash_visits['age_segment'].unique(), 
                                inline=True,
                                id = 'age_checklist',  
                            ),
                        ], className='six columns',
                    ),
                ], className='row',
            ),
            ],
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Markdown('#### События по темам карточек'),
                        dcc.Graph(
                            style={'hight': '80vw'},
                            id = 'visits_topic_area'
                        ),
                    ], className='four columns',
                ),
                html.Div(
                    [
                        dcc.Markdown('#### % событий по темам карточек'),
                        dcc.Graph(
                            style={'hight': '80vw'},
                            id = 'visits_topic_area_perc',
                        ),
                    ], className='four columns', 
                ),
                html.Div(
                    [
                        dcc.Markdown('#### События по темам источников'),
                        dcc.Graph(
                            style={'hight': '80vw'},
                            id = 'source_topic_pie'
                        ),
                    ], className='four columns',
                ),
            ], className='row',
        ),
        dcc.Markdown('#### Темы источников - темы карточек'),
        dcc.Graph(
            id = 'source_topic_heatmap',
            style={'hight': '100vw'},
        ),
    ]
)
app.title = "Дашборд Яндекс.Дзен - проект Антона Ч."

# Описываем логику дашборда
@app.callback(
    [
        Output('visits_topic_area', 'figure'),
        Output('visits_topic_area_perc', 'figure'),
        Output('source_topic_pie', 'figure'),
        Output('source_topic_heatmap', 'figure'),
     ],
    [
        Input('dt_selector', 'value'),
        Input('item_topic_selector', 'value'),
        Input('age_checklist', 'value'),
     ]
)
def update_figures(time_selector, item_topics, ages):
    
    # приводим входные параметры к нужному типу 
    start_dt = datetime.fromtimestamp(int(time_selector[0])).strftime('%Y-%m-%d %H:%M:%S')
    end_dt = datetime.fromtimestamp(int(time_selector[1])).strftime('%Y-%m-%d %H:%M:%S')
    
    # применяем фильтрацию по временной шкале
    filtered_data = dash_visits.query('dt >= @start_dt and dt <= @end_dt')
    # применяем фильтрацию по карточкам тем
    filtered_data = filtered_data.query('item_topic in @item_topics')
    # применяем фильтрацию по возрастному сегменту
    filtered_data = filtered_data.query('age_segment in @ages')

    topic_area = []
    topic_area_perc = []
    source_pie = []
    heatmap = []

    # строим заполненные области
    for item in filtered_data['item_topic'].unique():
        topic_area += [
            go.Scatter(
                x = filtered_data.query('item_topic == @item').groupby('dt')['visits'].sum().index,
                y = filtered_data.query('item_topic == @item').groupby('dt')['visits'].sum().values,
                mode='lines',
                stackgroup='one',
                line=dict(width=2),
                hoverinfo='name+x+y',
                name=item
            )
        ]

     # работаем с процентным отображением и заполнением области
    total = filtered_data \
        .groupby('dt') \
        .agg({'visits': 'sum'}) \
        .rename(columns = {'visits': 'total_visits'})

    filtered_data_perc = filtered_data \
        .set_index('dt') \
        .join(total) \
        .reset_index()
    
    filtered_data_perc['visits'] = filtered_data_perc['visits'] / filtered_data_perc['total_visits']
    
    for item in filtered_data_perc['item_topic'].unique():
        topic_area_perc += [
            go.Scatter(
                x = filtered_data_perc.query('item_topic == @item').groupby('dt')['visits'].sum().index,
                y = filtered_data_perc.query('item_topic == @item').groupby('dt')['visits'].sum().values,
                mode='lines',
                stackgroup='one',
                line=dict(width=2),
                hoverinfo='name+x+y',
                name=item
            )
        ]

    # строим круговую диаграмму по посещениям в разрезе источников
    filtered_data_source = filtered_data.groupby('source_topic')['visits'].sum()

    source_pie = [
        go.Pie(
            labels = filtered_data_source.index,
            values = filtered_data_source.values
                
        )
    ]

    # строим таблицу
    pivot = filtered_data[['item_topic', 'source_topic', 'visits']].pivot_table(
        index='item_topic',
        columns='source_topic',
        values='visits',
        aggfunc='sum'
    )
    pivot.fillna(0, inplace=True)
    heatmap = [
        go.Heatmap(
            x=pivot.columns,
            y=pivot.index,
            z=pivot.values,
            colorscale=[
                [0, 'rgb(255, 255, 204)'],
                [0.13, 'rgb(255, 237, 160)'],
                [0.25, 'rgb(254, 217, 118)'],
                [0.38, 'rgb(254, 178, 76)'],
                [0.5, 'rgb(253, 141, 60)'],
                [0.63, 'rgb(252, 78, 42)'],
                [0.75, 'rgb(227, 26, 28)'],
                [0.88, 'rgb(189, 0, 38)'],
                [1.0, 'rgb(128, 0, 38)']
            ],
            hovertemplate='Карточка: %{y}<br>Источник: %{x}<br>Посещений: %{z}',    
            name = ''      
        )
    ]

    # возвращаем заполненные области
    return (
        {
            'data': topic_area,
            'layout': go.Layout(
                xaxis={'title': 'Время события'},
                yaxis={'title': 'Количество событий'}
            )
        },
        {
            'data': topic_area_perc,
            'layout': go.Layout(
                xaxis={'title': 'Время события'},
                yaxis={'title': 'Доля (%) событий'}
            )
        },
        {
            'data': source_pie
        },
        {
            'data': heatmap
        },
    )

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
