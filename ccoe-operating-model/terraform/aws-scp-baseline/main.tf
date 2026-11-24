# Deploys the CCoE preventive baseline from policies/aws-scp to chosen targets.
terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

variable "target_ids" {
  description = "Organization root, OU or account IDs to attach the baseline to"
  type        = list(string)
}

locals {
  policy_files = fileset("${path.module}/../../policies/aws-scp", "*.json")
  attachments  = { for pair in setproduct(local.policy_files, var.target_ids) : "${pair[0]}:${pair[1]}" => { file = pair[0], target = pair[1] } }
}

resource "aws_organizations_policy" "scp" {
  for_each    = local.policy_files
  name        = "ccoe-${trimsuffix(each.value, ".json")}"
  description = "CCoE guardrail ${each.value}"
  type        = "SERVICE_CONTROL_POLICY"
  content     = file("${path.module}/../../policies/aws-scp/${each.value}")
  tags        = { owner = "ccoe", "cost-center" = "platform", environment = "shared", "data-classification" = "internal" }
}

resource "aws_organizations_policy_attachment" "attach" {
  for_each  = local.attachments
  policy_id = aws_organizations_policy.scp[each.value.file].id
  target_id = each.value.target
}
