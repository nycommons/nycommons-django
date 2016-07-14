var flight = require('flightjs');
require('leaflet-usermarker');

var locateButton = flight.component(function () {
    this.attributes({
        map: null
    });

    this.click = function (event) {
        this.attr.map.locate({
            enableHighAccuracy: true,
            setView: true,
            maxZoom: 16
        });
        return false;
    };

    this.onLocationFound = function (event) {
        if (this.userLayer) {
            this.attr.map.removeLayer(this.userLayer);
        }
        this.userLayer = L.userMarker(event.latlng, {
            pulsing: true,
            accuracy: event.accuracy,
            smallIcon: true
        });
        this.userLayer.addTo(this.attr.map);
    };

    this.after('initialize', function () {
        this.attr.map.on('locationfound', this.onLocationFound.bind(this));
        this.on('click', this.click);
    });
});

module.exports = {
    locateButton: locateButton
};
