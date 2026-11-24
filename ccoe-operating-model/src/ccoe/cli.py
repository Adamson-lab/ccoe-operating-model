"""ccoe command line interface."""
import argparse
import datetime
import json
import os
import sys

from . import adr, guardrails, raci, report


def _root(args):
    return os.path.abspath(args.root)


def cmd_validate(a):
    r = _root(a)
    errs = []
    rd = raci.load(f"{r}/data/raci.json")
    errs += [f"raci: {e}" for e in raci.validate(rd)]
    errs += [f"adr: {e}" for e in adr.lint(f"{r}/adr")]
    cat = guardrails.load_json(f"{r}/data/guardrails.json")
    ids = [g["id"] for g in cat["guardrails"]]
    if len(ids) != len(set(ids)):
        errs.append("guardrails: duplicate ids")
    errs += [f"exceptions: {e}" for e in guardrails.validate_exceptions(guardrails.load_json(f"{r}/data/exceptions.json"), set(ids))]
    if errs:
        print("\n".join(errs))
        return 1
    print(f"OK: {len(rd['activities'])} RACI activities, {len(adr.load_all(r + '/adr'))} ADRs, {len(ids)} guardrails, exceptions valid.")
    return 0


def cmd_check_plan(a):
    r = _root(a)
    cat = guardrails.load_json(f"{r}/data/guardrails.json")
    exc = guardrails.load_json(a.exceptions or f"{r}/data/exceptions.json")
    today = datetime.date.fromisoformat(a.today) if a.today else None
    findings = guardrails.check_plan(guardrails.load_json(a.plan), cat, exc, today)
    sys.stdout.write(guardrails.render(findings, a.format))
    return 1 if guardrails.blocking(findings) else 0


def _write(path, text, stdout):
    if stdout:
        sys.stdout.write(text)
    else:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"wrote {path}")
    return 0


def cmd_raci_md(a):
    return _write(f"{_root(a)}/docs/03-raci.md", raci.to_markdown(raci.load(f"{_root(a)}/data/raci.json")), a.stdout)


def cmd_adr_index(a):
    return _write(f"{_root(a)}/adr/README.md", adr.index_markdown(f"{_root(a)}/adr"), a.stdout)


def cmd_catalog(a):
    return _write(f"{_root(a)}/docs/04-guardrails-catalog.md", report.catalog_markdown(guardrails.load_json(f"{_root(a)}/data/guardrails.json")), a.stdout)


def cmd_scorecard(a):
    return _write(f"{_root(a)}/docs/08-scorecard.md", report.scorecard_markdown(guardrails.load_json(f"{_root(a)}/data/kpis.json")), a.stdout)


def main(argv=None):
    p = argparse.ArgumentParser(prog="ccoe", description="Cloud Center of Excellence toolkit")
    p.add_argument("--root", default=".", help="repository root")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate", help="validate RACI, ADRs, guardrails, exceptions").set_defaults(fn=cmd_validate)
    c = sub.add_parser("check-plan", help="evaluate a terraform plan JSON against guardrails")
    c.add_argument("plan")
    c.add_argument("--exceptions")
    c.add_argument("--today", help="override date (YYYY-MM-DD)")
    c.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    c.set_defaults(fn=cmd_check_plan)
    for name, fn in (("raci-md", cmd_raci_md), ("adr-index", cmd_adr_index), ("catalog", cmd_catalog), ("scorecard", cmd_scorecard)):
        s = sub.add_parser(name)
        s.add_argument("--stdout", action="store_true")
        s.set_defaults(fn=fn)
    a = p.parse_args(argv)
    return a.fn(a)
