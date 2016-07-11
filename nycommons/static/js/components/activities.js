var flight = require('flightjs');
var Handlebars = require('handlebars');
var moment = require('moment');

var loadActivities = require('../data/activities').loadActivities;

Handlebars.registerHelper('formatTimestamp', function (timestamp) {
    timestamp = Handlebars.escapeExpression(timestamp);
    return moment(timestamp).fromNow();
});

function activityMixin () {
    this.attributes({
        contentSelector: '.activity-section',
        expandSelector: '.activity-list-expand',
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
        this.select('streamSelector').html(content);
    };

    this.after('initialize', function () {
        $(document).on('receivedActivities', this.showFirst.bind(this));
        this.select('expandSelector').on('click', this.expand.bind(this));

        loadActivities();
    });
}, activityMixin);

var activities = flight.component(function () {
    this.collapse = function (e) {
        this.$node.hide();
        $(document).trigger('sidebarHeaderContentHidden');
        return false;
    };

    this.receivedActivities = function (e, data) {
        var content = this.template({
            actions: data.activities
        });
        this.select('streamSelector').html(content);
    };

    this.after('initialize', function () {
        $(document).on('receivedActivities', this.receivedActivities.bind(this));
        this.select('expandSelector').on('click', this.collapse.bind(this));
    });
}, activityMixin);

module.exports = {
    activities: activities,
    recentActivity: recentActivity
};
