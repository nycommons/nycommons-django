var flight = require('flightjs');
var Handlebars = require('handlebars');

var formatSquareFeet = require('../lib/area').formatSquareFeet;

Handlebars.registerHelper('formatArea', function (area) {
    area = Handlebars.escapeExpression(area);
    return formatSquareFeet(area);
});

var details = flight.component(function () {
    this.receivedLotCount = function (event, data) {
        this.$node.find('.details-header-property-count').text(data.count);
    };

    this.receivedOwnerCount = function (event, data) {
        var template = Handlebars.compile($('#details-template').html());
        var content = template({ lottypes: data.results });
        $('.details-body').html(content);

        this.$node.find('.details-toggle-owner-list').on('click', function () {
            $(this).toggleClass('expanded');
            $(this).parent().parent().find('.details-owner-list').slideToggle();
            return false;
        });
    };

    this.after('initialize', function () {
        this.on(document, 'receivedLotCount', this.receivedLotCount);
        this.on(document, 'receivedOwnerCount', this.receivedOwnerCount);
    });
});


module.exports = {
    details: details
};
