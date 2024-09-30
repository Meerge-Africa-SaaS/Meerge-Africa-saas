resource "aws_security_group" "maowWebserverSecurityGroup" {
	name        = "allow_ssh_http"
	description = "Allow ssh http inbound traffic"
	vpc_id      = var.maow_vpc_id

	dynamic "ingress" {
		for_each = var.ingress_rules
		content {
			from_port   = ingress.value["port"]
			to_port     = ingress.value["port"]
			protocol    = ingress.value["proto"]
			cidr_blocks = ingress.value["cidr_blocks"]
		}
	}

	egress {
		from_port   = 0
		to_port     = 0
		protocol    = "-1"
		cidr_blocks = ["0.0.0.0/0"]
	}

	tags = {
		Name    = "maowWebserverSecurityGroup"
		Project = "Meerge Africa"
	}
}

resource "aws_lb" "maowLoadBalancer" {
	name               = "web-app-lb"
	load_balancer_type = "application"
	subnets            = [var.maow_public_subnets[0].id, var.maow_public_subnets[1].id]
	security_groups    = [aws_security_group.maowWebserverSecurityGroup.id]
	tags = {
		Name    = "maowLoadBalancer"
		Project = "Meerge Africa"
	}
}

resource "aws_lb_listener" "maowLbListener" {
	load_balancer_arn = aws_lb.maowLoadBalancer.arn

	port     = 80
	protocol = "HTTP"

	default_action {
		target_group_arn = aws_lb_target_group.maowTargetGroup.id
		type             = "forward"
	}
}

resource "aws_lb_target_group" "maowTargetGroup" {
	name     = "example-target-group"
	port     = 80
	protocol = "HTTP"
	vpc_id   = var.moaw_vpc_id

	health_check {
		path                = "/"
		protocol            = "HTTP"
		matcher             = "200"
		interval            = 15
		timeout             = 3
		healthy_threshold   = 2
		unhealthy_threshold = 2
	}
	tags = {
		Name    = "maowTargetGroup"
		Project = "Meerge Africa"
	}
}

resource "aws_lb_target_group_attachment" "webserver1" {
	target_group_arn = aws_lb_target_group.maowTargetGroup.arn
	target_id        = aws_instance.web.id
	port             = 80
}

# resource "aws_lb_target_group_attachment" "webserver2" {
# 	target_group_arn = aws_lb_target_group.maowTargetGroup.arn
# 	target_id        = aws_instance.web.id
# 	port             = 80
# }

# resource "aws_instance" "webserver1" {
# 	ami                         = local.ami_id
# 	instance_type               = local.instance_type
# 	key_name                    = local.key_name
# 	subnet_id                   = var.maow_public_subnets[0].id
# 	security_groups             = [aws_security_group.maowWebserverSecurityGroup.id]
# 	associate_public_ip_address = true
#
# 	user_data = <<-EOF
#               #!/bin/bash -xe
#               sudo su
#               yum update -y
#               yum install -y httpd
#               echo "<h1>Hello, World!</h1>server: maowWebServer1" > /var/www/html/index.html
#               echo "healthy" > /var/www/html/hc.html
#               service httpd start
#               EOF
# }

# resource "aws_instance" "webserver2" {
# 	ami                         = local.ami_id
# 	instance_type               = local.instance_type
# 	key_name                    = local.key_name
# 	subnet_id                   = var.maow_public_subnets[0].id
# 	security_groups             = [aws_security_group.maowWebserverSecurityGroup.id]
# 	associate_public_ip_address = true
#
# 	user_data = <<-EOF
#               #!/bin/bash -xe
#               sudo su
#               yum update -y
#               yum install -y httpd
#               echo "<h1>Hello, World!</h1>server: maowWebServer2" > /var/www/html/index.html
#               echo "healthy" > /var/www/html/hc.html
#               service httpd start
#               EOF
# }

# EC2 instance for the local web app
resource "aws_instance" "web" {
  ami                    = local.ami_id # Amazon Linux
  instance_type          = local.instance_type
  subnet_id              = var.maow_public_subnets[0].id # Place this instance in one of the private subnets
  vpc_security_group_ids = [aws_security_group.maowWebserverSecurityGroup.id]

  associate_public_ip_address = true # Assigns a public IP address to your instance
  user_data_replace_on_change = true # Replace the user data when it changes

  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name

  user_data = <<-EOF
    #!/bin/bash
    set -ex
    yum update -y
    yum install -y yum-utils

    # Install Docker
    yum install -y docker
    service docker start

    # Install AWS CLI
    yum install -y aws-cli

    # Authenticate to ECR
    docker login -u AWS -p $(aws ecr get-login-password --region eu-west-2) 471112685546.dkr.ecr.eu-west-2.amazonaws.com

    # Pull the Docker image from ECR
    docker pull 471112685546.dkr.ecr.eu-west-2.amazonaws.com/meerge-africa:uat

    # Run the Docker image
	# --env SECRET_KEY=${var . secret_key} \
    docker run -d -p 80:8000 \
    471112685546.dkr.ecr.eu-west-2.amazonaws.com/meerge-africa:uat
    EOF

  tags = {
    Name = "MeergeAfrica_EC2_Complete_Server"
  }
}

# IAM role for EC2 instance to access ECR
resource "aws_iam_role" "ec2_role" {
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Principal = {
        Service = "ec2.amazonaws.com",
      },
      Effect = "Allow",
    }],
  })
}

# Attach the AmazonEC2ContainerRegistryReadOnly policy to the role
resource "aws_iam_role_policy_attachment" "ecr_read" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

# IAM instance profile for EC2 instance
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "meerge-africa_ec2_complete_profile"
  role = aws_iam_role.ec2_role.name
}