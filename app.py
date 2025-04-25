import dash
from dash import dcc, html, Input, Output, State, dash_table
import pandas as pd
from data_preprocessor import DataPreprocessor
from data_evaluator import DataEvaluator
from data_loader import DataLoader
from data_report import DataReport
from data_filter import DataFilter
import base64
from io import StringIO

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Data Processing Interface"),

    # 1. File Upload
    html.Div([
        html.H3("File Upload"),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=False
        ),
    ]),

    dash_table.DataTable(id='data-preview-table', page_size=10),
    # Data Preprocessing Control
    html.Div([
        html.H3("Data Preprocessing"),
        html.Button("Preprocess Data", id="preprocess-button", n_clicks=0),
    ]),

    # 4. Preprocessed Data Preview
    html.Div([
        html.H3("Preprocessed Data Preview"),
        dash_table.DataTable(id='preprocessed-data-table', page_size=10),
    ]),

    # 5. Result Field Creation
    html.Div([
        html.H3("Result Field Creation"),
        html.Div([
            html.Label("Result Field Name:"),
            dcc.Input(id="result-field-name", type="text", value="result", style={'marginRight': '10px'}),
        ]),
        html.Div([
            html.Label("Formula:"),
            dcc.Input(id="result-field-formula", type="text", value="", style={'width': '50%'}),
            html.Button("Create Result Field", id="create-result-button", n_clicks=0),
        ]),
    ]),

    # 6. Filter Customization
    html.Div([
        html.H3("Filter Customization"),
        html.Label("Filter Formula:"),
        dcc.Input(id="filter-formula", type="text", value="", style={'width': '50%', 'marginRight': '10px'}),
        html.Label("Columns to Display:"),
        dcc.Dropdown(id="columns-to-display", multi=True, style={'width': '50%'}),
            html.Button("Apply Filters", id="apply-filters-button", n_clicks=0),
            dash_table.DataTable(id="filtered-data-table", page_size=10)
    ]),

    # 7. Profit Calculation
    html.Div([
        html.H3("Profit Calculation"),
        html.Label("Select Profit Field:"),
        dcc.Dropdown(id="profit-field-dropdown", style={'width': '50%'}),
        html.Button("Calculate Profit", id="calculate-profit-button", n_clicks=0),
        html.Div(id='profit-result')
    ]),    
    dash_table.DataTable(id="result-data-table", page_size=10),

    # Hidden div to store the data
    html.Div(id='intermediate-data', style={'display': 'none'}),
    html.Div(id='preprocessed-data', style={'display': 'none'}),
    html.Div(id="data-with-result", style={"display": "none"}),
    html.Div(id='filtered-data', style={'display': 'none'}),

])


# Callback to handle file upload and store data
@app.callback(
    Output('intermediate-data', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def load_data(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            raise Exception("file not supported")
        
        loader = DataLoader(df)
        loaded_data = loader.load_data()

        return loaded_data.to_json(date_format='iso', orient='split')


# Callback to display data sample
@app.callback(
    Output('data-preview-table', 'data'),
    Input('intermediate-data', 'children')
)
def display_data(jsonified_data):
    if jsonified_data is not None:
        df = pd.read_json(jsonified_data, orient='split')
        return df.to_dict('records')

# Callback to preprocess data
@app.callback(
    Output('preprocessed-data', 'children'),
    Input('preprocess-button', 'n_clicks'),
    State('intermediate-data', 'children')
)
def preprocess_data(n_clicks, jsonified_data):
    if n_clicks > 0 and jsonified_data is not None:
        df = pd.read_json(jsonified_data, orient='split')
        preprocessor = DataPreprocessor(df)
        preprocessed_data = preprocessor.process_data()
        return preprocessed_data.to_json(date_format='iso', orient='split')


# Callback to display preprocessed data sample
@app.callback(
    Output('preprocessed-data-table', 'data'),
    Input('preprocessed-data', 'children')
)
def display_preprocessed_data(jsonified_data):
    if jsonified_data is not None:
        df = pd.read_json(jsonified_data, orient='split')
        return df.to_dict('records')


# Callback to create result field
@app.callback(
    Output('data-with-result', 'children'),
    Input('create-result-button', 'n_clicks'),
    State('preprocessed-data', 'children'),
    State('result-field-name', 'value'),
    State('result-field-formula', 'value')
)
def create_result_field(n_clicks, jsonified_data, field_name, formula):
    if n_clicks > 0 and jsonified_data is not None and field_name and formula:
        df = pd.read_json(jsonified_data, orient='split')
        evaluator = DataEvaluator(df)
        df_with_result = evaluator.create_custom_result(field_name, formula)
        return df_with_result.to_json(date_format='iso', orient='split')

@app.callback(
    Output('result-data-table', 'data'),
    Input('data-with-result', 'children')
)
def display_result_data(jsonified_data):
    if jsonified_data is not None:
        df = pd.read_json(jsonified_data, orient='split')
        return df.to_dict('records')



@app.callback(
    [Output('filtered-data', 'children'), Output('columns-to-display', 'options')],
    Input('apply-filters-button', 'n_clicks'),
    State('data-with-result', 'children'),
    State('filter-formula', 'value'),
    State('columns-to-display', 'value')
)
def filter_data(n_clicks, jsonified_data, filter_formula, selected_columns):
    if n_clicks > 0 and jsonified_data is not None:
        df = pd.read_json(jsonified_data, orient='split')
        filter = DataFilter(df)
        if selected_columns:
            filtered_data = filter.filter_columns(selected_columns)
        filtered_data = filter.filter_rows(filter_formula)
        
        return filtered_data.to_json(date_format='iso', orient='split'), [{'label': col, 'value': col} for col in df.columns]

@app.callback(
    Output('filtered-data-table', 'data'),
    Input('filtered-data', 'children')
)
def display_filtered_data(jsonified_data):
    if jsonified_data is not None:
        df = pd.read_json(jsonified_data, orient='split')
        return df.to_dict('records')


@app.callback(
    [Output('profit-result', 'children'), Output('profit-field-dropdown', 'options')],
    Input('calculate-profit-button', 'n_clicks'),
    State('filtered-data', 'children'),
    State('profit-field-dropdown', 'value')
)
def calculate_profit(n_clicks, jsonified_data, profit_field):
    if n_clicks > 0 and jsonified_data is not None and profit_field is not None:
        df = pd.read_json(jsonified_data, orient='split')
        report = DataReport(df)
        profit = report.calculate_profit(profit_field)
        return f"Profit: {profit}", [{'label': col, 'value': col} for col in df.columns]
    return None,[]


if __name__ == '__main__':
    app.run_server(debug=True)