import streamlit as st
from googleapiclient.discovery import build
from google.oauth2 import service_account
import json
import numpy as np
import pandas as pd
cred = {'type': 'service_account',
 'project_id': 'etf-model-369713',
 'private_key_id': '45aad76af9ae8f68ff8868b177ade3106abbb6f0',
 'private_key': '-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC0Sgnt59iKyLHQ\nZn7SowrdqUNOj+ColMW5ai1coBfFUTBb1dEhl0NAggJr8mSYvZW8PZy2rnknSgjI\ngLgyNfZSMPSLBw8Nzqzgd3v4GKPoErTZoJaZiht+WHvWkIpjDZbm3eGpf79onpVU\ncN+Ac1lRrQYD8k6qIa9aqnKm8Qqfe+ZUFForO94bBNa+4Dxd3B9iOlIasONTuZNI\ndEIeq0JFuY4oJYlNBWaiLAEfhqCRVnwL6cJUXPAU5goxAX/NKfzSVCL1mHAv03j7\npy/98EtxDXl3SFxMfqXwW7l2CgUOdUpU/Ctpkc3kua22zYA9/Q1sV737X8GgscQx\nRA2vhUQ/AgMBAAECggEABQCq7t2Iji1Mdc5qRXj9s7HfKr5mSvc510/Ba3kLv89l\nap7vuyFh3dfdrlYfAXf9QChrgUwtE3CD9uBPfCEwMQ6nsnXjLoxmEqJuH6+7WJSw\nTPueQitpYOOeqBEBrgbyAXz1pojjbEk+NoYdRYit2UzWRmTCVwkxPvBM1yIIG+29\nt56lSeo1lg8Ibui6mmZteQ2Q9u7GwbhPBJwgjzVwdwKFfxMdr7uuwnNuJRwAAoBt\n1M6ENoB1zUWeUStQlCgCR/xh8VbtwA5xe9p8nKOfwK2hesiskJrojTWXiszWaBu6\nHfAxHce+lSEacpBEI2FRWSiqxVgBlNmrgOu1C1DecQKBgQDsg2AEOH2xvVKSapyn\nwNazJVVxzuwuJYf8G9HQf2/ibHZrCL34Uo9o449NjS1o7FIyFP2rFcX2EwQTJUSg\nPbFVEjOc3X/xYO0ILrJ4bCN7vBFh0QrO/2Y/3XqbkQZGbosxmAsKEPCRA7spIMTk\nDcsGZTAYaI3EAVeoBlqK+1i7DwKBgQDDJMRBmP+0PzOj/oJLUlXk0I/YaaY0BQH5\nlnoogyW9rsABCp/W9wfD3fpxwOy7sQ/JHzSWXLD6L5NUVuSthNSXI8Xf4KX2Qhj5\nK4+lLj0YTfQdyP2FPNbqhtupWQfMSZmuo/swIa05GIEBgC7xaDrvPX3zs8sIaXhT\nsNSKO2aj0QKBgG1y/mP1oHU4H5YSMByRaMnOZRQdpb5VL/DDDv1le+lUOBigGwln\na2YmqJJC2tjLQ95ZSGp70PhnJGOXw4JECmRL4Aafmi2hpQ88TOrdYC5KgeC6VD4m\ngrLbU3naSwUc8t0odzNZU3pIN7x4paTDnUiAWxlwiOpDlMT068GVPyKRAoGBAIB/\nrmgPqplzYLrldcDJh9vzZjU4ZIQuo/1JFEmnCmwcLTzCVTyFUGyuuCK9ymVRk7Z5\nQPSeNr+YImjQCycjp6WancrtL/u3zKAPCjjX+M0PT+dpGV/qDw9CHFUoVhU0helU\n+6vXESzesNxfHwpB+0TcdhrK0rBIWz6o21vm/5BxAoGASW1SzD/wYvaXqMzBNWWz\nxumt5MPEg6wJ1byc1w50UZJe0ie2sby9G8n1x3D32Q6ixsEXywBCqKn8fzAfGPE1\nnl1XOfAgXO8CpK/8ZA/HzRIbEXyH+ufvyS/pgPdBR31XkD+sX5h5fB6RnlolT/Ys\n5HZ6sPgD1hwK16wBxtXTNB0=\n-----END PRIVATE KEY-----\n',
 'client_email': 'etf-model-83@etf-model-369713.iam.gserviceaccount.com',
 'client_id': '104785831308812239864',
 'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
 'token_uri': 'https://oauth2.googleapis.com/token',
 'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
 'client_x509_cert_url': 'https://www.googleapis.com/robot/v1/metadata/x509/etf-model-83%40etf-model-369713.iam.gserviceaccount.com'}


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
creds = service_account.Credentials.from_service_account_info(cred, scopes=SCOPES)

