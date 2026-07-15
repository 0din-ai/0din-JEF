# Security Policy

## Supported Versions

JEF (`0din-jef` on PyPI) does not maintain long-term-support branches. Only the
latest release published to [PyPI](https://pypi.org/project/0din-jef/) is
supported with security fixes. If you're running an older version, please
upgrade before reporting an issue.

## Reporting a Vulnerability

**Primary channel:** Please report security vulnerabilities using GitHub's
[Private Vulnerability Reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability).
Go to this repository's **Security** tab and select **Report a vulnerability**.
This creates a private advisory visible only to maintainers and lets us
coordinate a fix with you directly.

**Fallback channel:** If you're unable to use GitHub's reporting flow, email
**0din@mozilla.com**. This address is PGP-capable if you need to encrypt your
report.

Please do not open a public GitHub issue for security vulnerabilities.

## Response Expectations

We aim to acknowledge new reports within a few business days. We'll work with
you to understand and validate the issue, and to agree on a coordinated
disclosure timeline before any public disclosure. Timelines vary with
severity and complexity, but we'll keep you updated as we investigate and fix.

## Scope

JEF is a Python library for scoring and evaluating jailbreak attempts against
LLM outputs — it is not a hosted service, and doesn't process or store user
data on our infrastructure. Reports should generally concern the library's
code (e.g. supply-chain issues in our packaging/release pipeline, or
vulnerabilities in the scoring logic itself), not infrastructure we don't
operate.
