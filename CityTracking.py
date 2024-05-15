import folium
import osmnx as ox
import pandas as pd
import geopandas as gpd
import requests
from folium.plugins import MarkerCluster

ox.__version__

# Function to retrieve and plot hospitals and clinics with Folium
def plot_hospitals_and_clinics(place):
    # Download/model a street network for the specified place
    G = ox.graph_from_place(place, network_type="drive", retain_all=True)
    
    # Get center coordinates for the map
    center_lat, center_lon = ox.geocode(place)
    
    # Create a Folium map centered around the place
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

    # Create a MarkerCluster object
    marker_cluster = MarkerCluster().add_to(m)

    # Plot street network on Folium map
    ox.plot_graph_folium(G, graph_map=m, edge_color="blue", edge_width=0.3, bgcolor="#333333")
    
    # Retrieve hospital and clinic data for the place
    tags = {"amenity": ["hospital", "clinic"]}
    gdf = ox.features_from_place(place, tags)
    
    # Base URL for the geocoding API
    BASE_URL = 'https://nominatim.openstreetmap.org/search?format=json'

    # Iterate through each hospital or clinic and add markers to the map
    for idx, row in gdf.iterrows():
        # Construct the query parameters for the API request
        params = {
            "q": row["name"],
            "format": "json",
            "limit": 1
        }
        
        # Send a GET request to the geocoding API
        response = requests.get(BASE_URL, params=params)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # Check if any results were returned
            if data:
                # Extract latitude and longitude from the first result
                latitude = float(data[0]["lat"])
                longitude = float(data[0]["lon"])
                
                # Add marker to the marker cluster
                folium.Marker([latitude, longitude]).add_to(marker_cluster)
    
    # Display the Folium map
    m.save('city_map_with_hospitals_and_clinics.html')
    print("Map with hospitals and clinics saved as city_map_with_hospitals_and_clinics.html")

# Read the CSV file which contains the big cities
df = pd.read_csv('ro.csv')

# Message for the user
city_name = input("Enter the name of the city: ")

# Searching for the city in the data frame
city_row = df[df['city'] == city_name]

if not city_row.empty:
    # Plot hospitals and clinics for the specified city using Folium
    plot_hospitals_and_clinics(city_name)
else:
    print("City not found in the dataset.")
    
