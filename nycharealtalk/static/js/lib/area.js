var numeral = require('numeral');

var squareFootPerAcre = 43560;

module.exports = {
    formatSquareFeet: function (area) {
        if (!area) return 'unknown area';
        var units = 'sq ft';
        if (area > squareFootPerAcre) {
            area /= squareFootPerAcre;
            units = 'acres';
        }
        return numeral(area).format('0,0.[0]') + ' ' + units;
    }
};
