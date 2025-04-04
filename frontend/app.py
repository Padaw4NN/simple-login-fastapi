import dash
from dash import html, dcc
from dash.dependencies import Output, Input, State
import requests

dash_app = dash.Dash(__name__)
server = dash_app.server

dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

login_layout = html.Div([
    html.H2("Login"),
    dcc.Input(id='email', type='email', placeholder='Email'),
    dcc.Input(id='password', type='password', placeholder='Password'),
    html.Button('Login', id='login-button'),
    html.Div(id='login-output')
])

register_layout = html.Div([
    html.H2("Register"),
    dcc.Input(id='reg-email', type='email', placeholder='Email'),
    dcc.Input(id='reg-username', type='text', placeholder='Username'),
    dcc.Input(id='reg-password', type='password', placeholder='Password'),
    html.Button('Register', id='register-button'),
    html.Div(id='register-output')
])

@dash_app.callback(
    dash.Output('page-content', 'children'),
    [dash.Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/login':
        return login_layout
    elif pathname == '/register':
        return register_layout
    return html.H1("Welcome to the App")

@dash_app.callback(
    Output('login-output', 'children'),
    [Input('login-button', 'n_clicks')],
    [State('email', 'value'), State('password', 'value')]
)
def login_user(n_clicks, email, password):
    if n_clicks > 0 and email and password:
        response = requests.post("http://backend:8081/login", json={"email": email, "password": password})
    if response.status_code == 200:
        return response.json().get("message", "Successful Login!")
    else:
        return response.json().get("message", "Incorrect Credentials!")
    #return ""

@dash_app.callback(
    Output('register-output', 'children'),
    [Input('register-button', 'n_clicks')],
    [State('reg-email', 'value'), State('reg-username', 'value'), State('reg-password', 'value')]
)
def register_user(n_clicks, email, username, password):
    if n_clicks > 0 and email and username and password:
        response = requests.post("http://backend:8081/register", json={"email": email, "username": username, "password": password})
        return response.json().get("message", "Registration successfully!")
    return ""

if __name__ == '__main__':
    dash_app.run(host='0.0.0.0', port=8050, debug=False)
