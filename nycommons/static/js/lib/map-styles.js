//
// Lot map styles by layer for maps
//
var _ = require('underscore');

var fillColors = {
    library: '#00AEEF',
    nycha: '#F5A623',
    post_office: '#662D91',
    default: '#000000',
    in_use: '#e64c9b',
    private: '#b4d0d1',
    public: '#1f9e48',
    gutterspace: '#1f9e48'
};

module.exports = {
    fillColors: fillColors,

    getLayerColor: function (layers) {
        if (_.contains(layers, 'library')) {
            return fillColors.library;
        }
        if (_.contains(layers, 'NYCHA')) {
            return fillColors.nycha;
        }
        if (_.contains(layers, 'post office')) {
            return fillColors.post_office;
        }
        if (_.contains(layers, 'in_use')) {
            return fillColors.in_use;
        }
        if (_.contains(layers, 'public')) {
            return fillColors.public;
        }
        if (_.contains(layers, 'private')) {
            return fillColors.private;
        }
        if (_.contains(layers, 'gutterspace')) {
            return fillColors.gutterspace;
        }
        return fillColors.default;
    }
};
