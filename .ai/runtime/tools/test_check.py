#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Check that code is accompanied by tests, against the testing standard (it-role-library/standards/testing.md).

For production code — errors:
    missing-test-file          no test file for it by the language's convention (FooTest, test_foo.py, foo.test.ts …)
    untested                   a public function or method that no related test calls
    missing-integration-test   code that talks to a database, an HTTP service, a broker or a cloud SDK, with no
                               integration test exercising it (FooIT, @Testcontainers, pytest.mark.integration …)
For test code — warnings:
    no-assertion               a test that asserts nothing
    sleep                      a test that sleeps instead of controlling time
    disabled                   a disabled or skipped test without a ticket or reason
    mocks-subject              a test that mocks the class it is testing

    test_check.py PATH... [--json] [--errors-only]
    test_check.py selftest

Only code inside a project (pom.xml, build.gradle, package.json, pyproject.toml, requirements.txt, go.mod, *.csproj …)
is held to it. Public elements are recognised by doc_check.py, so both checks agree on what is public. This is a
heuristic: it matches by naming convention and finds calls by name. Whether a test is good is a reviewer's judgement.
"""
import argparse
import json
import os
import re
import signal
import sys

for _s in (sys.stdin, sys.stdout, sys.stderr):  # Windows consoles default to a code page, not UTF-8
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")
sys.argv = [a.encode("utf-8", "surrogateescape").decode("utf-8", "replace") for a in sys.argv]
sys.dont_write_bytecode = True        # no __pycache__ inside an installed library: nothing left behind on uninstall
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doc_check  # noqa: E402  (shares the recognition of public declarations)

DESCRIPTORS = ("pom.xml", "build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts", "package.json",
               "pyproject.toml", "setup.py", "setup.cfg", "requirements.txt", "pytest.ini", "tox.ini", "go.mod",
               "Cargo.toml")
SKIP = doc_check.SKIP_DIRS
TEST_DIR_PARTS = {"test", "tests", "__tests__", "spec", "it", "integrationtest", "integration-test", "testing"}
TEST_NAME = re.compile(r"(^test_.*\.py$|_test\.(py|go)$|(Test|Tests|IT|IntegrationTest|Spec)\.(java|kt|cs)$|"
                       r"^Test\w+\.(java|kt)$|\.(test|spec|int\.test|integration\.test)\.[jt]sx?$)")
NOT_TESTABLE = {"toString", "equals", "hashCode", "main", "__repr__", "__str__", "__eq__", "__hash__", "String"}
ACCESSOR = re.compile(r"^(get|is|has|set)[A-Z]")
BOUNDARY = {
    "java": re.compile(r"^\s*import\s+(static\s+)?(java\.sql|javax\.sql|jakarta\.persistence|javax\.persistence|"
                       r"org\.springframework\.(jdbc|data|web\.client|web\.reactive\.function\.client|kafka|amqp)|"
                       r"org\.hibernate|java\.net\.http|okhttp3|org\.apache\.(http|hc|kafka)|jakarta\.jms|javax\.jms|"
                       r"software\.amazon\.awssdk|com\.amazonaws|redis\.clients|io\.lettuce|com\.mongodb|org\.mongodb)",
                       re.M),
    "python": re.compile(r"^\s*(import|from)\s+(sqlite3|psycopg2?|pymysql|mysql|sqlalchemy|requests|httpx|aiohttp|"
                         r"urllib\.request|boto3|botocore|redis|pymongo|kafka|pika|confluent_kafka|asyncpg)\b", re.M),
    "ts": re.compile(r"""(from|require\()\s*['"](pg|mysql2?|mongodb|mongoose|redis|ioredis|axios|node-fetch|kafkajs|"""
                     r"""amqplib|@aws-sdk/[\w-]+|@prisma/client|typeorm|sequelize|knex)['"]|\bfetch\(""", re.M),
    "csharp": re.compile(r"^\s*using\s+(System\.Data|Microsoft\.Data\.SqlClient|Npgsql|Microsoft\.EntityFrameworkCore|"
                         r"System\.Net\.Http|Amazon\.|StackExchange\.Redis|Confluent\.Kafka|RabbitMQ)", re.M),
    "go": re.compile(r'"(database/sql|net/http|github\.com/jackc/pgx[\w/]*|github\.com/(go-)?redis/[\w/-]*|'
                     r'go\.mongodb\.org/[\w/-]*|github\.com/segmentio/kafka-go|github\.com/aws/aws-sdk-go[\w/-]*)"'),
}
BOUNDARY["kotlin"] = BOUNDARY["java"]
INTEGRATION_MARK = re.compile(r"@Testcontainers|@SpringBootTest|@DataJpaTest|@JdbcTest|@DataMongoTest|@JooqTest|"
                              r"pytest\.mark\.integration|testcontainers|//\s*go:build\s+integration|"
                              r"WebApplicationFactory|GenericContainer|PostgreSQLContainer", re.I)
