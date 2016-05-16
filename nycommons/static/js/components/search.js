var flight = require('flightjs');

var searchButton = flight.component(function () {
    this.click = function (event) {
        $(this.attr.searchBar).toggle();
        return false;
    };

    this.after('initialize', function () {
        this.on('click', this.click);
    });
});

module.exports = {
    searchButton: searchButton
};
