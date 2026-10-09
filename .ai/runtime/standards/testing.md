# Testing standard

Code is not finished until it is tested. Every agent that writes or
changes production code writes the tests that go with it, in the same
change, and runs them. This is enforced: a hook checks that what Claude
wrote has tests, Claude cannot finish a turn in which it changed
production code without having run the tests afterwards and seen them
pass, reviews apply this as criterion C4, and the CI configurations
below make it a build failure.

## What accompanies a change

1. **Unit tests for every public behaviour added or changed**: the
normal case, the boundaries (empty, one, many, minimum, maximum,
exactly-at-threshold) and at least one failure path — the exception or
error the contract promises. A boundary named in a requirement gets a
test *at* the boundary.
2. **Integration tests for every boundary to the outside world** that
the change adds or alters: a database, an HTTP or gRPC service, a
message broker, the file system, a cache. They run against the real
thing in a container (Testcontainers) or a faithful local equivalent —
not against a mock of it.
3. **A regression test for every fixed defect**, written first and seen
to fail before the fix.
4. **The suite is run after the last change, and passes.** A failing
test is fixed, not deleted, weakened or disabled; a test is disabled
only with a ticket that says why and until when.

## How tests are written

- **One behaviour per test**, named for the behaviour:
`appliesDiscountFromThresholdInclusive`, not `testTotal2`.
- **Arrange, act, assert.** Assert on outcomes — the returned value, the
stored state, the thrown exception. Verify an interaction only when the
interaction *is* the behaviour (an e-mail is sent, an event is
published).
- **Deterministic and independent.** No `sleep`; inject a clock, a
random seed, an id generator. No order dependence; no shared mutable
state between tests. A flaky test is a defect.
- **Fast unit tests.** Milliseconds each; no network, no database, no
file system. Anything slower is an integration test and is named and run
as one.
- **A test must be able to fail.** If breaking the code under test does
not break the test, the test is wrong. Mutation testing (PIT for Java,
mutmut for Python, Stryker for JavaScript) measures this.

## Mocks: when, and when not

Mock a **collaborator** at the edge of the unit — an interface the class
depends on, whose real implementation is slow, remote or
non-deterministic. Never mock:

- **the class under test**, or a value object, or a simple data class —
use the real one;
- **types you do not own** (a JDBC `Connection`, an HTTP client, an AWS
SDK client) in unit tests — wrap them in an interface you own and mock
that, and cover the wrapper with an integration test against the real
thing;
- **so much that the test only re-states the implementation.** If a test
mocks everything and verifies every call, it will break on every
refactoring and catch nothing.

Prefer a **fake** (an in-memory repository) to a mock where a
collaborator has real behaviour.

## Per language

| Language | Unit | Mocks | Integration | Naming and layout |
| --- | --- | --- | --- | --- |
| Java | JUnit 5 (Jupiter), AssertJ, `@ParameterizedTest` | Mockito with `MockitoExtension` | Testcontainers; Spring `@DataJpaTest` / `@SpringBootTest` slices | `src/test/java/.../FooTest.java` (Surefire); `FooIT.java` (Failsafe) |
| Kotlin | JUnit 5, kotest assertions | MockK | Testcontainers | as Java |
| Python | pytest, `@pytest.mark.parametrize` | `unittest.mock`, pytest-mock | pytest with `@pytest.mark.integration`, testcontainers-python | `tests/test_foo.py`; `tests/integration/` |
| TypeScript / JavaScript | Vitest or Jest | `vi.mock` / `jest.mock` | Testcontainers for Node, supertest | `foo.test.ts`; `foo.int.test.ts` |
| C# | xUnit or NUnit, FluentAssertions | NSubstitute or Moq | Testcontainers for .NET, `WebApplicationFactory` | `Foo.Tests` project, `FooTests.cs` |
| Go | `testing`, table-driven tests, testify | interfaces with hand-written fakes, gomock | testcontainers-go, `//go:build integration` | `foo_test.go` beside `foo.go` |

## Java examples

A unit test with boundaries and a failure path:

```java
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.math.BigDecimal;
import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

class InvoiceCalculatorTest {

    private final InvoiceCalculator calculator = new InvoiceCalculator();

    @ParameterizedTest(name = "subtotal {0} gives total {1}")
    @CsvSource({"999.99, 999.99", "1000.00, 950.00", "1000.01, 950.01"})
    @DisplayName("the discount applies from the threshold, inclusive")
    void appliesDiscountFromThresholdInclusive(String subtotal, String expected) {
        List<InvoiceLine> lines = List.of(new InvoiceLine(1, new BigDecimal(subtotal)));

        BigDecimal total = calculator.total(lines);

        assertThat(total).isEqualByComparingTo(expected);
    }

    @Test
    void anEmptyInvoiceTotalsZero() {
        assertThat(calculator.total(List.of())).isEqualByComparingTo(BigDecimal.ZERO);
    }

    @Test
    void rejectsANegativeQuantity() {
        List<InvoiceLine> lines = List.of(new InvoiceLine(-1, BigDecimal.TEN));

        assertThatThrownBy(() -> calculator.total(lines))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("quantity");
    }
}
```

A collaborator mocked at the edge of the unit — the repository, never
the service under test:

