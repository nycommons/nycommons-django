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

function loadPathwayActivities (app, model, id, requestedPage) {
    var url = Django.url('pathway_activity_list') + '?' + $.param({
        app: app,
        model: model,
        id: id,
        page: requestedPage
    });
    singleminded.remember({
        name: 'loadPathwayActivities' + requestedPage,
        jqxhr: $.getJSON(url, function (data) {
            $(document).trigger('receivedPathwayActivities', { activities: data.actions });
        })
    });
}

module.exports = {
    loadActivities: loadActivities,
    loadNextActivitiesPage: loadNextActivitiesPage,

    loadPathwayActivities: loadPathwayActivities
};
