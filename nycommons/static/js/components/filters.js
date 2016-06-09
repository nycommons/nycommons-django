//
// filters.js
//
// Map filters
//
var _ = require('underscore');
var flight = require('flightjs');
var turf = {};
turf.inside = require('turf-inside');
turf.point = require('turf-point');


var defaultFilters = {
    layers: ['organizing', 'in_use', 'no_people', 'in_use_started_here'],
    ownerTypes: ['private_opt_in', 'public'],
    parents_only: true
};


var renamedFilters = {
    ownerTypes: 'owner_types',
    privateOwnerPks: 'private_owners',
    publicOwnerPks: 'public_owners'
};


function normalizeFilters(filters) {
    // Normalize filters that are arrays
    _.each(['layers', 'ownerTypes', 'privateOwnerPks', 'publicOwnerPks'], function (key) {
        if (filters[key]) {
            filters[key] = filters[key].join(',');
        }
    });

    // Rename filters for url
    _.each(renamedFilters, function (newName, oldName) {
        if (filters[oldName] !== undefined) {
            filters[newName] = filters[oldName];
            delete filters[oldName];
        }
    });

    // Handle boundary
    if (filters.boundaryLayer && filters.boundaryPk) {
        filters.boundary = filters.boundaryLayer + '::' + filters.boundaryPk;
        delete filters.boundaryPk;
        delete filters.boundaryLayer;
    }
    return filters;
}


function toParams(filters) {
    return normalizeFilters(_.extend({}, defaultFilters, filters));
}



// An individual filter (eg a checkbox)
var filter = flight.component(function () {
    this.attributes({
        filterList: null
    });

    this.handleChange = function (event) {
        this.attr.filterList.trigger('filterChanged', {
            name: this.name,
            type: this.type,
            value: this.$node.prop('checked')
        });
    };

    this.after('initialize', function () {
        this.name = this.$node.attr('name');
        this.type = this.$node.data('type');
        this.on('change', this.handleChange);
    });
});

// A group of filters, should be one per page
var filters = flight.component(function () {
    this.handleFilterChanged = function (event, data) {
        $(document).trigger('filtersChanged', {
            filters: this.aggregateFilters()
        });
    };

    this.aggregateFilters = function () {
        var layers = this.$node.find('.filter[data-type=layer]:checked').map(function () {
            return $(this).attr('name');
        });
        return {
            layers: layers
        }
    };

    this.currentFilters = function () {
        return this.aggregateFilters();
    };

    this.after('initialize', function () {
        filter.attachTo(this.$node.find('.filter'), {
            filterList: this
        });

        // Set off filterChanged with current state of filters
        this.handleFilterChanged();

        this.on('filterChanged', this.handleFilterChanged);
    });
});

module.exports = {
    filters: filters,

    lotShouldAppear: function (lot, filters, boundariesLayer) {
        // Should a lot show up on the map?
        //
        // The filters UI is split into three categories:
        //  * boundaries
        //  * ownership
        //  * layers / categories
        //
        // We follow these three categories to find a reason to exclude a lot.
        // If a lot fails for any of the three categories, it fails for all and
        // is not shown.
        var layer = lot.feature.properties.commons_type;
        if (!_.contains(filters.layers, layer)) {
            return false;
        }

        /*
         * Boundaries
         */

        // Look at current boundary, hide anything not in it
        /*
        if (boundariesLayer.getLayers().length > 0) {
            var centroid = lot.getBounds().getCenter(),
                point = turf.point([centroid.lng, centroid.lat]),
                polygon = boundariesLayer.getLayers()[0].toGeoJSON();
            if (!turf.inside(point, polygon)) {
                return false;
            }
        }
        */

        return true;
    },

    paramsToFilters: function (params) {
        var filters = _.extend({}, params);
        //filters.layers = filters.layers.split(',');
        //filters.owner_types = filters.owner_types.split(',');
        if (filters.public_owners) {
            filters.public_owners = _.map(filters.public_owners.split(','), function (ownerPk) {
                return parseInt(ownerPk);
            });
        }
        if (filters.private_owners) {
            filters.private_owners = _.map(filters.private_owners.split(','), function (ownerPk) {
                return parseInt(ownerPk);
            });
        }
        return filters;
    },

    // Take the current state of the map and filters to create params suitable
    // for requests (eg counts)
    filtersToParams: function (map, options) {
        /*
        var filters = {
            publicOwnerPks: $('.filter-owner-public').val().split(','),
            privateOwnerPks: $('.filter-owner-private').val().split(',')
        };
        filters.layers = _.map($('.filter-layer:checked'), function (layer) {
            return $(layer).attr('name'); 
        });
        filters.ownerTypes = _.map($('.filter-owner-type:checked'), function (ownerType) {
            return $(ownerType).attr('name'); 
        });

        // Add boundary, if any
        $.each($('.filter-boundaries'), function () {
            if ($(this).val() !== '') {
                filters.boundaryLayer = $(this).data('layer');
                filters.boundaryPk = $(this).val();
            }
        });

        var params = toParams(filters);

        // Add BBOX if requested
        if (options && options.bbox) {
            params.bbox = map.getBounds().toBBoxString();
        }

        return params;
        */
        return {};
    },

    toParams: toParams
};
