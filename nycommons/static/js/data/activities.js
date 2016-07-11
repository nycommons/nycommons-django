var singleminded = require('../lib/singleminded');

var activities = [];
var page = 0;
var totalPages;

function loadActivities (requestedPage) {
    var pageToLoad = page + 1;
    if (requestedPage) {
        pageToLoad = requestedPage;
    }
    var baseUrl = Django.url('activity_list');
    singleminded.remember({
        name: 'loadActivities' + pageToLoad,
        jqxhr: $.getJSON(baseUrl + '?page=' + pageToLoad, function (data) {
            activities = activities.concat(data.actions);
            page = data.pagination.page;
            totalPages = data.pagination.pages;
            $(document).trigger('receivedActivities', { activities: data.actions });
        })
    });
}

function loadNextActivitiesPage () {
    if (page && totalPages && page < totalPages) {
        loadActivities(page + 1);
    }
}

module.exports = {
    loadActivities: loadActivities,
    loadNextActivitiesPage: loadNextActivitiesPage
};
