import streamlit as st
import pandas as pd


def default_plot(means_dataframe):
    json_means = means_dataframe.to_json(orient='records')

    vega_lite_spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "layer": [
            {
                "mark": {"type": "line", "point": True},
                "encoding": {
                    "x": {"field": "Test", "type": "ordinal", "sort": {"field": "index"}},
                    "y": {"field": "Normalized", "type": "quantitative"},
                },
                "data": {"values": json_means}
            }
        ]
    }
    return vega_lite_spec
