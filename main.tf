terraform {
	# Run init/plan/apply with "backend" commented-out (ueses local backend) to provision Resources (Bucket, Table)
	# Then uncomment "backend" and run init, apply after Resources have been created (uses AWS)
# 	backend "s3" {
# 		bucket         = "tf-state-backend"
# 		key            = "tf-infra/terraform.tfstate"
# 		region         = "eu-west-2"
# 		dynamodb_table = "terraform-state-locking"
# 		encrypt        = true
# 	}

	#   required_version = ">=0.13.0"
	required_providers {
		aws = {
			source = "hashicorp/aws"
			#       version = "~>3.0"
		}
	}
}

provider "aws" {
	region = "eu-west-2"
}

module "tf-state" {
	source      = "./iac/aws/modules/tf-state"
	bucket_name = "ma-o-tf-state-backend"
}