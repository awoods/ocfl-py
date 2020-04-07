"""OCFL Validation Logger.

Handle logging of validation errors and warnings.
"""
import json
import os
import os.path
import re
import logging


class ValidationLogger(object):
    """Class for OCFL ValidationLogger."""

    validation_codes = None

    def __init__(self, warnings=False, lang='en'):
        """Initialize OCFL validation logger."""
        self.warnings = warnings
        self.lang = lang
        self.codes = {}
        self.messages = []
        self.num_errors = 0
        self.num_warnings = 0
        self.info = 0
        self.spec = 'https://ocfl.io/draft/spec/'
        if self.validation_codes is None:
            with open(os.path.join(os.path.dirname(__file__), 'data/validation-errors.json'), 'r') as fh:
                self.validation_codes = json.load(fh)

    def error_or_warning(self, code, severity='error', **args):
        """Add error or warning to self.codes."""
        if code in self.validation_codes and 'description' in self.validation_codes[code]:
            desc = self.validation_codes[code]['description']
            lang_desc = None
            if self.lang in desc:
                lang_desc = desc[self.lang]
            elif 'en' in desc:
                lang_desc = desc['en']
            elif len(desc) > 0:
                # first key alphabetically
                lang_desc = desc[sorted(list(desc.keys()))[0]]
            else:
                lang_desc = "Unknown " + severity + ": %s - no description, params (%s)"
            # Add in any parameters
            if 'params' in self.validation_codes[code]:
                params = []
                for param in self.validation_codes[code]['params']:
                    params.append(str(args[param]) if param in args else '???')
                try:
                    lang_desc = lang_desc % tuple(params)
                except TypeError:
                    lang_desc += str(args)
            message = '[' + code + '] ' + lang_desc
        else:
            message = "Unknown " + severity + ": %s - params (%s)" % (code, str(args))
        # Add link to spec
        m = re.match(r'''([EW](\d\d\d))''', code)
        if m and int(m.group(2)) < 200:
            message += ' (see ' + self.spec + '#' + m.group(1) + ')'
        # Store set of codes with last message for that code, and _full_ list of messages
        self.codes[code] = message
        if severity == 'error' or self.warnings:
            self.messages.append(message)

    def error(self, code, **args):
        """Add error code to self.codes."""
        self.error_or_warning(code, severity='error', **args)
        self.num_errors += 1

    def warn(self, code, **args):
        """Add warning code to self.codes."""
        self.error_or_warning(code, severity='warning', **args)
        self.num_warnings += 1

    def __str__(self):
        """String of validator status."""
        s = ''
        for message in sorted(self.messages):
            s += message + '\n'
        return s
