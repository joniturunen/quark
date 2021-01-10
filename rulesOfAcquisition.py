import sys
from csv import DictReader


def getRuleOfAcquisition(rule_number):
    file = 'common/rules_of_acquisition.csv'

    with open(file) as f:
        fieldnames = ['no', 'rule', 'episode']
        reader = DictReader(f, fieldnames=fieldnames, delimiter='|')
        data = [row for row in reader]

    return data[rule_number-1]


if __name__ == '__main__':
    if len(sys.argv) > 1:
        rule_number = int(sys.argv[1])
    else:
        print(f'\nRequire one cli argument (int) for rule number\n')
        raise Exception()
    print(dict(getRuleOfAcquisition(rule_number)))
