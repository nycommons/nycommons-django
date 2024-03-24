//
// lotdetailpage.js
//
// Scripts that only run on the lot detail page.
//

var L = require('leaflet');

require('leaflet-dataoptions');
require('leaflet-geojson-gridlayer');

var collapsibleSection = require('../components/collapse').collapsibleSection;
var sameOwnerSection = require('../components/same-owner').sameOwnerSection;
var mapstyles = require('../map/styles');
var StreetView = require('../lib/streetview');
var usercontent = require('../components/usercontent').usercontent;


function getLotLayerOptions(lotPk) {
    return {
        pointToLayer: function (feature, latlng) {
            return L.circleMarker(latlng);
        },
        style: function (feature) {
            var style = mapstyles.getStyle(feature);

            // Style this lot distinctly
            if (feature.id === lotPk) {
                style.fillOpacity = 1;
            }
            else {
                style.fillOpacity = 0.2;
            }
            return style;
        }
    };
}

function addBaseLayer(map) {
    var streets = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
}

function addLotsLayer(map) {
    var url = map.options.lotsTilesUrl,
        lotLayerOptions = getLotLayerOptions(map.options.lotPk);
    L.geoJsonGridLayer(url, {
        layers: {
            'lots-centroids': {
                maxZoom: 1,
                pointToLayer: function (feature, latlng) {
                    return L.circleMarker(latlng);
                }
            },
            'lots-polygons': lotLayerOptions
        }
    }).addTo(map);
}

function initFacebookLink($link) {
    var url = 'http://www.facebook.com/sharer/sharer.php?' + $.param({
        u: window.location.href
    });
    $link.attr('href', url);
}

function initTwitterLink($link) {
    var url = 'http://twitter.com/intent/tweet?' + $.param({
        related: 'nycommons',
        text: $link.data('tweet'),
        url: window.location.href
    });
    $link.attr('href', url);
}

$(document).ready(function () {
    if ($('.lot-detail-page').length > 0) {
        var options = {
            attributionControl: false,
            doubleClickZoom: false,
            dragging: false,
            scrollWheelZoom: false,
            touchZoom: false,
            zoom: $('#lot-detail-map').data('lZoom'),
            center: $('#lot-detail-map').data('lCenter'),
            bbox: $('#lot-detail-map').data('lBbox'),
            zoomControl: $('#lot-detail-map').data('lZoomControl'),
            lotsTilesUrl: $('#lot-detail-map').data('lLotsTilesUrl'),
            lotPk: $('#lot-detail-map').data('lLotPk')
        };

        var map = L.map('lot-detail-map', options);

        var bbox = map.options.bbox;

        if (bbox) {
            map.fitBounds([
                [bbox[1], bbox[0]],
                [bbox[3], bbox[2]]
            ], { padding: [20, 20], maxZoom: 18 });
        }

        addBaseLayer(map);
        addLotsLayer(map);
        StreetView.load_streetview(
            $('.lot-detail-header-image').data('lon'),
            $('.lot-detail-header-image').data('lat'),
            $('.lot-detail-header-image'),
            $('.lot-detail-header-streetview-error')
        );
    }

    $('.btn-add-to-group').click(function () {
        if (!confirm("Group these two lots? This will move notes, organizers, and other content to the group and is very difficult to undo.")) {
            return false;
        }
        var url = Django.url('lots:add_to_group', { pk: $(this).data('lot') });
        $.post(url, { lot_to_add: $(this).data('lot-to-add') }, function (data) {
            window.location = Django.url('lots:lot_detail', { pk: data.group });
        });
        return false;
    });

    $('.btn-remove-from-group').click(function () {
        if (!confirm("Remove this lot from the group?")) {
            return false;
        }
        var url = Django.url('lots:remove_from_group', { pk: $(this).data('lot') });
        $.post(url, {}, function (data) {
            window.location = Django.url('lots:lot_detail', { pk: data.former_group });
        });
        return false;
    });

    $('.btn-show-private-organizers').click(function () {
        $('.organizer-list-private').slideToggle();
        return false;
    });

    $('.lot-detail-print').click(function () {
        window.print();
        return false;
    });

    initFacebookLink($('.share-facebook'));
    initTwitterLink($('.share-twitter'));

    collapsibleSection.attachTo('section.collapsible');
    sameOwnerSection.attachTo('.lot-detail-same-owner');
    usercontent.attachTo('.usercontent-list');
});
