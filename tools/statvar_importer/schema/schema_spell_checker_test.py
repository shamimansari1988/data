# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Unit tests for property_value_cache.py."""

import os
import sys
import unittest

from absl import app
from absl import logging

import schema_spell_checker

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_SCRIPT_DIR)
sys.path.append(os.path.dirname(_SCRIPT_DIR))
sys.path.append(os.path.dirname(os.path.dirname(_SCRIPT_DIR)))
sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(_SCRIPT_DIR))),
                 'util'))

from config_map import ConfigMap


class SchemaSpellCheckerTest(unittest.TestCase):

    def test_get_words(self):
        word = 'A DCS sentenceWith camelCase+ [snake_case] & 10OrMoreWords'
        expected_words = [
            'sentence', 'With', 'camel', 'Case', 'snake', 'case', 'Or', 'More',
            'Words'
        ]
        self.assertEqual(expected_words, schema_spell_checker.get_words(word))

    def test_spell_check_nodes(self):
        nodes = {
            'TestNode1': {
                'Node': 'dcid:TestNode1',
                'typeOf': 'schema:Class',
                # Typo in value dcid
                'propWithError': 'dcs:Val,dcs:Childs',
                'goodProp': 'dcid:Person',
                # Capitalized acronyms ignored for spell check
                'allowedProp': '"Capitalized Acronyms like ABCD allowed"',
            },
            'TestNode2': {
                'property': 'dcid:GoodValue',
                'nonUsEnglishError': 'colour',  # British English value error
                'typpOProp': 'ErrorProp',  # Error in property name
            },
            'TestNode3': {
                'description': '"Long sentence & having MoreThn1 words"',
                'property': 'TypoEr',
                # autogenerated value ignored
                'spellChcekIgnores': 'dc/abc123werfraw',
                # human-curated value not ignored.
                'spellCheckedProp': 'dcid:dc/topic/SpelErr',
            },
        }
        expected_errors = {
            'TestNode1': {
                'propWithError': 'childs'
            },
            'TestNode2': {
                'nonUsEnglishError': 'colour',
                'typpOProp': 'typp'
            },
            'TestNode3': {
                'description': 'thn',
                'spellCheckedProp': 'spel'
            }
        }

        self.assertEqual(expected_errors,
                         schema_spell_checker.spell_check_nodes(nodes))
        # Test with spell check only on quoted values
        self.assertEqual({'TestNode3': {
            'description': 'thn'
        }},
                         schema_spell_checker.spell_check_nodes(
                             nodes, ConfigMap({'spell_check_text_only': True})))
