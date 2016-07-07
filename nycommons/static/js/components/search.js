var flight = require('flightjs');

var searchButton = flight.component(function () {
    this.click = function (event) {
        $(this.attr.searchBar).toggle();
        $('body').toggleClass('search-enabled');
        return false;
    };

    this.after('initialize', function () {
        this.on('click', this.click);
    });
});

var searchBar = flight.component(function () {
    this.close = function (event) {
        this.$node.hide();
        $('body').removeClass('search-enabled');
        return false;
    };

    this.after('initialize', function () {
        this.$node.find('.map-search-close').on('click', this.close.bind(this));
    });
});

module.exports = {
    bar: searchBar,
    button: searchButton
};
