var flight = require('flightjs');
var Handlebars = require('handlebars');
var moment = require('moment');

Handlebars.registerHelper('formatTimestamp', function (timestamp) {
    timestamp = Handlebars.escapeExpression(timestamp);
    return moment(timestamp).fromNow();
});

var activities = flight.component(function () {
    this.attributes({
        streamSelector: '.activity-stream'
    });

    this.showFirst = function () {
        $.getJSON(this.baseUrl)
            .done((function (data) {
                this.actions = data.actions;
                this.currentPage = data.pagination.page;
                this.totalPages = data.pagination.pages;
                var content = this.template({
                    actions: this.actions.slice(0, 1)
                });
                this.select('streamSelector').html(content);
            }).bind(this));
    };

    this.after('initialize', function () {
        this.template = Handlebars.compile($('#activity-list-template').html());
        this.baseUrl = Django.url('activity_list');

        this.showFirst();
    });
});

module.exports = {
    activities: activities
};
