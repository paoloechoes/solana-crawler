import json
import os
import pandas as pd
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from .data import get_transfers_for_address


app = FastAPI()
app.mount(
    "/static",
    StaticFiles(
        directory=os.path.dirname(os.path.abspath(__file__)) + "/ui/static"
    ),
    name="static",
)
app.mount(
    "/ui",
    StaticFiles(directory=os.path.dirname(os.path.abspath(__file__)) + "/ui"),
    name="ui",
)
templates = Jinja2Templates(
    directory=os.path.dirname(os.path.abspath(__file__)) + "/ui/templates"
)


def _build_graph(
    central_address: str, df_in: pd.DataFrame, df_out: pd.DataFrame
):
    """
    Return two lists of Nodes and Edges which repersent the graph.
    """
    nodes = {}
    edges = []
    nodes[central_address] = {
        "id": central_address,
        "label": central_address,
        "color": "#ff9900",
    }

    for _, row in df_in.iterrows():
        from_address = row["from_address"]
        if from_address not in nodes:
            nodes[from_address] = {"id": from_address, "label": from_address}
        edges.append(
            {
                "from": from_address,
                "to": central_address,
                "label": "in",
                "value": row["value"],
            }
        )

    for _, row in df_out.iterrows():
        to_address = row["to_address"]
        if to_address not in nodes:
            nodes[to_address] = {"id": to_address, "label": to_address}
        edges.append(
            {
                "from": central_address,
                "to": to_address,
                "label": "out",
                "value": row["value"],
            }
        )

    return list(nodes.values()), edges


@app.get("/{address}", response_class=HTMLResponse)
async def index(request: Request, address: str, num: int = 10):
    df_txs = get_transfers_for_address(address, num=num)
    nodes, edges = _build_graph(address, df_txs[0], df_txs[1])
    html_table_in = df_txs[0].to_html()
    html_table_out = df_txs[1].to_html()

    df_in_json = df_txs[0].to_dict(orient="records")
    df_out_json = df_txs[1].to_dict(orient="records")

    context = {
        "request": request,
        "table_in": html_table_in,
        "table_out": html_table_out,
        "nodes": nodes,
        "edges": edges,
        "df_out": df_out_json,
        "df_in": df_in_json,
    }
    return templates.TemplateResponse("index.html", context)
