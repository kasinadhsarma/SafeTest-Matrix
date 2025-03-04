import numpy as np
from sklearn.tree import DecisionTreeClassifier
from keras.models import Sequential
from keras.layers import LSTM, Dense

class RiskModel:
    def __init__(self):
        self.decision_tree_model = DecisionTreeClassifier()
        self.lstm_model = Sequential()
        self.lstm_model.add(LSTM(50, return_sequences=True, input_shape=(1, 10)))
        self.lstm_model.add(LSTM(50))
        self.lstm_model.add(Dense(1, activation='sigmoid'))
        self.lstm_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    def train_decision_tree(self, X, y):
        self.decision_tree_model.fit(X, y)

    def evaluate_decision_tree(self, X, y):
        return self.decision_tree_model.score(X, y)

    def train_lstm(self, X, y):
        self.lstm_model.fit(X, y, epochs=10, batch_size=32)

    def evaluate_lstm(self, X, y):
        return self.lstm_model.evaluate(X, y)
