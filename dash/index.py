import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, ALL, MATCH, Patch, ctx, dash_table
from dash.exceptions import PreventUpdate
import time
import pandas as pd

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


TEXT = '''There are some other worrying signals that wage growth could be slowing.'''
text_list = list(TEXT)
slider_min, slider_max = 0, len(text_list)
slider_marks = {i: v for i, v in enumerate(text_list)}
add_label_button = dbc.Button('Add Label', id='add-label-button', n_clicks=0)
save_labels_button = dbc.Button('Save Labels', id='save-labels-button')
button_row = dbc.Row([dbc.Col(add_label_button), dbc.Col(save_labels_button)])

app.layout = dbc.Container(
    [
        html.H1("SpanCat Labeling"),
        html.Hr(),
        button_row,
        html.Br(),
        html.Div(id='dynamic-slider-container-div', children=[]),
        html.Div(id='temp-output')
    ],
    fluid=True
)


@app.callback(
    Output('dynamic-slider-container-div', 'children'),
    Input('add-label-button', 'n_clicks')
    )
def display_dropdowns(n_clicks):
    patched_children = Patch()
    new_element = html.Div([
        html.Br(),
        dcc.RangeSlider(
            slider_min, slider_max, step=1, marks=slider_marks, value=[4, 11], allowCross=False,
            id={'type': 'dynamic-range-slider', 'index': n_clicks}),
        html.Br(),
        html.H4('Type label for selected span:'),
        dbc.InputGroup([
            dbc.InputGroupText(id={'type': 'dynamic-selected-group-text', 'index': n_clicks}),
            dbc.Input(id={'type': 'dynamic-input-text', 'index': n_clicks})
        ], className='mb-3'),
        html.Hr(),
    ])
    patched_children.append(new_element)
    return patched_children


@app.callback(
    Output({'type': 'dynamic-selected-group-text', 'index': MATCH}, 'children'),
    Input({'type': 'dynamic-range-slider', 'index': MATCH}, 'value'),
)
def display_output(slider_value):
    return text_list[slider_value[0]:slider_value[1]]


@app.callback(
    Output('temp-output', 'children'),
    Input('save-labels-button', 'n_clicks'),
    State({'type': 'dynamic-input-text', 'index': ALL}, 'value'),
    State({'type': 'dynamic-range-slider', 'index': ALL}, 'value'),
    prevent_initial_call=True
)
def save_labels(n_clicks, all_labels, all_range_values):
    tuples_list = [(ind[0], ind[1], label) for label, ind in zip(all_labels, all_range_values)]
    dict2save = {'text': TEXT, 'labels': tuples_list}
    with open("labeled_data.txt", "a") as saved_file:
        saved_file.write('{}'.format(dict2save) + '\n')
    return 'Saved data as: {}'.format(tuples_list)


if __name__ == "__main__":
    app.run_server(debug=True)