ETF_SHEET_ID = '1j38MEMdIPUbyGK2Vir7t-NRwaH5TJLNoUdf2l54lC7o'
CL_PR_SHEET_ID = '1O7ZbPpO4L5i_VMJcGq4O-kRXKaXQtwvr1peh5MCwxgM'


service = build('sheets', 'v4', credentials=creds)

sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=ETF_SHEET_ID,
                            range='ETF_DATA!A:ZZ').execute()
values = result.get('values',[]) 

ETFs = pd.DataFrame(values)
new_header = ETFs.iloc[0] 
ETFs = ETFs[1:] 
ETFs.columns = new_header
ETFs.reset_index(drop=True, inplace=True)
tickers = ETFs['Ticker']
ETFs[['Beta','Price','Change_1D','Return_1W','Return_1M',
      'Return_3M','Return_6M','Return_12M','PctRank_1W',
      'PctRank_1M','PctRank_3M','PctRank_6M','PctRank_12M',
      'ShortMoM_avg','MoM_avg','ChgRnk_1M','ChgRnk_3M','ChgRnk_6M',
      'ChgRnk_12M','Fallin1Mmore20','Fallin1Wmore10','StdevNegativeReturn',
      'HistExcessReturn_1W','HistExcessReturn_1M','HistExcessReturn_3M',
      'HistExcessReturn_6M','HistExcessReturn_12M']] = ETFs[['Beta','Price','Change_1D','Return_1W','Return_1M',
                                                             'Return_3M','Return_6M','Return_12M','PctRank_1W',
                                                             'PctRank_1M','PctRank_3M','PctRank_6M','PctRank_12M',
                                                             'ShortMoM_avg','MoM_avg','ChgRnk_1M','ChgRnk_3M','ChgRnk_6M',
                                                             'ChgRnk_12M','Fallin1Mmore20','Fallin1Wmore10','StdevNegativeReturn',
                                                             'HistExcessReturn_1W','HistExcessReturn_1M','HistExcessReturn_3M',
                                                             'HistExcessReturn_6M','HistExcessReturn_12M']].astype(float)
result = sheet.values().get(spreadsheetId=CL_PR_SHEET_ID,
                            range='Close_Price!A:ZZ').execute()
values = result.get('values',[]) 

combined_df = pd.DataFrame(values)
new_header = combined_df.iloc[0] 
combined_df = combined_df[1:] 
combined_df.columns = new_header
combined_df.reset_index(drop=True, inplace=True)
combined_df['Date'] = pd.to_datetime(combined_df['Date'])
combined_df.set_index('Date', inplace=True)
combined_df.replace('',np.nan,inplace = True)
combined_df = combined_df.astype(float)

etf_dma  = ETFs.loc[(ETFs['50DMAModel'] == 'INVESTED') & (ETFs['100DMAModel'] == 'INVESTED') & (ETFs['200DMAModel'] == 'INVESTED')]
etf_tr_1 = ETFs.loc[(ETFs['200DMAModel'] == 'INVESTED') & (ETFs['50DMAModel'] == 'CASH')]
etf_tr_2 = ETFs.loc[(ETFs['200DMAModel'] == 'CASH') & (ETFs['50DMAModel'] == 'INVESTED') & (ETFs['Fallin1Wmore10']<= 10)]
etf_ex_1 = ETFs.loc[ETFs['HistExcessReturn_12M']>=80]
etf_ex_2 = ETFs.loc[ETFs['HistExcessReturn_12M']<=20]
etf_vol  = ETFs.loc[(ETFs['HistExcessReturn_12M']<=30) & (ETFs['Fallin1Wmore10'] >=15)]
etf_ex50 = ETFs.loc[(ETFs['HistExcessReturn_12M']>=20) & (ETFs['50DMAModel'] == 'CASH') & (ETFs['100DMAModel'] == 'INVESTED') & (ETFs['200DMAModel'] == 'INVESTED')]

st.header('ETF Frame Work')

