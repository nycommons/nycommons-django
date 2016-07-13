//
// mappage.js
//
// Scripts that only run on the map page.
//

var _ = require('underscore');
var L = require('leaflet');

require('../map/lotmap');
require('bootstrap_button');
require('bootstrap_tooltip');
require('jquery-infinite-scroll');
require('leaflet-loading');
require('../handlebars.helpers');
var activities = require('../components/activities');
var details = require('../components/details');
var exportLink = require('../components/export').exportLink;
var filters = require('../components/filters');
var hashHandler = require('../components/hash');
var legend = require('../components/legend').legend;
var locateButton = require('../components/locate').locateButton;
var search = require('../components/search');
require('../components/sidebar');
require('../data/lotcounts').init();
require('../data/ownercounts').init();


// Watch out for IE 8
var console = window.console || {
    warn: function () {}
};

function updateDetailsLink(map) {
    var params = map.buildLotFilterParams();
    delete params.parents_only;

    var l = window.location,
        query = '?' + $.param(params),
        url = l.protocol + '//' + l.host + l.pathname + query + l.hash;
    $('a.details-link').attr('href', url);
}

function checkForBoundaries() {
    // Check for city council / community board layers, console a warning
    var url = window.location.protocol + '//' + window.location.host +
        Django.url('inplace:layer_upload');
    if ($('.filter-city-council-districts').length === 0) {
        console.warn('No city council districts! Add some here: ' + url);
    }
    if ($('.filter-community-districts').length === 0) {
        console.warn('No community districts! Add some here: ' + url);
    }
}

function addBoundary(map, layer, pk, options) {
    if (!pk || pk === '') {
        map.removeBoundaries();
    }

    options = options || {};
    if (options.zoomToBounds === undefined) {
        options.zoomToBounds = true;
    }
    var url = Django.url('inplace:boundary_detail', { pk: pk });
    $.getJSON(url, function (data) {
        map.updateBoundaries(data, options);
    });
}

$(document).ready(function () {
    if ($('.map-page').length > 0) {
        var params;

        var mapOptions = {
            filterParams: filters.filtersToParams(null, {}),
            onMouseOverFeature: function (feature) {},
            onMouseOutFeature: function (feature) {}
        };

        // Get the current center/zoom from hash
        var parsedHash = hashHandler.parse();
        if (parsedHash.center) {
            mapOptions.center = parsedHash.center;
        }
        if (parsedHash.zoom) {
            mapOptions.zoom = parsedHash.zoom;
        }

        var map = L.lotMap('map', mapOptions);
        map.addControl(L.control.zoom({ position: 'bottomright' }));

        checkForBoundaries();

        $(document).on('filtersChanged', function (event, data) {
            map.updateFilters(data.filters);
            var params = map.buildLotFilterParams();
            $(document).trigger('updateLotCount', { map: map });
            $(document).trigger('updateOwnerCount', { map: map });
            hashHandler.update(map);
        });

        // Add boundary when input changes
        $(document).on('boundaryChanged', function (event, data) {
            addBoundary(map, data.layer, data.value, {});
        });

        // Show and hide lots based on boundary geometry
        map.on('boundarieschange', function (event) {
            map.updateFilters(map.currentFilters);
        });

        activities.activities.attachTo('.map-header-content-activities');
        activities.recentActivity.attachTo('.recent-activity');
        legend.attachTo('#map-legend');
        locateButton.attachTo('.map-header-locate-btn', { map: map });
        search.button.attachTo('.map-header-search-btn', { searchBar: '.map-search' });
        search.bar.attachTo('.map-search', { map: map });
        details.details.attachTo('.details-section');
        filters.filters.attachTo('.filters-section', { initialFilters: parsedHash.filters || {} });
        exportLink.attachTo('.export', { map: map });

        // Add lots *after* filters are set up so we have initial filters loaded
        map.addLotsLayer();

        $('.details-print').click(function () {
            window.print();
            return false;
        });

        $(document).trigger('updateLotCount', { map: map });
        $(document).trigger('updateOwnerCount', { map: map });
        map.on({
            'moveend': function () {
                hashHandler.update(map);
                $(document).trigger('mapMoved');
                $(document).trigger('updateLotCount', { map: map });
                $(document).trigger('updateOwnerCount', { map: map });
            },
            'zoomend': function () {
                hashHandler.update(map);
                $(document).trigger('mapMoved');
                $(document).trigger('updateLotCount', { map: map });
                $(document).trigger('updateOwnerCount', { map: map });
            }
        });

        $('.admin-button-add-lot').click(function () {
            map.enterLotAddMode();
        });

        $('.admin-button-email').click(function () {
            map.enterMailMode();
        });

        $(document).on('legendCollapsed', function () {
            $('body').addClass('map-legend-collapsed');
        });
        $(document).on('legendExpanded', function () {
            $('body').removeClass('map-legend-collapsed');
        });
    }
});
