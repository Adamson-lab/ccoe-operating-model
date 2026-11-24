package ccoe.storage

import rego.v1

# Mirrors G-DATA-001 / G-DATA-002 / G-DATA-003
deny contains msg if {
	rc := input.resource_changes[_]
	rc.type == "aws_ebs_volume"
	not rc.change.after.encrypted == true
	msg := sprintf("G-DATA-002 %s must be encrypted", [rc.address])
}

deny contains msg if {
	rc := input.resource_changes[_]
	rc.type == "aws_db_instance"
	not rc.change.after.storage_encrypted == true
	msg := sprintf("G-DATA-003 %s must use storage encryption", [rc.address])
}

deny contains msg if {
	rc := input.resource_changes[_]
	rc.type == "aws_s3_bucket_public_access_block"
	some attr in ["block_public_acls", "block_public_policy", "ignore_public_acls", "restrict_public_buckets"]
	not rc.change.after[attr] == true
	msg := sprintf("G-DATA-001 %s: %s must be true", [rc.address, attr])
}
