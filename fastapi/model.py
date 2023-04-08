import os
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import datetime
from pathlib import Path
from copy import deepcopy

import numpy as np
import pandas as pd
import joblib
from prophet import Prophet

BASE_DIR = Path(__file__).resolve(strict=True).parent

dtype = {"month":object, "resale_price":np.int64, "town":object, "flat_type":object}
DATA = pd.DataFrame()
for chunk in pd.read_csv('hdb_data.csv',
                         header=None,
                         names=['month', 'resale_price', 'town', 'flat_type'],
                         chunksize=1000,
                         dtype=dtype):
    DATA = pd.concat([DATA, chunk], ignore_index=True)


def preprocess_df_by_params(town, flat_type):
    df = deepcopy(DATA)
    df = df[(df.town == town) & (df.flat_type == flat_type)]
    df = df[['month', 'resale_price']]
    df = df.groupby(['month'], as_index=False).mean().round(0)
    df = df[['month', 'resale_price']]
    df = df.rename({'month': 'ds', 'resale_price': 'y'}, axis=1)
    return df


def train(params: dict):
    town = params['town']
    flat_type = params['flat_type']
    town_flat_type = town+' '+flat_type
    df = preprocess_df_by_params(town, flat_type)
    m = Prophet(seasonality_mode='multiplicative',
                changepoint_prior_scale=0.5,
                seasonality_prior_scale=0.01,
                changepoint_range=0.95)
    m.fit(df)
    joblib.dump(m, Path(BASE_DIR).joinpath(f"{town_flat_type}.joblib"))
    return m


def predict(params: dict):
    town = params['town']
    flat_type = params['flat_type']
    town_flat_type = town+' '+flat_type
    model_file = Path(BASE_DIR).joinpath(f"{town_flat_type}.joblib")
    print(model_file)
    if not model_file.exists():
        print("Model Built from Scratch")
        model = train(params)
    else:
        print("Model Loaded")
        model = joblib.load(model_file)
    future = model.make_future_dataframe(periods=36, freq='MS')
    forecast = model.predict(future)
    return {'town': town,
            'flat_type': flat_type,
            "data": forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict("records")}


def convert(params: dict):
    prediction = predict(params)
    prediction_list = prediction['data']

    output = {data["ds"].strftime("%m/%d/%Y"): {"yhat": data["yhat"],
                                                "yhat_lower": data["yhat_lower"],
                                                "yhat_upper": data["yhat_upper"]}
              for data in prediction_list}
    prediction['data'] = output
    return prediction