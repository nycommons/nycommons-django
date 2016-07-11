var flight = require('flightjs');
var Handlebars = require('handlebars');
var moment = require('moment');

var loadActivities = require('../data/activities').loadActivities;

Handlebars.registerHelper('formatTimestamp', function (timestamp) {
    timestamp = Handlebars.escapeExpression(timestamp);
    return moment(timestamp).fromNow();
});

var recentActivity = flight.component(function () {
    this.attributes({
        contentSelector: '.activity-section',
        expandSelector: '.activity-list-expand',
        streamSelector: '.activity-stream'
    });

    this.expand = function (e) {
        e.preventDefault();
        console.log('expand');
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
        this.template = Handlebars.compile($('#activity-list-template').html());

        $(document).on('receivedActivities', this.showFirst.bind(this));
        this.select('expandSelector').on('click', this.expand.bind(this));

        loadActivities();
    });
});

module.exports = {
    recentActivity: recentActivity
};
