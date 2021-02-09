interface WeatherRequirement {
    weather: string;
    requirement: string;
}

interface MarkerData {
    location: L.LatLngLiteral;
    activity: string;
    weatherRequirements: WeatherRequirement[];
}

class MapView {
    private map: L.Map;
    private markers: MarkerData[];

    get Markers(): MarkerData[] {
        return this.markers;
    }

    constructor(latitude: number, longitude: number) {
        this.map = L.map('map').setView([latitude, longitude], 13);
        this.markers = [];

        L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', {
            maxZoom: 20,
            subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
            attribution: 'Map data and Imagery &copy; Google'
        }).addTo(this.map);

        this.map.on('click', (e: { latlng: L.LatLngExpression; }) => {
            const marker = L.marker(e.latlng).addTo(this.map);
            const markerData = {
                location: {
                    lat: marker.getLatLng().lat,
                    lng: marker.getLatLng().lng
                },
                activity: prompt('activity', 'Rain Collecting'),
                weatherRequirements: [{
                    weather: prompt('weather', 'rain'),
                    requirement: prompt('requirement', 'heavy')
                }]
            };

            marker.bindPopup(
                `<p>${markerData.location.lat}, ${markerData.location.lng}</p><p>${markerData.activity}</p>
                <p>${markerData.weatherRequirements[0].weather}: ${markerData.weatherRequirements[0].requirement}</p>`
            ).openPopup();

            this.markers.push(markerData);
        });
    }
}

async function fetchJson(markers: MarkerData[]) {
    const response =  await fetch('http://localhost:5000/', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(markers)
    });
    return await response.json();
}

function doStuff(map: MapView): void {
    setTimeout(async () => console.log(await fetchJson(map.Markers)), 5000);
}

navigator.geolocation.getCurrentPosition(
    async position => doStuff(new MapView(position.coords.latitude, position.coords.longitude)),
    () => doStuff(new MapView(-36.8509, 174.7645))
);