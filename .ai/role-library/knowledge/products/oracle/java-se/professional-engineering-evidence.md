# Java SE professional engineering evidence

Use the version-matched doclet specification when changing accessible APIs. Review generated documentation or doclint where supported, including parameter, exception and return semantics. Prefer a single-line // comment for short ordinary notes and use multiline Javadoc for documented declarations. Java's grammar permits local inference in supported releases; the explicit-type restriction is a JAI writing rule. Verify the project JDK distribution, Java release and support or licensing terms before relying on a vendor roadmap. Compare measured latency, allocations or throughput against a representative baseline before claiming an improvement.

- [JDK 25 JavaDoc Documentation Comment Specification](https://docs.oracle.com/en/java/javase/25/docs/specs/javadoc/doc-comment-spec.html)
- [Local Variable Type Inference](https://docs.oracle.com/en/java/javase/25/language/local-variable-type-inference.html)
- [Java SE 25 java.util.logging package](https://docs.oracle.com/en/java/javase/25/docs/api/java.logging/java/util/logging/package-summary.html)
- [Code Conventions for the Java Programming Language](https://www.oracle.com/java/technologies/javase/codeconventions-introduction.html)
- [Troubleshoot Performance Issues Using Flight Recorder](https://docs.oracle.com/en/java/javase/25/troubleshoot/troubleshoot-performance-issues-using-jfr.html)
- [Oracle Java SE Support Roadmap](https://www.oracle.com/java/technologies/java-se-support-roadmap.html)
- [Sun Java Code Conventions for comments, historical](https://www.oracle.com/java/technologies/javase/codeconventions-comments.html)
- [Oracle Java Tutorials example of generic diamond, JDK 8](https://docs.oracle.com/javase/tutorial/java/generics/types.html)
