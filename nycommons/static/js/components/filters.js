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
    commonsTypes: 'commons_type',
    'priority-organizing': 'priority_organizing'
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

    this.handleReset = function () {
        this.$node.prop('checked', true);
        if (this.type === 'layer') {
            this.toggleLayerOwners();
        }
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
        var $filterItem = this.$node.parents('.filters-list-item');
        if (this.isChecked()) {
            // Check all the owners for this layer
            this.findLayerOwners().each(function () {
                $(this).prop('checked', true);
            });
            $filterItem.removeClass('collapse');
        }
        else {
            $filterItem.addClass('collapse');
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
        this.attr.filterList.on('filtersReset', this.handleReset.bind(this));
    });
});

var filterCollapseButton = flight.component(function () {
    this.onClick = function (e) {
        this.$filterItem.toggleClass('collapse');
    };

    this.after('initialize', function () {
        this.$filterItem = this.$node.parents('.filters-list-item');
        this.on('click', this.onClick.bind(this));
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

    this.handleReset = function () {
        this.$node.val('');
        var details = {
            name: this.name,
            type: this.type,
            value: null
        };
        $(document).trigger('boundaryChanged', details);
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
        this.attr.filterList.on('filtersReset', this.handleReset.bind(this));
    });
});

var priorityFilter = flight.component(function () {
    this.attributes({
        filterList: null
    });

    this.handleChange = function () {
        var checked = this.$node.is(':checked');

        // If priority & organizing, clear others
        if (this.name === 'priority-organizing' && checked) {
            $('.filter-priority-organizing-list .filter[id!="' + this.name + '"]').prop('checked', false);
        }

        var details = {
            name: this.name,
            type: this.type,
            value: checked
        };
        this.attr.filterList.trigger('filterChanged', details);
        return false;
    };

    this.handleReset = function () {
        this.$node.prop('checked', false);
    };

    this.after('initialize', function () {
        this.name = this.$node.attr('id');
        this.type = 'priority-organizing';

        // Check initial filters and set this input as appropriate
        var initialFilters = this.attr.filterList.attr.initialFilters;
        if (initialFilters[this.name]) {
            this.$node.prop('checked', true);
            this.handleChange();
        }
        this.on('change', this.handleChange);
        this.attr.filterList.on('filtersReset', this.handleReset.bind(this));
    });
});

var resetButton = flight.component(function () {
    this.attributes({
        filterList: null
    });

    this.handleClick = function () {
        this.attr.filterList.trigger('filtersReset');
        return false;
    };

    this.after('initialize', function () {
        this.on('click', this.handleClick);
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
        var filters = {};

        // Get layers
        var $selectedLayers = this.$node.find('.filter[data-type=layer]:checked');
        filters.layers = $selectedLayers.map(function () {
            return $(this).attr('name');
        }).get();

        // Get owners
        filters.owners = {};
        $selectedLayers.each(function () {
            var name = $(this).attr('name'),
                $selectedOwners = $(this).parent().find('.filter[data-type=owner]:checked');
            filters.owners[name] = $selectedOwners.map(function () {
                return $(this).data('owner-pk');
            }).get();
        });

        this.$node.find('.filter-priority-organizing-list .filter:checked').each(function () {
            filters[$(this).attr('id')] = true;
        });

        // Get boundaries
        filters.boundaries = {};
        var $selectedBoundary = this.$node.find('.filter-boundaries option:selected[value!=""]');
        if ($selectedBoundary.length) {
            filters.boundaries = {
                layer: $selectedBoundary.parent().data('layer'),
                value: $selectedBoundary.val()
            };
        }

        return filters;
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
        priorityFilter.attachTo(this.$node.find('.filter-priority-organizing-list :input'), {
            filterList: this
        });
        resetButton.attachTo(this.$node.find('.reset'), {
            filterList: this
        });
        filterCollapseButton.attachTo(this.$node.find('.filter-layer-collapse'));

        // Set off filterChanged with current state of filters
        this.handleFilterChanged();

        this.on('filterChanged', this.handleFilterChanged);
        this.on('filtersReset', this.handleFilterChanged);
    });
});

module.exports = {
    filters: filters,

    lotShouldAppear: function (lot, filters, boundariesLayer) {
        // Should a lot show up on the map?
        //
        // The filters UI is split into four categories:
        //  * boundaries
        //  * priority / organizing
        //  * ownership
        //  * layers / categories
        //
        // We follow these three categories to find a reason to exclude a lot.
        // If a lot fails for any of the three categories, it fails for all and
        // is not shown.

        /*
         * Priority / organizing
         */
        if (filters.priority || filters['priority-organizing']) {
            if (!lot.feature.properties.priority) {
                return false;
            }
        }
        if (filters.organizing || filters['priority-organizing']) {
            if (!lot.feature.properties.organizing) {
                return false;
            }
        }

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

        // Add priority / organizing
        $('.filter-priority-organizing-list .filter:checked').each(function () {
            filters[$(this).attr('id')] = true;
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
