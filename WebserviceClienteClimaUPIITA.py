import requests

# URL del servidor web (asegúrate de que la dirección y el puerto coincidan)
url_base = 'http://localhost:9092'
pais = "Mexico"

def obtener_temperatura(pais):
    url = f'{url_base}/temperature/{pais}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(f"ciudad: {data['ciudad']}")
        return f'Temperatura en {pais}: {data["temperatura"]}°C'
    elif response.status_code == 404:
        return f'País no encontrado: {pais}'
    else:
        return f'Error en la solicitud: Código {response.status_code}'

def obtener_lugar(pais):
    url = f'{url_base}/lugar/{pais}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Nombre: {data['nombre']}")
        # You can print other location-related data here.
        return f'Nombre: {data["nombre"]}'
    
    elif response.status_code == 404:
        return f'País no encontrado: {pais}'
    else:
        return f'Error en la solicitud: Código {response.status_code}'

def obtener_canciones(pais):
    url = f'{url_base}/spotify/{pais}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        if data:
            for i, track in enumerate(data[:10]):
                if i == 10:
                    break
                name = track['name']
                artist = track['artists'][0]['name']
                print(f'{i + 1}. {name} - {artist}')
            return "Lista de canciones impresa en la consola."
        else:
            return "No se encontraron canciones para la lista especificada."
    
    elif response.status_code == 404:
        return f'Playlist no encontrada: {pais}'
    else:
        return f'Error en la solicitud: Código {response.status_code}'

obtener_temperatura("Mexico")
#obtener_lugar(pais)
#obtener_canciones(pais)