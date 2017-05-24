var L = require('leaflet');

require('./lotpath');


L.LotPolygon = L.Polygon.extend({

    _pickOpacity: function (zoom) {
        if (zoom >= 18) {
            return 0.65;
        }
        if (zoom >= 17) {
            return 0.85;
        }
        return 1;
    },

    _updatePath: function () {
        // Update opacity
        this.options.fillOpacity = this._pickOpacity(this._map.getZoom());
        //this._updateStyle();

        L.Polygon.prototype._updatePath.call(this);
    }

});

L.LotPolygon.include(L.LotPathMixin);

L.LotPolygon.addInitHook(function () {
    this.on({
        'add': function () {
            this.initActionPath();
            // Bring park buildings to the front, they're small!
            if (this.feature.properties.commons_type === 'park building') {
                this.bringToFront();
            }
        }
    });
});

L.lotPolygon = function (latlngs, options) {
    return new L.LotPolygon(latlngs, options);
};
