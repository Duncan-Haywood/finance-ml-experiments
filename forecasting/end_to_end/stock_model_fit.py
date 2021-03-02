from keras.layers import Dense, GRU
from keras import Sequential
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam
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
        model.evaluate(test_data)