import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pickle
import datetime
from PIL import Image
    
    
comorb = 2  
    
med_model = pickle.load(open('models/huber_model.sav', 'rb'))
high_model = pickle.load(open('models/high_model.sav', 'rb'))
low_model = pickle.load(open('models/low_model.sav', 'rb'))

#mit_image = Image.open("Processed data/mit_logo2.png")

#st.image(mit_image, use_column_width=False)
    
#st.title("Next PSA value prediction using longitudinal data")

st.markdown("<h1 style='text-align: center'>Estimating Future PSA in Patients on Active Surveillance for Prostate Cancer</h1>", unsafe_allow_html = True)
st.markdown("<h6>Authors: Aziz Ayed, Samuel Carbunaru, Claire-Alix Saillard, John A. Onofrey, Intae Moon, Steven L. Chang, Adam S. Feldman, Madhur Nayan</h6>", unsafe_allow_html = True)

st.markdown("<h3 style='text-align: center'>Clinical features</h1>", unsafe_allow_html = True)

cols_others1 = st.columns(2)
cols_others2 = st.columns(2)

race = st.radio("Race", ("White", "Black", "Asian", "Hispanic", "Other"), horizontal = True)
    
#cols_race = st.columns(5)

st.markdown("---")

st.markdown("<h3 style='text-align: center'>PSA assessments</h1>", unsafe_allow_html = True)

cols_psa = st.columns(3)
cols_delta = st.columns(3)
cols_recent = st.columns(3)

st.markdown("\n")
st.markdown("\n")

with cols_others1[0]:
    date_diag = st.date_input("Date of diagnosis", value = datetime.datetime(2020, 6, 10))
    
with cols_others1[1]:
    age_diag = st.number_input("Age at diagnosis", value = 60)

with cols_others2[0]:
    volume = st.number_input("Prostate volume", value = 50) 
    
with cols_others2[1]:
    bmi_t3 = st.number_input("BMI", min_value = 0, value = 23)
    bmi_t2 = bmi_t3
    bmi_t1 = bmi_t3
    
    
#with cols_race[0]:
    
#    white = st.checkbox("White") * 1

#with cols_race[1]:
    
#    black = st.checkbox("Black") * 1

#with cols_race[2]:
    
#    asian = st.checkbox("Asian") * 1

#with cols_race[3]:
    
#    hispanic = st.checkbox("Hispanic") * 1 

#with cols_race[4]:
    
#    other = st.checkbox("Other") * 1

white = (race == "White") * 1
black = (race == "Black") * 1
asian = (race == "Asian") * 1
hispanic = (race == "Hispanic") * 1
other = (race == "Other") * 1

with cols_recent[0]:
    
    st.markdown("\n")
    st.markdown("\n")
    st.markdown("Twice prior to most recent")

with cols_recent[1]:
    
    date_psa1 = st.date_input("", min_value = date_diag, value = datetime.datetime(2020, 8, 10))
    ddiag1 = (date_psa1 - date_diag).days
    delta_t3 = np.floor(ddiag1/30.5)
    
    
with cols_recent[2]:
    
    psa_t3 = st.number_input("", min_value = 0.0, value = 6.0, step = 0.1)

with cols_delta[0]:
    
    st.markdown("\n")
    st.markdown("\n")
    st.markdown("Prior to most recent")
    

with cols_delta[1]:
    
    date_psa2 = st.date_input("", value = datetime.datetime(2021, 1, 10), min_value = date_psa1)
    ddiag2 = ddiag1 + (date_psa2 - date_psa1).days
    delta_t2 = delta_t3 + np.floor(ddiag2/30.5)
    #delta_t1 = delta_t2 + st.number_input("Number of days between t and t-1", value = 30)

with cols_delta[2]:
    
    psa_t2 = st.number_input("", min_value = 0.0, value = 5.0, step = 0.1)
    #delta_t = delta_t1 + st.number_input("Number of days between t and t+1", value = 30)    
    
