//
// sidebar.js
//
// Sidebar for map
//


$(document).ready(function () {
    $('.filter-button').click(function () {
        $('.map-header-content-default').hide();
        $('.map-header-content-filters').show();
        return false;
    });
});
