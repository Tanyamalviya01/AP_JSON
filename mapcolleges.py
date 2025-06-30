import json
from plotly.graph_objs import Scattergeo, Layout
from plotly import offline

univ_file = open('univ.json', 'r')
univ_data = json.load(univ_file)

schools_file = open('schools.geojson', 'r')
schools_data = json.load(schools_file)

names = []
lons = []
lats = []
enrollments = []
males = []
females = []

for u in univ_data:
    if u.get("NCAA", {}).get("NAIA conference number football (IC2020)") == 108:
        names.append(u.get("instnm"))
        enroll = u.get("Total  enrollment (DRVEF2020)")
        enrollments.append(enroll)
        women_pct = u.get("Percent of total enrollment that are women (DRVEF2020)")
        women = int(enroll * (women_pct / 100))
        men = enroll - women
        females.append(women)
        males.append(men)
        lons.append(u.get("Longitude location of institution (HD2020)"))
        lats.append(u.get("Latitude location of institution (HD2020)"))

addresses = []
for i in range(len(names)):
    addr = ""
    for feature in schools_data["features"]:
        if names[i] in feature["properties"]["NAME"]:
            street = feature["properties"]["STREET"]
            city = feature["properties"]["CITY"]
            state = feature["properties"]["STATE"]
            zip_code = feature["properties"]["ZIP"]
            addr = f"{street} {city} {state} {zip_code}"
            break
    addresses.append(addr)


hover_texts = []
for i in range(len(names)):
    name = names[i]
    address = addresses[i]
    total = enrollments[i]
    male = males[i]
    female = females[i]
    text = f"{name}<br>{address}<br>Total Enrollment: {total:,}<br>Male: {male:,}<br>Female: {female:,}"
    hover_texts.append(text)

data = [
    {
        'type': 'scattergeo',
        'lon': lons,
        'lat': lats,
        'text': hover_texts,
        'hoverinfo': 'text',
        'marker': {
            'size': [5 + .0001 * enrollment for enrollment in enrollments],
            'color': enrollments,
            'colorscale': 'Viridis',
            'reversescale': True,
            'colorbar': {'title': 'Total Enrollment'}
        }
    }
]

my_layout = Layout(title='Big 12 Conference Schools - Enrollment Data')

fig = {'data': data, 'layout': my_layout}

offline.plot(fig, filename='big12_schools_map.html')
