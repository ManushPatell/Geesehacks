let map;
let directionsService;
let directionsRenderer;

function initMap() {
  console.log('Map initialized');
  // Initialize the map centered on the Waterloo Police Station
  map = new google.maps.Map(document.getElementById('map'), {
      center: { lat: 43.4695, lng: -80.5224 }, // Waterloo Police Station coordinates
      zoom: 15
  });

  directionsService = new google.maps.DirectionsService();
  directionsRenderer = new google.maps.DirectionsRenderer();
  directionsRenderer.setMap(map);

  // Add a marker for the Waterloo Police Station
  const stationLocation = { lat: 43.4695, lng: -80.5224 }; // Waterloo Police Station coordinates
  new google.maps.Marker({
      position: stationLocation,
      map: map,
      title: 'Waterloo Police Station'
  });
}

function getRoute() {
  console.log('Button clicked!');
  const address = document.getElementById('caller-address').value;

  if (!address) {
      alert('Please enter an address.');
      return;
  }

  // Geocode the caller's address to get latitude and longitude
  const geocoder = new google.maps.Geocoder();
  geocoder.geocode({ address }, (results, status) => {
      if (status === google.maps.GeocoderStatus.OK) {
          const callerLocation = results[0].geometry.location;

          // Define the starting point (Waterloo Police Station) and destination (caller)
          const request = {
              origin: { lat: 43.4695, lng: -80.5224 }, // Waterloo Police Station location
              destination: callerLocation, // Emergency caller's location
              travelMode: google.maps.TravelMode.DRIVING,
              unitSystem: google.maps.UnitSystem.METRIC
          };

          // Get the directions from the DirectionsService
          directionsService.route(request, (result, status) => {
              if (status === google.maps.DirectionsStatus.OK) {
                  // Display the route on the map
                  directionsRenderer.setDirections(result);
              } else {
                  alert('Directions request failed due to ' + status);
              }
          });
      } else {
          alert('Geocode was not successful for the following reason: ' + status);
      }
  });
}

// Attach the event listener to the "Get Route" button
document.getElementById('get-route-btn').addEventListener('click', getRoute);
