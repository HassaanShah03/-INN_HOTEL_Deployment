
import streamlit as st
import numpy as np
import pandas as pd
import pickle

with open('final_model_xgb.pkl','rb') as file:
    model = pickle.load(file)

with open('transformer.pkl','rb') as file:
    pt = pickle.load(file)

def predctions(input_list):
    
    input_list = np.array(input_list,dtype=object)
    
    pred = model.predict_proba([input_list])[:,1][0]

    if pred>0.5:
        return f'This booking is more likely to get cancelled: Chances {round(pred,2)}'
    else:
        return f'This booking is less likely to get cancelled: Chances {round(pred,2)}'

def main():
    st.title('INN HOTEL GROUPS')
    lt = st.text_input('Enter the lead time. ')
    mst = (lambda x:1 if x== 'Online' else 0)(st.selectbox('Enter the type of booking',['Online','Offline']))
    spcl = st.selectbox('Select the number of special request made',[0,1,2,3,4,5])
    price = st.text_input('Enter the price offered for the room')
    adults = st.selectbox('Select the number of adults in booking',[0,1,2,3,4])
    wkend = st.text_input('Enter the weekend nights in the booking')
    wk = st.text_input('Enter the weeknights in booking')
    park = (lambda x:1 if x== 'Yes' else 0)(st.select_slider('Is parking included in the booking',['Yes','No']))
    month = st.slider('What will be the month of arrival',min_value=1,max_value=12,step=1)
    day = st.slider('What will be the day of arival',min_value=1,max_value=31,step=1)
    wkday_lambda = (lambda x:0 if x=='Mon' else 1 if x=='Tue' else 2 if x=='Wed' else 3 if x=='Thur' else 4 if x=='Fri' else 5 if x=='Sat' else 6)
    wkday = wkday_lambda(st.selectbox('What is the weekday of arival',['Mon','Tue','Wed','Thur','Fri','Sat','Sun']))

    tran_data = pt.transform([[float(lt),float(price)]])
    lt_t = tran_data[0][0]
    price_t = tran_data[0][1]

    inp_list = [lt_t,mst,spcl,price_t,adults,wkend,park,wk,month,day,wkday]

    if st.button('Predict'):
        response = prediction(inp_list)
        st.success(response)

if __name__=='__main__':
    main()
