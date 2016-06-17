var numeral = require('numeral');

function deparam(s) {
    var vars = {},
        param,
        params = s.split('&');
    for(var i = 0; i < params.length; i++) {
        param = params[i].split('=');
        vars[param[0]] = decodeURIComponent(param[1]);
    }
    return vars;
}

function param(obj) {
    var parts = Object.keys(obj).map(function (key) {
        return [key, JSON.stringify(obj[key])].join('=');
    });
    return parts.join('&');
}

module.exports = {
    parse: function () {
        var hashStr = window.location.hash.slice(1);
        if (!hashStr || hashStr.length === 0) return {};

        var hash = deparam(hashStr);
        var parsed = {};
        if (hash.map && hash.map !== '') {
            mapOptions = hash.map.split('/');
            parsed.center = mapOptions.slice(1);
            parsed.zoom = mapOptions[0];
        }
        Object.keys(hash).forEach(function (key) {
            if (key === 'map' || hash[key] === undefined) return;
            if (!parsed.filters) {
                parsed.filters = {};
            }
            parsed.filters[key] = JSON.parse(hash[key]);
        });
        return parsed;
    },

    update: function (map) {
        var mapParams = map.getZoom() + '/' + numeral(map.getCenter().lat).format('0.0000') + '/' + numeral(map.getCenter().lng).format('0.0000');
        window.location.hash = '#map=' + mapParams + '&' + param(map.currentFilters);
    }
};