```java
import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class InvoiceServiceTest {

    @Mock
    private InvoiceRepository repository;

    @InjectMocks
    private InvoiceService service;

    @Test
    void onlyTheOwnerMayDeleteAnInvoice() {
        Invoice invoice = new Invoice("INV-1", "alice");
        when(repository.findById("INV-1")).thenReturn(Optional.of(invoice));

        boolean deleted = service.delete("bob", "INV-1");

        assertThat(deleted).isFalse();
    }

    @Test
    void theOwnerDeletesTheirInvoice() {
        Invoice invoice = new Invoice("INV-1", "alice");
        when(repository.findById("INV-1")).thenReturn(Optional.of(invoice));

        service.delete("alice", "INV-1");

        verify(repository).delete(invoice);              // here the interaction is the behaviour
    }
}
```

An integration test against a real database, run by Failsafe because its
name ends in `IT`:

```java
import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

@Testcontainers
class JdbcInvoiceRepositoryIT {

    @Container
    private static final PostgreSQLContainer<?> POSTGRES = new PostgreSQLContainer<>("postgres:16-alpine");

    private JdbcInvoiceRepository repository;

    @BeforeEach
    void connect() {
        repository = new JdbcInvoiceRepository(POSTGRES.getJdbcUrl(), POSTGRES.getUsername(), POSTGRES.getPassword());
        repository.migrate();
    }

    @Test
    void aCustomerNameWithAQuoteIsStoredAndFoundLiterally() {
        repository.save(new Invoice("INV-1", "O'Brien"));

        assertThat(repository.findByCustomer("O'Brien")).extracting(Invoice::id).containsExactly("INV-1");
        assertThat(repository.findByCustomer("x' OR '1'='1")).isEmpty();
    }
}
```

The last assertion is the integration test doing what no mock can:
proving the query is parameterised against a real database.

## Exemptions

- **Prototypes** in `experiments/`: the experiment's own measurement
replaces unit tests; they never ship.
- **Generated code**, and pure declarations without behaviour
(interfaces, records and data classes with no logic, constants): tested
through the code that uses them.
- **Trivial accessors** and `toString`, `equals`, `hashCode` — unless
they carry logic.
- **Code outside a project** (no `pom.xml`, `build.gradle`,
`package.json`, `pyproject.toml`, `requirements.txt`, `go.mod`,
`*.csproj` …): a one-off script needs no test suite.

## How it is enforced

| Layer | What it does |
| --- | --- |
| `test_check.py` | for production code: a matching test file, a test calling each public function or method, an integration test where the code talks to a database, a service or a broker; for test code: assertions present, no `sleep`, no unexplained `@Disabled`, the class under test not mocked |
| hook after every file write | checks the tests for what Claude just wrote or changed, and tells Claude at once |
| hook after every command | notices test runs (`mvn test`, `gradle test`, `pytest`, `npm test`, `go test`, `dotnet test` …) and whether they failed |
| hook when Claude finishes | Claude cannot finish while code it wrote lacks tests, while the tests have not been run since its last change, or while the last run failed; on a second attempt it may, and you are told what remains |
| review criterion C4 | `/review` applies this standard; `/rework` fixes the findings |
| your CI | the configurations below run unit and integration tests and fail the build |

`test_check.py` is a heuristic: it matches test files by naming
convention and finds calls by name. It cannot tell whether a test is
*good* — that is the reviewer's judgement and, with mutation testing,
the CI's. To switch the test hooks off for one project, create an empty
file `.ai/no-test-check` in it.

## CI configurations

**Maven** — Surefire runs `*Test`, Failsafe runs `*IT` in `verify`;
JaCoCo reports coverage and can set a floor:

```xml
<plugin>
  <artifactId>maven-surefire-plugin</artifactId>
</plugin>
<plugin>
  <artifactId>maven-failsafe-plugin</artifactId>
  <executions><execution><goals><goal>integration-test</goal><goal>verify</goal></goals></execution></executions>
</plugin>
<plugin>
  <groupId>org.jacoco</groupId><artifactId>jacoco-maven-plugin</artifactId>
  <executions>
    <execution><goals><goal>prepare-agent</goal></goals></execution>
    <execution><id>check</id><goals><goal>check</goal></goals>
      <configuration><rules><rule><element>BUNDLE</element><limits><limit>
        <counter>BRANCH</counter><value>COVEREDRATIO</value><minimum>0.80</minimum>
      </limit></limits></rule></rules></configuration>
    </execution>
  </executions>
</plugin>
```

A coverage floor catches untested code; it does not prove the tests are
good. Add PIT (`pitest-maven`) to measure whether the tests detect
changes.

**Gradle** — `test` with `useJUnitPlatform()`, a separate
`integrationTest` source set, and `jacocoTestCoverageVerification`.

**Python** — `pytest --cov --cov-fail-under=80`, with `-m "not
integration"` for the fast run and a separate job for `-m integration`.

**TypeScript** — `vitest run --coverage` with `coverage.thresholds`, or
Jest's `coverageThreshold`.

**C#** — `dotnet test --collect:"XPlat Code Coverage"` with a coverlet
threshold.

**Go** — `go test ./...` and `go test -tags integration ./...`;
`-coverprofile` for coverage.
