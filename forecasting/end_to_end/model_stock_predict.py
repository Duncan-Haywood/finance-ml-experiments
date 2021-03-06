import numpy as np
class ModelPredict:    
    @staticmethod
    def evaluate_model(model=None,test_data=None):
        test_error = model.evaluate(test_data)
        return test_error[1]
    @classmethod
    def pred_next_days(cls, future_num_days=None, previous_days=None, model=None):
        y_preds = list()
        new_days = previous_days
        for day in range(future_num_days):
            y_pred = cls.predict_tomorrow(previous_days=new_days, model=model)
            new_days = cls.update_to_tomorrow(previous_days=new_days, y_pred=y_pred)
            y_preds.append(y_pred)
        y_preds = np.array(y_preds).flatten()
        return y_preds
    @staticmethod
    def predict_tomorrow(previous_days=None, model=None):
        y_pred = model.predict(previous_days)
        return y_pred
    @staticmethod
    def update_to_tomorrow(previous_days=None, y_pred=None):
        """previous days is np array with shape (any, ..., any); y_pred is 2d array"""
        new_days = np.concatenate((previous_days[:,1:,:], np.array([y_pred])), axis=1)
        return new_days