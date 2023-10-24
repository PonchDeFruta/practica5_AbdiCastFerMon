import base64
import requests
import http.server
import socketserver
import json
import random


client_id = 'a1aeb2e69aee4b43815b29db43ddef4c'
client_secret = '38af18397c0545e1b970a0404b91f031'
country_codes = {
    "Argentina": "AR",
    "Australia": "AU",
    "Austria": "AT",
    "Belgium": "BE",
    "Brazil": "BR",
    "Canada": "CA",
    "Chile": "CL",
    "Colombia": "CO",
    "Denmark": "DK",
    "Finland": "FI",
    "France": "FR",
    "Germany": "DE",
    "Hong Kong": "HK",
    "Hungary": "HU",
    "India": "IN",
    "Indonesia": "ID",
    "Ireland": "IE",
    "Italy": "IT",
    "Japan": "JP",
    "Malaysia": "MY",
    "Mexico": "MX",
    "Netherlands": "NL",
    "New Zealand": "NZ",
    "Norway": "NO",
    "Philippines": "PH",
    "Poland": "PL",
    "Portugal": "PT",
    "Singapore": "SG",
    "South Africa": "ZA",
    "Spain": "ES",
    "Sweden": "SE",
    "Switzerland": "CH",
    "Taiwan": "TW",
    "Turkey": "TR",
    "United Kingdom": "GB",
    "United States": "US",
}

datosopenweathermap_json = {
    "ciudad": "",
    "temperatura": "",
    "condiciones_climaticas": ""
}

datosgeonames_json = {
    "nombre": "",
    "pais": "",
    "poblacion": ""
}  





def obtener_datos_meteorologicos(ciudad):
    app_key = "8a915e32c25f6576a1735a2bf02b453e"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={app_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200 :
            temperatura = data["main"]["temp"] - 273.15  # Convertir de Kelvin a Celsius
            condiciones_climaticas = data["weather"][0]["description"]
           # print(f"Temperatura en {ciudad}: {temperatura:.2f}°C")
           # print(f"Condiciones Climáticas en {ciudad}: {condiciones_climaticas}")

            datosopenweathermap_json ["ciudad"] = ciudad
            datosopenweathermap_json ["temperatura"] = temperatura
            datosopenweathermap_json ["condiciones_climaticas"] =  condiciones_climaticas
        else:
            print("Datos meteorológicos no disponibles.")
    except Exception as e:
        print(f"Error: {str(e)}")


def obtener_informacion_ubicacion(geonames_username, lugar):
    url = f"http://api.geonames.org/searchJSON?name={lugar}&maxRows=1&username={geonames_username}"
    try:
        response = requests.get(url)
        data = response.json()
        if "geonames" in data and data["geonames"]:
            ubicacion = data["geonames"][0]
            #print(f"Nombre: {ubicacion['name']}")
            #print(f"País: {ubicacion['countryName']}")
            #print(f"Población: {ubicacion['population']}")

            datosgeonames_json["nombre"] = ubicacion['name']
            datosgeonames_json["pais"] = ubicacion['countryName']
            datosgeonames_json["poblacion"] = ubicacion['population']
        else:
            print("Ubicación no encontrada.")
    except Exception as e:
        print(f"Error: {str(e)}")


def top_playlist(pais):
    access_token = obtener_token()
    if pais in country_codes:
        country_code = country_codes[pais]
        endpoint = 'https://api.spotify.com/v1/browse/categories/toplists/playlists'

        headers = {
            'Authorization': f'Bearer {access_token}',
        }

        params = {
            'country': country_code,
        }
        response = requests.get(endpoint, headers=headers, params=params)
        data = response.json()
        if 'playlists' in data:
            playlist_id = data['playlists']['items'][0][
                'id']  # Obtén el ID de la lista de reproducción de las principales canciones
            top_tracks_endpoint = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
            top_tracks_response = requests.get(top_tracks_endpoint, headers=headers)
            top_tracks_data = top_tracks_response.json()

            if 'items' in top_tracks_data:
                top_tracks = top_tracks_data['items']
                return json.dumps(top_tracks, indent=2)
            else:
                print('Error al obtener las principales canciones.')
                return None
        else:
            print('Error al obtener la lista de reproducción de las principales canciones.')
            return None
    else:
        print("No hay informacion")


def obtener_token():
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{client_id}:{client_secret}'.encode('utf-8')).decode(
            'utf-8'),
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    payload = {'grant_type': 'client_credentials'}

    response = requests.post(url, headers=headers, data=payload)
    data = response.json()
    access_token = data['access_token']
    return access_token


if __name__ == "__main__":
    #Coloca tu usuario de geonames
    geonames_username = "diegofch"
    lugar = "México"  # Cambia esto a la ubicación que desees consultar

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):

        if self.path.startswith('/temperature/'):
            ciudad = self.path[13:]  # Obtener el nombre de la ciudad desde la ruta
            obtener_datos_meteorologicos(ciudad)  # Llamar a la función para obtener datos meteorológicos
            data = datosopenweathermap_json
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())  # Enviar la respuesta en formato JSON

        elif self.path.startswith('/lugar/'):
            lugar = self.path[7:]  # Obtener el nombre del lugar desde la ruta
            obtener_informacion_ubicacion(geonames_username, lugar)  # Llamar a la función para obtener información de ubicación
            data = datosgeonames_json
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())  # Enviar la respuesta en formato JSON

        elif self.path.startswith('/spotify/'):
            pais = self.path[9:]  # Obtener el nombre del país desde la ruta
            top_tracks_json = top_playlist(pais)  # Llamar a la función para obtener las principales canciones de Spotify
            if top_tracks_json:
                data = top_tracks_json
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(data).encode())  # Enviar la respuesta en formato JSON

        else:
            super().do_GET()


# Configuración del servidor
with socketserver.TCPServer(("", 9092), MyHandler) as httpd:
    print("Servidor web en el puerto 9090")
    httpd.serve_forever()