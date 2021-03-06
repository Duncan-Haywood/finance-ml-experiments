from keras.layers import Dense, GRU, Input, LSTM, Activation, Bidirectional
from keras import Sequential
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam
from keras.activations import relu
import numpy as np
class ModelFit:
    @classmethod
    def train_model(cls, train_data=None, validation_data=None, model=None, epochs=300):
        early_stop = EarlyStopping(monitor='val_loss', patience=40, restore_best_weights=True)
        model = cls.gru_model()
        history = model.fit(train_data, validation_data=validation_data, callbacks=[early_stop], epochs=epochs)
        return history, model
    @staticmethod
    def gru_model(nodes=50, dropout=0.0, recurrent_dropout=0.0, learning_rate=0.01, loss='mse', optimizer=Adam, metrics=['mse']):
        model = Sequential()
        model.add(Input(shape=(None, 1)))
        model.add(GRU(nodes))
        model.add(Dense(1, activation='linear'))
        model.compile(optimizer=optimizer(learning_rate=learning_rate),
                  loss=loss,
                  metrics=metrics)
        return model
    @staticmethod
    def stack_3_lstm_model(nodes=50, dropout=0.0, recurrent_dropout=0.0, learning_rate=0.01, loss='mse', optimizer=Adam, metrics=['mse']):
        lstm_layer = LSTM(nodes, dropout=dropout, recurrent_dropout=recurrent_dropout, return_sequences=True)
        model = Sequential()
        model.add(Input(shape=(None, 1)))
        model.add(lstm_layer)
        model.add(lstm_layer)
        model.add(lstm_layer)
        model.add(Dense(1, activation='linear'))
        model.compile(optimizer=optimizer(learning_rate=learning_rate),
                  loss=loss,
                  metrics=metrics)
        return model
    @staticmethod
    def lstm_dense_model(nodes=50, dropout=0.0, recurrent_dropout=0.0, learning_rate=0.01, loss='mse', optimizer=Adam, metrics=['mse']):
        lstm_layer = LSTM(nodes, dropout=dropout, recurrent_dropout=recurrent_dropout)
        model = Sequential()
        model.add(Input(shape=(None, 1)))
        model.add(lstm_layer)
        model.add(Dense(32))
        model.add(Activation(relu))
        model.add(Dense(1, activation='linear'))
        model.compile(optimizer=optimizer(learning_rate=learning_rate),
                  loss=loss,
                  metrics=metrics)
        return model
    @staticmethod
    def bi_stack_lstm_model(nodes=50, dropout=0.0, recurrent_dropout=0.0, learning_rate=0.01, loss='mse', optimizer=Adam, metrics=['mse']):
        lstm_layer = LSTM(nodes, recurrent_dropout=recurrent_dropout, return_sequences=True)
        model = Sequential()
        model.add(Input(shape=(None, 1)))
        model.add(Bidirectional(lstm_layer))
        model.add(Bidirectional(lstm_layer))
        model.add(Dense(1, activation='linear'))
        model.compile(optimizer=optimizer(learning_rate=learning_rate),
                  loss=loss,
                  metrics=metrics)
        return model

