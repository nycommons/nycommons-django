//
// sidebar.js
//
// Sidebar for map
//


$(document).ready(function () {
    $('.filter-button').click(function () {
        $('.map-header-content-default').hide();
        $('.map-legend').hide();
        $('.map-header-content-filters').show();
        return false;
    });

    $('.map-header-content-filters .close').click(function () {
        $('.map-header-content-filters').hide();
        $('.map-header-content-default').show();
        $('.map-legend').show();
        return false;
    });
});
