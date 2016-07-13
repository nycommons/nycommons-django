var _ = require('underscore');
var flight = require('flightjs');

var legendHeader = flight.component(function () {
    this.attributes({
        legend: null
    });

    this.onClick = function (e) {
        e.stopPropagation();
        this.attr.legend.toggleCollapse();
    };

    this.after('initialize', function () {
        this.on('click', this.onClick);
    });
});

var legend = flight.component(function () {
    this.attributes({
        legendHeaderSelector: '.legend-header',
        lotsCount: '.lots-count'
    });

    this.toggleCollapse = function () {
        this.$node.toggleClass('collapse');
        if (this.$node.hasClass('collapse')) {
            $(document).trigger('legendCollapsed');
        }
        else {
            $(document).trigger('legendExpanded');
        }
    };

    this.receivedLotCount = function (event, data) {
        this.select('lotsCount').text(data.count);
    };

    this.receivedOwnerCount = function (event, data) {
        _.each(data.results, function (element) {
            this.$node.find('.legend-count[data-type="' + element.type + '"]').text(element.count);
        }, this);
    };

    this.after('initialize', function () {
        legendHeader.attachTo(this.select('legendHeaderSelector'), {
            legend: this
        });
        this.on(document, 'receivedLotCount', this.receivedLotCount);
        this.on(document, 'receivedOwnerCount', this.receivedOwnerCount.bind(this));
    });
});

module.exports = {
    legend: legend
};
