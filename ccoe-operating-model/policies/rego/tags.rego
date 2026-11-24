package ccoe.tags

import rego.v1

# Mirror of G-TAG-001 for teams that prefer OPA/Conftest. Input: terraform show -json
required := {"owner", "cost-center", "environment", "data-classification"}
taggable := {"aws_instance", "aws_ebs_volume", "aws_db_instance", "aws_s3_bucket", "aws_kms_key", "aws_lambda_function", "aws_vpc"}

deny contains msg if {
	rc := input.resource_changes[_]
	taggable[rc.type]
	tags := object.get(rc.change.after, "tags", {})
	missing := required - {k | tags[k]}
	count(missing) > 0
	msg := sprintf("G-TAG-001 %s missing tags: %v", [rc.address, missing])
}
