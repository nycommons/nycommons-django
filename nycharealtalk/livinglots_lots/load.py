"""
Helpers for loading lots en masse.

"""
import re


def get_addresses_in_range(address_range):
    """
    For an address with a house number range (eg, '1-9 Main St'), return the
    addresses in that range. Assumes that all of the addresses are on the same
    side of the street and that all of the addresses will be odd or all of the
    addresses will be even.

    With the example input, '1-9 Main St', this should return a tuple:

        ('1 Main St', '3 Main St', '5 Main St', '7 Main St', '9 Main St',)

    If no range is detected, a tuple containing the given address should be
    returned, eg for '8 Main St':

        ('8 Main St',)

    This is relatively naive and will not work with complicated house numbers
    (eg, house numbers that are anything other than integers).

    """
    address_range = address_range.strip()
    m = re.match('^(\d+)\s*-\s*(\d+)\s+(.*)$', address_range)

    # Regex did not match, bail out with the original address
    if not m:
        return (address_range,)

    # Get range components and create addresses
    start = int(m.group(1))
    end = int(m.group(2))
    street = m.group(3)
    return tuple('%d %s' % (n, street) for n in range(start, end + 2, 2))
