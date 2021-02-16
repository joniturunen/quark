import sys
import random
from csv import DictReader


def rules(rule_number=None, file='common/rules_of_acquisition.csv', res='I have not heard of that one..', max_results=126):
    with open(file, 'r') as data_obj:
        fieldnames = ['number', 'rule', 'source']
        reader = DictReader(data_obj, fieldnames=fieldnames, delimiter='|')
        rand = random.randint(0, max_results-1)
        for i, line in enumerate(reader):
            if not rule_number:
                if i == rand:
                    res = '**' + line.get('rule') + '**\n'
                    res += f"> *That is the rule of acquisition number **{line.get('number')}***"
            elif rule_number == int(line.get("number")):
                res = '**' + line.get('rule') + '**\n'
                res += f'> *That is the rule of acquisition number **{rule_number}***'
        return res


if __name__ == '__main__':
    try:
        print(rules(int(sys.argv[1])))
    except:
        print(f'Need int for argument')
