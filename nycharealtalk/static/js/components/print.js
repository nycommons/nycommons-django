var _ = require('underscore');
var flight = require('flightjs');
var Spinner = require('spin.js');
var spinnerOptions = require('../lib/spinner-options');

var printButton = flight.component(function () {
    this.handleClick = function (e) {
        this.addMapImage($('#map'), window.location.href);
        $('body').addClass('map-print-page');
        return false;
    };

    this.addMapImage = function ($map, pageUrl) {
        var url = window.mapScreenshotUrl + '?';
        url += $.param({
            height: $map.height(),
            width: $map.width(),
            element: '#map',
            remove: '.map-sidebar,.map-menu,#djDebug,.leaflet-control-container',
            url: pageUrl
        });
        this.spinner = new Spinner(spinnerOptions).spin($('.map-sidebar')[0]);
        $.getJSON(url, (function (data) {
            this.spinner.stop();
            var mapImage = $('<img></img>')
                .attr('src', data.url)
                .addClass('map-print-image');
            $('body').append(mapImage);
        }).bind(this));
    };

    this.after('initialize', function () {
        this.on('click', this.handleClick.bind(this));
    });
});

var printModePrintButton = flight.component(function () {
    this.handleClick = function (e) {
        window.print();
        return false;
    };

    this.after('initialize', function () {
        this.on('click', this.handleClick.bind(this));
    });
});

var printModeExitButton = flight.component(function () {
    this.handleClick = function (e) {
        $('.map-print-image').remove();
        $('body').removeClass('map-print-page');
        this.attr.map.invalidateSize();
        return false;
    };

    this.after('initialize', function () {
        this.on('click', this.handleClick.bind(this));
    });
});

module.exports = {
    printButton: printButton,
    printModeExitButton: printModeExitButton,
    printModePrintButton: printModePrintButton
};
