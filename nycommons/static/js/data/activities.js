var singleminded = require('../lib/singleminded');

var activities = [];
var page = 0;
var totalPages;

function loadActivities (requestedPage) {
    var pageToLoad = page + 1;
    if (requestedPage) {
        page = requestedPage;
    }
    var baseUrl = Django.url('activity_list');
    singleminded.remember({
        name: 'loadActivities' + pageToLoad,
        jqxhr: $.getJSON(baseUrl, function (data) {
            activities = activities.concat(data.actions);
            page = data.pagination.page;
            totalPages = data.pagination.pages;
            $(document).trigger('receivedActivities', { activities: activities });
        })
    });
}

module.exports = {
    loadActivities: loadActivities
};