with st.sidebar:

  category = st.multiselect('Category:',ETFs['Category'].unique())
  sub = st.multiselect ('Sub Category:',ETFs['Sub category'].unique())
  etf = st.multiselect('ETF Tickers:', ETFs['Ticker'])
  

  if (category == []) and (etf == []) and (sub ==[]):

    d_etf = ETFs.loc[ETFs['Ticker'] == 'SPY']

  elif (category == []) and (etf == []) and (sub !=[]):

    d_etf = ETFs.loc[ETFs['Sub category'].isin(sub)]
    etf_dma = etf_dma.loc[etf_dma['Sub category'].isin(sub)]
    etf_tr_1 = etf_tr_1.loc[etf_tr_1['Sub category'].isin(sub)]
    etf_tr_2 = etf_tr_2.loc[etf_tr_2['Sub category'].isin(sub)]
    etf_ex_1 = etf_ex_1.loc[etf_ex_1['Sub category'].isin(sub)]
    etf_ex_2 = etf_ex_2.loc[etf_ex_2['Sub category'].isin(sub)]
    etf_ex50 = etf_ex50.loc[etf_ex50['Sub category'].isin(sub)]

  elif (category == []) and (etf != []) and (sub ==[]):

    d_etf = ETFs.loc[ETFs['Ticker'].isin(etf)]
    etf_dma = etf_dma.loc[etf_dma['Ticker'].isin(etf)]
    etf_tr_1 = etf_tr_1.loc[etf_tr_1['Ticker'].isin(etf)]
    etf_tr_2 = etf_tr_2.loc[etf_tr_2['Ticker'].isin(etf)]
    etf_ex_1 = etf_ex_1.loc[etf_ex_1['Ticker'].isin(etf)]
    etf_ex_2 = etf_ex_2.loc[etf_ex_2['Ticker'].isin(etf)]
    etf_vol = etf_vol.loc[etf_vol['Ticker'].isin(etf)]
    etf_vol = etf_vol.loc[etf_vol['Ticker'].isin(etf)]
    etf_ex50 = etf_ex50.loc[etf_ex50['Ticker'].isin(etf)]

  elif (category == []) and (etf != []) and (sub !=[]):
    
    d_etf = ETFs.loc[(ETFs['Ticker'].isin(etf)) & (ETFs['Sub category'].isin(sub))]
    etf_dma = etf_dma.loc[(etf_dma['Ticker'].isin(etf)) & (etf_dma['Sub category'].isin(sub))]
    etf_tr_1 = etf_tr_1.loc[(etf_tr_1['Ticker'].isin(etf)) & (etf_tr_1['Sub category'].isin(sub))]
    etf_tr_2 = etf_tr_2.loc[(etf_tr_2['Ticker'].isin(etf)) & (etf_tr_2['Sub category'].isin(sub))]
    etf_ex_1 = etf_ex_1.loc[(etf_ex_1['Ticker'].isin(etf)) & (etf_ex_1['Sub category'].isin(sub))]
    etf_ex_2 = etf_ex_2.loc[(etf_ex_2['Ticker'].isin(etf)) & (etf_ex_2['Sub category'].isin(sub))]
    etf_vol = etf_vol.loc[(etf_vol['Ticker'].isin(etf)) & (etf_vol['Sub category'].isin(sub))]
    etf_ex50 = etf_ex50.loc[(etf_ex50['Ticker'].isin(etf)) & (etf_ex50['Sub category'].isin(sub))]


  elif (category != []) and (etf == []) and (sub ==[]):

    d_etf = ETFs.loc[ETFs['Category'].isin(category)]
    etf_dma = etf_dma.loc[etf_dma['Category'].isin(category)]
    etf_tr_1 = etf_tr_1.loc[etf_tr_1['Category'].isin(category)]
    etf_tr_2 = etf_tr_2.loc[etf_tr_2['Category'].isin(category)]
    etf_ex_1 = etf_ex_1.loc[etf_ex_1['Category'].isin(category)]
    etf_ex_2 = etf_ex_2.loc[etf_ex_2['Category'].isin(category)]
    etf_vol = etf_vol.loc[etf_vol['Category'].isin(category)]
    etf_ex50 = etf_ex50.loc[etf_ex50['Category'].isin(category)]

  elif (category != []) and (etf == []) and (sub !=[]):

    d_etf = ETFs.loc[(ETFs['Category'].isin(category)) & (ETFs['Sub category'].isin(sub))]
    etf_dma = etf_dma.loc[(etf_dma['Category'].isin(category)) & (etf_dma['Sub category'].isin(sub))]
    etf_tr_1 = etf_tr_1.loc[(etf_tr_1['Category'].isin(category)) & (etf_tr_1['Sub category'].isin(sub))]
    etf_tr_2 = etf_tr_2.loc[(etf_tr_2['Category'].isin(category)) & (etf_tr_2['Sub category'].isin(sub))]
    etf_ex_1 = etf_ex_1.loc[(etf_ex_1['Category'].isin(category)) & (etf_ex_1['Sub category'].isin(sub))]
    etf_ex_2 = etf_ex_2.loc[(etf_ex_2['Category'].isin(category)) & (etf_ex_2['Sub category'].isin(sub))]
    etf_vol = etf_vol.loc[(etf_vol['Category'].isin(category)) & (etf_vol['Sub category'].isin(sub))]
    etf_ex50 = etf_ex50.loc[(etf_ex50['Category'].isin(category)) & (etf_ex50['Sub category'].isin(sub))]

  elif (category  != []) and (etf != []) and (sub ==[]):

    d_etf = ETFs.loc[(ETFs['Ticker'].isin(etf)) & (ETFs['Category'].isin(category))]
    etf_dma = etf_dma.loc[(etf_dma['Ticker'].isin(etf)) & (etf_dma['Category'].isin(category))]
    etf_tr_1 = etf_tr_1.loc[(etf_tr_1['Ticker'].isin(etf)) & (etf_tr_1['Category'].isin(category))]
    etf_tr_2 = etf_tr_2.loc[(etf_tr_2['Ticker'].isin(etf)) & (etf_tr_2['Category'].isin(category))]
    etf_ex_1 = etf_ex_1.loc[(etf_ex_1['Ticker'].isin(etf)) & (etf_ex_1['Category'].isin(category))]
    etf_ex_2 = etf_ex_2.loc[(etf_ex_2['Ticker'].isin(etf)) & (etf_ex_2['Category'].isin(category))]
    etf_vol = etf_vol.loc[(etf_vol['Ticker'].isin(etf)) & (etf_vol['Category'].isin(category))]
    etf_ex50 = etf_ex50.loc[(etf_ex50['Ticker'].isin(etf)) & (etf_ex50['Category'].isin(category))]

  else:

    d_etf = ETFs.loc[(ETFs['Ticker'].isin(etf)) & (ETFs['Category'].isin(category)) & (ETFs['Sub category'].isin(sub))]
    etf_dma = etf_dma.loc[(etf_dma['Ticker'].isin(etf)) & (etf_dma['Category'].isin(category)) & (etf_dma['Sub category'].isin(sub))]
    etf_tr_1 = etf_tr_1.loc[(etf_tr_1['Ticker'].isin(etf)) & (etf_tr_1['Category'].isin(category)) & (etf_tr_1['Sub category'].isin(sub))]
    etf_tr_2 = etf_tr_2.loc[(etf_tr_2['Ticker'].isin(etf)) & (etf_tr_2['Category'].isin(category)) & (etf_tr_2['Sub category'].isin(sub))]
    etf_ex_1 = etf_ex_1.loc[(etf_ex_1['Ticker'].isin(etf)) & (etf_ex_1['Category'].isin(category)) & (etf_ex_1['Sub category'].isin(sub))]
    etf_ex_2 = etf_ex_2.loc[(etf_ex_2['Ticker'].isin(etf)) & (etf_ex_2['Category'].isin(category)) & (etf_ex_2['Sub category'].isin(sub))]
    etf_vol = etf_vol.loc[(etf_vol['Ticker'].isin(etf)) & (etf_vol['Category'].isin(category)) & (etf_vol['Sub category'].isin(sub))]
    etf_ex50 = etf_ex50.loc[(etf_ex50['Ticker'].isin(etf)) & (etf_ex50['Category'].isin(category)) & (etf_ex50['Sub category'].isin(sub))]
   

  st.dataframe(d_etf)

  url = "https://drive.google.com/file/d/1Y6kDfVQy-exsuics-oc2glWqtijI1-Dh/view?usp=share_link"

  st.write("clik on the link to view charts(%s)" % url)
  
  url2 = "https://docs.google.com/spreadsheets/d/1j38MEMdIPUbyGK2Vir7t-NRwaH5TJLNoUdf2l54lC7o/edit?usp=share_link"
  
  st.write("clik on the link to view database(%s)" % url2)

st.write('## ETFs above 50,100,200 DMA')
st.dataframe(etf_dma)

st.write('## Change in Trend')
st.write('### Above 200 DMA And Below 50 DMA')

st.dataframe(etf_tr_1)

st.write('### Below 200 DMA And Above 50 DMA')

st.dataframe(etf_tr_2)

st.write('## Excess Returns')
st.write('### Excess Return above 80 percentile')
st.dataframe(etf_ex_1)

st.write('### Excess Return below 20 percentile')
st.dataframe(etf_ex_2)

st.write('## High volatility and Large Drawdowns')
st.dataframe(etf_vol)

st.write('## Excess Returms > 20 and losing Short Term Momentum(50DMA)')
st.dataframe(etf_ex50)

