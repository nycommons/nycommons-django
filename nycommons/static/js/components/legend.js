var _ = require('underscore');
var flight = require('flightjs');

var legend = flight.component(function () {
    this.attributes({
        lotsCount: '.lots-count'
    });

    this.receivedLotCount = function (event, data) {
        this.select('lotsCount').text(data.count);
    };

    this.receivedOwnerCount = function (event, data) {
        _.each(data.results, function (element) {
            console.log(element.type, element.count);
            this.$node.find('.legend-count[data-type="' + element.type + '"]').text(element.count);
        }, this);
    };

    this.after('initialize', function () {
        this.on(document, 'receivedLotCount', this.receivedLotCount);
        this.on(document, 'receivedOwnerCount', this.receivedOwnerCount.bind(this));
    });
});

module.exports = {
    legend: legend
};
