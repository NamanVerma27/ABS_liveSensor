# estimator.py

class TargetValueMapping:
    """
    Maps the target variable ('neg', 'pos') to (0, 1).
    """
    def __init__(self):
        self.neg: int = 0
        self.pos: int = 1

    def to_dict(self):
        return self.__dict__

    def reverse_mapping(self):
        mapping_response = self.to_dict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))


class SensorModel:
    """
    A wrapper class that holds both the preprocessor and the model.
    """
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise e
    
    def predict(self, x):
        """
        Applies preprocessing and then prediction.
        """
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise e