var L = require('leaflet');
var _ = require('underscore');

require('./lotmultipolygon');
require('./lotpolygon');


L.LotGeoJson = L.GeoJSON.extend({
    initialize: function (geojson, options) {
        L.GeoJSON.prototype.initialize.call(this, geojson, options);
    },

    addData: function (geojson) {
        var features = L.Util.isArray(geojson) ? geojson : geojson.features,
            i, len, feature;

        if (features) {
            for (i = 0, len = features.length; i < len; i++) {
                // Only add this if geometry or geometries are set and not null
                feature = features[i];
                if (feature.geometries || feature.geometry || feature.features || feature.coordinates) {
                    this.addData(features[i]);
                }
            }
            return this;
        }

        var options = this.options;

        if (options.filter && !options.filter(geojson)) { return; }

        var layer = this.geometryToLotLayer(geojson, options.pointToLayer, options.coordsToLatLng, options);
        layer.feature = L.GeoJSON.asFeature(geojson);

        layer.defaultOptions = layer.options;
        this.resetStyle(layer);

        if (options.onEachFeature) {
            options.onEachFeature(geojson, layer);
        }

        return this.addLayer(layer);
    },

    geometryToLotLayer: function (geojson, pointToLayer, coordsToLatLng, vectorOptions) {
        var geometry = geojson.type === 'Feature' ? geojson.geometry : geojson,
            coords = geometry.coordinates,
            layers = [],
            latlng, latlngs, i, len,
            options = L.extend({}, vectorOptions, { commons_type: geojson.properties.commons_type });

        coordsToLatLng = coordsToLatLng || L.GeoJSON.coordsToLatLng;

        switch (geometry.type) {
        case 'Point':
            latlng = coordsToLatLng(coords);
            return pointToLayer ? pointToLayer(geojson, latlng) : new L.Marker(latlng);

        case 'MultiPoint':
            for (i = 0, len = coords.length; i < len; i++) {
                latlng = coordsToLatLng(coords[i]);
                layers.push(pointToLayer ? pointToLayer(geojson, latlng) : new L.Marker(latlng));
            }
            return new L.FeatureGroup(layers);

        case 'LineString':
            latlngs = L.GeoJSON.coordsToLatLngs(coords, 0, coordsToLatLng);
            return new L.Polyline(latlngs, options);

        case 'Polygon':
            if (coords.length === 2 && !coords[1].length) {
                throw new Error('Invalid GeoJSON object.');
            }
            latlngs = L.GeoJSON.coordsToLatLngs(coords, 1, coordsToLatLng);
            return L.lotPolygon(latlngs, options);

        case 'MultiLineString':
            latlngs = L.GeoJSON.coordsToLatLngs(coords, 1, coordsToLatLng);
            return new L.MultiPolyline(latlngs, options);

        case 'MultiPolygon':
            latlngs = L.GeoJSON.coordsToLatLngs(coords, 2, coordsToLatLng);
            return L.lotMultiPolygon(latlngs, options);

        case 'GeometryCollection':
            for (i = 0, len = geometry.geometries.length; i < len; i++) {

                layers.push(L.GeoJSON.geometryToLayer({
                    geometry: geometry.geometries[i],
                    type: 'Feature',
                    properties: geojson.properties
                }, pointToLayer, coordsToLatLng, options));
            }
            return new L.FeatureGroup(layers);

        default:
            throw new Error('Invalid GeoJSON object.');
        }
    }

});

L.lotGeoJson = function (geojson, options) {
    return new L.LotGeoJson(geojson, options);
};
