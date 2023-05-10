from astra.flight_tools import nozzleLiftFixedAscent
from astra.simulator import *
from datetime import datetime, timedelta
import logging
from argparse import ArgumentParser
from json import loads
parser = ArgumentParser("run_simulation.py", add_help=True)
parser.add_argument('flight_profile', type=open,
                    help="Flight Profile JSON file with launch parameters")
parser.add_argument('--now', action='store_true',
                    help="Set launch time to now")
parser.add_argument('--time', action='store',
                    help="Set exact launch time in ISO format")

args = parser.parse_args()

config: dict = {}
with args.flight_profile as profile:
    config = loads(profile.read())

expected_parameters: list = [
    "name",
    "launch",
    "number_of_simulations",
    "balloon_model",
    "lift_kg",
    "payload_weight_kg",
    "parachute_model",
    "gas_type",
    "timeout_hours"
]

for parameter in expected_parameters:
    if parameter not in config.keys():
        print(
            F"ERROR: Couldn't find expected parameter: {parameter} in flight profile")
        exit(1)

def to_utc(dt: datetime): return (dt - dt.utcoffset()).replace(tzinfo=None)

if args.now:
    launch_datetime = datetime.utcnow()
elif args.time:
    launch_datetime = to_utc(datetime.fromisoformat(args.time))
else:
    launch_datetime = to_utc(datetime.fromisoformat(
        config['launch']['time']).astimezone())

print(F"Launching from {config['launch']['latitude']},{config['launch']['longitude']} "
      F"\nat UTC time: {launch_datetime} "
      F"\npayload of {config['payload_weight_kg']}kg "
      F"\nwith lift of {config['lift_kg']}kg")

logging.basicConfig(level=logging.ERROR)

simEnvironment = forecastEnvironment(launchSiteLat=config['launch']['latitude'],      # deg
                                     # deg
                                     launchSiteLon=config['launch']["longitude"],
                                     # m
                                     launchSiteElev=config['launch']["longitude"],
                                     dateAndTime=launch_datetime,
                                     forceNonHD=False,
                                     debugging=False)
# Launch setup
simFlight = flight(environment=simEnvironment,
                   balloonGasType='Helium',
                   balloonModel='TA800',
                   #  5029g mirando 25km 5.68m3
                   # USAR A CALCULADORA DO HABHUB http://habhub.org/calc/                                # kg
                   nozzleLift=config['lift_kg'],
                   # kg
                   payloadTrainWeight=config['payload_weight_kg'],
                   parachuteModel=config['parachute_model'],
                   numberOfSimRuns=config['number_of_simulations'],
                   trainEquivSphereDiam=0.1,                    # m
                   floatingFlight=False,
                   floatingAltitude=25000,                      # m
                   excessPressureCoeff=1,
                   outputFile=os.path.join('..', config['name']),
                   debugging=False,
                   log_to_file=False,
                   floatDuration=1*60*60+30*60,  # seconds
                   cutdownTimeout=config['timeout_hours']*3600)
# Run the simulation
simFlight.run()

flight_data = {}
with open(f"../{config['name']}/out.json", 'r') as flight_paths:
  flight_data = loads(flight_paths.read())
flights = flight_data['flightPaths']
landings = [ x['points'][-1] for x in flights]

import plotly.express as px
fig = px.density_mapbox(landings, lat="lat", lon="lng", zoom=8)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()