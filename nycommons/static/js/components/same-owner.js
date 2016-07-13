var flight = require('flightjs');
var Spinner = require('spin.js');

var spinnerOptions = {
    left: '100%',
    length: 5,
    position: 'relative',
    radius: 6,
    top: '15px',
    width: 2
};

var sameOwnerSection = flight.component(function () {
    this.attributes({
        contentSelector: '.lot-detail-same-owner-content',
        expandSelector: 'h2'
    });

    this.loadDetails = function (e) {
        if (this.loaded) return;
        var spinner = new Spinner(spinnerOptions).spin(this.select('expandSelector')[0]);
        this.loaded = true;
        var params = $.param({
            organizing: this.$node.data('organizing'),
            priority: this.$node.data('priority')
        });
        var url = Django.url('lots:lot_same_owner', { pk: this.$node.data('lot') });
        this.select('contentSelector').load(url + '?' + params, function () {
            spinner.stop();
        });
    };

    this.after('initialize', function () {
        this.loaded = false;
        this.select('expandSelector').on('click', this.loadDetails.bind(this));
    });
});

module.exports = {
    sameOwnerSection: sameOwnerSection
};
