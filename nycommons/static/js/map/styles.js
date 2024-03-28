//
// Lot map styles by layer for maps
//

var fillColors = [
    {
        keys: ['demolition_proposed', 'demolition_completed'],
        color: '#000000',
    },
    {
        keys: ['radpact_converted', 'radpact_planned'],
        color: '#057FC6',
    },
    {
        keys: ['preservation_trust_voting_planned', 'preservation_trust_complete'],
        color: '#662D91',
    },
    {
        keys: ['private_infill_planned', 'private_infill_completed'],
        color: '#00C3FF',
    },
    {
        keys: ['section_8_pre_2014'],
        color: '#F66557',
    },
    {
        keys: ['new_public_housing_built', 'new_public_housing_planned'],
        color: '#4DEF3E',
    },
    {
        keys: ['nycha_modernization_planned', 'nycha_modernization_complete'],
        color: '#E669EE',
    },
];

var defaultFill = '#F5A623';

var priorityColor = '#bf1e2d';

function getLayerColor(props) {
    var matches = fillColors.filter(function (e) {
        return e.keys.filter(function (k) {
            return props[k];
        }).length > 0;
    });

    if (matches.length > 0) {
        return matches[0].color;
    }

    return defaultFill;
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
        style.fillColor = getLayerColor(feature.properties);

        if (feature.properties.priority) {
            style.color = priorityColor;
            style.stroke = true;
            style.weight = 1;
        }
        return style;
    }
};
