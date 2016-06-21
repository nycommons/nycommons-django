var flight = require('flightjs');
var Handlebars = require('handlebars');

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
                $(this).parent().find('.details-owner-list').slideToggle();
                return false;
            });
        });
    }

    this.after('initialize', function () {
        this.updateOwnershipOverview();
        $(document).on('filtersChanged', this.updateOwnershipOverview.bind(this));
    });
});


module.exports = {
    details: details
};
