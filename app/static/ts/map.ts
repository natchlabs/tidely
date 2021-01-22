interface WeatherRequirement {
    weather: string;
    requirement: string;
}

interface MarkerData {
    marker: L.Marker;
    activities: string[];
    weatherRequirements: WeatherRequirement[];
}

class MapView {
    private map: L.Map;

    constructor(latitude: number, longitude: number) {
        this.map = L.map('map').setView([latitude, longitude], 13);

        L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', {
            maxZoom: 20,
            subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
            attribution: 'Map data and Imagery &copy; Google'
        }).addTo(this.map);

        this.map.on('click', (e: { latlng: L.LatLngExpression; }) => {
            this.addMarkerDataToMap({
                marker: L.marker(e.latlng),
                activities: [prompt('activity', 'Rain Collecting')],
                weatherRequirements: [{
                    weather: prompt('weather', 'rain'),
                    requirement: prompt('requirement', 'heavy')
                }]
            });
        });
    }

    public addMarkerDataToMap(markerData: MarkerData): void {
        markerData.marker.addTo(this.map).bindPopup(`<p>${markerData.marker.getLatLng()}</p>
            <p>${markerData.activities[0]}</p>
            <p>${markerData.weatherRequirements[0].weather}:
            ${markerData.weatherRequirements[0].requirement}</p>`).openPopup();
    }
}

navigator.geolocation.getCurrentPosition(
    async position => new MapView(position.coords.latitude, position.coords.longitude),
    () => new MapView(-36.8509, 174.7645)
);