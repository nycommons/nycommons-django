var flight = require('flightjs');

var exportLink = flight.component(function () {
    this.attributes({
        map: null
    });

    this.updateLink = function () {
        var url = this.$node.data('baseurl') + this.attr.map.getParamsQueryString({ bbox: true });
        this.$node.attr('href', url);
    };

    this.after('initialize', function () {
        this.updateLink();
        this.on(document, 'filtersChanged', this.updateLink);
        this.on(document, 'mapMoved', this.updateLink);
    });
});


module.exports = {
    exportLink: exportLink
};
