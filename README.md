#Flask Weather API

#####This is a simple Flask API that fetches the weather forecast for a specified location using the SMHI API.

##Installation

To run the API, you'll need to have Python 3 installed on your machine.

1. Clone this repository:

```
git clone https://github.com/your-username/flask-weather-api.git
```

2. Install the Python dependencies using pip:

```
pip install -r requirements.txt
```

## Usage

To run the API, use the following command:

```
python app.py
```

The API will start running on http://localhost:5000. You can access the Swagger documentation for the API by navigating to http://localhost:5000/apidocs/ in your web browser.

To test the API, you can use a tool like curl or Postman. Here's an example curl command to fetch the weather forecast for a location:

```
curl -X POST "http://localhost:5000/weather" \
     -H "Content-Type: application/json" \
     -d '{"location": "Stockholm, Sweden"}'
```

This will return a JSON response containing the weather forecast for Stockholm.

## API Endpoints

### POST /weather

This endpoint fetches the weather forecast for a specified location using the SMHI API.

#### Request Parameters

| Parameter | Type   | Description                                  |
|-----------|--------|----------------------------------------------|
| location  | string | The location for which to fetch the forecast. |

#### Example Request

```json
{
  "location": "Stockholm, Sweden"
}
```
Example Response

```json
{
  "response": "The temperature in Stockholm, Sweden is 10.4 degrees Celsius, and the wind speed is 3.3 m/s."
}
```


##License

This project is licensed under the MIT License - see the LICENSE file for details.
