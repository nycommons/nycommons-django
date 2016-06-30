var flight = require('flightjs');

var legend = flight.component(function () {
    this.attributes({
        lotsCount: '.lots-count'
    });

    this.receivedLotCount = function (event, data) {
        this.select('lotsCount').text(data.count);
    };

    this.after('initialize', function () {
        this.on(document, 'receivedLotCount', this.receivedLotCount);
    });
});

module.exports = {
    legend: legend
};
