package ccoe.network

import rego.v1

# Mirrors G-NET-001 for aws_security_group_rule
deny contains msg if {
	rc := input.resource_changes[_]
	rc.type == "aws_security_group_rule"
	a := rc.change.after
	a.type == "ingress"
	"0.0.0.0/0" in a.cidr_blocks
	some port in [22, 3389]
	a.from_port <= port
	port <= a.to_port
	msg := sprintf("G-NET-001 %s opens port %d to the internet", [rc.address, port])
}
