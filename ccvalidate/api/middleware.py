import json
import random
from django.urls import reverse
from django.http import JsonResponse

# Min and Max number of digits for a credit card
CC_DIGITS_MIN = 15
CC_DIGITS_MAX = 19

industries = {
    "1": "Airlines (Diners Club enRoute)",
    "2": "Airlines (Diners Club enRoute)",
    "3": "Travel & Entertainment (non-banks such as American Express, "
         "Diner's Club, JCB, and Carte Blanche)",
    "4": "Banking & Financial (Visa, Switch, and Electron)",
    "5": "Banking & Financial (Mastercard and Bankcard)",
    "6": "Merchandising & Finance (Discover Card, Laser, Solo, Switch,"
         " and China UnionPay)",
    "7": "Petroleum",
    "8": "Telecommunications",
    "9": "National Assignment",
    "": "Unknown"
}

issuers = [
    'Visa',
    'Discover',
    'JCB',
    'Diners Club',
    'China UnionPay',
    'Maestro',
    'American Express',
    'MasterCard'
]

issuers_digits = {
    'Visa': "40",
    'Discover': "65",
    'JCB': "35",
    'Diners Club': "36",
    'China UnionPay': "62",
    'Maestro': "56",
    'American Express': "37",
    'MasterCard': "51"
}


def mii_set(card):
    return card[:1]


def mii_details_set(card):
    return industries[card[:1]]


def iin_set(card):
    return card[:6]


def visa(inn):
    if inn[:1] == '4':
        return True
    return False


def mastercard(inn):
    if 51 <= int(inn[:2]) <= 55:
        return True
    return False


def jcb(inn):
    if inn[:2] == '35':
        return True
    return False


def amex(inn):
    if inn[:2] == '37':
        return True
    if inn[:1] == '3':
        return True
    return False


def diners(inn):
    if inn[:2] == '36':
        return True
    if inn[:2] == '38':
        return True
    if inn[:3] == '300':
        return True
    if inn[:3] == '301':
        return True
    if inn[:3] == '302':
        return True
    if inn[:3] == '303':
        return True
    if inn[:3] == '304':
        return True
    if inn[:3] == '305':
        return True
    return False


def china(inn):
    if inn[:2] == '62':
        return True
    return False


def discover(inn):
    if inn[:2] == '65':
        return True
    if inn[:3] == '644':
        return True
    if inn[:4] == '6011':
        return True
    return False


def maestro(inn):
    if inn[:2] == '50':
        return True
    if 56 <= int(inn[:2]) <= 69:
        return True
    return False


def iin_details_set(card):
    for network in issuers:
        if network == 'Visa':
            if visa(card[:6]):
                return network
        if network == 'MasterCard':
            if mastercard(card[:6]):
                return network
        if network == 'Discover':
            if discover(card[:6]):
                return network
        if network == 'JCB':
            if jcb(card[:6]):
                return network
        if network == 'Diners Club':
            if diners(card[:6]):
                return network
        if network == 'China UnionPay':
            if china(card[:6]):
                return network
        if network == 'Maestro':
            if maestro(card[:6]):
                return network
        if network == 'American Express':
            if amex(card[:6]):
                return network
        if network == 'Unknown':
            return network


def pan_set(card):
    pan_end = len(card) - 1
    return card[6:pan_end]


def check_digit_set(card):
    return card[-1:]


def luhn(ccnumber):
    # this function was pretty easy when you use the whole cc number
    # instead of just the personal account number...Doh!
    # mapping of digit doubled and then digits are added together #
    doubled_digits = {
        '0': 0,
        '1': 2,
        '2': 4,
        '3': 6,
        '4': 8,
        '5': 1,
        '6': 3,
        '7': 5,
        '8': 7,
        '9': 9
    }
    card_end = len(ccnumber) - 1
    number_no_check = ccnumber[:card_end]
    check = ccnumber[-1:]
    # Start from right side of digits
    odd_digits = number_no_check[-1::-2]
    even_digits = number_no_check[-2::-2]
    double_sum = 0

    for d in odd_digits:
        double_sum += int(doubled_digits[d])

    sum_digits = double_sum

    for d in even_digits:
        sum_digits += int(d)

    units_digit = sum_digits % 10
    calculated_check = 10 - units_digit

    if units_digit == 0:
        calculated_check = 0

    if calculated_check == int(check):
        return True
    return False


