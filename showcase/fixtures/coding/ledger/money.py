"""Amounts like '9,500원' and how they are summed."""


def parse_amount(text):
    return int(text.replace(",", "").replace("원", ""))


def total(amounts):
    return sum(parse_amount(a) for a in amounts)
