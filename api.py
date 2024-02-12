import io
import requests
import json
import base64
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from collections import Counter
import io
from datetime import datetime, timedelta
import datetime
from dateutil.parser import parse
import math
from sqlalchemy import create_engine

def get_DATA(start,end,brand):

    #get token for access

    client_id = "easyvision-nexus-api-prod"
    client_secret = "bae10ef2-ab9d-47cd-9223-0f4e4a489917"
    authorization = base64.b64encode(bytes(client_id + ":" + client_secret, "ISO-8859-1")).decode("ascii")

    headers = {"Authorization": f"Basic {authorization}",
        "Content-Type": "application/x-www-form-urlencoded"
        }

    body = {"grant_type": "password",
        "username" : "rawaservices",
        "password" : "A6QCx3Canuz&GP",
        }

    response = requests.post("https://accounts.greenyellow.com/auth/realms/GreenYellow-prod/protocol/openid-connect/token", data=body, headers=headers)
    res = response.json()
    TOKEN = res['access_token']


    #get sites elements from BD suivi CPE
    bd = pd.read_excel('BD_suiviCPE.xlsx',  sheet_name='test', header=0, skiprows=0)
    codeRef_list=[]
    siteRef_list =[]
    brancheRef_list =[]
    noDataList=[]

    for index, row in bd.iterrows():
        codeRef_list.append(row['siteCode'])
        siteRef_list.append(row['siteName'])
        brancheRef_list.append(row['Branch'])



    #print(brancheRef_list)

    start='"'+start+'"'
    end='"'+end+'"'

    # Create an empty DataFrame
    all_sites = pd.DataFrame()

    # Loop through each site
    for i in range(0,len(codeRef_list)):
        codeRef_list[i]='"'+codeRef_list[i]+'"'
        if brancheRef_list[i] == brand:
            query="""query findConsumptionTemperatureBySite {
            findConsumptionTemperatureBySite(
            params: {
            salesforceName: """+str(codeRef_list[i])+"""
            type: ["CONSO_REAL"]
            energyType: "ELECTRICITY"
            startDate: """+start+"""
            endDate: """+end+"""
            }
           ) {
           salesforceName
           type
           meterId
           energyType
           value {
           dateTime
           value
           }
           }
        }
        """
            payload = {'query': query }
            url = "https://gylabs.westeurope.cloudapp.azure.com:8443/easyvision-nexus/graphql"
            r = requests.post(url, json=payload, headers={"Authorization": f"Bearer {TOKEN}"})
            # import data into a dataframe
            try:
                data = r.json()
                df =data['data']['findConsumptionTemperatureBySite']
                print(' - '+codeRef_list[i]+' - OK')
                count_site += 1
                rows=[]
                for data in df:
                    salesforceName = str(data['salesforceName'])
                    typ = data['type']
                    meterId=data['meterId']
                    value=data['value']
                    for row in value:
                        dateTime=row['dateTime']
                        RealConsumption = row['value']
                        row['salesforceName']= salesforceName
                        row['type']=typ
                        row['meterId']=meterId
                        rows.append(row)
                df= pd.DataFrame(rows)
            # preprocess data
                # sum the  two values of consumption
                if len(Counter(df['meterId']).keys())>1:
                    conso=df.groupby(['type','dateTime'])['value'].sum()
                    conso=pd.DataFrame(conso).reset_index()
                    conso.rename(columns={'value':'real_Consumption_kwh_meter_sum'}, inplace=True)
                    df=pd.merge(df, conso, on=['type','dateTime'],how='inner')
                else:
                    df=df.assign(real_Consumption_kwh_meter_sum=df['value'])
                # create NBmeter
                # data cleaning

                df1=df.groupby('type')['meterId'].apply(lambda x: list(x.unique())).reset_index().assign(NBmeter=lambda d: d['meterId'].str.len())
                df1=df1.drop('meterId', axis=1)
                df=pd.merge(df, df1, on='type', how='right')
                df = df.rename({'value': 'real_Consumption_kwh_meter'}, axis=1)
                data=df.loc[:,['type','dateTime','salesforceName','NBmeter','real_Consumption_kwh_meter_sum']]
                df=data.drop_duplicates()
            #    df1[['Date','time']] = df1.dateTime.str.split(" ",expand=True)
            #    df1[['hour','m','s']] = df1.time.str.split(":",expand=True)
            #    res = round(df1.groupby(['type','salesforceName','Date','hour'])['real_Consumption_kwh_meter_sum'].mean().reset_index())
            #    res = res.rename({'real_Consumption_kwh_meter_sum': 'mean consumption'}, axis=1)
            #    df=pd.merge(res, df1, on=['type','salesforceName', 'Date', 'hour'],how='right')
            #    df.drop_duplicates(subset =['type','salesforceName', 'Date', 'hour'], keep = 'first', inplace=True)
            #    df=df.drop(columns =['time','s','m','real_Consumption_kwh_meter_sum','hour','Date'])
            # Concatenate the data from this site into the overall DataFrame
                all_sites = pd.concat([all_sites, df])

            except Exception as e:

                print(' - '+codeRef_list[i]+' - not found')
                noDataList.append(codeRef_list[i]+'-'+siteRef_list[i])

    # Rename the columns
    #all_sites.columns = ['Type', 'SalesforceName', 'mean consumption', 'dateTime', 'NBmeter','Date', 'hour']

    week=datetime.datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')
    # Reset the index
    all_sites = all_sites.reset_index(drop=True)

    all_sites.to_csv('pool_P60/'+brand+'-S'+str(week.isocalendar()[1])+'-'+str(week.strftime("%m"))+str(week.year)+'.csv', encoding='utf-8', index=True)

    # match df with Metre table in db
    df = df.drop(columns=['NBmeter'])
    df.rename(columns={'type': 'energySource', 'dateTime': 'date_time', 'salesforceName': 'code_site', 'real_Consumption_kwh_meter_sum': 'Real Consumption (kWh)'}, inplace=True)

    # Enregistrement des données dans la base de données PostgreSQL
    engine = create_engine('postgresql://postgresql:mdp@localhost:5432/suivi_cpe')
    df.to_sql('meter', engine, if_exists='append', index=False)


    #print(df1)
    print('Sites téléchragés:')
    print(str(count_site))
    print('Sites introuvables sur Easyvision :')
    print(noDataList)
    return all_sites