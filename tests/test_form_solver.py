"""Compare bounded form search against an independent exhaustive small-bank oracle."""
import copy
import itertools
from pathlib import Path
import random
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'evals'))
from fixture import c, harbor


class FormSolverTests(unittest.TestCase):
    def test_seeded_banks_match_exhaustive_oracle(self):
        rng = random.Random(20261021)
        for case in range(80):
            d = harbor()
            d['blueprint']['required_methods'] = {'practical': rng.randrange(3)}
            for i in d['items']:
                i['status'] = 'retired' if rng.random() < .18 else 'approved'
                i['enemy_groups'] = [f'GROUP_{rng.randrange(4)}'] if rng.random() < .35 else []
            for r in d['reviews']:
                r['item_fingerprint'] = c.content_fingerprint(c.index_items(d)[r['item_id']])
            candidates = [i for i in d['items'] if i['status'] == 'approved']
            feasible = []
            for selection in itertools.combinations(candidates, 8):
                if any(sum(i['domain_id'] == key for i in selection) != count for key, count in [('D', 4), ('S', 2), ('R', 2)]):
                    continue
                if sum(i['type'] == 'practical' for i in selection) < d['blueprint']['required_methods']['practical']:
                    continue
                groups = [g for i in selection for g in i['enemy_groups']]
                if len(groups) != len(set(groups)):
                    continue
                feasible.append({i['id'] for i in selection})
            before = copy.deepcopy(d)
            actual = c.assemble(d, 'SEARCH')
            with self.subTest(case=case):
                self.assertEqual(actual['assembled'], bool(feasible))
                self.assertEqual(d, before, 'Form search mutated its input')
                if feasible:
                    self.assertIn({r['item_id'] for r in actual['form']['item_refs']}, feasible)


if __name__ == '__main__': unittest.main()
