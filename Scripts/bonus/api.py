from fastapi import FastAPI, File, UploadFile

import pandas as pd
from fastapi.responses import JSONResponse
from datetime import datetime
from .model import Model

import numpy as np
import codecs
import csv

app = FastAPI()

model = Model()        

@app.post("/update", status_code=200)
def upload(file: UploadFile = File(...)):
    df = model.get_dataset()
    df_new = pd.read_csv(file.file)
    # TODO Revise pydantic model of new data
    df = pd.concat([df,df_new])
    model.set_dataset(df)
    #Make updates to model
    features, target = model.preprocess(df_new, 'vo2_max')
    if model.is_trained():
        predicted_target, score = model.predict(features,target)
        print(score)
    else:
        model.fit(features,target)
        predicted_target,  score = model.predict(features,target)
        model.set_score(score)
        print(score)
    #if we get a poor prediction from the trained model.
    if score < model.get_best_score():
        features, target = model.preprocess(df, 'vo2_max')
        model.fit(features,target)
        predicted_target,  score = model.predict(features, target)
        model.set_score(score)
    return score