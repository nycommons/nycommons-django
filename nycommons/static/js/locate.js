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

    this.after('initialize', function () {
        var map = this.attr.map;
        var that = this;
        map.on('locationfound', function (event) {
            if (that.userLayer) {
                map.removeLayer(that.userLayer);
            }
            that.userLayer = L.userMarker(event.latlng, {
                pulsing: true,
                accuracy: event.accuracy,
                smallIcon: true
            });
            that.userLayer.addTo(map);
        });
        this.on('click', this.click);
    });
});

module.exports = {
    locateButton: locateButton
};
