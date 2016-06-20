var flight = require('flightjs');
var Handlebars = require('handlebars');

var details = flight.component(function () {
    this.attributes({
        map: null
    });

    this.updateOwnershipOverview = function () {
        var url = Django.url('lots:lot_ownership_overview');
        $.getJSON(url + '?' + this.attr.map.getParamsQueryString({ bbox: true }), function (data) {
            var template = Handlebars.compile($('#details-template').html());
            var content = template({ lottypes: data });
            $('.details-body').html(content);
            $('.map-printable-details').html(content);
            $('.details-show-owners :input').change(function () {
                var $list = $('.details-owner-list-' + $(this).data('type')),
                    $otherButton = $('.details-show-organizing-' + $(this).data('type'));
                if ($(this).is(':checked')) {
                    $list.slideDown();

                    // Slide up other one
                    if ($otherButton.is('.active')) {
                        $('.details-show-organizing-' + $(this).data('type')).button('toggle');
                    }
                }
                else {
                    $list.slideUp();
                }
            });
            $('.details-show-organizing :input').change(function () {
                var $list = $('.details-organizing-' + $(this).data('type')),
                    $otherButton = $('.details-show-owners-' + $(this).data('type'));
                if ($(this).is(':checked')) {
                    $list.slideDown();

                    // Slide up other one
                    if ($otherButton.is('.active')) {
                        $('.details-show-owners-' + $(this).data('type')).button('toggle');
                    }
                }
                else {
                    $list.slideUp();
                }
            });
        });
    }

    this.after('initialize', function () {
        // TODO on filters change, updateOwnershipOverview
        this.updateOwnershipOverview();
    });
});


module.exports = {
    details: details
};
