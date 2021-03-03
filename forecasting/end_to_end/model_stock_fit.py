from keras.layers import Dense, GRU
from keras import Sequential
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam
import numpy as np
class ModelFit:
    def __init__(self):
        pass
    
    @staticmethod
    def gru_model(nodes=50, dropout=0.0, recurrent_dropout=0.0, learning_rate=0.01, loss='mse', optimizer=Adam, metrics=['mse']):
        model = Sequential()
        model.add(GRU(nodes))
        model.add(Dense(1, activation='linear'))
        model.compile(optimizer=optimizer(learning_rate=learning_rate),
                  loss=loss,
                  metrics=metrics)
        return model
    @classmethod
    def train_model(cls, train_data=None, validation_data=None, model=None):
        early_stop = EarlyStopping(monitor='val_loss', patience=40, restore_best_weights=True)
        model = cls.gru_model()
        history = model.fit(train_data, validation_data=validation_data, callbacks=[early_stop], epochs=300)
        return history, model
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
        return y_preds
    @staticmethod
    def predict_tomorrow(previous_days=None, model=None):
        y_pred = model.predict(previous_days)
        return y_pred
    @staticmethod
    def update_to_tomorrow(previous_days=None, y_pred=None):
        """previous days is np array with shape (any, ..., any); y_pred is scalar"""
        new_days = np.concatenate((previous_days[:,1:,:], np.array([[[y_pred]]])), axis=1)
        return new_days
    