INTEGRATION_NAME = re.compile(r"(IT|IntegrationTest)\.(java|kt|cs)$|\.(int|integration)\.test\.[jt]sx?$|"
                              r"(^|[\\/])(integration|integrationTest|it)[\\/]", re.I)


def finding(path, line, sev, rule, msg, key=""):
    """Build one result: file, line, severity (error or warning), rule, message and a stable key."""
    return {"file": path, "line": line, "severity": sev, "rule": rule, "message": msg, "key": key}


def project_root(path):
    """The nearest folder above path holding a build or project descriptor, or None outside any project."""
    d = os.path.dirname(os.path.abspath(path)) if not os.path.isdir(path) else os.path.abspath(path)
    while True:
        try:
            names = os.listdir(d)
        except OSError:
            names = []
        if any(n in DESCRIPTORS or n.endswith((".csproj", ".sln", ".fsproj")) for n in names):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def is_test_path(path):
    """True for a test source file, by folder (src/test, tests, __tests__ …) or by name (FooTest, test_foo …)."""
    norm = path.replace("\\", "/")
    parts = [p.lower() for p in norm.split("/")[:-1]]
    return bool(TEST_NAME.search(os.path.basename(path))) or any(p in TEST_DIR_PARTS for p in parts) \
        or "/src/test/" in norm or any(p.endswith(".tests") for p in parts)


def generated(path):
    """True for vendored, generated or build-output code, which carries no test obligation."""
    return any(p in SKIP for p in re.split(r"[\\/]", path)[:-1])


_TEST_CACHE = {}


def test_files(root):
    """Every test source file in the project at root, as {path: text}; cached per root for one run."""
    if root not in _TEST_CACHE:
        found = {}
        for dp, dirs, fs in os.walk(root):
            dirs[:] = [x for x in dirs if x not in SKIP and not x.startswith(".")]
            for f in fs:
                p = os.path.join(dp, f)
                if doc_check.LANG.get(os.path.splitext(f)[1].lower()) and is_test_path(p):
                    try:
                        found[p] = open(p, encoding="utf-8", errors="replace").read()
                    except OSError:
                        pass
        _TEST_CACHE[root] = found
    return _TEST_CACHE[root]


def subject_names(path, lang):
    """The names a test uses to refer to this file's code: the class or module name, and for Python its import path."""
    stem = os.path.splitext(os.path.basename(path))[0]
    names = {stem}
    if lang == "python":
        names.add(stem)
    if lang == "ts":
        names |= {stem, re.sub(r"[-_](\w)", lambda m: m.group(1).upper(), stem)}
    return names


def expected_test_files(path, lang):
    """The test file names the language's convention gives this production file."""
    stem = os.path.splitext(os.path.basename(path))[0]
    ext = os.path.splitext(path)[1]
    return {"java": [f"{stem}Test.java", f"{stem}Tests.java", f"{stem}IT.java", f"Test{stem}.java"],
            "kotlin": [f"{stem}Test.kt", f"{stem}Tests.kt", f"{stem}IT.kt"],
            "python": [f"test_{stem}.py", f"{stem}_test.py"],
            "ts": [f"{stem}.test{ext}", f"{stem}.spec{ext}", f"{stem}.int.test{ext}"],
            "csharp": [f"{stem}Tests.cs", f"{stem}Test.cs"],
            "go": [f"{stem}_test.go"]}.get(lang, [])


def testable(e, lang):
    """True for a public function or method with behaviour a test must exercise."""
    kind, name, _line, overrides = e
    if kind not in ("function", "method") or overrides or name in NOT_TESTABLE:
        return False
    if lang in ("java", "kotlin", "csharp") and ACCESSOR.match(name):
        return False
    return not (lang == "python" and name.startswith("__"))


