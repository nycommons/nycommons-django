//
// Lot map styles by layer for maps
//

var fillColors = {
    library: '#057FC6',
    park: '#4def3e',
    'public housing': '#F5A623',
    'post office': '#662D91',
    'vacant lot / garden': '#1F9E48',
    waterfront: '#E669EE',
    default: '#000000'
};

var priorityColor = '#bf1e2d';

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
            stroke: false
        };
        style.fillColor = getLayerColor(feature.properties.commons_type);

        if (feature.properties.priority) {
            style.color = priorityColor;
            style.stroke = true;
        }
        return style;
    }
};
