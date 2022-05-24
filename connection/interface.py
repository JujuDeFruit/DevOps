# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 13:38:33 2020

@author: Paul
"""

# pylint: disable=no-member
# pylint: disable=import-error
# pylint: disable=no-name-in-module
# pylint: disable=global-statement
# pylint: disable=unused-argument
# pylint: disable=broad-except
# pylint: disable=too-many-arguments
# pylint: disable=global-at-module-level
# pylint: disable=too-many-locals
# pylint: disable=invalid-name
# pylint: disable=too-many-function-args

import time
import dash
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc


import connect
from dash_components import server_tab, add_server_tab
from functions_interface import (
    recup_memory,
    recup_response_time,
    has_values,
    recup_static_infos,
    recup_processes,
    recup_logs,
    recup_rx_tx,
)

tabs = [
    dbc.Tab(add_server_tab, label="Add server", id="add-tab"),
]

app = dash.Dash(external_stylesheets=[dbc.themes.LITERA])

app.layout = html.Div(
    children=[
        dbc.Card(
            [
                dbc.CardHeader(
                    dbc.Tabs(
                        children=tabs,
                        id="card-tabs",
                        active_tab="tab-0",
                        card=True,
                    )
                ),
            ],
        ),
        # Hidden div for empty output callback
        html.Div(id="hidden-div", style={"display": "none"}),
    ]
)


@app.callback(
    Output("hidden-div", "children"),
    Input("interval-component", "n_intervals"),
    [State("card-tabs", "active_tab")],
)
def update(n_iteration, active_tab):
    """
    Refresh data get from the server

    Parameters
    ----------
    n_iteration: iteration to call this function
    active_tab: current tab

    """
    global SSH_DICT
    if SSH_DICT[active_tab] is not None:
        SSH_DICT[active_tab].execute()


@app.callback(
    Output("loader", "style"),
    Input("check-component", "n_intervals"),
    [State("loader", "style"), State("card-tabs", "active_tab")],
)
def update_loader(n_iteration, style, active_tab):
    """
    Update loader, to make it disappears when data is loaded

    Parameters
    ----------
    n_iteration: current iteration
    style: current style of the loader
    active_tab: current tab

    Returns
    -------
    style: style of the loader, can contain
        display: none to make it disappear

    """
    global SSH_DICT
    ssh = SSH_DICT[active_tab]
    if ssh is not None and has_values(ssh):
        style["display"] = "none"
    return style


@app.callback(
    Output("infos-table", "children"),
    Input("interval-component", "n_intervals"),
    [
        State("card-tabs", "active_tab"),
    ],
)
def load_static_infos(n_iteration, active_tab):
    """
    Load static informations (such as model name...) from the server

    Parameters
    ----------
    n_iteration: current iteration
    active_tab: current tab

    Returns
    -------
    children: update card iformations to print lines in array

    """
    global SSH_DICT
    ip_serv, proc, model, freq, nb_cpu = recup_static_infos(SSH_DICT[active_tab])
    children = (
        html.Tbody(
            [
                html.Tr([html.Td("IP address"), html.Td(ip_serv)]),
                html.Tr([html.Td("Processor number"), html.Td(proc)]),
                html.Tr([html.Td("Model name"), html.Td(model)]),
                html.Tr([html.Td("CPU frequence"), html.Td(freq + " MHz")]),
                html.Tr([html.Td("Number of CPU cores"), html.Td(nb_cpu)]),
            ],
        ),
    )
    return children


list_tx = []
list_rx = []
list_time = []
TX_PREC = 0
RX_PREC = 0


@app.callback(
    Output("py-memory", "figure"),
    Output("py-response-time", "figure"),
    Output("scat-tx", "figure"),
    Output("scat-rx", "figure"),
    Input("interval-component", "n_intervals"),
    [State("card-tabs", "active_tab")]
)
def update_graph(n_iteration, active_tab):
    """
    Update data in graphs

    Parameters
    ----------
    n_iteration: current iteration
    active_tab: current tab

    Returns
    -------
    figure_memory: new figure to display in the memory graph
    figure_response_time: new figure to display in the response time graph

    """
    global SSH_DICT

    ssh = SSH_DICT[active_tab]
    mem_labs, mem_vals, mem_percent, cpu_labs, cpu_vals, \
        cpu_percent, mem_cpu_cache_total = recup_memory(ssh)
    print(cpu_percent)
    response_time = recup_response_time(ssh)
    rx, tx = recup_rx_tx(ssh)
    cur_time = time.strftime("%H:%M:%S", time.localtime())

    figure_memory = {
        "data": [
            go.Pie(
                labels=mem_labs,
                values=mem_vals,
                title={"text": "Use percentage : " + str(round(mem_percent, 1)) + "%"},
            )
        ],
        "layout": {"title": "Memory Pie"},
    }

    figure_response_time = {
        "data": [
            go.Indicator(
                mode="gauge+number",
                value=response_time,
                domain={"x": [0, 1], "y": [0, 1]},
            )
        ],
        "layout": {"title": "Response Time"},
    }

    global RX_PREC
    global TX_PREC
    if TX_PREC == 0 and RX_PREC == 0:
        TX_PREC = tx
        RX_PREC = rx
    else:
        tx_calc = int(tx) - int(TX_PREC)
        rx_calc = int(rx) - int(RX_PREC)
        TX_PREC = tx
        RX_PREC = rx
        list_tx.append(tx_calc)
        list_rx.append(rx_calc)
        list_time.append(cur_time)

    figure_tx = {
        "data": [
            go.Scatter(
                y=list_tx,
                x=list_time,
                mode="lines",
                name="TX",
            ),
            go.Scatter(
                y=list_rx,
                x=list_time,
                mode="lines",
                name="RX",
            ),
        ],
        "layout": {"title": "TX/RX Packets Stats"},
    }

    figure_memory_cpu = {
        "data": [
            go.Pie(
                labels=cpu_labs,
                values=cpu_vals,
                title={"text": "CPU Cache Total : " + str(round(mem_cpu_cache_total, 1)) + "KB"},
            )
        ],
        "layout": {"title": "CPU Cache Pie"},
    }

    return figure_memory, figure_response_time, figure_tx, figure_memory_cpu


@app.callback(
    Output("process-table", "children"),
    Input("interval-component", "n_intervals"),
    [State("card-tabs", "active_tab")],
)
def update_processes(n_iteration, active_tab):
    """
    Get and update processes running on the server

    Parameters
    ----------
    n_iteration: current iteration
    active_tab: current tab

    Returns
    -------
    children: return new children with processes to print

    """
    global SSH_DICT
    processes = recup_processes(SSH_DICT[active_tab])
    children = []
    for procs in processes:
        children.append(
            html.Tr([html.Td(procs[0]), html.Td(procs[1]), html.Td(procs[2])]),
        )
    return children


@app.callback(
    Output("logs-table", "children"),
    Input("interval-component", "n_intervals"),
    [State("card-tabs", "active_tab")],
)
def update_logs(n_iteration, active_tab):
    """
    Update & get logs

    Parameters
    ----------
    n_iteration: current iteration
    active_tab: current tab

    Returns
    -------
    children: children containing all processes to print

    """
    global SSH_DICT
    children = []
    logs = recup_logs(SSH_DICT[active_tab])
    for data in logs:
        splitted = data.split(" | ")
        try:
            children.append(
                html.Tr(
                    [
                        html.Td(splitted[0]),
                        html.Td(splitted[1], style={"word-break": "break-word"}),
                        html.Td(splitted[2]),
                        html.Td(splitted[3]),
                    ]
                )
            )
        except Exception:
            pass
    return children


@app.callback(
    [
        Output("card-tabs", "children"),
        Output("toast-error", "is_open"),
        Output("toast-success", "is_open"),
        Output("toast-remove", "is_open"),
        Output("toast-exist", "is_open"),
        Output("card-tabs", "active_tab"),
    ],
    [Input("submit-add-server", "n_clicks"), Input("delete-server", "n_clicks")],
    [
        State("server-name", "value"),
        State("ip", "value"),
        State("username", "value"),
        State("password", "value"),
        State("port", "value"),
        State("card-tabs", "active_tab"),
    ],
)
def add_remove_server(
        n_add, n_remove, server_name, ip_serv, username, password, port, active_tab
):
    """
    Add or remove a server from the board.

    Parameters
    ----------
    n_add: number of time button add server was clicked
    n_remove: number of time button delete server was clicked
    server_name: server name to add
    ip_serv: ip of the new server
    username: username to connect to on the new server
    password: password to connect to
    port: port to connect to
    active_tab: current tab

    Returns
    -------
    tabs: new tabs (remove, added or nothing)
    boolean: print error toast
    boolean: print success toast
    boolean: print remove toast
    boolean: print exist toast
    "tab-0": active tab set

    """
    # List of ssh connections
    global SSH_DICT

    # If user click on add server
    if n_add is not None and n_add > 0:
        config = {
            "ip": str(ip_serv),
            "user": str(username),
            "password": str(password),
            "port": int(port),
        }

        # Create new ssh object with configuration
        new_ssh = connect.SSH(server_=config)

        # If server is added many times, cancel and return warning
        if new_ssh in SSH_DICT.values():
            return tabs, False, False, False, True, "tab-0"

        # Try connection
        err = new_ssh.connect()

        # If connection is OK
        if not err:
            # Update tabs
            tabs.append(dbc.Tab(server_tab, label=server_name, id=server_name))
            # Add current client to connected client dict corresponding to the good tab
            SSH_DICT["tab-" + str(len(SSH_DICT) + 1)] = new_ssh
            # Return success toast
            return tabs, False, True, False, False, "tab-0"
        # Return error toast
        return tabs, True, False, False, False, "tab-0"

    # If user clicked on remove server
    if n_remove is not None and n_remove > 0:
        # Get current tab id (0 for the first beginning by left)
        idx = int(active_tab.split("-")[1])
        tab = tabs[idx]
        # Remove ssh client from the list
        SSH_DICT[active_tab].close()
        SSH_DICT.pop(active_tab)
        # Remove tab
        tabs.remove(tab)
        # Return toast
        return tabs, False, False, True, False, "tab-0"
    return None


if __name__ == "__main__":

    global SSH_DICT

    SSH_DICT = {}

    app.run_server(debug=False, host="0.0.0.0")

    for val in SSH_DICT.values():
        if val is not None:
            val.close()