with cols_psa[0]:
        #psa_t3 = st.number_input("PSA at t-3", min_value = 0.0, value = 6.0, step = 0.1)
        st.markdown("\n")
        st.markdown("\n")
        st.markdown("\n")
        st.markdown("\n")
        st.markdown("\n")
        st.markdown("Most recent")
        
with cols_psa[1]:
        st.markdown("<h6 style='text-align: center'>Dates</h6>", unsafe_allow_html = True)    
        date_psa3 = st.date_input("", value = datetime.datetime(2021, 5, 10), min_value = date_psa2)
        ddiag3 = ddiag2 + (date_psa3 - date_psa1).days
        delta_t1 = delta_t2 + np.floor(ddiag3/30.5)
        
with cols_psa[2]:
        st.markdown("<h6 style='text-align: center'>PSA values</h6>", unsafe_allow_html = True)    
        psa_t1 = st.number_input("", min_value = 0.0, value = 7.0, step = 0.1)
    
next_psa = st.selectbox("Months to next expected PSA assessment", (3, 6, 12, 24))

delta_t = delta_t1 + next_psa

ddiag4 = ddiag3 + np.floor(next_psa * 30.5)
    
input_dict = {"PSA_t-3": psa_t3, "delta_t-3": delta_t3/30, "bmi_t-3": bmi_t3,
              "PSA_t-2": psa_t2, "delta_t-2": delta_t2/30, "bmi_t-2": bmi_t2,
              "PSA_t-1": psa_t1, "delta_t-1": delta_t1/30, "bmi_t-1": bmi_t1,
              "delta_t": delta_t/12, "age_diag": age_diag, "Asian": asian, "Black": black,
              "Hispanic": hispanic, "Unknown/other": other, "White": white, 
              "wscore_agg": comorb, "prostate_volume": volume}

input_df = pd.DataFrame([input_dict])
              

st.markdown("---")

st.markdown("<h3 style='text-align: center'>Estimating future PSA value</h1>", unsafe_allow_html = True)    
    
st.markdown("\n")
st.markdown("\n")
    
col1, col2, col3 , col4, col5 = st.columns(5)

with col1:
    pass
with col2:
    pass
with col4:
    interval = st.checkbox("Prediction interval")
with col5:
    pass
with col3 :
    center_button = st.button("Estimate")
    
if center_button:
    
    med_pred = float(med_model.predict(input_df))
    low_pred = float(low_model.predict(input_df))
    high_pred = float(high_model.predict(input_df))
    
    st.success("The prediction is: {:0.2f}, with a 80% prediction interval of [{:0.2f}, {:0.2f}] (80% prediction interval)".format(med_pred, low_pred, high_pred))
    
    fig = plt.figure() 
    
    delta_vec = [ddiag1, ddiag2, ddiag3, ddiag4]
    psa_vec = [psa_t3, psa_t2, psa_t1, high_pred]
    
    plt.plot(delta_vec[0:3], psa_vec[0:3], "k-", label = "Past PSAs")
    plt.plot([delta_vec[2], delta_vec[3]], [psa_t1, med_pred], "r:", label = "Predicted median")
    if interval:
        plt.fill_between([delta_vec[2], delta_vec[3]], [psa_t1, low_pred], [psa_t1, high_pred], alpha = 0.1, color="red", label = "80% interval prediction", linewidth = 2)
    
    plt.xlim((delta_t3 - 10, max(delta_vec) + 10)) 
    plt.ylim((0, (max(psa_vec) + 5)))
    
    plt.legend()
    
    plt.title("PSA evolution")
    plt.xlabel("Time to diagnosis")
    plt.ylabel("PSA value")    
    
    st.pyplot(fig)
    
st.markdown("\n")
st.markdown("\n")    

st.markdown("<h6 style='text-align: center'>Disclaimer: This tool is intended to illustrate how previous PSA values can be used to estimate a future PSA value in patients on active surveillance for prostate cancer. It is not intended for clinical use.</h6>", unsafe_allow_html = True)    


    
