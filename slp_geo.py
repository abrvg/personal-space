import json
import pandas as pd
import plotly.express as px


#INPUT
df_mx = pd.read_csv("conjunto_de_datos_iter_24CSV20.csv", 
                    usecols=["ENTIDAD", "NOM_MUN", "NOM_LOC", "PNACENT", "PNACOE"])

with open('MX-SLP.json') as response:
    geo = json.load(response)

    
#Filter INEGI Data
df_mx = df_mx[df_mx["NOM_LOC"] == "Total del Municipio"].copy()


#Data types
df_mx["NOM_MUN"] = df_mx["NOM_MUN"].astype(str)
df_mx["PNACENT"] = df_mx["PNACENT"].astype(int)
df_mx["PNACOE"] =  df_mx["PNACOE"].astype(int)

# To match with the geojson file
df_mx["id"] = df_mx["NOM_MUN"]


# The percentage is calculated with those born in the state and those
#that born in other state
df_mx["PerPNACOE"] = df_mx["PNACOE"]/(df_mx["PNACENT"] + df_mx["PNACOE"])


#Create figure
fig = px.choropleth(df_mx, geojson=geo, locations='id', color='PerPNACOE',
                           color_continuous_scale="Viridis",
                           range_color=(0, 0.40),
                           scope="north america",
                           labels={'PerPNACOE':'% of population born in other State'}
                   )
                    
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
fig.write_html("slp-map.html")


#df_mx.to_csv("archive.csv")