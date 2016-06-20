var _ = require('underscore');
var Handlebars = require('handlebars');
var L = require('leaflet');
var mapstyles = require('./lib/map-styles');
var Spinner = require('spin.js');

require('livinglots.addlot');
require('livinglots.emailparticipants');
require('livinglots.boundaries');
require('leaflet-plugins-bing');
require('leaflet-dataoptions');
require('leaflet-geojsongridlayer');
require('leaflet-usermarker');

var filters = require('./components/filters');
require('./leaflet.lotmarker');


L.LotMap = L.Map.extend({
    lotsLayer: null,
    currentFilters: {},
    userLayer: null,
    userLocationZoom: 16,

    filters: null,

    compiledPopupTemplate: null,

    getPopupTemplate: function () {
        if (this.compiledPopupTemplate) {
            return this.compiledPopupTemplate;
        }
        var source = $("#popup-template").html();
        this.compiledPopupTemplate = Handlebars.compile(source);
        return this.compiledPopupTemplate;
    },

    lotLayerOptions: {
        onEachFeature: function (feature, layer) {
            layer.on({
                'click': function (event) {
                    var latlng = event.latlng,
                        x = this._map.latLngToContainerPoint(latlng).x,
                        y = this._map.latLngToContainerPoint(latlng).y - 100,
                        point = this._map.containerPointToLatLng([x, y]),
                        template = this._map.getPopupTemplate();
                    this.bindPopup('<div id="popup"></div>').openPopup();
                    var spinner = new Spinner().spin($('#popup')[0]);
                    $.getJSON(Django.url('lots:lot_detail_json', { pk: this.feature.id }), function (data) {
                        spinner.stop();
                        layer.setPopupContent(template(data));
                    });
                    return this._map.setView(point, this._map._zoom);
                },
                'mouseover': function (event) {
                    this._map.options.onMouseOverFeature(event.target.feature);
                },
                'mouseout': function (event) {
                    this._map.options.onMouseOutFeature(event.target.feature);
                }
            });
        },
        pointToLayer: function (feature, latlng) {
            return L.lotMarker(latlng, {});
        },
        style: function (feature) {
            var style = {
                fillColor: '#000000',
                fillOpacity: 1,
                stroke: 0
            };
            style.fillColor = mapstyles.getLayerColor([feature.properties.commons_type]);
            return style;
        },
        popupOptions: {
            autoPan: false,
            maxWidth: 300,
            minWidth: 300,
            offset: [0, 0]
        }
    },

    initialize: function (id, options) {
        L.Map.prototype.initialize.call(this, id, options);
        this.addBaseLayer();

        // When new lots are added ensure they should be displayed
        var map = this;
        this.on('layeradd', function (event) {
            if (event.layer.feature) {
                // We have something other than a layer (eg a boundary), add it
                if (event.layer.feature.properties.commons_type === undefined) {
                    event.layer.addTo(map);
                    return;
                }

                var lot = event.layer;
                if (filters.lotShouldAppear(lot, map.currentFilters, map.boundariesLayer)) {
                    lot.addTo(map);
                }
                else {
                    lot.removeFrom(map);
                }
            }
        });
    },

    buildLotFilterParams: function (options) {
        return filters.filtersToParams(this, options);
    },

    getParamsQueryString: function (options, overrides) {
        var params = this.buildLotFilterParams(options);
        return $.param(_.extend(params, overrides));
    },

    addBaseLayer: function () {
        var streets = L.tileLayer('http://{s}.tile.stamen.com/toner/{z}/{x}/{y}.png', {
            attribution: 'Map tiles by <a href="http://stamen.com/">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.'
        }).addTo(this);
        var bing = new L.BingLayer('Ajio1n0EgmAAvT3zLndCpHrYR_LHJDgfDU6B0tV_1RClr7OFLzy4RnkLXlSdkJ_x');

        L.control.layers({
            streets: streets,
            satellite: bing,
        }, null, { position: 'bottomright' }).addTo(this);
    },

    addLotsLayer: function () {
        var url = this.options.lotCentroidsUrl;
        var centroidsOptions = _.extend({ maxZoom: 15 }, this.lotLayerOptions);
        var polygonsOptions = _.extend({ minZoom: 15 }, this.lotLayerOptions);
        this.lotsLayer = L.geoJsonGridLayer(url, {
            layers: {
                'lots-centroids': centroidsOptions,
                'lots-polygons': polygonsOptions
            }
        }).addTo(this);
    },

    updateFilters: function (filters) {
        this.currentFilters = filters;
        this.updateDisplayedLots(filters);
    },

    updateDisplayedLots: function (currentFilters) {
        if (!this.lotsLayer) return;
        var layers = this.lotsLayer.getLayers();
        var map = this,
            zoom = map.getZoom();
        layers.forEach(function (layer) {
            var minZoom = layer.options.minZoom,
                maxZoom = layer.options.maxZoom;
            layer.eachLayer(function (lot) {
                if ((minZoom && zoom < minZoom) || (maxZoom && zoom > maxZoom)) {
                    lot.removeFrom(map);
                    return;
                }
                if (filters.lotShouldAppear(lot, currentFilters, map.boundariesLayer)) {
                    lot.addTo(map);
                }
                else {
                    lot.removeFrom(map);
                }
            }, this);
        }, this);
    },

    addUserLayer: function (latlng, opts) {
        opts = opts || {};
        this.userLayer = L.userMarker(latlng, {
            smallIcon: true,
        }).addTo(this);
        if (opts.popupContent) {
            this.userLayer.bindPopup(opts.popupContent).openPopup();
        }
        this.setView(latlng, this.userLocationZoom);
    },

    removeUserLayer: function () {
        if (this.userLayer) {
            this.removeLayer(this.userLayer);
        }
    }
});

L.lotMap = function (id, options) {
    return new L.LotMap(id, options);
};
