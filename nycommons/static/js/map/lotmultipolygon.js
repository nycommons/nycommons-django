var L = require('leaflet');

require('./lotpolygon');

L.LotMultiPolygon = L.FeatureGroup.extend({

    initialize: function (latlngs, options) {
        this._layers = {};
        this._options = options;
        this.setLatLngs(latlngs);
    },

    setLatLngs: function (latlngs) {
        var i = 0,
            len = latlngs.length;

        this.eachLayer(function (layer) {
            if (i < len) {
                layer.setLatLngs(latlngs[i++]);
            } else {
                this.removeLayer(layer);
            }
        }, this);

        while (i < len) {
            this.addLayer(new L.LotPolygon(latlngs[i++], this._options));
        }

        return this;
    },

    getLatLngs: function () {
        var latlngs = [];

        this.eachLayer(function (layer) {
            latlngs.push(layer.getLatLngs());
        });

        return latlngs;
    },

    show: function () {
        this.eachLayer(function (layer) {
            layer.show();
        });
    },

    hide: function () {
        this.eachLayer(function (layer) {
            layer.hide();
        });
    }
});

L.LotMultiPolygon.include(L.LotPathMixin);

L.LotMultiPolygon.addInitHook(function () {
    this.on({
        'add': function () {
            this.initActionPath();
            // Bring park buildings to the front, they're small!
            if (this.options.commons_type === 'park building') {
                this.bringToFront();
            }
        }
    });
});

L.lotMultiPolygon = function (latlngs, options) {
    return new L.LotMultiPolygon(latlngs, options);
};
