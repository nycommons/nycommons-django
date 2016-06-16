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

module.exports = {
    parse: function () {
        var hash = deparam(window.location.hash.slice(1));
        var parsed = {};
        if (hash.map && hash.map !== '') {
            mapOptions = hash.map.split('/');
            parsed.center = mapOptions.slice(1);
            parsed.zoom = mapOptions[0];
        }
        return parsed;
    },

    update: function (map) {
        var mapParams = map.getZoom() + '/' + numeral(map.getCenter().lat).format('0.0000') + '/' + numeral(map.getCenter().lng).format('0.0000');
        window.location.hash = '#map=' + mapParams;
    }
};
