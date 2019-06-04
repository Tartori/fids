class InvestigatorConfig:
    def __init__(self, config):
        keys = config.keys()
        self._add_default_rules()
        self._parse_rules(config['rules'] if 'rules' in keys else None)
        self.same_config = config['same_config'] if 'same_config' in keys else True
        self.greater = config['greater'] if 'greater' in keys else []
        self.equal = config['equal'] if 'equal' in keys else []

    def _add_default_rules(self):
        self.rules = []
        self.rules.append(RuleConfig(name='p', equal=['meta_mode']))
        self.rules.append(RuleConfig(name='ftype', equal=['meta_conten']))
        self.rules.append(RuleConfig(name='i', equal=['meta_addr']))
        self.rules.append(RuleConfig(name='l', equal=['meta_link']))
        self.rules.append(RuleConfig(name='n', equal=['meta_nlink']))
        self.rules.append(RuleConfig(name='u', equal=['']))
        self.rules.append(RuleConfig(name='g', equal=['meta_gid']))
        self.rules.append(RuleConfig(name='s', equal=['meta_size']))
        self.rules.append(RuleConfig(name='b', equal=['']))
        self.rules.append(RuleConfig(
            name='m', equal=['meta_modification_time', 'meta_modification_time_nano']))
        self.rules.append(RuleConfig(
            name='a', equal=['meta_access_time', 'meta_access_time_nano']))
        self.rules.append(RuleConfig(
            name='c', equal=['meta_changed_time', 'meta_changed_time_nano']))
        self.rules.append(RuleConfig(name='S', greater=['meta_size']))
        self.rules.append(RuleConfig(name='', equal=['']))

    def _parse_rules(self, rules_config):
        if rules_config is None:
            return
        for rule in rules_config:
            self.rules.append(RuleConfig(config=rule))


class InvestigationsConfig:
    pass


class RuleConfig:
    def __init__(self, config=None, name='', regex='', included=[], greater=[], equal=[]):
        if config is not None:
            self._by_config(config)
        elif name:
            self._by_values(name, regex=regex, included=included,
                            greater=greater, equal=equal)

    def _by_config(self, config):
        keys = config.keys()
        if(not 'name' in keys):
            return
        self.name = config['name']
        self.regex = config['regex'] if 'regex' in keys else ''
        self.inlcuded = config['inlcuded'] if 'inlcuded' in keys else []
        self.greater = config['greater'] if 'greater' in keys else []
        self.equal = config['equal'] if 'equal' in keys else []

    def _by_values(self, name, regex='', included=[], greater=[], equal=[]):
        self.name = name
        self.regex = regex
        self.inlcuded = included
        self.greater = greater
        self.equal = equal
