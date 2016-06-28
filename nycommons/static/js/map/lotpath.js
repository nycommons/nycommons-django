var L = require('leaflet');

L.LotPathMixin = {

    initActionPath: function() {
        if (this.feature && this.feature.properties.organizing && !this._actionPath) {
            this._actionPath = $('.map-icon-organizing svg polygon').clone().get()[0];
            if (this._path) {
                this._container = this._path.parentNode;
            }
            if (this.getLayers) {
                this._container = this.getLayers()[0]._path.parentNode;
            }
            this.updateActionPathScale();

            this._map.on('zoomend', this.updateActionPathScale.bind(this));
            this.on('remove', this.removeActionPath.bind(this));
        }
    },

    removeActionPath: function() {
        if (this._actionPath && this._actionPath.parentNode) {
            this._actionPath.parentNode.removeChild(this._actionPath);
        }
    },

    updateActionPathScale: function () {
        if (this._actionPath && this._map) {
            this._container.appendChild(this._actionPath);

            var latlng = (this.getBounds ? this.getBounds().getCenter() : this.getLatLng());
            var bbox = this._actionPath.getBBox(),
                point = this._map.latLngToLayerPoint(latlng),
                zoom = this._map.getZoom(),
                scale = 0.5;

            // Translate and scale around the layer's point
            if (zoom >= 16) {
                scale = 1.5;
            }
            else if (zoom >= 15) {
                scale = 1.5;
            }
            else if (zoom >= 14) {
                scale = 1.2;
            }
            else if (zoom >= 13) {
                scale = 1;
            }
            var x = point.x - ((bbox.width * scale) / 2),
                y = point.y - bbox.height * scale;
            this._actionPath.setAttribute('transform', 'translate(' + x + ',' + y + ') scale(' + scale + ')');
        }
    }

};
