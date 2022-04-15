from tkinter.ttk import Style
from turtle import color
import folium
import pandas

map=folium.Map(Location=[38.58,-99.09],zoom_start=6)
fg=folium.FeatureGroup(name="Volcanoes & Places")

sev_wond={"Great Pyramid of Giza":[29.9764,31.1313],"Hanging Gardens of Babylon":[22.832,45.70],"Temple of Artemis":[37.94,27.36],"Statue of Jesus":[33.72,36.37],"Mausoleum of Augustus":[41.90,12.47],"Colossus of Rhodes":[36.45,28.22],"Taj Mahal of Agra":[27.1751,78.0421]}

for key,value in sev_wond.items():
    fg.add_child(folium.Marker(location=value,popup=key, icon=folium.Icon(color='green')))

data=pandas.read_csv("Volcanoes.txt")
lon = list(data["LON"])
lat = list(data["LAT"])
elev = list(data["ELEV"])
name = list(data["NAME"])

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

def color_volcano(elv):
    if elv < 1000:
        return 'green'
    elif 1000 < elv < 3000:
        return 'orange'
    else:
        return 'red'        

for lt,ln,el,nam in zip(lat,lon,elev,name):
    iframe = folium.IFrame(html=html % (nam, nam, el), width=200, height=100)
    fg.add_child(folium.CircleMarker(location=[lt,ln],radius=6,popup=folium.Popup(iframe), fill_color=color_volcano(el),color='grey',fill_opacity=0.7))

fg1=folium.FeatureGroup(name="Population Densit")

fg1.add_child(folium.GeoJson(data=(open('world.json','r',encoding='utf-8-sig').read()),
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 1000000 else 'yellow' if 1000000<= x['properties']['POP2005']< 10000000 else 'orange' if 10000000<= x['properties']['POP2005']< 100000000 else 'red' }))

map.add_child(fg)
map.add_child(fg1)
map.add_child(folium.LayerControl())

map.save("Map1.html")
