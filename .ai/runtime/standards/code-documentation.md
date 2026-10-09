# Source code documentation standard

Every agent that writes or changes source code follows this standard. It
is enforced, not advisory: a hook checks each source file Claude writes,
Claude cannot finish a turn while public API it wrote is undocumented,
reviews apply it as criterion C8, and the CI configurations at the end
make it a build failure in your own pipeline.

## Principles

1. **Document the contract, not the implementation.** A doc comment says
what an element is for, what it accepts, what it returns, what it
throws, and what it assumes or guarantees: nullability, units, ranges,
side effects, thread safety, ownership of resources. Someone calling it
should never need to read its body.
2. **Every public element is documented** — in the language's own
doc-comment format, so that the language's tools (Javadoc, Sphinx,
TypeDoc, DocFX, godoc, Dokka) render it.
3. **Inline comments say *why*, never *what*.** The code already says
what it does. A comment earns its place by explaining a decision the
reader could not reconstruct: a constraint, a trade-off, a non-obvious
invariant, a workaround and its reason, a reference to a specification
or ticket.
4. **No narration, no dead code.** Comments such as "here is the block
for X", "step 3: loop over the items", "now we validate", or their
equivalents in any language, are removed. Commented-out code is deleted
— version control keeps it. A `TODO` names a ticket or an owner.
5. **Document what you write or change.** A new file is documented in
full. When you change an existing element's signature or behaviour, its
documentation is brought up to date in the same change. Documenting
untouched legacy code is separate work, proposed rather than done
silently.

## Per language

| Language | Format | Required on | Must state | Reference |
| --- | --- | --- | --- | --- |
| Java | Javadoc `/** … */` | every public class, interface, enum, record and annotation type, and every public or protected member of a public type; members of interfaces | summary sentence; `@param` for every parameter, type parameter and record component; `@return` (or `{@return …}`) for non-void methods; `@throws` for every declared and documented runtime exception | Oracle, *How to Write Doc Comments for the Javadoc Tool*; Google Java Style Guide §7 |
| Kotlin | KDoc `/** … */` | every declaration not `private` or `internal` | summary; `@param`, `@return`, `@throws` where they apply | Kotlin coding conventions, *Documentation comments* |
| Python | docstrings | every module; every public class, function and method of a library module | summary line; parameters, return value and raised exceptions, in one consistent style (Google, NumPy or reST) | PEP 257; PEP 8 |
| TypeScript, JavaScript | TSDoc / JSDoc `/** … */` | every exported function, class, interface, type, enum and constant | summary; `@param` for every parameter; `@returns`; `@throws` | TSDoc specification; JSDoc |
| C# | XML documentation `///` | every public or protected type and member | `<summary>`; `<param>` for every parameter; `<returns>`; `<exception>` | Microsoft, *XML documentation comments* |
| Go | doc comments `//` directly above | every exported identifier; each package once | begins with the identifier's name, as a full sentence | *Go Doc Comments* (go.dev/doc/comment) |

Shell scripts carry a header comment: purpose, usage, inputs, outputs
and exit codes. SQL migrations state what they change and whether they
can be reversed.

## Java example

```java
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.List;

/**
 * Computes invoice totals, applying the volume discount defined by the pricing policy.
 *
 * <p>Amounts are exact: all arithmetic uses {@link java.math.BigDecimal} with two decimal places and
 * {@link java.math.RoundingMode#HALF_EVEN}. Instances are immutable and thread-safe.
 *
 * @since 1.2
 */
public final class InvoiceCalculator {

    /** Subtotal from which the volume discount applies, inclusive, in euros. */
    public static final BigDecimal DISCOUNT_THRESHOLD = new BigDecimal("1000.00");

    private static final BigDecimal DISCOUNT_FACTOR = new BigDecimal("0.95");

    /**
     * Returns the total of the given lines after the volume discount.
     *
     * @param lines the invoice lines; must not be {@code null}, may be empty
     * @return the total, never negative, rounded to two decimal places
     * @throws IllegalArgumentException if a line has a negative quantity or unit price
     */
    public BigDecimal total(List<InvoiceLine> lines) {
        BigDecimal subtotal = BigDecimal.ZERO;
        for (InvoiceLine line : lines) {
            subtotal = subtotal.add(line.amount());
        }
        // The policy grants the discount from the threshold inclusive (PRICING-114); ">=" is deliberate.
        if (subtotal.compareTo(DISCOUNT_THRESHOLD) >= 0) {
            subtotal = subtotal.multiply(DISCOUNT_FACTOR);
        }
        return subtotal.setScale(2, RoundingMode.HALF_EVEN);
    }
}
```

