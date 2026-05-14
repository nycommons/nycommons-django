var flight = require('flightjs');

var header = flight.component(function () {
    this.attributes({
        'headerWrapperSelector': '.header-wrapper',
        'menuItemSelector': '.mainmenu-item'
    });

    this.onMouseEnter = function (e) {
        var $target = $(e.target);
        if ($target.is('.mainmenu-item-parent')) {
            var $submenu = $target.nextAll('.submenu');
            this.select('headerWrapperSelector').css({
                'margin-top': $submenu.outerHeight() + 25 + 'px'
            });
        }
    };

    this.onMouseLeave = function (e) {
        this.select('headerWrapperSelector').css({ 'margin-top': '0' });
    };

    this.after('initialize', function () {
        // Only listen for events on wide screens
        if ($(document).width() <= 480) return;

        this.select('menuItemSelector').on('mouseenter', this.onMouseEnter.bind(this));
        this.select('menuItemSelector').on('mouseleave', this.onMouseLeave.bind(this));
    });
});

module.exports = {
    header: header
};
