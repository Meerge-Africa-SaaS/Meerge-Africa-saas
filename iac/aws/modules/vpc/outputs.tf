output "mao_vpc_id" {
	description = "VPC Id"
	value       = aws_vpc.maoVPC.id
}

output "mao_public_subnets" {
	description = "Will be used by Web Server Module to set subnet_ids"
	value = [
		aws_subnet.maoPublicSubnet1,
		aws_subnet.maoPublicSubnet2
	]
}

output "mao_private_subnets" {
	description = "Will be used by RDS Module to set subnet_ids"
	value = [
		aws_subnet.maoPrivateSubnet1,
		aws_subnet.maoPrivateSubnet2
	]
}