`InvoiceLine` is assumed to be a documented record with an `amount()`
accessor. The only inline comment explains a decision and cites its
source. A comment such as `// loop over the lines` or `// here is the
discount block` would be removed.

## Exemptions

- **Tests:** test classes and methods need no API documentation; a
test's name says what it verifies. A non-obvious fixture or setup still
gets a *why* comment.
- **Overrides:** a method that overrides or implements a documented one
inherits its documentation (`@Override` in Java, `override` in Kotlin
and C#), unless its behaviour differs.
- **Generated code** and vendored third-party code.
- **Prototypes** in `experiments/`: a module or file header stating
purpose and status is enough; they never ship.

## How it is enforced

| Layer | What it does |
| --- | --- |
| `doc_check.py` | deterministic check: missing doc comments on public elements, missing `@param` / `@return` / `@throws`, missing module docstrings; narration, commented-out code and untracked `TODO`s as warnings |
| hook after every file write | runs `doc_check.py` on what Claude just wrote or changed and shows the result to Claude at once |
| hook when Claude finishes | Claude cannot end its turn while public API it wrote is undocumented; on a second attempt it may, and the remaining items are shown to you |
| review criterion C8 | `/review` applies this standard; findings go to the ledger and `/rework` fixes them |
| your CI | the configurations below make it a build failure, which no agent can bypass |

`doc_check.py` is a fast heuristic: it reads declarations line by line
rather than compiling, so a very unusual layout can escape it. The
compiler-grade checks are the CI configurations. To switch the hooks off
for one project, create an empty file `.ai/no-doc-check` in it.

## CI configurations

**Java — javac doclint**, in Maven (`maven-compiler-plugin`):

```xml
<compilerArgs>
  <arg>-Xdoclint:all</arg>
  <arg>-Werror</arg>
</compilerArgs>
```

**Java — Checkstyle**, in addition or instead:

```xml
<module name="MissingJavadocType"><property name="scope" value="protected"/></module>
<module name="MissingJavadocMethod">
  <property name="scope" value="protected"/>
  <property name="allowMissingPropertyJavadoc" value="false"/>
</module>
<module name="JavadocMethod">
  <property name="validateThrows" value="true"/>
</module>
<module name="JavadocType"/>
<module name="JavadocStyle"/>
<module name="TodoComment"><property name="format" value="TODO(?!\s*\(?[A-Z]+-\d+)"/></module>
```

**Python — Ruff**, in `pyproject.toml`:

```toml
[tool.ruff.lint]
extend-select = ["D", "ERA"]        # pydocstyle; eradicate (commented-out code)
[tool.ruff.lint.pydocstyle]
convention = "google"
```

**TypeScript — ESLint** with `eslint-plugin-jsdoc`: enable
`jsdoc/require-jsdoc` for exported declarations (`publicOnly: true`),
`jsdoc/require-param`, `jsdoc/require-returns`,
`jsdoc/check-param-names`.

**C#** — set
`<GenerateDocumentationFile>true</GenerateDocumentationFile>` and treat
warning `CS1591` as an error.

**Kotlin** — detekt rules `UndocumentedPublicClass`,
`UndocumentedPublicFunction`, `UndocumentedPublicProperty`.

**Go** — `revive` with the `exported` rule.