def check_production(path, ranges=None, root=None):
    """Findings for one production file. With ranges, only elements and imports inside the edited lines count."""
    lang = doc_check.LANG.get(os.path.splitext(path)[1].lower())
    if not lang or is_test_path(path) or generated(path) or "experiments" in re.split(r"[\\/]", path):
        return []
    root = root or project_root(path)
    if not root:
        return []
    try:
        src = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return []
    in_scope = (lambda ln: True) if ranges is None else (lambda ln: any(a <= ln <= b for a, b in ranges))
    elems = [e for e in doc_check.public_elements(path) if testable(e, lang) and in_scope(e[2])]
    bmatch = [m for m in BOUNDARY[lang].finditer(src) if in_scope(src.count("\n", 0, m.start()) + 1)] \
        if lang in BOUNDARY else []
    if not elems and not bmatch:
        return []
    tests = test_files(root)
    names = subject_names(path, lang)
    expected = expected_test_files(path, lang)
    by_name = [t for t in tests if os.path.basename(t) in expected]
    related = {t: x for t, x in tests.items() if t in by_name or any(re.search(rf"\b{re.escape(n)}\b", x) for n in names)}
    if lang == "go":                                  # Go tests live beside the code, in the same package
        related.update({t: x for t, x in tests.items() if os.path.dirname(t) == os.path.dirname(path)})
    rel = os.path.relpath(path, root)
    out = []
    if not related:
        out.append(finding(path, 1, "error", "missing-test-file",
                           f"no test for {rel}: expected {' or '.join(expected[:2])} with tests of its public behaviour",
                           key="testfile"))
    corpus = "\n".join(related.values())
    for kind, name, line, _ in elems:
        called = re.search(rf"(\b|\.|::){re.escape(name)}\s*[(<\[]|::{re.escape(name)}\b|\.{re.escape(name)}\b",
                           corpus)
        if not called:                      # with no test file at all, every element is still an obligation
            out.append(finding(path, line, "error", "untested",
                               f"no test calls {kind} '{name}': cover its normal case, a boundary and a failure path",
                               key=f"untested {name}"))
    if bmatch:
        integration = {t: x for t, x in related.items() if INTEGRATION_NAME.search(t) or INTEGRATION_MARK.search(x)}
        if not integration:
            line = src.count("\n", 0, bmatch[0].start()) + 1
            what = bmatch[0].group(0).strip().split()[-1].strip("'\";()")[:40]
            out.append(finding(path, line, "error", "missing-integration-test",
                               f"{rel} talks to an external system ({what}) but no integration test exercises it "
                               "against the real thing (Testcontainers, a *IT test, pytest.mark.integration …)",
                               key="integration"))
    return out


TEST_METHOD = {
    "java": re.compile(r"@(Test|ParameterizedTest|RepeatedTest|TestFactory)\b"),
    "kotlin": re.compile(r"@(Test|ParameterizedTest)\b"),
    "python": re.compile(r"^[ \t]*(async[ \t]+)?def[ \t]+test_\w+", re.M),   # [ \t], not \s: never across lines
    "ts": re.compile(r"\b(it|test)\s*\(\s*['\"`]"),
}
ASSERTION = re.compile(r"\bassert|\bverify\s*\(|\bexpect\s*\(|\bfail\s*\(|\.should|pytest\.raises|assertThat|"
                       r"assertThrows|assertEquals|\bthen\s*\(|\.toBe|\.toEqual|\.toThrow|StepVerifier")
DISABLED = re.compile(r"@Disabled\b(\(\s*\))?(?!\s*\()|@Ignore\b(?!\s*\()|pytest\.mark\.skip\b(?!\s*\(\s*reason)|"
                      r"\b(it|test|describe)\.skip\(|\bxit\(|t\.Skip\(\s*\)")
TICKET = re.compile(r"[A-Z][A-Z0-9]+-\d+|#\d+|https?://")


def blocks(src, starts, lang):
    """Yield (line, body) for each test starting at the given offsets: up to the end of its body."""
    for st in starts:
        if lang == "python":
            m = re.compile(r"^([ \t]*)(async[ \t]+)?def[ \t]", re.M).search(src, st)
            if not m:
                continue
            indent = len(m.group(1))
            lines = src[m.start():].split("\n")
            body = [lines[0]]
            for ln in lines[1:]:
                if ln.strip() and len(ln) - len(ln.lstrip()) <= indent:
                    break
                body.append(ln)
            yield src.count("\n", 0, m.start()) + 1, "\n".join(body)
        else:
            i = src.find("{", st)
            if i < 0:
                continue
            depth, j = 0, i
            while j < len(src):
                depth += {"{": 1, "}": -1}.get(src[j], 0)
                if depth == 0:
                    break
                j += 1
            yield src.count("\n", 0, st) + 1, src[st:j + 1]


