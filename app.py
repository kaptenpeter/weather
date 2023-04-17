from flask import Flask, request, jsonify
import requests
import json
from geopy.geocoders import Nominatim
from flasgger import Swagger, swag_from

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/weather', methods=['POST'])
@swag_from({
    'summary': 'Get weather forecast based on location',
    'description': 'This endpoint fetches the weather forecast for a specified location using the SMHI API.',
    'parameters': [
        {
            'name': 'location',
            'description': 'The location for which to fetch the weather forecast (e.g., "Stockholm, Sweden").',
            'in': 'body',  # Change 'json' to 'body'
            'schema': {
                'type': 'object',
                'properties': {
                    'location': {
                        'type': 'string'
                    }
                },
                'required': ['location']
            }
        }
    ],
    'consumes': ['application/json'],
    'responses': {
        '200': {
            'description': 'A JSON object containing the weather forecast for the specified location.',
            'schema': {
                'type': 'object',
                'properties': {
                    'response': {
                        'type': 'string',
                        'description': 'A text description of the weather forecast.'
                    }
                }
            }
        },
        '400': {
            'description': 'An error message if the location parameter is missing or invalid.',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'A description of the error.'
                    }
                }
            }
        },
        '500': {
            'description': 'An error message if there was an issue fetching or processing the weather forecast.',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'A description of the error.'
                    }
                }
            }
        }
    }
})

def get_weather():
    """
    Fetches the weather forecast for a specified location using the SMHI API.

    ---
    responses:
      200:
        description: A JSON object containing the weather forecast for the specified location.
        schema:
          type: object
          properties:
            response:
              type: string
              description: A text description of the weather forecast.
      400:
        description: An error message if the location parameter is missing or invalid.
        schema:
          type: object
          properties:
            error:
              type: string
              description: A description of the error.
      500:
        description: An error message if there was an issue fetching or processing the weather forecast.
        schema:
          type: object
          properties:
            error:
              type: string
              description: A description of the error.
    """

    # Get the location from the request JSON
    location = request.json.get('location')

    if not location:
        error_message = 'The location parameter is missing or invalid.'
        return jsonify({'error': error_message}), 400

    # Obtain the longitude and latitude for the specified location
    geolocator = Nominatim(user_agent="weather_app")
    location_obj = geolocator.geocode(location)

    if not location_obj:
        error_message = f'Could not geocode location "{location}".'
        return jsonify({'error': error_message}), 400

    longitude = round(location_obj.longitude, 6)
    latitude = round(location_obj.latitude, 6)

    # Define the SMHI API endpoint for weather forecasts
    smhi_endpoint = f"https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/{longitude}/lat/{latitude}/data.json"

    try:
        # Make a request to the SMHI API to fetch the forecast data
        response = requests.get(smhi_endpoint)

        # Check the response status code
        if response.status_code != 200:
            error_message = f"API request failed with status code {response.status_code}"
            return jsonify({'error': error_message}), 500

        # Parse the JSON response from the SMHI API
        forecast_data = json.loads(response.text)

        # Extract the relevant weather forecast data from the JSON response
        temperature = forecast_data["timeSeries"][0]["parameters"][10]["values"][0]
        wind_speed = forecast_data["timeSeries"][0]["parameters"][14]["values"][0]

        # Format the weather forecast information into a response string
        response_text = f"The temperature in {location} is {temperature} degrees Celsius, and the wind speed is {wind_speed} m/s."

    except requests.exceptions.RequestException as e:
        error_message = f"API request failed with error {e}"
        return jsonify({'error': error_message}), 500

    except (KeyError, IndexError, json.JSONDecodeError) as e:
        error_message = f"Unable to parse API response - {e}"
        return jsonify({'error': error_message}), 500

    # Return the response as JSON
    return jsonify({'response': response_text})


if __name__ == '__main__':
    app.run(debug=True, port=5000)

