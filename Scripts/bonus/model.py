from sklearn.linear_model import LinearRegression
from typing import Tuple, Union, List

import numpy as np
import pandas as pd
import joblib
import os

class Model:
    def __init__(self):
        self._dataset = pd.DataFrame()
        self._target_column = None
        self._model = None
        self._trained_model_params = "bonus/models/trained_model.sav"
        self._best_score = 0

    def get_dataset(self):
        return self._dataset
    
    def get_best_score(self):
        return self._best_score
    
    def set_score(self, score):
        self._best_score = score
    
    def set_dataset(self, df):
        self._dataset = df

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        if data.equals(self._dataset):
            print("Updating dataset for future training")
            self._dataset = data

        data_with_new_features = self._generate_new_features(data)
        
        #select most important features
        features = self._apply_one_hot_encoding(data_with_new_features)

        if target_column:
            self._target_column = target_column
            target = data[[self._target_column]]

            return features, target
        
        return features

    
    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        target_col = target[self._target_column]

        self._model = LinearRegression()
        self._model.fit(features, target_col)

        joblib.dump(self._model, self._trained_model_params)
        return None
    
    def predict(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> List[int]:
        """
        Predict vo2_max for new data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        
        Returns:
            (List[int]): predicted targets.
            float: score of the prediction in that particular dataset.
        """
        # We have to persist the model to handle the case where we use predict without fitting the data
        model = self._get_model()
        y_preds = model.predict(features)

        return y_preds.tolist(), model.score(features,target)

    def is_trained(self) -> bool:
        return self._model is not None



    def _generate_new_features(
        self,
        data: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Add the calculated new features for the data:
        'is_elderly'

        Args:
            data (pd.DataFrame): raw data.

        Returns:
            pd.DataFrame: Dataframe with new columns
        """
        data['is_elderly'] = np.where(data['age'] > 60, 1,0)
        return data
        

    def _apply_one_hot_encoding(
            self,
            data: pd.DataFrame
        ) -> pd.DataFrame:
        """
        Apply one hot encoding for categorical column 'gender
        and erase name and target columns.

        Args:
            data (pd.DataFrame): raw data.

        Returns:
            pd.DataFrame: Dataframe with encoded features
        """
        data = pd.get_dummies(data, columns=['gender'])
        return data.drop(['vo2_max','name', 'date'], axis=1)

    def _get_model(
            self
        ) -> LinearRegression:
        """
        Getter for the Model parameter of the class

        Returns:
            LinearRegression: model
        """
        if self._model is None:
            print(os.path.exists(self._trained_model_params))
            if os.path.exists(self._trained_model_params):
                try:
                    trained_model = joblib.load(self._trained_model_params)
                    print(trained_model)
                    self._model = trained_model 

                except Exception:

                    raise ModelNotTrainedException("Model not trained")

        return self._model
    
class ModelNotTrainedException(Exception):
    pass