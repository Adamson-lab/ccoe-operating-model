# Guardrail Catalogue

_Generated from `data/guardrails.json` by `ccoe catalog`._

| ID | Guardrail | Domain | Layer | Severity | Controls | Automated check |
|---|---|---|---|---|---|:-:|
| G-IAM-001 | No IAM users with long-lived access keys; use federated SSO | Identity | detective | mandatory | NIST-800-53:IA-5, CIS-AWS:1.14, SOC2:CC6.1, ISO27001:A.5.17 | org/runtime |
| G-IAM-002 | No IAM policy granting Action * on Resource * | Identity | proactive | mandatory | NIST-800-53:AC-6, CIS-AWS:1.16, SOC2:CC6.3, ISO27001:A.8.2 | yes |
| G-DATA-001 | S3 buckets must block all public access | Data Protection | proactive | mandatory | NIST-800-53:AC-3, CIS-AWS:2.1.4, PCI-DSS:1.4, NDPA-2023:Security | yes |
| G-DATA-002 | EBS volumes must be encrypted | Data Protection | proactive | mandatory | NIST-800-53:SC-28, CIS-AWS:2.2.1, PCI-DSS:3.5, ISO27001:A.8.24 | yes |
| G-DATA-003 | RDS instances must use storage encryption | Data Protection | proactive | mandatory | NIST-800-53:SC-28, CIS-AWS:2.3.1, PCI-DSS:3.5, NDPA-2023:Security | yes |
| G-KMS-001 | KMS keys must have automatic rotation enabled | Data Protection | proactive | mandatory | NIST-800-53:SC-12, CIS-AWS:3.6, ISO27001:A.8.24 | yes |
| G-NET-001 | No ingress from 0.0.0.0/0 to SSH (22) or RDP (3389) | Network | proactive | mandatory | NIST-800-53:SC-7, CIS-AWS:5.2, PCI-DSS:1.3, SOC2:CC6.6 | yes |
| G-NET-002 | EC2 instances must not auto-assign public IPs | Network | proactive | mandatory | NIST-800-53:SC-7, PCI-DSS:1.4, ISO27001:A.8.20 | yes |
| G-LOG-001 | CloudTrail must be multi-region with log file validation | Logging | proactive | mandatory | NIST-800-53:AU-2, CIS-AWS:3.1, SOC2:CC7.2, ISO27001:A.8.15 | yes |
| G-HARD-001 | EC2 must require IMDSv2 | Platform Hardening | proactive | mandatory | NIST-800-53:CM-6, CIS-AWS:5.6, SOC2:CC6.8 | yes |
| G-ORG-001 | Deny leaving the AWS Organization | Governance & Org | preventive | mandatory | NIST-800-53:CM-5, SOC2:CC6.1 | org/runtime |
| G-ORG-002 | Deny use of the root user in member accounts | Governance & Org | preventive | mandatory | NIST-800-53:AC-6, CIS-AWS:1.7, ISO27001:A.8.2 | org/runtime |
| G-ORG-003 | Protect security tooling (CloudTrail, Config, GuardDuty) | Governance & Org | preventive | mandatory | NIST-800-53:AU-9, SOC2:CC7.2, ISO27001:A.8.15 | org/runtime |
| G-REG-001 | Resources only in approved regions (data residency) | Governance & Org | preventive | mandatory | NDPA-2023:Security, ISO27001:A.5.34, SOC2:CC6.1 | yes |
| G-TAG-001 | Mandatory tags: owner, cost-center, environment, data-classification | Cost & Tagging | proactive | mandatory | SOC2:CC2.1, ISO27001:A.5.9, NIST-800-53:CM-8 | yes |
| G-COST-001 | Prefer gp3 over gp2 volumes | Cost & Tagging | proactive | advisory | FinOps-Foundation:Optimize | yes |
