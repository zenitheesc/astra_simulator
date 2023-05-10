# ASTRA High Altitude Balloon Flight Planner
 
University of Southampton

This README file explains how to use the ASTRA High Altitude Balloon Flight Planner without the web interface.

See the included examples and notebooks for usage.

Distribution
------------
This module has been tested on python 2.7 and 3.6
**This fork adds support for python 3.10**
Use of the Anaconda Python distribution is recommended.

# Run Locally with Script

First, use a virtual enviroment 
```shell
$ virtualenv .venv
$ source .venv/bin/activate
(.venv)$ pip3 install -r requirements.txt
```
Create a Flight Profile based on the example given:

```json
{
    "name": "example",
    "launch":{
        "time": "2023-05-10T11:00:00-03:00",
        "latitude": -15.796388,
        "longitude":-47.910330,
        "altitude": 860.0
    },
    "number_of_simulations": 50,
    "balloon_model": "TA800",
    "lift_kg": 5.5,
    "payload_weight_kg": 3.7,
    "parachute_model": "SPH72",
    "gas_type": "Helium",
    "timeout_hours": 4
}
```
<details closed>
<summary>How to get the lift parameter</summary>

This information can be either directly measured after the balloon is inflated using a baggage scale. Or it can be calculated using the [~~HABhub~~ SondeHub calculator](https://sondehub.org/calc/), as a function of either a target burst altitude or ascent rate. 

</details>


Then run the script:
```shell
(.venv)$ python3 run_simulation.py --help
usage: run_simulation.py [-h] [--now] [--time TIME] flight_profile

positional arguments:
  flight_profile  Flight Profile JSON file with launch parameters

options:
  -h, --help      show this help message and exit
  --now           Set launch time to now
  --time TIME     Set exact launch time in ISO format
```

For example:
```shell
(.venv)$ python3 run_simulation.py flight_profiles/example.json
```

Once all the steps are done your browser should pop up with a density plot of balloon landings:

![example_output](https://i.imgur.com/ah7yGSy.png)

KML and CSV files are created inside a folder with the name in the flight profile



Copyright 2013, University of Southampton.