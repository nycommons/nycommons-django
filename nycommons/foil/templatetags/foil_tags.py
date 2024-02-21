from django import template

register = template.Library()


def _block_and_lot_number(lot):
    """
    Get block and lot number for lot. If it is a group, join them logically.
    """
    if lot.block and lot.lot_number:
        return 'Block %d Lot %d' % (lot.block, lot.lot_number)
    else:
        blocks = list(set([l.block for l in lot.lots if l.block]))
        block_strs = []
        for block in sorted(blocks):
            if not block:
                continue
            block_lots = [l for l in lot.lots if l.block == block]
            block_strs.append('Block %d %s' % (
                block,
                '%s %s' % (
                    'Lot' if len(block_lots) == 1 else 'Lots',
                    ', '.join(sorted([str(l.lot_number) for l in
                                      block_lots])),
                )
            ))
        return '; '.join(block_strs)


def foil_body(lot):
    return """Dear FOIL Officer,

Please treat this request for all documents in your Agency's possession related to %s %s as a request under the New York State Freedom of Information Law.

Please send electronic copies of all documents to this email address.

I look forward to hearing from you within five days as required by law.

Best,

ADD YOUR NAME HERE. YOU CAN ALSO ADD MORE DETAILS ABOUT THE DOCUMENTS YOU ARE LOOKING FOR TO THE LETTER ABOVE. REMEMBER TO DELETE THIS LINE BEFORE YOU SEND!""" % (
        lot.borough, _block_and_lot_number(lot)
    )


def foil_subject(lot):
    return 'FOIL Request: %s %s' % (
        lot.borough, _block_and_lot_number(lot)
    )


register.filter('foil_body', foil_body)
register.filter('foil_subject', foil_subject)
