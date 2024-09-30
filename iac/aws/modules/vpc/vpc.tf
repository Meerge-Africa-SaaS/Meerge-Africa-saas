resource "aws_vpc" "maoVPC" {
	cidr_block       = var.vpc_cidr
	  enable_dns_support   = true
	  enable_dns_hostnames = true
	instance_tenancy = "default"
	tags = {
		Name    = "maoVPC"
		Project = "Meerge Africa"
	}
}

resource "aws_internet_gateway" "maoIGW" {
	vpc_id = aws_vpc.maoVPC.id
	tags = {
		Name    = "maoIGW"
		Project = "Meerge Africa"
	}
}

resource "aws_eip" "maoNatGatewayEIP1" {
	tags = {
		Name    = "maoNatGatewayEIP1"
		Project = "Meerge Africa"
	}
}
resource "aws_nat_gateway" "maoNatGateway1" {
	allocation_id = aws_eip.maoNatGatewayEIP1.id
	subnet_id     = aws_subnet.maoPublicSubnet1.id
	tags = {
		Name    = "maoNatGateway1"
		Project = "Meerge Africa"
	}
}
resource "aws_subnet" "maoPublicSubnet1" {
	vpc_id            = aws_vpc.maoVPC.id
	cidr_block        = var.public_subnet_cidrs[0]
	availability_zone = var.availability_zones[0]
	tags = {
		Name    = "maoPublicSubnet1"
		Project = "Meerge Africa"
	}
}

resource "aws_eip" "maoNatGatewayEIP2" {
	tags = {
		Name    = "maoNatGatewayEIP2"
		Project = "Meerge Africa"
	}
}
resource "aws_nat_gateway" "maoNatGateway2" {
	allocation_id = aws_eip.maoNatGatewayEIP2.id
	subnet_id     = aws_subnet.maoPublicSubnet1.id
	tags = {
		Name    = "maoNatGateway2"
		Project = "Meerge Africa"
	}
}
resource "aws_subnet" "maoPublicSubnet2" {
	vpc_id            = aws_vpc.maoVPC.id
	cidr_block        = var.public_subnet_cidrs[1]
	availability_zone = var.availability_zones[1]
	tags = {
		Name    = "maoPublicSubnet2"
		Project = "Meerge Africa"
	}
}

resource "aws_subnet" "maoPrivateSubnet1" {
	vpc_id            = aws_vpc.maoVPC.id
	cidr_block        = var.private_subnet_cidrs[0]
	availability_zone = var.availability_zones[0]
	tags = {
		Name    = "maoPrivateSubnet1"
		Project = "Meerge Africa"
	}
}
resource "aws_subnet" "maoPrivateSubnet2" {
	vpc_id            = aws_vpc.maoVPC.id
	cidr_block        = var.private_subnet_cidrs[1]
	availability_zone = var.availability_zones[1]
	tags = {
		Name    = "maoPrivateSubnet2"
		Project = "Meerge Africa"
	}
}

resource "aws_route_table" "maoPublicRT" {
	vpc_id = aws_vpc.maoVPC.id
	route {
		cidr_block = "0.0.0.0/0"
		gateway_id = aws_internet_gateway.maoIGW.id
	}
	tags = {
		Name    = "maoPublicRT"
		Project = "Meerge Africa"
	}
}
resource "aws_route_table" "maoPrivateRT1" {
	vpc_id = aws_vpc.maoVPC.id
	route {
		cidr_block     = "0.0.0.0/0"
		nat_gateway_id = aws_nat_gateway.maoNatGateway1.id
	}
	tags = {
		Name    = "maoPrivateRT1"
		Project = "Meerge Africa"
	}
}
resource "aws_route_table" "maoPrivateRT2" {
	vpc_id = aws_vpc.maoVPC.id
	route {
		cidr_block     = "0.0.0.0/0"
		nat_gateway_id = aws_nat_gateway.maoNatGateway2.id
	}
	tags = {
		Name    = "maoPrivateRT2"
		Project = "Meerge Africa"
	}
}

resource "aws_route_table_association" "maoPublicRTassociation1" {
	subnet_id      = aws_subnet.maoPublicSubnet1.id
	route_table_id = aws_route_table.maoPublicRT.id
}
resource "aws_route_table_association" "maoPublicRTassociation2" {
	subnet_id      = aws_subnet.maoPublicSubnet2.id
	route_table_id = aws_route_table.maoPublicRT.id
}
resource "aws_route_table_association" "maoPrivateRTassociation1" {
	subnet_id      = aws_subnet.maoPrivateSubnet1.id
	route_table_id = aws_route_table.maoPrivateRT1.id
}
resource "aws_route_table_association" "maoPrivateRTassociation2" {
	subnet_id      = aws_subnet.maoPrivateSubnet2.id
	route_table_id = aws_route_table.maoPrivateRT2.id
}