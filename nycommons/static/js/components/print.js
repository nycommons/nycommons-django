var flight = require('flightjs');

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
            remove: '.map-sidebar,.map-menu,#djDebug,.leaflet-control-container',
            url: pageUrl
        });
        var mapImage = $('<img></img>')
            .attr('src', url)
            .addClass('map-print-image');
        $('body').append(mapImage);
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
