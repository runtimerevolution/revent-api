data "aws_availability_zones" "available_zones" {}

resource "aws_default_vpc" "default_vpc" {}

resource "aws_default_subnet" "default_subnets" {
  count = length(data.aws_availability_zones.available_zones.names)

  availability_zone = data.aws_availability_zones.available_zones.names[count.index]
}
