var _ = require('underscore');
var flight = require('flightjs');
var Handlebars = require('handlebars');
var moment = require('moment');

var activitiesData = require('../data/activities');

Handlebars.registerHelper('formatTimestamp', function (timestamp) {
    timestamp = Handlebars.escapeExpression(timestamp);
    return moment(timestamp).fromNow();
});

function activityMixin () {
    this.attributes({
        contentSelector: '.activity-section',
        expandSelector: '.activity-list-expand',
        listSelector: '.activity-stream ul',
        streamSelector: '.activity-stream'
    });

    this.after('initialize', function () {
        this.template = Handlebars.compile($('#activity-list-template').html());
    });
}

var recentActivity = flight.component(function () {
    this.expand = function (e) {
        e.preventDefault();
        $(document).trigger('sidebarHeaderContentShown', {
            name: 'activities'
        });
        return false;
    };

    this.showFirst = function (e, data) {
        var content = this.template({
            actions: data.activities.slice(0, 1)
        });
        this.select('listSelector').html(content);
    };

    this.after('initialize', function () {
        $(document).on('receivedActivities', this.showFirst.bind(this));
        this.select('expandSelector').on('click', this.expand.bind(this));

        activitiesData.loadActivities();
    });
}, activityMixin);

var activities = flight.component(function () {
    this.collapse = function (e) {
        this.$node.hide();
        $(document).trigger('sidebarHeaderContentHidden', { name: 'activities' });
        return false;
    };

    this.receivedActivities = function (e, data) {
        var content = this.template({
            actions: data.activities
        });
        this.select('listSelector').append(content);
    };

    this.onScroll = function (e) {
        var actionTop = this.$node.find('.action:last-of-type').offset().top;
        var documentHeight = $(document).height();
        if (actionTop - documentHeight < 150) {
            activitiesData.loadNextActivitiesPage();
        }
    };

    this.after('initialize', function () {
        $(document).on('receivedActivities', this.receivedActivities.bind(this));
        this.select('expandSelector').on('click', this.collapse.bind(this));

        this.scrollable = this.select('streamSelector');
        this.scrollable.on('scroll', _.debounce(this.onScroll.bind(this), 200));
    });
}, activityMixin);


/*
 * This component is used on pathway details pages to show recent activity for
 * lots that pathway applies to.
 */
var pathwayRecentActivity = flight.component(function () {
    this.loadNextPage = function () {
        activitiesData.loadPathwayActivities(this.app, this.model, this.id, ++this.page);
    }

    this.receivedActivities = function (e, data) {
        var content = this.template({
            actions: data.activities
        });
        this.select('listSelector').append(content);
    };

    this.after('initialize', function () {
        $(document).on('receivedPathwayActivities', this.receivedActivities.bind(this));
        this.app = this.$node.data('app');
        this.model = this.$node.data('model');
        this.id = this.$node.data('id');
        this.page = 0;
        this.loadNextPage();
    });
}, activityMixin);

module.exports = {
    activities: activities,
    pathwayRecentActivity: pathwayRecentActivity,
    recentActivity: recentActivity
};
