var singleminded = require('../lib/singleminded');

function updateLotCount (event, data) {
    var url = Django.url('lots:lot_count') + '?' + data.map.getParamsQueryString({ bbox: true });
    singleminded.remember({
        name: 'updateLotCount',
        jqxhr: $.getJSON(url, function (data) {
            var count = data['lots-count'];
            $(document).trigger('receivedLotCount', { count: count });
        })
    });
};

module.exports = {
    init: function () {
        $(document).on('updateLotCount', updateLotCount);
    }
};
