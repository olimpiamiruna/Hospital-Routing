import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox
import folium
import pandas as pd
import requests
import pprint

BASE_URL = 'https://nominatim.openstreetmap.org/search?format=json'

# Define your place
place = "Timisoara, Timis, Romania"
street = "Calea Torontalului, Timis,Romania"

# Get the boundary GeoDataFrame
gdf = ox.geocode_to_gdf(place)

# Get the road network graph
G = ox.graph_from_place(place, network_type="drive")

# Plot the road network
fig, ax = ox.plot_graph(
    G,
    show=False,
    close=False,
    bgcolor="#333333",
    edge_color="w",
    edge_linewidth=0.3,
    node_size=0,
)

# Plot the boundary
gdf.plot(ax=ax, fc="k", ec="#666666", lw=1, alpha=1, zorder=-1)

# Convert the graph nodes to a GeoDataFrame
nodes = ox.graph_to_gdfs(G, edges=False)

G_street = ox.graph_from_address(street, network_type="drive")
nodes_street = ox.graph_to_gdfs(G_street, edges=False)

# Create a Folium map centered on the location
m = folium.Map(location=[nodes_street['y'].mean(), nodes_street['x'].mean()], zoom_start=15)

# Add the boundary as a GeoJSON layer
folium.GeoJson(gdf).add_to(m)
'''
# Add nodes as points to the map
for index, row in nodes.iterrows():
    folium.CircleMarker(location=[row['y'], row['x']], radius=2, color='blue', fill=True).add_to(m)
'''
params = {
    "q": street,
    "format": "json"
}

response = requests.get(BASE_URL, params=params)
if response.status_code == 200:
    data = response.json()
    if data:
        latitude = float(data[0]["lat"])
        longitude = float(data[0]["lon"])
        print("Latitude:", latitude)
        print("Longitude:", longitude)
        location = float(latitude), float(longitude)
        folium.Marker(location).add_to(m)
    else:
        print("No results found for the address:", street)
else:
    print("Error:", response.status_code)
# Save the map to an HTML file
m.save('map_with_points.html')

# Display the map
m
