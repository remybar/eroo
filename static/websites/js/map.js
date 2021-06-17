let map;

function initMap() {
    const mapDiv = document.getElementById("location-map");
    const lat = parseFloat(mapDiv.getAttribute("data-latitude"));
    const lng = parseFloat(mapDiv.getAttribute("data-longitude"));
    const zoom = parseInt(mapDiv.getAttribute("data-zoom")) || 13;
    map = new google.maps.Map(mapDiv, {
        center: { lat: lat, lng: lng },
        zoom: zoom,
    });
    new google.maps.Marker({
        position: { lat: lat, lng: lng },
        map,
    });
}
