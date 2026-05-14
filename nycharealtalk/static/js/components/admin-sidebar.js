var _ = require('underscore');
var flight = require('flightjs');
var Spinner = require('spin.js');
var spinnerOptions = _.extend({}, require('../lib/spinner-options'), {
    top: '8px'
});

var emailParticipants = flight.component(function () {
    this.attributes({
        failureContainerSelector: '.email-participants-failure-container',
        formContainerSelector: '.email-participants-form-container',
        formEmailsSelector: '.email-participants-form-emails',
        formOrganizersSelector: '.email-participants-form-organizers',
        formSelector: '.email-participants-form',
        map: null,
        submitButtonSelector: '.email-participants-submit',
        subjectSelector: ':input[name=subject]',
        successContainerSelector: '.email-participants-success-container',
        successEmailsSelector: '.email-participants-success-emails',
        successSubjectSelector: '.email-participants-success-subject',
        successOrganizersSelector: '.email-participants-success-organizers',
        textSelector: ':input[name=text]'
    });

    this.submitDisabled = function () {
        var subject = this.select('subjectSelector').val(),
            text = this.select('textSelector').val();
        return subject === '' || text === '' || this.emailCount === 0;
    };

    this.updateSubmitDisabled = function () {
        this.select('submitButtonSelector').prop('disabled', this.submitDisabled());
    };

    this.updateMailCount = function () {
        var params = this.attr.map.getParamsQueryString({}, {
            bbox: this.attr.map.getBounds().toBBoxString()
        });
        $.getJSON(this.emailOrganizersCountUrl + '?' + params, this.mailCountReceived.bind(this));
    };

    this.mailCountReceived = function (data) {
        this.emailCount = data.emails;
        this.select('formEmailsSelector').text(data.emails);
        this.select('formOrganizersSelector').text(data.organizers);
        this.updateSubmitDisabled();
    };

    this.sendMail = function () {
        var params = this.attr.map.getParamsQueryString({}, {
            bbox: this.attr.map.getBounds().toBBoxString(),
            subject: this.select('subjectSelector').val(),
            text: this.select('textSelector').val()
        });

        var spinner = new Spinner(spinnerOptions)
            .spin(this.select('submitButtonSelector')[0]);

        $.getJSON(this.sendEmailUrl + '?' + params)
            .always(function () {
                spinner.stop();
            })
            .done((function (data) {
                this.select('successEmailsSelector').text(data.emails);
                this.select('successSubjectSelector').text(data.subject);
                this.select('successOrganizersSelector').text(data.organizers);
                this.select('formContainerSelector').hide();
                this.select('successContainerSelector').show();
            }).bind(this))
            .fail((function (data) {
                this.select('formContainerSelector').hide();
                this.select('failureContainerSelector').show();
            }).bind(this));
    };

    this.onSubmit = function (e) {
        // If already disabled, don't send mail
        if (this.select('submitButtonSelector').is('disabled')) {
            return false;
        }
        this.select('submitButtonSelector').prop('disabled', true);
        this.sendMail();
        e.stopPropagation();
        return false;
    };

    this.onKeyUp = function (e) {
        this.updateSubmitDisabled();
    };

    this.onReset = function (e) {
        this.select('subjectSelector').val('');
        this.select('textSelector').val('');
        this.select('formContainerSelector').show();
        this.select('failureContainerSelector').hide();
        this.select('successContainerSelector').hide();
    };

    this.after('initialize', function () {
        this.on('reset', this.onReset.bind(this));
        this.select('submitButtonSelector').on('click', this.onSubmit.bind(this));
        this.select('subjectSelector').on('keyup', this.onKeyUp.bind(this));
        this.select('textSelector').on('keyup', this.onKeyUp.bind(this));
        this.sendEmailUrl = Django.url('lots:lot_email_organizers');
        this.emailOrganizersCountUrl = Django.url('lots:lot_count_organizers');
        this.updateMailCount();

        this.attr.map.on({
            'filterschanged': this.updateMailCount.bind(this),
            'moveend': this.updateMailCount.bind(this),
            'zoomend': this.updateMailCount.bind(this)
        });
    });
});

var adminSection = flight.component(function () {
    this.attributes({
        expandSelector: '.sidebar-section-admin-expand'
    });

    this.expand = function (e) {
        $(document).trigger('sidebarHeaderContentShown', {
            name: 'admin'
        });
        return false;
    };

    this.after('initialize', function () {
        this.select('expandSelector').on('click', this.expand.bind(this));
    });
});

var adminSidebar = flight.component(function () {
    this.attributes({
        emailButton: '.admin-button-email-participants',
        emailContainer: '.email-participants-container',
        expandSelector: '.sidebar-section-admin-expand',
        map: null
    });

    this.enterEmailMode = function (e) {
        this.select('emailContainer').show();
        this.select('emailContainer').trigger('reset');
        return false;
    };

    this.after('initialize', function () {
        this.select('emailButton').on('click', this.enterEmailMode.bind(this));
        emailParticipants.attachTo('.email-participants-container', { map: this.attr.map });
    });
});

module.exports = {
    adminSection: adminSection,
    adminSidebar: adminSidebar
};
