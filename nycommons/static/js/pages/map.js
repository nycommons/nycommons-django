//
// mappage.js
//
// Scripts that only run on the map page.
//

var _ = require('underscore');
var Handlebars = require('handlebars');
var L = require('leaflet');
var Spinner = require('spin.js');
var styles = require('../lib/map-styles');

require('../leaflet.lotmap');
require('bootstrap_button');
require('bootstrap_tooltip');
require('jquery-infinite-scroll');
require('leaflet-loading');
require('../handlebars.helpers');
require('../map.search.js');
var filters = require('../components/filters');
var legend = require('../components/legend').legend;
var locateButton = require('../components/locate').locateButton;
var searchButton = require('../components/search').searchButton;
require('../components/sidebar');
var oasis = require('../lib/oasis');


// Watch out for IE 8
var console = window.console || {
    warn: function () {}
};

function updateOwnershipOverview(map) {
    var url = Django.url('lots:lot_ownership_overview');
    $.getJSON(url + '?' + map.getParamsQueryString({ bbox: true }), function (data) {
        var template = Handlebars.compile($('#details-template').html());
        var content = template({
            lottypes: data.owners
        });
        $('.details-overview').html(content);
        $('.map-printable-details').html(content);
        $('.details-area-compare-tooltip').tooltip();
        $('.details-show-owners :input').change(function () {
            var $list = $('.details-owner-list-' + $(this).data('type')),
                $otherButton = $('.details-show-organizing-' + $(this).data('type'));
            if ($(this).is(':checked')) {
                $list.slideDown();

                // Slide up other one
                if ($otherButton.is('.active')) {
                    $('.details-show-organizing-' + $(this).data('type')).button('toggle');
                }
            }
            else {
                $list.slideUp();
            }
        });
        $('.details-show-organizing :input').change(function () {
            var $list = $('.details-organizing-' + $(this).data('type')),
                $otherButton = $('.details-show-owners-' + $(this).data('type'));
            if ($(this).is(':checked')) {
                $list.slideDown();

                // Slide up other one
                if ($otherButton.is('.active')) {
                    $('.details-show-owners-' + $(this).data('type')).button('toggle');
                }
            }
            else {
                $list.slideUp();
            }
        });
    });
}

function updateDetailsLink(map) {
    var params = map.buildLotFilterParams();
    delete params.parents_only;

    var l = window.location,
        query = '?' + $.param(params),
        url = l.protocol + '//' + l.host + l.pathname + query + l.hash;
    $('a.details-link').attr('href', url);
}

