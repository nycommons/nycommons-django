var _ = require('underscore');
var flight = require('flightjs');
var singleminded = require('../lib/singleminded');

var legend = flight.component(function () {
    this.attributes({
        lotsCount: '.lots-count',
        map: null
    });

    this.onCount = function (data) {
        var count = data['lots-count'];
        this.select('lotsCount').text(count);
        $(document).trigger('receivedLotCount', { count: count });
    };

    this.updateLotCount = function (event) {
        var url = Django.url('lots:lot_count') + '?' + this.attr.map.getParamsQueryString({ bbox: true });
        singleminded.remember({
            name: 'updateLotCount',
            jqxhr: $.getJSON(url, this.onCount.bind(this))
        });
    };

    this.after('initialize', function () {
        var map = this.attr.map;
        this.on(document, 'updateLotCount', this.updateLotCount);
    });
});

module.exports = {
    legend: legend
};
