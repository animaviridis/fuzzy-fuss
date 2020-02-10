import re

from fuzzy_fuss.rbs.rule import Rule


class RuleBaseParser(object):
    RULE_PATTERN = r"(?P<name>Rule\s*\d+):{0,1} if (?P<propositions>.+) then (?P<conclusion>.+)"
    ATOM_PATTERN = r"(?P<variable>\w+) (?:is|will be) (?P<value>\w+)"

    def __init__(self):
        self._rules = dict()
        self._variables = dict()
        self._measurements = dict()

    @staticmethod
    def match_rule(line):
        line = line.replace('the ', '')

        m = re.fullmatch(RuleBaseParser.RULE_PATTERN, line, re.IGNORECASE)
        if not m:
            return

        md = m.groupdict()
        prop = re.findall(RuleBaseParser.ATOM_PATTERN, md['propositions'], re.IGNORECASE)
        connectives = [s.strip(' ') for s in re.findall(r" and | or ", md['propositions'])]
        conclusion = re.fullmatch(RuleBaseParser.ATOM_PATTERN, md['conclusion']).groups()

        rule = Rule(name=md['name'], prop_atoms=prop, prop_connectives=connectives, conclusion=conclusion)
        return rule


if __name__ == '__main__':
    rl = r"Rule 1 If the driving is good and the journey_time is short then the tip will be big"
    match = RuleBaseParser.match_rule(rl)
    print(match or 'no match')