function initializeBoundaries(map) {
    // Check for city council / community board layers, console a warning
    var url = window.location.protocol + '//' + window.location.host +
        Django.url('inplace:layer_upload');
    if ($('.filter-city-council-districts').length === 0) {
        console.warn('No city council districts! Add some here: ' + url);
    }
    if ($('.filter-community-districts').length === 0) {
        console.warn('No community districts! Add some here: ' + url);
    }

    $('.filter-boundaries').change(function (e, options) {
        // Clear other boundary filters
        $('.filter-boundaries').not('#' + $(this).attr('id')).val('');

        addBoundary(map, $(this).data('layer'), $(this).val(), options);
    });

    // If boundaries were set via query string trigger change here. Can't do 
    // until the map exists, but we actually do want to set most the other 
    // filters before the map exists.
    $('.filter-boundaries').each(function () {
        if ($(this).val()) {
            $(this).trigger('change', { zoomToBounds: false });
        }
    });
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

function deparam() {
    var vars = {},
        param,
        params = window.location.search.slice(1).split('&');
    for(var i = 0; i < params.length; i++) {
        param = params[i].split('=');
        vars[param[0]] = decodeURIComponent(param[1]);
    }
    return vars;
}

function setFiltersUIFromQueryParams(params) {
    // Clear checkbox filters
    $('.filter[type=checkbox]').prop('checked', false);

    // Set layers filters
    var layers = params.layers.split(',');
    _.each(layers, function (layer) {
        $('.filter-layer[name=' + layer +']').prop('checked', true);
    });

    // Set owner types
    if (params.owner_types) {
        _.each(params.owner_types.split(','), function (owner_type) {
            $('.filter-owner-type[name=' + owner_type +']').prop('checked', true);
        });
    }

    // Set owners filters
    if (params.public_owners) {
        $('.filter-owner-public').val(params.public_owners);
    }
    if (params.private_owners) {
        $('.filter-owner-private').val(params.private_owners);
    }

    // Set boundaries filters
    if (params.boundary) {
        var split = params.boundary.split('::'),
            layer = split[0].replace(/\+/g, ' '),
            id = split[1];
        $('.filter-boundaries[data-layer="' + layer + '"]').val(id);
    }
}

// TODO button no longer exists but we should load recent activity
/*
var spinner = new Spinner().spin($('.activity-stream')[0]);

var url = Django.url('activity_list');
$('.activity-stream').load(url, function () {
    $('.action-list').infinitescroll({
        loading: {
            finishedMsg: 'No more activities to load.'
        },
        behavior: 'local',
        binder: $('.overlaymenu-news .overlaymenu-menu-content'),
        itemSelector: 'li.action',
        navSelector: '.activity-stream-nav',
        nextSelector: '.activity-stream-nav a:first'
    });
});
*/

$(document).ready(function () {
    if ($('.map-page').length > 0) {
        var params;
        if (window.location.search.length) {
            setFiltersUIFromQueryParams(deparam());
        }

        var mapOptions = {
            filterParams: filters.filtersToParams(null, {}),
            onMouseOverFeature: function (feature) {},
            onMouseOutFeature: function (feature) {}
        };

        // Get the current center/zoom first rather than wait for map to load
        // and L.hash to set them. This is slightly smoother
        var hash = window.location.hash;
        if (hash && hash !== '') {
            hash = hash.slice(1).split('/');
            mapOptions.center = hash.slice(1);
            mapOptions.zoom = hash[0];
        }

        var map = L.lotMap('map', mapOptions);
        map.addControl(L.control.zoom({ position: 'bottomright' }));

        initializeBoundaries(map);

        map.addLotsLayer();

        $(document).on('filtersChanged', function (event, data) {
            map.updateFilters(data.filters);
            var params = map.buildLotFilterParams();
            $(document).trigger('updateLotCount');
        });

        legend.attachTo('#map-legend', { map: map });
        locateButton.attachTo('.map-header-locate-btn', { map: map });
        searchButton.attachTo('.map-header-search-btn', { searchBar: '.map-search' });
        filters.filters.attachTo('.filters-section');

        $('.details-print').click(function () {
            window.print();
            return false;
        });

        $('form.map-search-form').mapsearch()
            .on('searchstart', function (e) {
                map.removeUserLayer();
            })
            .on('searchresultfound', function (e, result) {
                var oasisUrl = oasis.vacantLotsUrl(result.latitude, result.longitude);
                map.addUserLayer([result.latitude, result.longitude], {
                    popupContent: '<p>This is the point we found when we searched.</p><p>Not seeing a vacant lot here that you expected? Check <a href="' + oasisUrl + '" target="_blank">OASIS in this area</a>. Learn more about using OASIS in our <a href="/faq/#why-isnt-vacant-lot-near-me-map" target="_blank">FAQs</a>.</p>'
                });
            });

        $(document).trigger('updateLotCount');
        map.on({
            'moveend': function () {
                $(document).trigger('updateLotCount');
            },
            'zoomend': function () {
                $(document).trigger('updateLotCount');
            },
            'lotlayertransition': function (e) {
                map.addLotsLayer(map.buildLotFilterParams());
                map.updateDisplayedLots();
            }
        });

        $('.export').click(function (e) {
            var url = $(this).data('baseurl') + map.getParamsQueryString({ bbox: true });
            window.location.href = url;
            e.preventDefault();
        });

        $('.admin-button-add-lot').click(function () {
            map.enterLotAddMode();
        });

        $('.admin-button-email').click(function () {
            map.enterMailMode();
        });
    }
});
