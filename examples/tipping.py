import os

from fuzzy_fuss.rbs.rule_base_parser import RuleBase

rb = RuleBase()
rb.parse(os.path.join(os.path.dirname(__file__), "tipping_rulebase.txt"))

# plot the parsed variables
for fv in rb.variables.values():
    fv.plot_range(margin=10)