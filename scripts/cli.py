
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COMMANDS = {
    ("pipeline",): ROOT / "scripts/pipeline/run_pipeline.py",
    ("other", "sync"): ROOT / "scripts/cli_sync.py",

    ("build", "seed"): ROOT / "scripts/builders/build_seed.py",
    ("build", "registry"): ROOT / "scripts/builders/build_content_registry.py",
    ("build", "execution"): ROOT / "scripts/builders/build_execution_queue.py",
    ("build", "golden"): ROOT / "scripts/builders/build_golden_queue.py",
    ("build", "pack"): ROOT / "scripts/builders/build_golden_pack.py",
    ("build", "factory"): ROOT / "scripts/builders/build_content_factory.py",
    ("build", "master"): ROOT / "scripts/builders/build_knowledge_master.py",
    ("build", "completion"): ROOT / "scripts/builders/build_completion_levels.py",
    ("build", "forms"): ROOT / "scripts/builders/merge_behind_forms.py",
    ("build", "finalize"): ROOT / "scripts/builders/build_finalize_behind_import.py",
    ("build", "graph"): ROOT / "scripts/builders/build_name_graph.py",
    ("build", "integrity"): ROOT / "scripts/builders/build_graph_integrity.py",
    ("build", "taxonomy"): ROOT / "scripts/builders/build_taxonomy.py",
    ("build", "families"): ROOT / "scripts/builders/build_canonical_families.py",
    ("build", "cleanup"): ROOT / "scripts/builders/fix_master_cleanup.py",
    ("build", "smart-queue"): ROOT / "scripts/builders/build_smart_queue.py",
    ("build", "smart-queue-v2"): ROOT / "scripts/builders/build_smart_queue_v2.py",
    ("build", "language"): ROOT / "scripts/builders/build_language_resolver.py",
    ("build", "smart-queue-v3"): ROOT / "scripts/builders/build_smart_queue_v3.py",
    ("build", "execution"): ROOT / "scripts/builders/build_execution_queue.py",
    ("build","batches"): ROOT/"scripts/builders/build_execution_batches.py",
    ("build", "fetch-results"): ROOT / "scripts/builders/build_fetch_results.py",
    ("build", "behind-cache"): ROOT / "scripts/builders/build_behind_cache.py",
    ("build", "parser-test"): ROOT / "scripts/builders/build_parser_test.py",
    ("build", "etymology"): ROOT / "scripts/builders/build_etymology_graph.py",
    ("build", "merge"): ROOT / "scripts/builders/build_merge_fetch_results.py",
    ("build", "confidence"): ROOT / "scripts/builders/fix_confidence_scale.py",
    ("build", "master-v2"): ROOT / "scripts/builders/build_master_v2.py",
    ("build", "confidence-v2"): ROOT / "scripts/builders/fix_confidence_v2.py",
    ("build", "schema"): ROOT / "scripts/builders/build_master_schema.py",
    ("build", "legacy-patch"): ROOT / "scripts/builders/build_legacy_patch.py",
    ("build", "family-lookup"): ROOT / "scripts/builders/build_family_lookup_v2.py",
    ("build", "confidence-v3"): ROOT / "scripts/builders/fix_confidence_v3.py",
    ("build", "family-merge"): ROOT / "scripts/builders/build_family_merge.py",
    ("build", "family-graph"): ROOT / "scripts/builders/build_family_graph.py",
    ("build","family-verification"): ROOT / "scripts/builders/build_family_verification.py",
    ("build", "etymology-full"): ROOT / "scripts/builders/build_etymology_graph_full.py",

    ("audit", "factory"): ROOT / "scripts/audits/audit_content_factory.py",
    ("audit", "master"): ROOT / "scripts/audits/audit_knowledge_master.py",
    ("audit", "batch"): ROOT / "scripts/audits/audit_knowledge_batch.py",
    ("audit", "completion"): ROOT / "scripts/audits/audit_completion.py",
    ("audit", "mapping"): ROOT / "scripts/audits/audit_mapping.py",
    ("audit", "graph"): ROOT / "scripts/audits/audit_name_graph.py",
    ("audit", "templates"): ROOT / "scripts/audits/audit_template_candidates.py",
    ("audit", "taxonomy"): ROOT / "scripts/audits/audit_taxonomy.py",
    ("audit", "taxonomy-sources"): ROOT / "scripts/audits/audit_taxonomy_sources.py",
    ("audit", "integrity"): ROOT / "scripts/audits/audit_integrity.py",
    ("audit", "confidence"): ROOT / "scripts/audits/audit_confidence.py",
    ("audit", "family-coverage"): ROOT / "scripts/audits/audit_family_coverage.py",
    ("audit", "local-pron"): ROOT / "scripts/audits/audit_local_pron_sources.py",
    ("audit", "language"): ROOT / "scripts/audits/audit_language_resolver.py",
    ("audit", "smart-queue"): ROOT / "scripts/audits/audit_smart_queue_v3.py",
    ("audit", "execution"): ROOT / "scripts/audits/audit_execution_queue.py",
    ("audit","batches"): ROOT/"scripts/audits/audit_execution_batches.py",
    ("audit", "etymology"): ROOT / "scripts/audits/audit_etymology_graph.py",
    ("audit", "schema"): ROOT / "scripts/audits/audit_master_schema.py",
    ("audit", "family-lookup"): ROOT / "scripts/audits/audit_family_lookup.py",
    ("audit", "platform"): ROOT / "scripts/audits/audit_platform.py",
    ("audit", "family-graph"): ROOT / "scripts/audits/audit_family_graph.py",
    ("audit","language-distribution"): ROOT / "scripts/audits/audit_language_distribution.py",

    ("fetch",): ROOT / "scripts/executors/fetch_behind_smart.py",
    ("fetch","overnight"): ROOT / "scripts/executors/fetch_behind_smart.py",
}


