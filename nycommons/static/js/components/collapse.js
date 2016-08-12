var flight = require('flightjs');

var collapsibleSection = flight.component(function () {
    this.toggle = function (event) {
        if (!this.$header.is('.collapsed')) {
            this.$header.addClass('collapse-collapsing');
            this.$header.addClass('collapsed');
            this.$content.slideUp(400, (function () {
                this.$header.removeClass('collapse-collapsing');
            }).bind(this));
        }
        else {
            this.$header.addClass('collapse-expanding');
            this.$header.removeClass('collapsed');
            this.$content.slideDown(400, (function () {
                this.$header.removeClass('collapse-expanding');
            }).bind(this));
        }
        return false;
    };

    this.after('initialize', function () {
        this.$header = this.$node.find('h1,h2,h3,h4,h5,h6').first();
        this.$content = this.$header.next();
        this.$header.on('click', this.toggle.bind(this));

        // Hide on init if collapsed
        if (this.$header.is('.collapsed')) {
            this.$content.hide();
        }
    });
});

module.exports = {
    collapsibleSection: collapsibleSection
};
