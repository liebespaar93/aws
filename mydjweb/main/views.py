from django.shortcuts import render
from pandas.core.algorithms import value_counts
from .models import Coffee
from .froms import CoffeeForm
# Create your views here.

## import here ##
import numpy as np
import pandas as pd
import plotly.offline 
import plotly.graph_objects as gobj
import plotly.express as px
############ EDA ##############

########### section 1#################
fig = gobj.Figure()
pd.options.plotting.backend = "plotly"
wine_df = pd.read_csv('main/static/winedata/winemag-data_first150k.csv')
wine_df=wine_df.fillna({'country':'no','designation':'no','price':0,'province':'no','region_1':'no','region_2':'no' })
print(wine_df.isnull().sum())
wind_dfPCP=wine_df[['points','country','price']].groupby(['country','points']).mean().reset_index()
fig = wind_dfPCP.plot.line(x="points",y="price", color="country", line_group="country")
fig.update_layout(yaxis_tickprefix = '$', yaxis_tickformat = ',.')
plot_div = plotly.offline.plot(fig,include_plotlyjs=False,output_type="div")

############## section 2###############
fig2 = gobj.Figure()
variety_df = wine_df['variety'].value_counts()
variety_df = variety_df[variety_df > 1000]
variety_df.reset_index()['index']
winevar_df=wine_df[wine_df.variety.isin(variety_df.reset_index()['index'])]
winevarietypoints_df = winevar_df[['variety','points']].value_counts().reset_index().sort_values(by = ['variety','points']).reset_index().drop(['index'], axis=1)
winevarietypoints_df['relative'] = (winevarietypoints_df[0]/winevarietypoints_df.groupby(['variety']).sum().loc[winevarietypoints_df.variety[0]][0])**0.25
fig = winevarietypoints_df.plot.bar(x="relative",y="variety",color="points")
plot_div2 = plotly.offline.plot(fig,include_plotlyjs=False,output_type="div")
############EDA ###############


    ########### Coffeee ##############
def main(request):
    
    coffee_DB = Coffee.objects.all()

    if request.method == "POST":
        # cafe post 처리
        print("requw 데이", request.POST)
        coffeeform = CoffeeForm(request.POST)

        if request.POST.get('view'):
            print('view')
        elif request.POST.get('create') and coffeeform.is_valid():
            form = CoffeeForm(request.POST)
            if form.is_valid():
                form.save()
        elif request.POST.get('update'):
            print('udate')
            cofe = Coffee.objects.get(id=request.POST.get('cafe_id'))
            form = CoffeeForm(request.POST,instance= cofe)
            if form.is_valid():
                form.save(commit=True)
        elif request.POST.get('delet'):
            print('delet')
            cofe = Coffee.objects.get(id=request.POST.get('cafe_id'))
            cofe.delete()
    coffeeform = CoffeeForm()
    return render(request,"index.html", {"coffee_list":coffee_DB, "coffee_form":coffeeform,'plot_div': plot_div,'plot_div2':plot_div2,})

        ########### Coffeee end ##############

    ########### DEA ##############


        ########### DEA end ##############

