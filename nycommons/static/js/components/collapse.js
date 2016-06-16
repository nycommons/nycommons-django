var flight = require('flightjs');

var collapsibleSection = flight.component(function () {
    this.toggle = function (event) {
        if (this.$content.is(':visible')) {
            this.$content.slideUp();
            this.$header.addClass('collapsed');
        }
        else {
            this.$content.slideDown();
            this.$header.removeClass('collapsed');
        }
        return false;
    };

    this.after('initialize', function () {
        this.$header = this.$node.find('h1,h2,h3,h4,h5,h6:eq(0)');
        this.$content = this.$header.next();
        this.$header.on('click', this.toggle.bind(this));
    });
});

module.exports = {
    collapsibleSection: collapsibleSection
};
