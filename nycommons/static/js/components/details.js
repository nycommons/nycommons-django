var flight = require('flightjs');
var Handlebars = require('handlebars');

var formatSquareFeet = require('../lib/area').formatSquareFeet;

Handlebars.registerHelper('formatArea', function (area) {
    area = Handlebars.escapeExpression(area);
    return formatSquareFeet(area);
});

var details = flight.component(function () {
    this.attributes({
        map: null
    });

    this.updateOwnershipOverview = function () {
        var url = Django.url('lots:lot_ownership_overview');
        var $details = this.$node;

        $.getJSON(url + '?' + this.attr.map.getParamsQueryString({ bbox: true }), function (data) {
            var template = Handlebars.compile($('#details-template').html());
            var content = template({ lottypes: data });
            $('.details-body').html(content);
            $('.map-printable-details').html(content);

            $details.find('.details-toggle-owner-list').on('click', function () {
                $(this).toggleClass('expanded');
                $(this).parent().parent().find('.details-owner-list').slideToggle();
                return false;
            });
        });
    }

    this.receivedLotCount = function (event, data) {
        this.$node.find('.details-header-property-count').text(data.count);
    };

    this.after('initialize', function () {
        this.updateOwnershipOverview();
        this.on(document, 'filtersChanged', this.updateOwnershipOverview);
        this.on(document, 'receivedLotCount', this.receivedLotCount);
    });
});


module.exports = {
    details: details
};
