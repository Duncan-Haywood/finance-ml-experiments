#!/usr/bin/env python
# coding: utf-8

# In[1]:


def predict_tomorrow(previous_days, model):
    y_pred = model.predict(previous_days)
    return y_pred
def update_to_tomorrow(previous_days, y_pred):
    new_days = previous_days[1:-1].append(y_pred)
    return new_days
def pred_next_days(num_days, previous_days, model):
    y_preds = list()
    new_days = previous_days
    for day in num_days:
        y_pred = predict_tomorrow(new_days, model)
        new_days = update_to_tomorrow(new_days, y_pred)
        y_preds.append(y_pred)
    return(y_preds)

