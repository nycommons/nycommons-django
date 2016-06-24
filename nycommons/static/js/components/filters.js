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
    parents_only: true
};

var renamedFilters = {
    commonsTypes: 'commons_type'
};

function normalizeFilters(filters) {
    // Normalize filters that are arrays
    _.each(['layers'], function (key) {
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
        if (this.type === 'layer') {
            this.toggleLayerOwners();
        }
        this.attr.filterList.trigger('filterChanged', {
            name: this.name,
            type: this.type,
            value: this.isChecked()
        });
    };

    this.isChecked = function () {
        return this.$node.prop('checked');
    };

    this.findLayerOwners = function () {
        return this.$node.parent().parent().parent().find('.filter-owner');
    };

    this.findParentLayer = function () {
        return this.$node.parent().parent().parent().find('.filter-layer');
    };

    this.toggleLayerOwners = function () {
        var $layerOwners = this.$node.parent().find('.filter-owners-list');
        if (this.isChecked()) {
            // Check all the owners for this layer
            this.findLayerOwners().each(function () {
                $(this).prop('checked', true);
            });
            $layerOwners.show();
        }
        else {
            $layerOwners.hide();
        }
    };

    this.after('initialize', function () {
        this.name = this.$node.attr('name');
        this.type = this.$node.data('type');

        var initialFilters = this.attr.filterList.attr.initialFilters;
        if (this.type === 'layer') {
            if (initialFilters.layers) {
                this.$node.prop('checked', _.contains(initialFilters.layers, this.name));
            }
        }
        else if (this.type === 'owner') {
            if (initialFilters.owners) {
                var layer = this.findParentLayer().attr('name');
                var pk = this.$node.data('owner-pk');
                var checked = false;
                if (initialFilters.owners[layer] && _.contains(initialFilters.owners[layer], pk)) {
                    checked = true;
                }
                this.$node.prop('checked', checked);
            }
        }

        if (this.type === 'layer') {
            this.toggleLayerOwners();
        }
        this.on('change', this.handleChange);
    });
});

var boundaryFilter = flight.component(function () {
    this.attributes({
        filterList: null
    });

    this.handleChange = function () {
        // Clear all other boundaries selects
        var layer = this.name;
        $('.filter-boundaries[data-layer!="' + layer + '"]').val('');

        var details = {
            name: this.name,
            type: this.type,
            value: this.$node.find('option:selected').val()
        };
        this.attr.filterList.trigger('filterChanged', details);
        $(document).trigger('boundaryChanged', details);
        return false;
    };

    this.after('initialize', function () {
        this.name = this.$node.data('layer');
        this.type = 'boundary';

        // Check initial filters and set this input as appropriate
        var initialFilters = this.attr.filterList.attr.initialFilters;
        if (initialFilters.boundaries && initialFilters.boundaries.layer === this.name) {
            this.$node.val(initialFilters.boundaries.value);
            this.handleChange();
        }
        this.on('change', this.handleChange);
    });
});

// A group of filters, should be one per page
var filters = flight.component(function () {
    this.attributes({
        initialFilters: null
    });

    this.handleFilterChanged = function (event, data) {
        $(document).trigger('filtersChanged', {
            filters: this.aggregateFilters()
        });
    };

    this.aggregateFilters = function () {
        // Get layers
        var $selectedLayers = this.$node.find('.filter[data-type=layer]:checked');
        var layers = $selectedLayers.map(function () {
            return $(this).attr('name');
        }).get();

        // Get owners
        var owners = {};
        $selectedLayers.each(function () {
            var name = $(this).attr('name'),
                $selectedOwners = $(this).parent().find('.filter[data-type=owner]:checked');
            owners[name] = $selectedOwners.map(function () {
                return $(this).data('owner-pk');
            }).get();
        });

        // Get boundaries
        var boundaries = {};
        var $selectedBoundary = this.$node.find('.filter-boundaries option:selected[value!=""]');
        if ($selectedBoundary.length) {
            boundaries = {
                layer: $selectedBoundary.parent().data('layer'),
                value: $selectedBoundary.val()
            };
        }

        return {
            boundaries: boundaries,
            layers: layers,
            owners: owners
        }
    };

    this.currentFilters = function () {
        return this.aggregateFilters();
    };

    this.after('initialize', function () {
        filter.attachTo(this.$node.find('.filter'), {
            filterList: this
        });
        boundaryFilter.attachTo(this.$node.find('.filter-boundaries'), {
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

        /*
         * Layers
         */
        var layer = lot.feature.properties.commons_type;
        if (!_.contains(filters.layers, layer)) {
            return false;
        }

        /*
         * Owners
         */
        var ownerId = lot.feature.properties.owner_id;
        if (!_.contains(filters.owners[layer], ownerId)) {
            return false;
        }

        /*
         * Boundaries
         */
        if (boundariesLayer && boundariesLayer.getLayers().length > 0) {
            var centroid;
            try {
                centroid = lot.getBounds().getCenter();
            }
            catch (e) {
                centroid = lot.getLatLng();
            }
            var point = turf.point([centroid.lng, centroid.lat]),
                polygon = boundariesLayer.getLayers()[0].toGeoJSON();
            if (!turf.inside(point, polygon)) {
                return false;
            }
        }

        return true;
    },

    // Take the current state of the map and filters to create params suitable
    // for backend requests (eg counts). These will be different from permalink
    // URL params.
    filtersToParams: function (map, options) {
        var filters = {};
        filters.commonsTypes = _.map($('.filter-layer:checked'), function (layer) {
            return $(layer).attr('name');
        }).join();

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
    },

    toParams: toParams
};
