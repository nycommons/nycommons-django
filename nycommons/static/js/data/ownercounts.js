function updateOwnerCount (event, data) {
    var url = Django.url('lots:lot_ownership_overview') + '?' + data.map.getParamsQueryString({ bbox: true });
    $.getJSON(url, function (data) {
        $(document).trigger('receivedOwnerCount', { results: data });
    });
}

module.exports = {
    init: function () {
        $(document).on('updateOwnerCount', updateOwnerCount);
    }
};
