
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COMMANDS = {
    ("pipeline",): ROOT / "scripts/pipeline/run_pipeline.py",

    ("build", "seed"): ROOT / "scripts/builders/build_seed.py",
    ("build", "registry"): ROOT / "scripts/builders/build_content_registry.py",
    ("build", "queue"): ROOT / "scripts/builders/build_golden_queue.py",
    ("build", "pack"): ROOT / "scripts/builders/build_golden_pack.py",
    ("build", "factory"): ROOT / "scripts/builders/build_content_factory.py",
    ("build", "master"): ROOT / "scripts/builders/build_knowledge_master.py",

    ("audit", "factory"): ROOT / "scripts/audits/audit_content_factory.py",
    ("audit", "master"): ROOT / "scripts/audits/audit_knowledge_master.py",
    ("audit", "batch"): ROOT / "scripts/audits/audit_knowledge_batch.py",
}


def run_script(path: Path):
    print(f"[RUN] {path.relative_to(ROOT)}")
    subprocess.run([sys.executable, str(path)], check=True)
    print("[OK]\n")


def help_screen():
    print("=" * 45)
    print("LENABA CLI")
    print("=" * 45)
    print()
    print("Build:")
    print("  python scripts/cli.py build seed")
    print("  python scripts/cli.py build registry")
    print("  python scripts/cli.py build queue")
    print("  python scripts/cli.py build pack")
    print("  python scripts/cli.py build factory")
    print("  python scripts/cli.py build master")
    print("  python scripts/cli.py build all")
    print()
    print("Audit:")
    print("  python scripts/cli.py audit master")
    print("  python scripts/cli.py audit factory")
    print("  python scripts/cli.py audit batch")
    print()
    print("Other:")
    print("  python scripts/cli.py test")
    print("  python scripts/cli.py check")
    print("  python scripts/cli.py pipeline")


def build_all():
    run_script(COMMANDS[("build", "seed")])
    run_script(COMMANDS[("build", "registry")])
    run_script(COMMANDS[("build", "queue")])
    run_script(COMMANDS[("build", "pack")])
    run_script(COMMANDS[("build", "master")])


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

    script = COMMANDS.get(args)

    if script is None:
        print("Unknown command.\n")
        help_screen()
        sys.exit(1)

    run_script(script)


if __name__ == "__main__":
    main()