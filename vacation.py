import streamlit as st
import pandas as pd
import numpy as np
from pulp import *

num_employees = st.slider('Number of Employees', min_value=1, max_value=100)
vacation_dates = st.date_input('Vacation Dates', [(2023, 7, 1), (2023, 7, 31)], [min_date, max_date], key='dates')

# Define the optimization problem
model = LpProblem("Optimum Vacation Requests", LpMaximize)

# Define the decision variables
employees = range(num_employees)
days = pd.date_range(start=min_date, end=max_date, freq='D')
variables = LpVariable.dicts("Request", [(e,d) for e in employees for d in days], cat='Binary')

# Define the objective function
model += lpSum([variables[(e,d)] for e in employees for d in days])

# Define the constraints
for e in employees:
    model += lpSum([variables[(e,d)] for d in days]) <= max_vacation_days
for d in days:
    model += lpSum([variables[(e,d)] for e in employees]) <= 1

# Solve the optimization problem
model.solve()

# Output the results
st.write('Optimum Vacation Schedule:')
for e in employees:
    st.write('Employee', e)
    for d in days:
        if variables[(e,d)].value() == 1.0:
            st.write(d.strftime('%Y-%m-%d'))
