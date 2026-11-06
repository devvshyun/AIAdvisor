# Deliberately messy formatting: the hooks showcase checks that a formatter hook cleans it up.
from ledger.money import parse_amount,total
def monthly(lines ):
    rows=[l.split(" ") for l in lines if l.strip()]
    return {r[0] :parse_amount(r[1]) for r in rows}
def grand_total(lines): return total([l.split(" ")[1] for l in lines if l.strip()])