def run_script(path: Path, extra_args=None):

    if extra_args is None:
        extra_args = []

    module = (
        path.relative_to(ROOT)
            .with_suffix("")
            .as_posix()
            .replace("/", ".")
    )

    print(f"[RUN] {module}")

    subprocess.run(
        [sys.executable, "-m", module, *extra_args],
        cwd=ROOT,
        check=True,
    )

    print("[OK]\n")

def print_group(title: str, group: str):

    print(f"{title}:")

    cmds = sorted(
        key[1:]
        for key in COMMANDS
        if key[0] == group and len(key) > 1
    )

    for cmd in cmds:
        print(f"  python scripts/cli.py {group} {' '.join(cmd)}")

    print()


def help_screen():

    print("=" * 45)
    print("LENABA CLI")
    print("=" * 45)
    print()

    print_group("Build", "build")
    print_group("Audit", "audit")
    print_group("Fetch", "fetch")
    print_group("Other", "other")

    print("Standalone:")
    print("  python scripts/cli.py test")
    print("  python scripts/cli.py check")
    print("  python scripts/cli.py pipeline")
    print()



def build_all():

    run_script(COMMANDS[("build", "seed")])
    run_script(COMMANDS[("build", "registry")])
    run_script(COMMANDS[("build", "queue")])
    run_script(COMMANDS[("build", "pack")])
    run_script(COMMANDS[("build", "master")])

    # Knowledge pipeline
    run_script(COMMANDS[("build", "forms")])
    run_script(COMMANDS[("build", "completion")])
    run_script(COMMANDS[("build", "graph")])
    run_script(COMMANDS[("build", "families")])
    run_script(COMMANDS[("build", "taxonomy")])


def run_tests():
    subprocess.run([sys.executable, "-m", "pytest", "-v"], check=True)


def run_check():
    build_all()
    run_script(COMMANDS[("audit", "master")])
    run_tests()


def main():

    args = tuple(sys.argv[1:])

    if not args:
        help_screen()
        return

    if args == ("build", "all"):
        build_all()
        return

    if args == ("test",):
        run_tests()
        return

    if args == ("check",):
        run_check()
        return

    # ---- Fetch executor ----
    if args[0] == "fetch":

        run_script(
            COMMANDS[("fetch",)],
            args[1:],
        )

        return

    script = COMMANDS.get(args)

    if script is None:
        print("Unknown command.\n")
        help_screen()
        sys.exit(1)

    run_script(script)


if __name__ == "__main__":
    main()
