//
// Lot map styles by layer for maps
//

var fillColors = {
    library: '#00AEEF',
    'public housing': '#F5A623',
    'post office': '#662D91',
    default: '#000000'
};

function getLayerColor (layer) {
    if (fillColors[layer] !== undefined) {
        return fillColors[layer];
    }
    return fillColors.default;
}

module.exports = {
    fillColors: fillColors,

    getLayerColor: getLayerColor,

    getStyle: function (feature) {
        var style = {
            fillColor: '#000000',
            fillOpacity: 1,
            stroke: 0
        };
        style.fillColor = getLayerColor(feature.properties.commons_type);
        return style;
    }
};
