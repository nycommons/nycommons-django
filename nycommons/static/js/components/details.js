var flight = require('flightjs');
var Handlebars = require('handlebars');

var formatSquareFeet = require('../lib/area').formatSquareFeet;

Handlebars.registerHelper('formatArea', function (area) {
    area = Handlebars.escapeExpression(area);
    return formatSquareFeet(area);
});

// Via https://gist.github.com/drmercer/c3e0b2e174718787dac5a181b2be83f6
Handlebars.registerHelper('plural', function(number, text) {
	var singular = number === 1;
	// If no text parameter was given, just return a conditional s.
	if (typeof text !== 'string') return singular ? '' : 's';
	// Split with regex into group1/group2 or group1(group3)
	var match = text.match(/^([^()\/]+)(?:\/(.+))?(?:\((\w+)\))?/);
	// If no match, just append a conditional s.
	if (!match) return text + (singular ? '' : 's');
	// We have a good match, so fire away
	return singular && match[1] // Singular case
		|| match[2] // Plural case: 'bagel/bagels' --> bagels
		|| match[1] + (match[3] || 's'); // Plural case: 'bagel(s)' or 'bagel' --> bagels
});

var details = flight.component(function () {
    this.receivedLotCount = function (event, data) {
        this.$node.find('.details-header-property-count').text(data.count);
    };

    this.receivedOwnerCount = function (event, data) {
        var template = Handlebars.compile($('#details-template').html());
        var content = template({ lottypes: data.results });
        $('.details-body').html(content);

        this.$node.find('.details-toggle-owner-list').on('click', function () {
            $(this).toggleClass('expanded');
            $(this).parents('.details-row').find('.details-owner-list').slideToggle();
            return false;
        });
    };

    this.updatePermalink = function (event) {
        this.$node.find('.details-permalink').attr('href', window.location.href);
    };

    this.after('initialize', function () {
        this.on(document, 'filtersChanged', this.updatePermalink);
        this.on(document, 'mapMoved', this.updatePermalink);
        this.on(document, 'receivedLotCount', this.receivedLotCount);
        this.on(document, 'receivedOwnerCount', this.receivedOwnerCount);
    });
});


module.exports = {
    details: details
};
