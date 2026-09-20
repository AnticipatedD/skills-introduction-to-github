# Define inputs, outputs, and success criteria
In this unit, you'll learn:
- How to define structured agent tasks using inputs, outputs, and success criteria
- Review examples of a task contract and a workflow that can define success criteria for an agent
- Task structure makes outcomes predictable
  
# Each agent task should be defined in terms of:
- Inputs: what the agent needs (issue context, constraints, boundaries).
- Outputs: what the agent produces (plan + PR + evidence).
- Success criteria: how results are evaluated (checks, scans, review outcomes).
- When tasks are under-specified, agents can produce changes that look plausible but don't actually solve the underlying problem.

# Example task contract: vulnerability remediation
**Inputs**
- A security alert or issue link describing the vulnerability.
- Repository scope: changes allowed under src/ and dependency files, but not infra/ unless explicitly requested.
- Constraints: no workflow changes without platform review; no secrets introduced; no direct-to-main pushes.

**Outputs** 
A pull request containing: 
- a structured plan (in PR description or Github/pull_request_template.md)
- a bounded changeset (commits on an agent branch).
- And evidence links to workflow run

**Success criteria** 
- Required checks pass (build/test/lint).
- Security signal is resolved (for example, the vulnerable version is replaced).
- Scope matches intent (no unexpected files changed).
- A rollback or escalation path is recorded for higher-risk changes.

> [!TIP]
> "CI passed" is necessary, but not always sufficient. Make success criteria reflect the real intent of the task (for example, "vulnerability resolved" rather than "tests passed").

# Implementation example: CI validation as an enforceable success signal
The following workflow is a common way to turn success criteria into a required status check.
on:
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test

  security-analysis:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write
    steps:
      - uses: actions/checkout@v4
      - name: Initialize analysis
        uses: github/codeql-action/init@v3
      - name: Analyze
        uses: github/codeql-action/analyze@v3 

When this workflow is configured as a required check (via rulesets or branch protection), a pull request can't be merged until the check passes. This ensures that success is enforced by the system-not assumed by the agent.

If success criteria are vague or missing, an agent may "complete the task" in a way that looks correct but fails the underlying goal. For example, the agent might update a dependency but leave the vulnerable version reachable through a transitive dependency or make broad changes that are difficult to validate.

With tasks defined, the next step is to design how the agent plans and executes its work in a way that remains reviewable.

# Pull requests are architectural control points
Pull requests are the primary control mechanism for agent execution in GitHub. Instead of allowing direct changes to protected branches, well-designed architectures route agent changes through pull requests and enforce merge requirements through policy.

A common safe workflow looks like this: 
Agent creates branch

    ↓

Agent opens pull request (includes plan)

    ↓

Required reviews validate approach

    ↓

GitHub Actions run required checks

    ↓

All checks pass + approvals complete

    ↓

Pull request can be merged

This structure ensures that execution is gated by both automation and human review.

# Implementation: PR template that requires a structured plan
A pull request template ensures that every agent PR provides consistent plan and evidence sections.

<!-- File: .github/pull_request_template.md -->

## Plan (required)
- **Goal:**
- **Scope (paths/files):**
- **Steps:**
  1.
  2.
  3.
- **Success criteria (verifiable):**
  - [ ] Required checks pass
  - [ ] Security signals reviewed (as applicable)
- **Risks + mitigations:**
- **Rollback / escalation plan:**

## Evidence
- Workflow run(s):
- Scan results (if applicable):

## Review checklist
- [ ] Plan reviewed and approved
- [ ] Required reviews satisfied
- [ ] Required checks satisfied

# Enforcing plan validation with required checks status checks
In addition to templates, you can enforce plan gating as a required status check. This turns a process expectation ("include a plan") into a system guarantee.

# File: .github/workflows/plan-gate.yml
name: Plan Gate

on:
  pull_request:
    branches: [ main ]

jobs:
  require-plan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Require plan artifact
        run: |
          if [ ! -f "Github/pull_request_template.md" ]; then
            echo "Github/pull_request_template.md is required for this pull request."
            exit 1
          fi
          echo "Github/pull_request_template.md found."

# Implementation note:

A repository administrator can mark Plan Gate as a required status check using rulesets/branch protection, ensuring PRs can't merge unless the plan exists.

GitHub can require explicit approval before workflows run on agent-generated changes.

# Using CODEOWNERS to ensure safety
CODEOWNERS ensures that changes to sensitive areas go to the right reviewers automatically.
# File: CODEOWNERS

/security/ @security-team
/.github/workflows/ @platform-team
/infra/ @platform-team
* @core-team

## License
MIT License – see [LICENSE](license.md) file.

---
© 2026 MD ABUL HOSSAIN. All Rights Reserved. 
