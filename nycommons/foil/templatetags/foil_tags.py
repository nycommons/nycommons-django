from django import template

register = template.Library()


def foil_body(lot):
    return """Dear FOIL Officer,

Please treat this request for all documents in your Agency's possession related to %s Block %s Lot %s as a request under the New York State Freedom of Information Law.

Please send electronic copies of all documents to this email address.

I look forward to hearing from you within five days as required by law.

Best,

ADD YOUR NAME HERE. YOU CAN ALSO ADD MORE DETAILS ABOUT THE DOCUMENTS YOU ARE LOOKING FOR TO THE LETTER ABOVE. REMEMBER TO DELETE THIS LINE BEFORE YOU SEND!""" % (
        lot.borough, lot.block, lot.lot_number
    )


def foil_subject(lot):
    return 'FOIL Request: %s Block %s Lot %s' % (
        lot.borough, lot.block, lot.lot_number
    )

register.filter('foil_body', foil_body)
register.filter('foil_subject', foil_subject)
