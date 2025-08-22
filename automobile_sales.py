import pandas as pd
import plotly.express as px
from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

sales_cvs = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"

df = pd.read_csv(sales_cvs)

# Create dash dashboard
app = Dash(__name__)


# Design the structure of dashboard
app.layout = html.Div([html.H1('Automobile Sales Statistics Dashboard',
                               style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 24}),
                       html.Div(dcc.Dropdown(id='dropdown-statistics',
                                             options=[{'label':'Yearly Statistics', 'value': 'Yearly Statistics'},
                                                      {'label':'Recession Period Statistics', 'value': 'Recession Period Statistics'}
                                                      ],
                                             value='Select Statistics',
                                             placeholder='Select a report type',
                                             style={'textAlign': 'center', 'width': '80%', 'padding': 3, 'fontSize': 20}
                                             )
                                ),
                       html.Div(dcc.Dropdown(id='select-year',
                                             options=[{'label': i, 'value': i} for i in range(1980, 2024, 1)],
                                             placeholder='Select-year',
                                             style={'textAlign': 'center', 'width': '80%', 'padding': 3, 'fontSize': 20}
                                             )
                                ),
                       html.Div(html.Div(id='output-container',
                                         className='chart-grid',
                                         style={'display': 'flex'})
                                )
                       ])


# Design of callback decorator and callback function
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value'))
def update_input_container(input_statistics):
    if input_statistics == 'Yearly Statistics':
        return False
    else:
        return True

@app.callback(Output(component_id='output-container', component_property='children'),
              [Input(component_id='dropdown-statistics', component_property='value'),
               Input(component_id='select-year', component_property='value')])
def update_output_container(input_statistics, entered_year):
    if input_statistics == 'Recession Period Statistics':
        df_recession = df[df['Recession'] == 1]

        # Plot 1
        autosales_yearly_rec = df_recession.groupby('Year')['Automobile_Sales'].mean().reset_index()
        r_chart_1 = dcc.Graph(figure=px.line(autosales_yearly_rec,
                                             x='Year',
                                             y='Automobile_Sales',
                                             markers=True,
                                             title='Average automobile sales over year during recession period'))

        # Plot 2
        autosales_type_rec = df_recession.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        r_chart_2 = dcc.Graph(figure=px.bar(autosales_type_rec,
                                            x='Vehicle_Type',
                                            y='Automobile_Sales',
                                            title='Average automobile sales by each vehicle types during recession period'))

        # Plot 3
        advertise_type_rec = df_recession.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        r_chart_3 = dcc.Graph(figure=px.pie(advertise_type_rec,
                                            names='Vehicle_Type',
                                            values='Advertising_Expenditure',
                                            title='Total advertising expenditure by each vehicle types during recession period'))

        # Plot 4
        unemploy_vehicle_rec = df_recession.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        r_chart_4 = dcc.Graph(figure=px.bar(unemploy_vehicle_rec,
                                x='unemployment_rate',
                                y='Automobile_Sales',
                                color='Vehicle_Type',
                                labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                                title='Effect of Unemployment Rate on Vehicle Type and Sales'))

        return html.Div([
            html.Div([r_chart_1, r_chart_2], style={'display': 'flex'}),
            html.Div([r_chart_3, r_chart_4], style={'display': 'flex'})
        ])

    elif input_statistics == 'Yearly Statistics' and entered_year:
        df_year = df[df['Year'] == entered_year]

        # Plot 1
        average_sale_year = df.groupby('Year')['Automobile_Sales'].mean().reset_index()
        y_chart_1 = dcc.Graph(figure=px.line(average_sale_year,
                                             x='Year',
                                             y='Automobile_Sales',
                                             title='Average Automobile sales yearly')
                              )

        # Plot 2
        monthly_sales_year = df_year.groupby('Month')['Automobile_Sales'].sum().reset_index()
        y_chart_2 = dcc.Graph(figure=px.line(monthly_sales_year,
                                             x='Month',
                                             y='Automobile_Sales',
                                             title='Total Monthly Automobile Sales')
                              )

        # Plot 3
        avg_sales_vehicle_year = df_year.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        y_chart_3 = dcc.Graph(figure=px.bar(avg_sales_vehicle_year,
                                            x='Vehicle_Type',
                                            y='Automobile_Sales',
                                            title='Average Vehicles Sold by Vehicle Type in the year {}'.format(entered_year))
                  )

        # Plot 4
        advertise_vehicle_year = df_year.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        y_chart_4 = dcc.Graph(figure=px.pie(advertise_vehicle_year,
                                            names='Vehicle_Type',
                                            values='Advertising_Expenditure',
                                            title='Total Advertisment Expenditure for Each Vehicle'))

        return html.Div([
            html.Div([y_chart_1, y_chart_2], style={'display': 'flex'}),
            html.Div([y_chart_3, y_chart_4], style={'display': 'flex'})
        ])


if __name__ == '__main__':
    app.run(debug=True)