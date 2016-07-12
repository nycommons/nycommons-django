function updateOwnerCount (event, data) {
    var url = Django.url('lots:lot_ownership_overview') + '?' + data.map.getParamsQueryString({ bbox: true });
    $.getJSON(url, function (data) {
        // Hide organizing_priority and organizing from the details view
        data.forEach(function (entry) {
            entry['in_details_view'] = (entry.type !== 'organizing_priority' && entry.type !== 'organizing');
        });
        $(document).trigger('receivedOwnerCount', { results: data });
    });
}

module.exports = {
    init: function () {
        $(document).on('updateOwnerCount', updateOwnerCount);
    }
};
