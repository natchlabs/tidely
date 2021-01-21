interface WeatherRequirement {
    weather: string;
    requirement: string;
}

interface MarkerData {
    marker: L.Marker;
    activities: string[];
    weatherRequirements: WeatherRequirement[];
}

navigator.geolocation.getCurrentPosition(async position => {
    const map = L.map('map').setView([position.coords.latitude, position.coords.longitude], 13);

    L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', {
        maxZoom: 20,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
        attribution: 'Map data and Imagery &copy; Google'
    }).addTo(map);

    map.on('click', (e: { latlng: L.LatLngExpression; }) => {
        
        const markerData: MarkerData = {
            marker: L.marker(e.latlng).addTo(map),
            activities: ['Rain Collecting'],
            weatherRequirements: [{
                weather: 'wind',
                requirement: 'low'
            }]
        };

        markerData.marker.bindPopup('<b>' + markerData.activities[0] + '</b>').openPopup();
    });
});