"""Module containing all components needed in the application"""
# pylint: disable=no-member
# pylint: disable=import-error

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

# Loader
loader = html.Div(
    id="loader",
    children=[
        html.Div(
            dbc.Button(
                id="spinner",
                children=[dbc.Spinner(size="lg"), " Loading..."],
                color="primary",
                disabled=True,
                style={
                    "align-items": "center",
                    "display": "flex",
                    "white-space": "break-spaces",
                },
            ),
        )
    ],
    style={
        "backgroundColor": "rgba(232,232,232,0.5)",
        "position": "absolute",
        "zIndex": "1",
        "height": "100%",
        "width": "100%",
        "top": "0",
        "left": "0",
        "display": "flex",
        "align-items": "center",
        "justify-content": "center",
    },
)

infos_tab = dbc.Card(
    children=[
        dbc.CardBody(
            dbc.Table(id="infos-table", children=[
                html.Tr([html.Td("IP address"), html.Td("")]),
                html.Tr([html.Td("Processor number"), html.Td("")]),
                html.Tr([html.Td("Model name"), html.Td("")]),
                html.Tr([html.Td("CPU frequence"), html.Td("")]),
                html.Tr([html.Td("Number of CPU cores"), html.Td("")]),
            ]),
        )
    ],
    id="infos-card",
    body=True,
    className="mt-3",
)

graph_tab = dbc.Card(
    children=[
        dbc.CardBody(
            dbc.Col(
                [
                    dbc.Row(
                        children=[
                            dcc.Graph(id="py-memory", style={"width": "45%"}),
                            dcc.Graph(id="scat-tx", style={"width": "45%"}),
                        ]
                    ),
                    dbc.Row(
                        children=[
                            dcc.Graph(id="py-response-time", style={"width": "45%"}),
                            dcc.Graph(id="scat-rx", style={"width": "45%"}),
                        ]
                    ),
                ]
            )
        )
    ],
    id="graph-card",
    body=True,
    className="mt-3",
)

processes_tab = dbc.Card(
    children=[
        dbc.CardBody(
            children=[
                dbc.Table(
                    children=[
                        html.Thead(
                            html.Tr(
                                [
                                    html.Th("Process number"),
                                    html.Th("Time"),
                                    html.Th("Command"),
                                ]
                            )
                        ),
                        html.Tbody(children=[], id="process-table"),
                    ],
                    bordered=True,
                )
            ]
        )
    ],
    id="processes-card",
    body=True,
    className="mt-3",
)

logs_tab = dbc.Card(
    children=[
        dbc.CardBody(
            children=[
                dbc.Table(
                    children=[
                        html.Thead(
                            html.Tr(
                                [
                                    html.Th("IP host"),
                                    html.Th("Request"),
                                    html.Th("Time"),
                                    html.Th("Request status"),
                                ]
                            )
                        ),
                        html.Tbody(
                            children=[],
                            id="logs-table",
                        ),
                    ],
                    bordered=False,
                )
            ]
        )
    ],
    id="logs-card",
    body=True,
    className="mt-3",
)

server_tab = dbc.Card(
    children=[
        dbc.CardBody(
            children=[
                html.Div(loader),
                dbc.Card(
                    [
                        dbc.CardHeader(
                            dbc.Tabs(
                                children=[
                                    dbc.Tab(
                                        infos_tab, label="Informations", id="infos-tab"
                                    ),
                                    dbc.Tab(graph_tab, label="Graphs", id="graph-tab"),
                                    dbc.Tab(
                                        processes_tab,
                                        label="Process",
                                        id="processes-tab",
                                    ),
                                    dbc.Tab(logs_tab, label="Logs", id="logs-tab"),
                                ],
                                id="sub-card-tabs",
                                card=True,
                                active_tab="tab-0",
                            )
                        ),
                    ],
                ),
                dbc.Button(
                    "Delete server",
                    color="danger",
                    id="delete-server",
                    style={"margin-top": "1%"},
                ),
                dcc.Interval(
                    id="interval-component",
                    interval=5000,  # in milliseconds
                    n_intervals=0,
                ),
                dcc.Interval(
                    id="check-component", interval=500, n_intervals=0  # in milliseconds
                ),
            ],
        ),
    ],
    body=True,
    className="mt-3",
)

add_server_tab = dbc.Card(
    children=[
        dbc.CardBody(
            children=[
                # Fake button
                html.Div(id="delete-server", style={"display": "none"}),
                dbc.Toast(
                    [html.P("Check at your inputs or check server.", className="mb-0")],
                    id="toast-error",
                    header="Error",
                    icon="danger",
                    dismissable=True,
                    style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                    is_open=False,
                ),
                dbc.Toast(
                    [html.P("Server added.", className="mb-0")],
                    id="toast-success",
                    header="Success",
                    icon="success",
                    dismissable=True,
                    style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                    is_open=False,
                ),
                dbc.Toast(
                    [html.P("Server removed.", className="mb-0")],
                    id="toast-remove",
                    header="Warning",
                    icon="warning",
                    dismissable=True,
                    style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                    is_open=False,
                ),
                dbc.Toast(
                    [html.P("This server is already added.", className="mb-0")],
                    id="toast-exist",
                    header="Warning",
                    icon="warning",
                    dismissable=True,
                    style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                    is_open=False,
                ),
                dbc.Form(
                    id="add-server-form",
                    children=[
                        dbc.Label("Server name", html_for="server-name"),
                        dbc.Input(
                            type="text",
                            id="server-name",
                            placeholder="Example: Unicorn",
                        ),
                        dbc.Label(
                            "IP address", html_for="ip", style={"margin-top": "2%"}
                        ),
                        dbc.Input(
                            type="text",
                            id="ip",
                            placeholder="Example: 128.1.56.93",
                        ),
                        dbc.Label(
                            "Username", html_for="username", style={"margin-top": "2%"}
                        ),
                        dbc.Input(
                            type="text",
                            id="username",
                            placeholder="Username to connect on server",
                        ),
                        dbc.Label(
                            "Password", html_for="password", style={"margin-top": "2%"}
                        ),
                        dbc.Input(
                            type="password",
                            id="password",
                            placeholder="ilovemypassword",
                        ),
                        dbc.Label("Port", html_for="port", style={"margin-top": "2%"}),
                        dbc.Input(
                            type="number",
                            id="port",
                            placeholder="Port to connect to.",
                        ),
                        dbc.Button(
                            "Add Server",
                            id="submit-add-server",
                            color="primary",
                            style={"margin-top": "2%"},
                            type="submit",
                        ),
                    ],
                    action="#",
                    method="",
                ),
            ]
        )
    ],
    body=True,
    className="mt-3",
)
