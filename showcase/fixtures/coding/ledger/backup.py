"""Deliberately unsafe code for the security showcase. Never run this file."""

import pickle
import subprocess

from ledger.money import parse_amount


def restore(blob):
    return pickle.loads(blob)  # untrusted bytes -> arbitrary code execution


def archive(name):
    subprocess.run(f"tar czf backups/{name}.tgz data/", shell=True)  # name is user input


def evaluate(expression):
    return eval(expression)  # user-typed formula


def biggest(amounts):
    return max(parse_amount(a) for a in amounts)
