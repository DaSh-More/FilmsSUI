import json
import re

import httpx
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")


@st.cache_data
def films_dataset():
    df = pd.read_csv("./netflix_titles.csv")
    return df


col_url, col_btn = st.columns([3, 1])
with col_url:
    url = st.text_input(
        "URL запроса",
        "https://ml.shevkunov.space/v2/models/filmsrec/versions/1/infer",
        label_visibility="collapsed",
    )
with col_btn:
    execute = st.button("Выполнить")
col1, col2, col3 = st.columns(3)

with col1:
    body = st.text_area(
        "JSON тело запроса",
        """{
    "inputs": [
        {
            "name": "film_index",
            "datatype": "INT64",
            "shape": [1],
            "data": [42]
        },
        {
            "name": "top_k",
            "datatype": "INT64",
            "shape": [1],
            "data": [7]
        }
    ]
}""",
        height="content",
    )
    if execute:
        json_body = json.loads(body)
        response = httpx.post(url, json=json_body)
        result = response.json()

        with col2:
            st.code(
                re.sub(
                    r"(\d)\s?\n\s*\]",
                    r"\1]",
                    re.sub(
                        r"\n\s*(\d+,?)(?:\n])?", r"\1 ", json.dumps(result, indent=2)
                    ),
                )
            )

        with col3:
            st.table(films_dataset().iloc[result["outputs"][0]["data"]]["title"])
