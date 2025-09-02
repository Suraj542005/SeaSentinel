from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="hotspot_mapper")
# location = geolocator.geocode("Ahmedabad, India")
location = geolocator.geocode("Lal Darwaja, Old City, Bhadra, Ahmedabad, Gujarat 380001, India")
print(location.latitude, location.longitude)
