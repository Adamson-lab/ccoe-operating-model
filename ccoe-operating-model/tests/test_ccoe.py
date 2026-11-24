import copy, datetime, json, os, tempfile, unittest
from ccoe import adr, guardrails, raci, report

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
J = lambda p: json.load(open(os.path.join(ROOT, p)))


class RaciTests(unittest.TestCase):
    def test_repo_matrix_valid(self):
        self.assertEqual(raci.validate(J("data/raci.json")), [])

    def test_two_accountables_rejected(self):
        d = copy.deepcopy(J("data/raci.json"))
        d["activities"][0]["raci"]["CC"] = "A"
        self.assertTrue(any("exactly one Accountable" in e for e in raci.validate(d)))

    def test_no_responsible_rejected(self):
        d = copy.deepcopy(J("data/raci.json"))
        d["activities"][0]["raci"] = {"EXEC": "A", "CC": "C"}
        self.assertTrue(any("Responsible" in e for e in raci.validate(d)))

    def test_unknown_role_and_letter(self):
        d = copy.deepcopy(J("data/raci.json"))
        d["activities"][0]["raci"]["GHOST"] = "Z"
        errs = raci.validate(d)
        self.assertTrue(any("unknown role" in e for e in errs) and any("invalid letter" in e for e in errs))

    def test_markdown_has_all_rows(self):
        md = raci.to_markdown(J("data/raci.json"))
        self.assertIn("A18", md)
        self.assertIn("**A/R**", md)


class AdrTests(unittest.TestCase):
    def test_repo_adrs_lint_clean(self):
        self.assertEqual(adr.lint(os.path.join(ROOT, "adr")), [])

    def test_bad_adr_detected(self):
        with tempfile.TemporaryDirectory() as d:
            open(os.path.join(d, "0001-x.md"), "w").write("# ADR-0001: X\n- Status: Maybe\n- Date: nope\n- Domain: other\n- Related: 0099\n- Supersedes: -\n\n## Context\nx\n")
            errs = adr.lint(d)
            joined = "\n".join(errs)
            for needle in ("status must", "ISO", "domain must", "unknown ADR 0099", "missing section"):
                self.assertIn(needle, joined)

    def test_supersede_requires_marked(self):
        with tempfile.TemporaryDirectory() as d:
            base = "# ADR-000{n}: T\n- Status: {s}\n- Date: 2026-01-01\n- Deciders: ARB\n- Domain: platform\n- Related: -\n- Supersedes: {sup}\n\n## Context\nc\n\n## Decision\nd\n\n## Consequences\nc\n\n## Alternatives considered\n- a\n"
            open(os.path.join(d, "0001-a.md"), "w").write(base.format(n=1, s="Accepted", sup="-"))
            open(os.path.join(d, "0002-b.md"), "w").write(base.format(n=2, s="Accepted", sup="0001"))
            self.assertTrue(any("not marked Superseded" in e for e in adr.lint(d)))


class GuardrailTests(unittest.TestCase):
    def setUp(self):
        self.cat = J("data/guardrails.json")
        self.exc = J("data/exceptions.json")
        self.good = J("tests/fixtures/plan_good.json")
        self.bad = J("tests/fixtures/plan_bad.json")
        self.today = datetime.date(2026, 11, 24)

    def ids(self, findings, status="violation"):
        return {f["guardrail"] for f in findings if f["status"] == status}

    def test_good_plan_has_no_blocking(self):
        f = guardrails.check_plan(self.good, self.cat, self.exc, self.today)
        self.assertEqual(guardrails.blocking(f), [])

    def test_bad_plan_triggers_expected_guardrails(self):
        f = guardrails.check_plan(self.bad, self.cat, {"exceptions": []}, self.today)
        expected = {"G-DATA-002", "G-DATA-003", "G-NET-001", "G-NET-002", "G-HARD-001", "G-IAM-002", "G-KMS-001", "G-TAG-001", "G-REG-001", "G-COST-001"}
        self.assertTrue(expected <= self.ids(f), expected - self.ids(f))

    def test_advisory_does_not_block(self):
        f = guardrails.check_plan(self.bad, self.cat, {"exceptions": []}, self.today)
        self.assertTrue(all(x["severity"] == "mandatory" for x in guardrails.blocking(f)))
        self.assertIn("G-COST-001", self.ids(f))

    def test_waiver_applies_until_expiry(self):
        f = guardrails.check_plan(self.bad, self.cat, self.exc, self.today)
        waived = [x for x in f if x["status"] == "waived"]
        self.assertEqual([(w["guardrail"], w["resource"]) for w in waived], [("G-DATA-002", "aws_ebs_volume.legacy_batch")])
        later = guardrails.check_plan(self.bad, self.cat, self.exc, datetime.date(2027, 2, 1))
        self.assertFalse([x for x in later if x["status"] == "waived"])
        self.assertTrue(any("expired" in x["note"] for x in later))

    def test_exception_validation(self):
        ids = {g["id"] for g in self.cat["guardrails"]}
        self.assertEqual(guardrails.validate_exceptions(self.exc, ids), [])
        bad = {"exceptions": [dict(self.exc["exceptions"][0], expires="2028-01-01"), dict(self.exc["exceptions"][0], id="EXC-2", guardrail="G-NOPE")]}
        errs = "\n".join(guardrails.validate_exceptions(bad, ids))
        self.assertIn("exceeds", errs)
        self.assertIn("unknown guardrail", errs)

    def test_catalogue_checks_all_executable(self):
        for g in self.cat["guardrails"]:
            list(guardrails.evaluate_rule(g, self.good))

    def test_all_ingress_protocols(self):
        plan = {"resource_changes": [{"address": "r", "type": "aws_vpc_security_group_ingress_rule", "change": {"actions": ["create"], "after": {"cidr_ipv4": "0.0.0.0/0", "from_port": 0, "to_port": 65535, "ip_protocol": "-1"}}}]}
        g = next(x for x in self.cat["guardrails"] if x["id"] == "G-NET-001")
        self.assertEqual(len(list(guardrails.evaluate_rule(g, plan))), 1)


class ReportTests(unittest.TestCase):
    def test_rag(self):
        self.assertEqual(report.rag({"current": 5, "target": 10, "better": "lower"}), "green")
        self.assertEqual(report.rag({"current": 90, "target": 95, "better": "higher"}), "amber")
        self.assertEqual(report.rag({"current": 50, "target": 95, "better": "higher"}), "red")

    def test_scorecard_renders(self):
        self.assertIn("KPIs", report.scorecard_markdown(J("data/kpis.json")))


if __name__ == "__main__":
    unittest.main()
