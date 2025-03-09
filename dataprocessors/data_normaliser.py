import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
from sklearn.preprocessing import Normalizer, PowerTransformer

class DataNormaliser:
    def __init__(self):
        """
        Initialize the Datanormaliser.
        """
        self.scalers = {}  # Store scalers for each column (if needed)
        pass

    def normalise_data(self, data, normalisation_methods):
        """
        normalise the data using specified methods.
        :param data: Input data as a pandas DataFrame.
        :param normalisation_methods: Dictionary specifying normalisation methods for each column.
                                      Example: {"D": "minmax", "L": "standard", "P": "robust"}
        :return: normalised data as a pandas DataFrame.
        """
        normalised_data = data.copy()
        for column, method in normalisation_methods.items():
            if method == "minmax":
                scaler = MinMaxScaler()
                normalised_data[column] = scaler.fit_transform(data[[column]])
                self.scalers[column] = scaler  # Store the scaler for later use (e.g., inverse transform)
            elif method == "standard":
                scaler = StandardScaler()
                normalised_data[column] = scaler.fit_transform(data[[column]])
                self.scalers[column] = scaler
            elif method == "robust":
                scaler = RobustScaler()
                normalised_data[column] = scaler.fit_transform(data[[column]])
                self.scalers[column] = scaler
            elif method == "l2":
                scaler = Normalizer(norm="l2")
                normalised_data[column] = scaler.fit_transform(data[[column]])
                self.scalers[column] = scaler
            elif method == "log":
                normalised_data[column] = np.log1p(data[column])  # Logarithmic transformation
            elif method == "power":
                scaler = PowerTransformer(method="yeo-johnson")  # Power transformation
                normalised_data[column] = scaler.fit_transform(data[[column]])
                self.scalers[column] = scaler
            else:
                raise ValueError(f"Unknown normalisation method: {method}")
        return normalised_data, self.scalers

    def inverse_transform(self, data, normalisation_methods):
        """
        Inverse transform the normalised data back to its original scale.
        :param data: normalised data as a pandas DataFrame.
        :param normalisation_methods: Dictionary specifying normalisation methods for each column.
        :return: Data in the original scale.
        """
        original_data = data.copy()
        for column, method in normalisation_methods.items():
            if method in ["minmax", "standard", "robust", "l2", "power"]:
                scaler = self.scalers.get(column)
                if scaler:
                    original_data[column] = scaler.inverse_transform(data[[column]])
            elif method == "log":
                original_data[column] = np.expm1(data[column])  # Inverse of log transformation
            else:
                raise ValueError(f"Unknown normalisation method: {method}")
        return original_data