def is_valid_check(card):
    if len(card) < CC_DIGITS_MIN:
        return False
    if len(card) > CC_DIGITS_MAX:
        return False
    if luhn(card):
        return True


def create_check_digit(number_no_check):
    # mapping of digit doubled and then digits are added together
    doubled_digits = {
        '0': 0,
        '1': 2,
        '2': 4,
        '3': 6,
        '4': 8,
        '5': 1,
        '6': 3,
        '7': 5,
        '8': 7,
        '9': 9
    }
    odd_digits = number_no_check[-1::-2]
    even_digits = number_no_check[-2::-2]
    double_sum = 0

    for d in odd_digits:
        double_sum += int(doubled_digits[d])

    sum_digits = double_sum

    for d in even_digits:
        sum_digits += int(d)

    units_digit = sum_digits % 10
    calculated_check = 10 - units_digit

    if units_digit == 0:
        calculated_check = 0

    return str(calculated_check)


class ValidCardMiddleware:
    """This class handles middleware that calculates/populates all
    Creditcard Model fields.  Could have put this in the view classes.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if (request.method == 'POST' and
                (request.path == reverse('create') or
                 request.path == reverse('validate'))):
            # do this if POST and either create or validate request paths
            if request.content_type != 'application/json':
                response = {
                    "Error": "Invalid Request Content-Type.  "
                             "Not application/json"
                }
                status = 400
                return JsonResponse(response, safe=True, status=status)
            data = json.loads(request.body)
            ccnumber = data.get('ccnumber')
            if ccnumber is None:
                response = {"Error": "Invalid ccnumber"}
                status = 400
                return JsonResponse(response, safe=True, status=status)
            if len(ccnumber) < CC_DIGITS_MIN:
                response = {
                    "Error": "Credit card number is not enough digits."
                }
                status = 400
                return JsonResponse(response, safe=True, status=status)
            if len(ccnumber) > CC_DIGITS_MAX:
                response = {
                    "Error": "Credit card number is too many digits."
                }
                status = 400
                return JsonResponse(response, safe=True, status=status)
            if not ccnumber.isdigit():
                response = {
                    "Error": "Credit card number is not only digits."
                }
                status = 400
                return JsonResponse(response, safe=True, status=status)

            mii = mii_set(ccnumber)
            mii_details = mii_details_set(ccnumber)
            iin = iin_set(ccnumber)
            iin_details = iin_details_set(ccnumber)
            pan = pan_set(ccnumber)
            network = iin_details
            check_digit = check_digit_set(ccnumber)
            valid = is_valid_check(ccnumber)
            # Populate request data for body
            data['valid'] = valid
            data['mii'] = mii
            data['mii_details'] = mii_details
            data['iin'] = iin
            data['iin_details'] = iin_details
            data['pan'] = pan
            data['network'] = network
            data['check_digit'] = check_digit

            body = json.dumps(data)
            request._body = body.encode('utf-8')

        if request.method == 'POST' and request.path == reverse('generate'):
            if request.content_type != 'application/json':
                response = {
                    "Error": "Invalid Request Content-Type. "
                             "Not application/json"
                }
                status = 400
                return JsonResponse(response, safe=True, status=status)
            data = json.loads(request.body)
            network = data.get('network')
            if network in issuers_digits:
                # set first two digits for valid card from network
                new_card = issuers_digits[network]
            else:
                response = {
                    "Error": "Invalid network."
                }
                status = 400
                return JsonResponse(response, safe=True, status=status)

            num_digits = 13
            # new_card = str(random.randint(3, 6))
            # new_card = new_card + str(random.randint(0, 9))
            if new_card == '37':
                # set number of digits to a total of 15
                # (including check digit) for Amex
                num_digits = 12
            for x in range(num_digits):
                new_card = new_card + str(random.randint(0, 9))

            check_digit = create_check_digit(new_card)
            ccnumber = new_card + check_digit
            mii = mii_set(ccnumber)
            mii_details = mii_details_set(ccnumber)
            iin = iin_set(ccnumber)
            iin_details = iin_details_set(ccnumber)
            pan = pan_set(ccnumber)
            network = iin_details
            valid = is_valid_check(ccnumber)
            data = {
                "ccnumber": ccnumber, "valid": valid, 'mii': mii,
                'mii_details': mii_details, 'iin': iin,
                'iin_details': iin_details, 'pan': pan,
                'network': network, 'check_digit': check_digit
            }
            body = json.dumps(data)
            request._body = body.encode('utf-8')

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