def check_test_file(path):
    """Warnings for one test file: tests that assert nothing, sleep, are disabled without a ticket, or mock their subject."""
    lang = doc_check.LANG.get(os.path.splitext(path)[1].lower())
    if not lang:
        return []
    try:
        src = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return []
    out = []
    if lang in TEST_METHOD:
        for line, body in blocks(src, [m.start() for m in TEST_METHOD[lang].finditer(src)], lang):
            if not ASSERTION.search(body):
                out.append(finding(path, line, "warning", "no-assertion",
                                   "this test asserts nothing, so it cannot fail when the behaviour breaks"))
    for m in re.finditer(r"Thread\.sleep\(|time\.sleep\(|\bsleep\(\d|setTimeout\([^)]*\d{3,}\)", src):
        out.append(finding(path, src.count("\n", 0, m.start()) + 1, "warning", "sleep",
                           "a test that sleeps is slow and flaky: inject a clock or wait on a condition"))
    for m in DISABLED.finditer(src):
        ln = src.count("\n", 0, m.start()) + 1
        if not TICKET.search(src.split("\n")[ln - 1]):
            out.append(finding(path, ln, "warning", "disabled",
                               "a disabled test needs a reason and a ticket, e.g. @Disabled(\"PAY-42: flaky until …\")"))
    stem = os.path.splitext(os.path.basename(path))[0]
    subject = re.sub(r"(Test|Tests|IT|IntegrationTest)$", "", stem)
    if lang in ("java", "kotlin") and subject and subject != stem:
        m = re.search(rf"(mock|spy|mockk)\(\s*{re.escape(subject)}(::class)?(\.class)?\s*\)|@(Mock|Spy|MockK)\s+"
                      rf"(private\s+|lateinit\s+var\s+\w+\s*:\s*)?{re.escape(subject)}\b", src)
        if m:
            out.append(finding(path, src.count("\n", 0, m.start()) + 1, "warning", "mocks-subject",
                               f"{stem} mocks {subject}, the class it tests: test the real class and mock its collaborators"))
    return out


def check_path(path):
    """All findings for one file, production or test."""
    return check_test_file(path) if is_test_path(path) else check_production(path)


def main():
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    if sys.argv[1:2] == ["selftest"]:
        return selftest()
    ap = argparse.ArgumentParser(description="Check that code is accompanied by tests.")
    ap.add_argument("paths", nargs="+"); ap.add_argument("--json", action="store_true")
    ap.add_argument("--errors-only", action="store_true")
    a = ap.parse_args()
    res = [f for p in doc_check.walk(a.paths) if doc_check.LANG.get(os.path.splitext(p)[1].lower())
           for f in check_path(p)]
    if a.errors_only:
        res = [f for f in res if f["severity"] == "error"]
    if a.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        for f in res:
            print(f"{f['file']}:{f['line']}: {f['severity']} [{f['rule']}] {f['message']}")
        e = sum(f["severity"] == "error" for f in res)
        print(f"\n{e} error(s), {len(res) - e} warning(s)" + ("" if e else " — the code is accompanied by tests"))
    return 1 if any(f["severity"] == "error" for f in res) else 0


