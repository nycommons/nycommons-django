var flight = require('flightjs');

var sameOwnerSection = flight.component(function () {
    this.attributes({
        contentSelector: '.lot-detail-same-owner-content',
        expandSelector: 'h2'
    });

    this.loadDetails = function (e) {
        if (this.loaded) return;
        this.loaded = true;
        var params = $.param({
            organizing: this.$node.data('organizing'),
            priority: this.$node.data('priority')
        });
        var url = Django.url('lots:lot_same_owner', { pk: this.$node.data('lot') });
        this.select('contentSelector').load(url + '?' + params);
    };

    this.after('initialize', function () {
        this.loaded = false;
        this.select('expandSelector').on('click', this.loadDetails.bind(this));
    });
});

module.exports = {
    sameOwnerSection: sameOwnerSection
};
