class InvestigatorConfig:
    def __init__(self, config):
        keys = config.keys()
        self._add_default_rules()
        self._parse_rules(config['rules'] if 'rules' in keys else None)
        self._parse_investigations(
            config['investigations'] if 'investigations' in keys else None)
        self.same_config = config['same_config'] if 'same_config' in keys else True
        self.validation_run = config['validation_run'] if 'validation_run' in keys else ''
        self.greater = []
        self.equal = []

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
        self.rules.append(RuleConfig(name='empty'))

    def _parse_rules(self, rules_config):
        if rules_config is None:
            return
        for rule in rules_config:
            self.rules.append(RuleConfig(config=rule))

    def _parse_investigations(self, investigation_config):
        self.investigations = []
        if investigation_config is None:
            return
        for inestigation in investigation_config:
            self.investigations.append(
                InvestigationsConfig(config=inestigation))

    def prepare_investigations(self):
        for rule in self.rules:
            rule.clean_greater_and_equal()
            rule.expand_rules(self.rules)
        for investigation in self.investigations:
            investigation.validate_rules(self.rules)

    def __repr__(self):
        return ("InvestigatorConfig("
                f"rules={self.rules},"
                f"investigations={self.investigations},"
                f"same_config={self.same_config},"
                f"validation_run={self.validation_run},"
                ")")


class InvestigationsConfig:
    def __init__(self, config):
        keys = config.keys()
        self.paths = config['paths'] if 'paths' in keys else []
        self.fileregexwhitelist = config['fileregexwhitelist'] if 'fileregexwhitelist' in keys else ''
        self.fileregexblacklist = config['fileregexblacklist'] if 'fileregexblacklist' in keys else ''
        self.rules = config['rules'] if 'rules' in keys else []
        self.greater = []
        self.equal = []

    def validate_rules(self, all_rules):
        if not self.rules:
            return
        for rule_name in self.rules:
            rule = next(rule for rule in all_rules if rule.name == rule_name)
            for grt in rule.greater:
                if not grt in self.greater:
                    self.greater.append(grt)
            for eq in rule.equal:
                if not eq in self.equal and not eq in self.greater:
                    self.equal.append(eq)

    def __repr__(self):
        return ("InvestigationsConfig("
                f"paths={self.paths},"
                f"fileregexwhitelist={self.fileregexwhitelist},"
                f"fileregexblacklist={self.fileregexblacklist},"
                f"rules={self.rules},"
                f"greater={self.greater},"
                f"equal={self.equal},"
                ")")


class RuleConfig:
    def __init__(self, config=None, name='', regex='', rules=[], greater=[], equal=[]):
        if config is not None:
            self._by_config(config)
        elif name:
            self._by_values(name, regex=regex, rules=rules,
                            greater=greater, equal=equal)

    def _by_config(self, config):
        keys = config.keys()
        if(not 'name' in keys):
            return
        self.name = config['name']
        self.rules = config['rules'] if 'rules' in keys else []
        self.greater = config['greater'] if 'greater' in keys else []
        self.equal = config['equal'] if 'equal' in keys else []

    def _by_values(self, name, regex='', rules=[], greater=[], equal=[]):
        self.name = name
        self.regex = regex
        self.rules = rules
        self.greater = greater
        self.equal = equal

    def clean_greater_and_equal(self):
        for eq in self.equal:
            if eq in self.greater:
                self.equal.remove(eq)

    def expand_rules(self, all_rules):
        if not self.rules:
            return
        for rule_name in self.rules:
            self.rules.remove(rule_name)
            rule = next(rule for rule in all_rules if rule.name == rule_name)
            rule.expand_rules(all_rules)
            for grt in rule.greater:
                if not grt in self.greater:
                    self.greater.append(grt)
                if grt in self.equal:
                    self.equal.remove(grt)
            for eq in rule.equal:
                if not eq in self.equal and not eq in self.greater:
                    self.equal.append(eq)

    def __repr__(self):
        return ("RuleConfig("
                f"name={self.name},"
                f"rules={self.rules},"
                f"greater={self.greater},"
                f"equal={self.equal},"
                ")")
