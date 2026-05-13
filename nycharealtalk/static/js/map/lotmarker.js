var L = require('leaflet');

require('./lotpath');


L.LotMarker = L.CircleMarker.extend({

    _pickRadius: function (zoom) {
        var radius = 4;   
        if (zoom >= 13) {
            radius = 6;
        }
        if (zoom >= 14) {
            radius = 9;
        }
        if (zoom >= 15) {
            radius = 12;
        }
        if (zoom >= 16) {
            radius = 15;
        }
        return radius;
    },

    _updatePath: function () {
        var zoom = this._map.getZoom();

        // Update the circle's radius according to the map's zoom level
        this.options.radius = this._radius = this._pickRadius(zoom);

        L.CircleMarker.prototype._updatePath.call(this);
    }

});

L.LotMarker.include(L.LotPathMixin);

L.LotMarker.addInitHook(function () {
    this.on({
        'add': function () {
            this.initActionPath();
            // Send parks to the back, there are too many
            if (this.feature.properties.commons_type === 'park') {
                this.bringToBack();
            }
        },
        'remove': function () {
            this.removeActionPath();
        }
    });
});

L.lotMarker = function (latlng, options) {
    return new L.LotMarker(latlng, options);
};
