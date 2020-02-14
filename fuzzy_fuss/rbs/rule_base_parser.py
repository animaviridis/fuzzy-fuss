from fuzzy_fuss.rbs.rule import Rule, Measurement
from fuzzy_fuss.rbs.parsed_object import ParsedObjDict
from fuzzy_fuss.rbs.variable import ParsedVariable


class RuleBase(object):
    def __init__(self):
        self.rules = ParsedObjDict(Rule)
        self.variables = {}
        self.measurements = ParsedObjDict(Measurement, float)
        self.name = None
        self._current_name = None

    def __repr__(self):
        v = self.variables
        return f"Rule base '{self.name}' with {len(v)} variables ({', '.join(v.keys())}) and {len(self.rules)} rules"

    def parse(self, filename):
        self.name = None
        self.variables[None] = ParsedVariable(None)

        with open(filename) as f:
            for line in f:
                line = line.strip('\n')
                if not line:
                    continue

                if self.rules.parse(line) or self.measurements.parse(line) \
                        or self.variables[self._current_name].parse(line):
                    continue

                if not self.name:
                    self.name = line
                else:
                    self.variables[line] = ParsedVariable(line)
                    self._current_name = line

        if len(self.variables[None]):
            raise RuntimeError(f"Encountered 4-tuples for unspecified variables: {dict(self.variables[None].items())}")
        self.variables.pop(None)

        self._current_name = None
