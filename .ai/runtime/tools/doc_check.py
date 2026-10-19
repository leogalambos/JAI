#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Check source files against the code documentation standard (it-role-library/standards/code-documentation.md).

Errors — the standard's requirements:
    missing-doc       a public element without a doc comment (Javadoc, KDoc, docstring, TSDoc, XML doc, godoc)
    missing-param     a parameter, type parameter or record component the doc comment does not describe
    missing-return    a non-void method or function whose doc comment does not describe its result
    missing-throws    a declared exception the doc comment does not describe
    missing-module    a Python module without a module docstring
Warnings — judgement calls, shown so they can be fixed:
    narration         a comment that narrates what the code does ("here is the block for…", "step 3", "now we…")
    commented-code    code left in a comment
    untracked-todo    a TODO or FIXME without a ticket or owner
    weak-doc          a Go doc comment that does not start with the identifier; Python parameters not described

    doc_check.py PATH... [--json] [--errors-only]      files or folders; exit 1 if any error
    doc_check.py selftest

Python is parsed with its own parser, so its results are exact. The other languages are read line by line:
fast, dependency-free and right for ordinary code, but an unusual layout can escape it — the compiler-grade
checks belong in CI (see the standard). Tests, generated code and vendored code are skipped.
"""
import argparse
import ast
import io
import json
import os
import re
import signal
import sys
import tokenize

for _s in (sys.stdin, sys.stdout, sys.stderr):  # Windows consoles default to a code page, not UTF-8
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")
sys.argv = [a.encode("utf-8", "surrogateescape").decode("utf-8", "replace") for a in sys.argv]

LANG = {".java": "java", ".kt": "kotlin", ".kts": "kotlin", ".py": "python", ".ts": "ts", ".tsx": "ts",
        ".js": "ts", ".jsx": "ts", ".mjs": "ts", ".cs": "csharp", ".go": "go"}
SKIP_DIRS = {"node_modules", "vendor", "third_party", "generated", "build", "target", "dist", "out", ".venv",
             "venv", ".git", "__pycache__", ".gradle", "bin", "obj"}
TEST_DIRS = {"test", "tests", "__tests__", "spec", "testdata", "testing"}
TEST_FILE = re.compile(r"(^test_.*\.py$|_test\.(py|go)$|(Test|Tests|IT)\.(java|kt|cs)$|\.(test|spec)\.[jt]sx?$)")

NARRATION = [re.compile(p, re.I) for p in (
    r"^(here|this)\s+(is|are|we|comes)\b",
    r"^(this|the following|next)\s+(block|section|part|code|loop|snippet|chunk)\b",
    r"^step\s*\d+\b",
    r"^(now|next|then|first|finally|afterwards),?\s+(we|let'?s|i)\b",
    r"^let'?s\b",
    r"^we\s+(now|then|next|first|need to|will|are going to)\b",
    r"^(start|end|beginning)\s+of\s+(the\s+)?(block|section|loop|function|method|code)\b",
    r"^(block|section|part)\s+(for|about|handling|dealing|related)\b",
)]
CODE_IN_COMMENT = re.compile(
    r"^\s*((if|for|while|return|import|from|def|class|public|private|protected|var|let|const|val|fun|func|"
    r"package|try|catch|switch|case)\b.*[;:{(=)]\s*$|[\w.\]\)]+\s*(=|\+=|-=)\s*[^=].*;\s*$|\w+\(.*\);\s*$|^\s*[{}]\s*$)")
TICKET = re.compile(r"([A-Z][A-Z0-9]+-\d+|#\d+|https?://|\(\w[\w.-]*\)|@\w+)")


class Finding(dict):
    """One result: file, line, severity, rule, element and message."""


def finding(path, line, sev, rule, msg, key=""):
    return Finding(file=path, line=line, severity=sev, rule=rule, message=msg, key=key)


def excluded(path):
    """True for tests, generated and vendored code, which the standard exempts."""
    parts = re.split(r"[\\/]", os.path.normpath(path))
    if any(p in SKIP_DIRS or p in TEST_DIRS for p in parts[:-1]):
        return True
    return bool(TEST_FILE.search(parts[-1])) or "src/test/" in path.replace("\\", "/")


# ------------------------------------------------------------------------------------------- comments
def comment_findings(path, comments):
    """Warnings for narration, commented-out code and untracked TODOs; comments is [(line, text)]."""
    out = []
    for line, text in comments:
        t = text.strip()
        if not t or re.fullmatch(r"[-=*#/~_ ]{3,}.*", t) and re.match(r"[-=*#/~_ ]{3,}", t):
            continue                                     # a banner or separator line, not prose
        if re.match(r"(TODO|FIXME|XXX)\b", t, re.I) and not TICKET.search(t):
            out.append(finding(path, line, "warning", "untracked-todo",
                               f"'{t[:60]}' — a TODO names a ticket or an owner, e.g. TODO(PAY-123)"))
        elif any(p.search(t) for p in NARRATION):
            out.append(finding(path, line, "warning", "narration",
                               f"'{t[:60]}' narrates what the code does; say why, or delete it"))
        elif CODE_IN_COMMENT.search(t):
            out.append(finding(path, line, "warning", "commented-code",
                               f"'{t[:60]}' looks like code left in a comment; delete it (version control keeps it)"))
    return out


# ---------------------------------------------------------------------------------------------- Python
def check_python(path, src, decls=None):
    out = []
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return [finding(path, e.lineno or 1, "error", "syntax", f"cannot parse: {e.msg}")]
    script = any(isinstance(n, ast.If) and "__main__" in ast.dump(n.test) for n in tree.body)
    empty_init = os.path.basename(path) == "__init__.py" and not src.strip()
    if not ast.get_docstring(tree) and not empty_init:
        out.append(finding(path, 1, "error", "missing-module", "the module has no docstring stating its purpose",
                           key="module"))
    sev = "warning" if script else "error"         # functions of a script are not exported (PEP 257)

    def params(fn):
        a = fn.args
        names = [x.arg for x in a.posonlyargs + a.args + a.kwonlyargs]
        return [n for n in names if n not in ("self", "cls")]

    def visit(body, prefix, public_scope):
        for n in body:
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                public = public_scope and not n.name.startswith("_")
                kind = "class" if isinstance(n, ast.ClassDef) else "function"
                key = f"{kind} {prefix}{n.name}"
                if public and decls is not None:
                    decls.append((kind, n.name, n.lineno, False))
                doc = ast.get_docstring(n)
                if public and not doc:
                    out.append(finding(path, n.lineno, sev, "missing-doc",
                                       f"public {kind} '{prefix}{n.name}' has no docstring", key=key))
                elif public and doc and kind == "function":
                    missing = [p for p in params(n) if not re.search(rf"\b{re.escape(p)}\b", doc)]
                    if missing:
                        out.append(finding(path, n.lineno, "warning", "weak-doc",
                                           f"docstring of '{prefix}{n.name}' does not describe: {', '.join(missing)}",
                                           key=key))
                if isinstance(n, ast.ClassDef):
                    visit(n.body, f"{prefix}{n.name}.", public)
    visit(tree.body, "", True)
    comments = []
    try:
        for tok in tokenize.generate_tokens(io.StringIO(src).readline):
            if tok.type == tokenize.COMMENT and not tok.string.startswith("#!"):
                comments.append((tok.start[0], tok.string.lstrip("#")))
    except (tokenize.TokenError, IndentationError):
        pass
    return out + comment_findings(path, comments)


# ---------------------------------------------------------------- C-family: Java, Kotlin, TS/JS, C#, Go
def strip_strings(line):
    return re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|`(?:\\.|[^`\\])*`', '""', line)


def split_comments(src, lang):
    """-> (code lines with comments blanked, {line: doc text ending there}, [(line, line-comment text)])."""
    lines = src.split("\n")
    code, docs, comments = [], {}, []
    in_block, block_is_doc, block_text = False, False, []
    for i, raw in enumerate(lines, 1):
        line = raw
        out = ""
        j = 0
        while j < len(line):
            if in_block:
                end = line.find("*/", j)
                if end < 0:
                    block_text.append(line[j:]); j = len(line); break
                block_text.append(line[j:end])
                if block_is_doc:
                    docs[i] = "\n".join(block_text)
                in_block = False; j = end + 2
                continue
            rest = strip_strings(line[j:])
            k_block = rest.find("/*")
            k_line = rest.find("//")
            if k_line >= 0 and (k_block < 0 or k_line < k_block):
                out += rest[:k_line]
                text = rest[k_line + 2:]
                if lang == "csharp" and text.startswith("/"):
                    docs.setdefault(i, "")
                    docs[i] = text[1:]
                    docs[-i] = "xmldoc"
                elif lang == "go":
                    comments.append((i, text)); docs[i] = text; docs[-i] = "line"
                else:
                    comments.append((i, text))
                j = len(line)
                continue
            if k_block >= 0:
                out += rest[:k_block]
                block_is_doc = rest[k_block:k_block + 3] == "/**" and rest[k_block:k_block + 4] != "/**/"
                in_block, block_text = True, []
                j = j + k_block + (3 if block_is_doc else 2)
                continue
            out += rest; j = len(line)
        code.append(out)
    return code, docs, comments


def doc_before(code, docs, idx, lang):
    """The doc comment that belongs to the declaration on line idx (1-based), or None."""
    k = idx - 1
    while k >= 1 and (not code[k - 1].strip() or re.match(r"\s*@\w+(\(.*\))?\s*$", code[k - 1])
                      or re.match(r"\s*\[[\w.(), =\"]+\]\s*$", code[k - 1])):
        if docs.get(k) is not None and docs.get(-k) is None:
            return docs[k]                                  # a /** */ ending on this line
        if lang == "csharp" and docs.get(-k) == "xmldoc":
            texts = []
            while k >= 1 and docs.get(-k) == "xmldoc":
                texts.insert(0, docs[k]); k -= 1
            return "\n".join(texts)
        if lang == "go" and docs.get(-k) == "line":
            texts = []
            while k >= 1 and docs.get(-k) == "line":
                texts.insert(0, docs[k]); k -= 1
            return "\n".join(texts)
        k -= 1
    return None


def annotations_above(code, idx):
    """The annotations directly above the declaration on line idx: only those belong to it."""
    found, k = [], idx - 1
    while k >= 1:
        t = code[k - 1].strip()
        if re.match(r"@\w+(\(.*\))?$", t):
            found.append(t)
        elif t:
            break
        k -= 1
    return " ".join(found)


def signature(code, idx):
    """Join the declaration starting at line idx until its parameter list closes."""
    text, depth, i = "", 0, idx
    while i <= len(code):
        text += " " + code[i - 1]
        depth = text.count("(") - text.count(")")
        if "(" in text and depth <= 0 or ("(" not in text and re.search(r"[{;=]", code[i - 1])):
            break
        i += 1
        if i - idx > 30:
            break
    return text


def param_names(sig, lang):
    m = re.search(r"\((.*)\)", sig, re.S)
    if not m or not m.group(1).strip():
        return []
    depth, cur, parts = 0, "", []
    for ch in m.group(1):
        depth += ch in "<([{"
        depth -= ch in ">)]}"
        if ch == "," and depth == 0:
            parts.append(cur); cur = ""
        else:
            cur += ch
    parts.append(cur)
    names = []
    for p in parts:
        p = re.sub(r"@\w+(\([^)]*\))?\s*", "", p).strip()
        p = p.split("=")[0].strip()
        if not p:
            continue
        if lang in ("kotlin", "ts"):
            n = re.split(r"\s*[:?]", p.replace("...", "").replace("vararg ", "").strip())[0].split()[-1]
        elif lang == "go":
            n = p.split()[0]
        else:
            n = re.sub(r"\.\.\.", " ", p).split()[-1]
        names.append(n.strip("&*"))
    return [n for n in names if re.match(r"^[A-Za-z_]\w*$", n)]


def check_cfamily(path, src, lang, decls=None):
    code, docs, comments = split_comments(src, lang)
    out = []
    depth = 0
    types = []                                     # (kind, public, depth at which its body opened)

    def api_scope():
        return all(t[1] for t in types)

    pending = None
    for idx, line in enumerate(code, 1):
        s = line.strip()
        decl = None
        if lang == "java":
            m = re.match(r"(?:(?:@\w+(?:\([^)]*\))?)\s+)*((?:(?:public|protected|private|abstract|static|final|sealed|"
                         r"non-sealed|strictfp)\s+)*)(class|interface|enum|record|@interface)\s+(\w+)", s)
            if m:
                mods = m.group(0)
                in_iface = types and types[-1][0] in ("interface", "@interface") and depth == types[-1][2]
                public = bool(re.search(r"\b(public|protected)\b", mods)) or (in_iface and "private" not in mods)
                decl = ("type", m.group(2), m.group(3), public)
            elif types and depth == types[-1][2] and not s.startswith(("return", "new ", "throw", "else", "if", "for",
                                                                          "while", "switch", "case", "}")):
                in_iface = types[-1][0] in ("interface", "@interface")
                mm = re.match(r"((?:(?:public|protected|private|static|final|abstract|synchronized|native|default|"
                              r"strictfp)\s+)*)(<[^>]+>\s+)?([\w<>\[\],.? ]+?\s+)?(\w+)\s*\(", s)
                fm = re.match(r"((?:(?:public|protected|private|static|final|transient|volatile)\s+)+)"
                              r"([\w<>\[\],.? ]+?)\s+(\w+)\s*(=|;)", s)
                if mm and mm.group(4) not in ("if", "for", "while", "switch", "catch", "synchronized", "return"):
                    mods = mm.group(1) or ""
                    public = bool(re.search(r"\b(public|protected)\b", mods)) or (in_iface and "private" not in mods)
                    if mm.group(3) or mm.group(4) == types[-1][3]:       # a return type, or a constructor
                        decl = ("method", mm.group(3) or "", mm.group(4), public, mm.group(2))
                elif fm:
                    public = bool(re.search(r"\b(public|protected)\b", fm.group(1)))
                    decl = ("field", fm.group(2), fm.group(3), public)
            if decl and decl[3] and api_scope():
                overrides = decl[0] == "method" and "@Override" in annotations_above(code, idx)
                if decls is not None:
                    is_ctor = decl[0] == "method" and not decl[1].strip()
                    decls.append(("constructor" if is_ctor else decl[0], decl[2], idx, overrides))
                doc = doc_before(code, docs, idx, lang)
                key = f"{decl[0]} {decl[2]}"
                if doc is None and not overrides:
                    out.append(finding(path, idx, "error", "missing-doc", f"public {decl[1] if decl[0] == 'type' else decl[0]} "
                                       f"'{decl[2]}' has no Javadoc", key=key))
                elif doc is not None and decl[0] in ("method", "type") and not overrides:
                    sig = signature(code, idx)
                    names = param_names(sig, lang) if (decl[0] == "method" or decl[1] == "record") else []
                    tparams = re.findall(r"\w+", (decl[4] or "") if decl[0] == "method" else
                                         (re.search(rf"{decl[2]}\s*<([^>]+)>", sig) or [None, ""])[1])
                    tparams = [t for t in tparams if t[0].isupper() and len(t) <= 3 and t not in ("extends", "super")]
                    miss = [n for n in names if not re.search(rf"@param\s+{re.escape(n)}\b", doc)]
                    miss += [f"<{t}>" for t in tparams if not re.search(rf"@param\s+<{t}>", doc)]
                    if miss:
                        out.append(finding(path, idx, "error", "missing-param",
                                           f"Javadoc of '{decl[2]}' does not describe: {', '.join(miss)}", key=key))
                    if decl[0] == "method" and decl[1].strip() not in ("", "void") and \
                            not re.search(r"@return\b|\{@return\b", doc):
                        out.append(finding(path, idx, "error", "missing-return",
                                           f"Javadoc of '{decl[2]}' does not describe its return value", key=key))
                    th = re.search(r"\)\s*throws\s+([\w.,\s]+?)\s*[{;]", sig + " {")
                    for ex in (th.group(1).replace(" ", "").split(",") if th else []):
                        if ex and not re.search(rf"@(throws|exception)\s+(\w+\.)*{re.escape(ex.split('.')[-1])}\b", doc):
                            out.append(finding(path, idx, "error", "missing-throws",
                                               f"Javadoc of '{decl[2]}' does not describe the declared {ex}", key=key))
        elif lang == "kotlin":
            m = re.match(r"((?:(?:public|private|internal|protected|open|abstract|final|data|sealed|enum|inline|value|"
                         r"annotation|override|suspend|operator|infix|tailrec|external|inner|const|lateinit)\s+)*)"
                         r"(class|interface|object|fun)\s+(<[^>]+>\s+)?([\w.]+)", s)
            if m and (not types or depth == types[-1][2]):
                mods = m.group(1) or ""
                public = not re.search(r"\b(private|internal)\b", mods)
                decl = ("method" if m.group(2) == "fun" else "type", m.group(2), m.group(4).split(".")[-1], public,
                        "override" in mods)
                if public and api_scope() and decls is not None:
                    decls.append((decl[0], decl[2], idx, decl[4]))
                if public and api_scope() and not decl[4]:
                    doc = doc_before(code, docs, idx, lang)
                    key = f"{decl[0]} {decl[2]}"
                    if doc is None:
                        out.append(finding(path, idx, "error", "missing-doc",
                                           f"public {decl[1]} '{decl[2]}' has no KDoc", key=key))
                    elif decl[0] == "method":
                        miss = [n for n in param_names(signature(code, idx), lang)
                                if not re.search(rf"@param\s+{re.escape(n)}\b", doc)]
                        if miss:
                            out.append(finding(path, idx, "error", "missing-param",
                                               f"KDoc of '{decl[2]}' does not describe: {', '.join(miss)}", key=key))
        elif lang == "ts":
            m = re.match(r"export\s+(default\s+)?(declare\s+)?(async\s+)?(abstract\s+)?"
                         r"(function\*?|class|interface|type|enum|const|let|var)\s+(\w+)", s)
            if m and depth == 0:
                kind, name = m.group(5), m.group(6)
                if decls is not None:
                    decls.append(("function" if kind.startswith("function") or "=>" in signature(code, idx) else kind,
                                  name, idx, False))
                doc = doc_before(code, docs, idx, lang)
                key = f"{kind} {name}"
                if doc is None:
                    out.append(finding(path, idx, "error", "missing-doc", f"exported {kind} '{name}' has no TSDoc",
                                       key=key))
                elif kind.startswith("function") or (kind == "const" and "=>" in signature(code, idx)):
                    miss = [n for n in param_names(signature(code, idx), lang)
                            if not re.search(rf"@param\s+(\{{[^}}]*\}}\s*)?\[?{re.escape(n)}\b", doc)]
                    if miss:
                        out.append(finding(path, idx, "error", "missing-param",
                                           f"TSDoc of '{name}' does not describe: {', '.join(miss)}", key=key))
        elif lang == "csharp":
            m = re.match(r"((?:\[[^\]]*\]\s*)*)((?:(?:public|protected|internal|private|static|abstract|sealed|virtual|"
                         r"override|partial|readonly|async|new|extern|unsafe)\s+)*)"
                         r"(class|interface|struct|enum|record)\s+(\w+)", s)
            mm = None if m else re.match(r"((?:(?:public|protected|internal|private|static|abstract|sealed|virtual|"
                                         r"override|async|new|extern|unsafe)\s+)+)([\w<>\[\],.? ]+?\s+)?(\w+)\s*[(<]", s)
            if m or (mm and types and depth == types[-1][2]):
                mods = (m.group(2) if m else mm.group(1)) or ""
                public = bool(re.search(r"\b(public|protected)\b", mods))
                name = m.group(4) if m else mm.group(3)
                kind = m.group(3) if m else "method"
                if public and api_scope() and name not in ("if", "for", "while", "switch") and decls is not None:
                    decls.append(("method" if kind == "method" else "type", name, idx, "override" in mods))
                if public and api_scope() and "override" not in mods and name not in ("if", "for", "while", "switch"):
                    doc = doc_before(code, docs, idx, lang)
                    key = f"{kind} {name}"
                    if doc is None:
                        out.append(finding(path, idx, "error", "missing-doc",
                                           f"public {kind} '{name}' has no XML documentation", key=key))
                    elif kind == "method":
                        miss = [n for n in param_names(signature(code, idx), lang)
                                if not re.search(rf'<param\s+name="{re.escape(n)}"', doc)]
                        if miss:
                            out.append(finding(path, idx, "error", "missing-param",
                                               f"XML documentation of '{name}' has no <param> for: {', '.join(miss)}",
                                               key=key))
                        rt = (mm.group(2) or "").strip()
                        if rt and rt not in ("void", "Task") and "<returns>" not in doc:
                            out.append(finding(path, idx, "error", "missing-return",
                                               f"XML documentation of '{name}' has no <returns>", key=key))
                if m:
                    decl = ("type", kind, name, public)
        elif lang == "go":
            m = re.match(r"func\s+(\([^)]*\)\s*)?([A-Z]\w*)\s*[\[(]|(type|var|const)\s+([A-Z]\w*)\b", s)
            if m and depth == 0:
                name = m.group(2) or m.group(4)
                if decls is not None:
                    decls.append(("function" if m.group(2) else m.group(3), name, idx, False))
                doc = doc_before(code, docs, idx, lang)
                key = f"ident {name}"
                if doc is None:
                    out.append(finding(path, idx, "error", "missing-doc",
                                       f"exported identifier '{name}' has no doc comment", key=key))
                elif not doc.strip().startswith(name) and not re.match(rf"\s*(A|An|The)\s+{name}\b", doc):
                    out.append(finding(path, idx, "warning", "weak-doc",
                                       f"doc comment of '{name}' should begin with '{name}'", key=key))
        opens, closes = line.count("{"), line.count("}")
        if decl and decl[0] == "type":
            pending = (decl[1], decl[3], decl[2])
        if pending and opens:
            types.append((pending[0], pending[1], depth + 1, pending[2]))
            pending = None
        depth += opens - closes
        while types and depth < types[-1][2]:
            types.pop()
    return out + comment_findings(path, comments if lang != "go" else
                                  [(l, t) for l, t in comments if docs.get(-l) != "line" or True])


# --------------------------------------------------------------------------------------------- driver
def check_file(path, ranges=None):
    """All findings for one file. With ranges (a list of (first, last) lines), only declarations whose line falls
    inside one of them are reported, plus comment findings inside them: the scope of an edit."""
    lang = LANG.get(os.path.splitext(path)[1].lower())
    if not lang or excluded(path):
        return []
    try:
        src = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return []
    res = check_python(path, src) if lang == "python" else check_cfamily(path, src, lang)
    if "experiments" in re.split(r"[\\/]", path):        # prototypes: header-level documentation only
        res = [f if f["rule"] == "missing-module" else Finding(f, severity="warning") for f in res]
    if ranges is not None:
        res = [f for f in res if any(a <= f["line"] <= b for a, b in ranges) or f["rule"] == "missing-module"
               and any(a <= 1 for a, _ in ranges)]
    return sorted(res, key=lambda f: (f["line"], f["rule"]))


def public_elements(path):
    """The public declarations of a source file, as (kind, name, line, overrides), recognised exactly as the
    documentation check recognises them: kind is class, type, function, method, constructor, field, ...
    Used by test_check.py, so that both checks agree on what is public."""
    lang = LANG.get(os.path.splitext(path)[1].lower())
    if not lang:
        return []
    try:
        src = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return []
    decls = []
    if lang == "python":
        check_python(path, src, decls)
    else:
        check_cfamily(path, src, lang, decls)
    return decls


def walk(paths):
    for p in paths:
        if os.path.isdir(p):
            for dp, dirs, fs in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
                for f in sorted(fs):
                    yield os.path.join(dp, f)
        else:
            yield p


def main():
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    if sys.argv[1:2] == ["selftest"]:
        return selftest()
    ap = argparse.ArgumentParser(description="Check source documentation against the standard.")
    ap.add_argument("paths", nargs="+"); ap.add_argument("--json", action="store_true")
    ap.add_argument("--errors-only", action="store_true")
    a = ap.parse_args()
    res = [f for p in walk(a.paths) for f in check_file(p)]
    if a.errors_only:
        res = [f for f in res if f["severity"] == "error"]
    if a.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        for f in res:
            print(f"{f['file']}:{f['line']}: {f['severity']} [{f['rule']}] {f['message']}")
        e = sum(f["severity"] == "error" for f in res)
        print(f"\n{e} error(s), {len(res) - e} warning(s)" + ("" if e else " — documentation meets the standard"))
    return 1 if any(f["severity"] == "error" for f in res) else 0


# ------------------------------------------------------------------------------------------- selftest
FIX = {
"Bad.java": '''package demo;

import java.util.List;

public class Bad {
    public static final int LIMIT = 10;

    // here is the block for totals
    public int total(List<Integer> values) throws java.io.IOException {
        return 0;
    }

    /** Sums. */
    public <T> int sum(List<T> values, int start) {
        return start;
    }

    @Override
    public String toString() { return "x"; }

    public static int compute(int a) {
        return a;
    }

    private int helper(int x) { return x; }
}
''',
"Good.java": '''package demo;

import java.util.List;

/** Computes totals of invoice amounts. */
public final class Good {

    /** The largest number of lines accepted. */
    public static final int LIMIT = 10;

    /**
     * Creates a calculator.
     */
    public Good() {
    }

    /**
     * Returns the sum of the values, starting from an offset.
     *
     * @param <T> the element type
     * @param values the values to add; must not be {@code null}
     * @param start the starting offset
     * @return the sum
     * @throws IllegalStateException if the calculator is closed
     */
    public <T extends Number> int sum(List<T> values, int start) throws IllegalStateException {
        // Overflow is impossible here: LIMIT bounds the input size (PAY-12).
        return start;
    }

    /**
     * A record of one line.
     *
     * @param amount the amount in cents
     */
    public record Line(long amount) {
    }
}
''',
"bad.py": '''import os


def total(lines, rate):
    # Step 1: loop over lines
    # x = compute(lines);
    # TODO fix this later
    return 0


class Thing:
    def run(self, n):
        return n
''',
"good.py": '''"""Invoice arithmetic."""


def total(lines, rate):
    """Return the total of the lines after applying the rate.

    Args:
        lines: the invoice lines.
        rate: the discount rate, between 0 and 1.
    """
    # Rounded once at the end: rounding per line drifts by a cent on long invoices (PAY-7).
    return 0


def _private(x):
    return x
''',
"bad.ts": '''export function total(lines: Line[], rate: number): number {
  return 0;
}

/** Discounted. */
export const discount = (amount: number, rate: number): number => amount * rate;
''',
"good.ts": '''/**
 * Returns the total of the lines.
 * @param lines - the invoice lines
 * @param rate - the discount rate
 * @returns the total
 */
export function total(lines: Line[], rate: number): number {
  return 0;
}
''',
"Bad.cs": '''namespace Demo
{
    /// <summary>Totals.</summary>
    public class Calc
    {
        public int Total(int a, int b)
        {
            return a + b;
        }

        /// <summary>Adds.</summary>
        public int Add(int a, int b) => a + b;

        public static int Max(int a, int b)
        {
            return a;
        }
    }
}
''',
"bad.go": '''package money

func Total(lines []int) int {
	return 0
}

// computes the sum
func Sum(a int) int { return a }

// Rate is the discount rate.
const Rate = 5
''',
"Bad.kt": '''package demo

class Calc {
    fun total(a: Int, b: Int): Int = a + b

    /** Adds [a]. */
    fun add(a: Int, b: Int): Int = a + b

    private fun helper() = 1

    private open fun hidden(a: Int) = a
}
''',
"tests/test_ignored.py": "def test_x():\n    assert True\n",
"narration.py": '''"""Module."""


def f():
    """Do it."""
    # section dealing with calculation
    return 1
''',
}


def selftest():
    import tempfile
    d = tempfile.mkdtemp(prefix="doc-check-selftest-")
    for name, text in FIX.items():
        p = os.path.join(d, name)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(text)
    got = {n: check_file(os.path.join(d, n)) for n in FIX}
    rules = lambda n, sev=None: sorted({(f["rule"], f["key"].split(" ")[-1]) for f in got[n]
                                        if sev is None or f["severity"] == sev})
    checks = []

    def ok(name, cond):
        checks.append((name, bool(cond)))

    jb = rules("Bad.java", "error")
    ok("java: undocumented public class, constant and method are errors",
       {("missing-doc", "Bad"), ("missing-doc", "LIMIT"), ("missing-doc", "total")} <= set(jb))
    ok("java: missing @param (including a type parameter) and @return are errors",
       ("missing-param", "sum") in jb and ("missing-return", "sum") in jb
       and any("<T>" in f["message"] for f in got["Bad.java"] if f["rule"] == "missing-param"))
    ok("java: @Override and private members are exempt", not any(k in ("toString", "helper") for _, k in jb))
    ok("java: 'public static' and 'public static final' members are recognised as public",
       ("missing-doc", "compute") in jb and ("missing-doc", "LIMIT") in jb)
    ok("java: narration is a warning", ("narration", "") in rules("Bad.java", "warning"))
    ok("java: a fully documented class passes, including a record's components and a declared exception",
       not [f for f in got["Good.java"] if f["severity"] == "error"])
    pb = rules("bad.py", "error")
    ok("python: no module docstring, and undocumented public function and class are errors",
       {("missing-module", "module"), ("missing-doc", "total"), ("missing-doc", "Thing")} <= set(pb))
    ok("python: step narration, commented-out code and an untracked TODO are warnings",
       {"narration", "commented-code", "untracked-todo"} <= {f["rule"] for f in got["bad.py"]})
    ok("python: a documented module passes; private helpers are exempt", not got["good.py"])
    ok("typescript: undocumented export and undocumented parameters are errors",
       ("missing-doc", "total") in rules("bad.ts") and ("missing-param", "discount") in rules("bad.ts"))
    ok("typescript: a documented export passes", not got["good.ts"])
    ok("c#: undocumented public method (also 'public static') and missing <param> are errors",
       ("missing-doc", "Total") in rules("Bad.cs") and ("missing-param", "Add") in rules("Bad.cs")
       and ("missing-doc", "Max") in rules("Bad.cs"))
    ok("go: undocumented export is an error; a comment not starting with the name is a warning",
       ("missing-doc", "Total") in rules("bad.go") and ("weak-doc", "Sum") in rules("bad.go")
       and ("missing-doc", "Rate") not in rules("bad.go"))
    ok("kotlin: undocumented public function and missing @param are errors; private is exempt",
       ("missing-doc", "total") in rules("Bad.kt") and ("missing-param", "add") in rules("Bad.kt")
       and not any(k in ("helper", "hidden") for _, k in rules("Bad.kt")))
    ok("tests are exempt", not got["tests/test_ignored.py"])
    ok("English section narration is recognised", any(f["rule"] == "narration" for f in got["narration.py"]))
    scoped = check_file(os.path.join(d, "Bad.java"), ranges=[(13, 17)])
    ok("edit scope: only declarations inside the edited lines are reported",
       scoped and all(13 <= f["line"] <= 17 for f in scoped) and len(scoped) < len(got["Bad.java"]))
    for n, good in checks:
        print(f"  {'pass' if good else 'FAIL'}  {n}")
    bad = sum(1 for _, g in checks if not g)
    print(f"\n{len(checks) - bad} of {len(checks)} checks passed")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
