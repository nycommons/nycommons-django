var flight = require('flightjs');

var adminSidebar = flight.component(function () {
    this.attributes({
        expandSelector: '.sidebar-section-admin-expand'
    });

    this.expand = function (e) {
        e.preventDefault();
        $(document).trigger('sidebarHeaderContentShown', {
            name: 'admin'
        });
        return false;
    };

    this.after('initialize', function () {
        this.select('expandSelector').on('click', this.expand.bind(this));
    });
});

module.exports = {
    adminSidebar: adminSidebar
};
