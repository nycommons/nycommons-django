var flight = require('flightjs');
var geocode = require('../lib/geocode').geocode;
var oasis = require('../lib/oasis');

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

var searchForm = flight.component(function () {
    this.attributes({
        querySelector: ':input[type=text]',
        submitSelector: ':input[type=submit]',
        warningSelector: '.warning'
    });

    this.searchResultError = function (e, message) {
        this.select('warningSelector').text(mesage).show();

        // Done searching
        this.select('submitSelector')
            .removeAttr('disabled');
    };

    this.searchResultFound = function (e, data) {
        this.select('submitSelector')
            .removeAttr('disabled');
        $(document).trigger('searchresultfound', data);
    };

    this.addCityAndState = function (query, city, state) {
        if (query.toLowerCase().indexOf(city) <= 0) {
            query += ', ' + city;
        }
        if (query.toLowerCase().indexOf(state) <= 0) {
            query += ', ' + state;
        }
        return query;
    };

    this.searchLotsAndParcels = function (opts) {
        var query = this.select('querySelector').val(),
            url = this.$node.data('lot-search-url') + '?' + $.param({ q: query });
        $.getJSON(url, function (data) {
            if (data.results.length > 0) {
                var result = data.results[0];
                this.$node.trigger('searchresultfound', [{
                    longitude: result.longitude,
                    latitude: result.latitude
                }]);
            }
            else {
                opts.failure();
            }
        });
    };

    this.searchByAddress = function () {
        var bounds = this.$node.data('bounds'),
            city = this.$node.data('city'),
            state = this.$node.data('state'),
            query = this.$node.find('input[type="text"]').val();

        query = this.addCityAndState(query, city, state);
        geocode(query, bounds, state, (function (result, status) {
            // Is result valid?
            if (result === null) {
                this.trigger('searchresulterror', this.$node.data('errorMessage'));
                return;
            }

            // Let the world know!
            var foundLocation = result.geometry.location;
            this.trigger('searchresultfound', [{
                longitude: foundLocation.lng(),
                latitude: foundLocation.lat(),
                query_address: query,
                found_address: result.formatted_address
            }]);
        }).bind(this));
    };

    this.search = function (e) {
        e.preventDefault();
        this.trigger('searchstart');
        this.select('warningSelector').hide();
        this.select('submitSelector')
            .attr('disabled', 'disabled');

        // Search by bbl, lot name, if that turns up nothing then
        // searchByAddress
        this.searchByAddress();
        /*
        this.searchLotsAndParcels({
            failure: function () {
                this.searchByAddress();
            }
        });
        */
        return false;
    };

    this.keypress = function (e) {
        if (e.keyCode === '13') {
            e.preventDefault();
            this.search(e);
        }
    };

    this.after('initialize', function () {
        this.select('querySelector').on('keypress', this.keypress.bind(this));
        this.on('submit', this.search.bind(this));
        this.on('searchresulterror', this.searchResultError.bind(this));
        this.on('searchresultfound', this.searchResultFound.bind(this));
    });
});

var searchBar = flight.component(function () {
    this.attributes({
        map: null
    });

    this.close = function (event) {
        this.$node.hide();
        $('body').removeClass('search-enabled');
        return false;
    };

    this.searchStart = function (event) {
        this.attr.map.removeUserLayer();
    };

    this.searchResultFound = function (event, data) {
        var oasisUrl = oasis.vacantLotsUrl(data.latitude, data.longitude);
        this.attr.map.addUserLayer([data.latitude, data.longitude], {
            popupContent: '<p>This is the point we found when we searched.</p><p>Not seeing a vacant lot here that you expected? Check <a href="' + oasisUrl + '" target="_blank">OASIS in this area</a>. Learn more about using OASIS in our <a href="/faq/#why-isnt-vacant-lot-near-me-map" target="_blank">FAQs</a>.</p>'
        });
    };

    this.after('initialize', function () {
        this.$node.find('.map-search-close').on('click', this.close.bind(this));
        searchForm.attachTo('.map-search-form');
        $(document).on('searchstart', this.searchStart.bind(this));
        $(document).on('searchresultfound', this.searchResultFound.bind(this));
    });
});

module.exports = {
    bar: searchBar,
    button: searchButton
};
