var _ = require('underscore');
var flight = require('flightjs');
var Handlebars = require('handlebars');
var moment = require('moment');
var Spinner = require('spin.js');
var spinnerOptions = _.extend({}, require('../lib/spinner-options'), {
    top: '8px'
});

Handlebars.registerHelper('contentTimestamp', function (timestamp) {
    timestamp = Handlebars.escapeExpression(timestamp);
    return moment(timestamp).format('MMM. D, YYYY, h:mm a');
});

var usercontent = flight.component(function () {
    this.attributes({
        errorSelector: '.usercontent-list-error',
        listContentSelector: '.usercontent-list-content'
    });

    this.loadContent = function (url) {
        this.trigger('usercontent:contentloading');
        $.getJSON(url)
            .done((function (data) {
                this.trigger('usercontent:contentloaded', data);
            }).bind(this))
            .fail((function () {
                this.trigger('usercontent:contenterror');
            }).bind(this));
    };

    this.loadLocalContent = function () {
        if (!this.$node.data('localContentUrl')) {
            return;
        }
        this.loadContent(this.$node.data('localContentUrl'));
    };

    this.onContentError = function (e) {
        if (this.spinner) {
            this.spinner.stop();
            this.spinner = null;
        }
        this.select('errorSelector').show();
    };

    this.onContentLoaded = function (e, data) {
        if (this.spinner) {
            this.spinner.stop();
            this.spinner = null;
        }
        this.content = this.content.concat(data.usercontent);
        this.content = _.sortBy(this.content, function (c) { return c.added; });
        this.content.reverse();

        var list = this.select('listContentSelector');
        list.empty();

        this.content.forEach(function (item) {
            list.append(this.templates[item.type](item));
        }, this);
    };

    this.onContentLoading = function (e) {
        if (this.spinner) return;
        this.spinner = new Spinner(spinnerOptions)
            .spin(this.select('listContentSelector')[0]);
    };

    this.after('initialize', function () {
        this.content = [];
        this.templates = {
            file: Handlebars.compile(this.$node.find('#usercontent-file-template').html()),
            note: Handlebars.compile(this.$node.find('#usercontent-note-template').html()),
            photo: Handlebars.compile(this.$node.find('#usercontent-photo-template').html())
        };

        this.on('usercontent:contenterror', this.onContentError.bind(this));
        this.on('usercontent:contentloaded', this.onContentLoaded.bind(this));
        this.on('usercontent:contentloading', this.onContentLoading.bind(this));

        this.loadLocalContent();
    });
});

module.exports = {
    usercontent: usercontent
};
