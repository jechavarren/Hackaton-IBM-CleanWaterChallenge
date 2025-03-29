import json
import logging
import pandas as pd
import requests


# Configure logging
logging.basicConfig(
    # filename='app.log',
    filemode="a",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class GetWaterDataPipeline:
    """
    Pipeline to get the water quelity data.
    """

    def __init__(self):

        self.constant='constant'

    def get_water_data(sampling_point_id: str, sampling_point_name: str):
        # empty list to append all data
        all_data = []

        # api url
        base_url = f"https://api.euskadi.eus/water-quality/sampling-points/{sampling_point_id}/measurements"
        PARAMS_OF_INTEREST = [
            "CLORO LIBRE RESIDUAL",
            "CONDUCTIVIDAD (20ºC)",
            "PH (20ºC)",
            "TEMPERATURA",
            "TURBIDEZ"
        ]

        response = requests.get(base_url)

        if response.status_code != 200:
                print(f"Error en la solicitud: {response.status_code}")

        datos = response.json()

        for d in datos:
            measurementDate = d['measurementDate']
            
            # check for all the measurement dates
            url2 = f"https://api.euskadi.eus/water-quality/sampling-points/{sampling_point_id}/measurements/{measurementDate}/analytical-data"

            response2 = requests.get(url2)

            if response2.status_code != 200:
                print(f"Error en la solicitud: {response2.status_code}")

            datos2 = response2.json()

            data_dict = {"sampling_point_id": sampling_point_id, "name": sampling_point_name, "measurement_date": measurementDate}

            # check for each of the parameters in each measurement date of the water tank
            for dat in datos2:
                param = dat.get("parameter")
                value = dat.get('value')
                if param in PARAMS_OF_INTEREST:
                    data_dict[param] = value

            all_data.append(data_dict)

        #save the data in a dataframa
        df_datos = pd.DataFrame(all_data)
        return df_datos