# ------------------------------------------------------------------------------------------- selftest
FIX = {
    "jproj/pom.xml": "<project/>",
    "jproj/src/main/java/demo/Calc.java": '''package demo;

/** Arithmetic. */
public class Calc {
    /** @param a a @param b b @return sum */
    public int add(int a, int b) { return a + b; }

    /** @param a a @param b b @return quotient */
    public int divide(int a, int b) { return a / b; }

    /** @return the name */
    public String getName() { return "calc"; }

    @Override
    public String toString() { return "Calc"; }
}
''',
    "jproj/src/main/java/demo/JdbcRepo.java": '''package demo;

import java.sql.Connection;

/** Stores things. */
public class JdbcRepo {
    /** @param id the id */
    public void save(String id) { }
}
''',
    "jproj/src/main/java/demo/Shape.java": '''package demo;

/** A shape. */
public interface Shape {
}
''',
    "jproj/src/test/java/demo/CalcTest.java": '''package demo;

import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import static org.mockito.Mockito.mock;

class CalcTest {
    private final Calc calc = new Calc();

    @Test
    void adds() {
        assertEquals(3, calc.add(1, 2));
    }

    @Test
    void logsOnly() throws Exception {
        Thread.sleep(500);
        System.out.println(calc.add(0, 0));
    }

    @Disabled
    @Test
    void later() { assertEquals(1, 1); }

    @Test
    void mocked() {
        Calc c = mock(Calc.class);
        assertEquals(0, c.add(1, 1));
    }
}
''',
    "pproj/pyproject.toml": "[project]\nname='p'\n",
    "pproj/pkg/store.py": '"""Storage."""\nimport sqlite3\n\n\ndef save(x):\n    """Save x."""\n    return x\n\n\n'
                          'def load(x):\n    """Load x."""\n    return x\n',
    "pproj/pkg/util.py": '"""Utilities."""\n\n\ndef helper(x):\n    """Help with x."""\n    return x\n',
    "pproj/tests/test_store.py": "from pkg import store\n\n\ndef test_save():\n    assert store.save(1) == 1\n",
    "pproj/tests/integration/test_store_db.py": "import pytest\nfrom pkg import store\n\n\n@pytest.mark.integration\n"
                                                "def test_load_from_db():\n    assert store.load(2) == 2\n",
    "gproj/go.mod": "module g\n",
    "gproj/money.go": "package g\n\n// Total sums.\nfunc Total(a int) int { return a }\n\n// Half halves.\nfunc Half(a int) int { return a / 2 }\n",
    "gproj/money_test.go": 'package g\n\nimport "testing"\n\nfunc TestTotal(t *testing.T) {\n\tif Total(1) != 1 {\n\t\tt.Fatal("x")\n\t}\n}\n',
    "tproj/package.json": "{}",
    "tproj/src/price.ts": "/** Price. @param a a */\nexport function price(a: number): number { return a; }\n",
    "pproj/tests/test_quality.py": 'from pkg import store\n\n\ndef test_asserts():\n    assert store.save(1) == 1\n\n\n'
                                   'def test_prints_only():\n    print(store.load(2))\n',
    "loose/script.py": '"""A one-off script."""\n\n\ndef run(x):\n    """Run."""\n    return x\n',
}


def selftest():
    import tempfile
    d = tempfile.mkdtemp(prefix="test-check-selftest-")
    for name, text in FIX.items():
        p = os.path.join(d, name)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(text)
    J = lambda n: os.path.join(d, n)
    rules = lambda fs: {(f["rule"], f["key"]) for f in fs}
    checks = []

    def ok(name, cond):
        checks.append((name, bool(cond)))

    calc = rules(check_production(J("jproj/src/main/java/demo/Calc.java")))
    ok("java: a public method no test calls is an error; tested ones, accessors and overrides are not",
       ("untested", "untested divide") in calc and not {k for _, k in calc} & {"untested add", "untested getName",
                                                                              "untested toString"})
    repo = rules(check_production(J("jproj/src/main/java/demo/JdbcRepo.java")))
    ok("java: no test file is an error, and JDBC code without an integration test is an error",
       ("missing-test-file", "testfile") in repo and ("missing-integration-test", "integration") in repo)
    ok("java: an interface without behaviour needs no test", not check_production(J("jproj/src/main/java/demo/Shape.java")))
    tq = {f["rule"] for f in check_test_file(J("jproj/src/test/java/demo/CalcTest.java"))}
    ok("java tests: no assertion, sleep, unexplained @Disabled and mocking the subject are warnings",
       {"no-assertion", "sleep", "disabled", "mocks-subject"} <= tq)
    st = rules(check_production(J("pproj/pkg/store.py")))
    ok("python: tested functions with an integration test pass", not st)
    ut = rules(check_production(J("pproj/pkg/util.py")))
    ok("python: a module with no test is an error", ("missing-test-file", "testfile") in ut)
    ok("go: tests beside the code count; an exported function none of them calls is an error",
       rules(check_production(J("gproj/money.go"))) == {("untested", "untested Half")})
    ok("typescript: an exported function with no test file is an error",
       ("missing-test-file", "testfile") in rules(check_production(J("tproj/src/price.ts"))))
    pq = check_test_file(J("pproj/tests/test_quality.py"))
    ok("python tests: a test that asserts passes; one that only prints is a warning, on the right line",
       [(f["rule"], f["line"]) for f in pq] == [("no-assertion", 8)])
    ok("code outside any project is not held to the standard", not check_production(J("loose/script.py")))
    scoped = check_production(J("jproj/src/main/java/demo/Calc.java"), ranges=[(5, 6)])
    ok("edit scope: only the edited method counts", not scoped)
    for n, good in checks:
        print(f"  {'pass' if good else 'FAIL'}  {n}")
    bad = sum(1 for _, g in checks if not g)
    print(f"\n{len(checks) - bad} of {len(checks)} checks passed")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
