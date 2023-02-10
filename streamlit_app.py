import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pickle
from PIL import Image
    
    
med_model = pickle.load(open('models/huber_model.sav', 'rb'))
high_model = pickle.load(open('models/high_model.sav', 'rb'))
low_model = pickle.load(open('models/low_model.sav', 'rb'))

#mit_image = Image.open("Processed data/mit_logo2.png")

#st.image(mit_image, use_column_width=False)
    
st.title("Next PSA value prediction using longitudinal data")

cols_psa = st.columns(3)
cols_bmi = st.columns(3)
cols_others = st.columns(3)
cols_delta = st.columns(4)
cols_race = st.columns(5)


with cols_psa[0]:
        psa_t3 = st.number_input("PSA at t-3", min_value = 0, value = 6)
        
with cols_psa[1]:
        psa_t2 = st.number_input("PSA at t-2", min_value = 0, value = 5)
        
with cols_psa[2]:
        psa_t1 = st.number_input("PSA at t-1", min_value = 0, value = 7)
    


    
    
with cols_bmi[0]:
        bmi_t3 = st.number_input("BMI at t-3", min_value = 0, value = 23)
        
with cols_bmi[1]:
        bmi_t2 = st.number_input("BMI at t-2", min_value = 0, value = 23)

with cols_bmi[2]:
        bmi_t1 = st.number_input("BMI at t-1", min_value = 0, value = 23)


        
        
        

with cols_delta[0]:
    
    delta_t3 = st.number_input("Number of days between t-3 and diagnosis", value = -200)
    
with cols_delta[1]:
    
    delta_t2 = delta_t3 + st.number_input("Number of days between t-2 and and t-3", value = 30)
    
with cols_delta[2]:
    delta_t1 = delta_t2 + st.number_input("Number of days between t-1 and t-2", value = 30)
    
with cols_delta[3]:
    delta_t = delta_t1 + st.number_input("Number of days between t and t-1", value = 30)
    



    
with cols_others[0]:
    comorb = st.number_input("Aggregated comorbidity score", step = 1, value = 0, max_value = 5)
    
with cols_others[1]:
    volume = st.number_input("Prostate volume", value = 50)    

with cols_others[2]:
    age_diag = st.number_input("Age at diagnosis", value = 60)


    
    

with cols_race[0]:
    white = st.checkbox("White") * 1
    
with cols_race[1]:
    black = st.checkbox("Black") * 1
    
with cols_race[2]:
    asian = st.checkbox("Asian") * 1
    
with cols_race[3]:
    hispanic = st.checkbox("Hispanic") * 1 
    
with cols_race[4]:
    other = st.checkbox("Other") * 1
    
    
input_dict = {"PSA_t-3": psa_t3, "delta_t-3": delta_t3, "bmi_t-3": bmi_t3,
              "PSA_t-2": psa_t2, "delta_t-2": delta_t2, "bmi_t-2": bmi_t2,
              "PSA_t-1": psa_t1, "delta_t-1": delta_t1, "bmi_t-1": bmi_t1,
              "delta_t": delta_t, "age_diag": age_diag, "Asian": asian, "Black": black,
              "Hispanic": hispanic, "Unknown/other": other, "White": white, 
              "wscore_agg": comorb, "prostate_volume": volume}
input_df = pd.DataFrame([input_dict])
              
    
col1, col2, col3 , col4, col5 = st.columns(5)

with col1:
    pass
with col2:
    pass
with col4:
    pass
with col5:
    pass
with col3 :
    center_button = st.button("Predict")
    
if center_button:
    
    med_pred = float(med_model.predict(input_df))
    low_pred = float(low_model.predict(input_df))
    high_pred = float(high_model.predict(input_df))
    
    st.success("The prediction is: {:0.2f}, with an upper bound of {:0.2f} (80% prediction interval)".format(med_pred, low_pred))
    
    fig = plt.figure() 
    
    delta_vec = [delta_t3, delta_t2, delta_t1, delta_t]
    psa_vec = [psa_t3, psa_t2, psa_t1, high_pred]
    
    plt.plot(delta_vec[0:3], psa_vec[0:3], "k-", label = "Past PSAs")
    plt.plot([delta_vec[2], delta_vec[3]], [psa_t1, med_pred], "r:", label = "Predicted median")
    plt.fill_between([delta_vec[2], delta_vec[3]], [psa_t1, low_pred], [psa_t1, high_pred], alpha = 0.1, color="red", label = "80% interval prediction", linewidth = 2)
    
    plt.xlim((delta_t3 - 10, max(delta_vec) + 10)) 
    plt.ylim((0, (max(psa_vec) + 5)))
    
    plt.legend()
    
    plt.title("PSA evolution")
    plt.xlabel("Time to diagnosis")
    plt.ylabel("PSA value")    
    
    st.pyplot(fig)
    
