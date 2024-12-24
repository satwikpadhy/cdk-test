from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam
)
from constructs import Construct

class CdkTestStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, "ExistingVPC",
            vpc_id="vpc-0c1aa7d66636bdac7"  # Replace with your existing VPC ID
        )

        # Security Group
        security_group = ec2.SecurityGroup(self, "pg-db-security-grp",
            vpc=vpc,
            description="Security Group for pg-db",
            allow_all_outbound=True
        )

        # Allow SSH access from anywhere (use with caution)
        security_group.add_ingress_rule(
            # peer=ec2.Peer.any_ipv4(),
            peer=ec2.Peer.ipv4('0.0.0.0/0'),
            connection=ec2.Port.tcp(22),
            description="Allow SSH Access from anywhere"
        )

        # Define an Amazon Machine Image (AMI)
        ami = ec2.MachineImage.generic_linux({
            #Ubuntu 22.04 arm64 ami
            "ap-south-1":"ami-0a87daabd88e93b1f"
        })

        # ec2_role = iam.CfnRole(s)

        # EC2 Instance with EBS volumes attached directly
        instance = ec2.Instance(self, "EC2Instance",
            instance_type=ec2.InstanceType("t4g.nano"),
            machine_image=ami,
            # role=
            vpc=vpc,
            security_group=security_group,
            key_name="cruzex-ec2-keypair",  # Replace with your key pair name
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/sda1",  # Root volume
                    volume=ec2.BlockDeviceVolume.ebs(10, volume_type=ec2.EbsDeviceVolumeType.GP3)  # Modify root volume size to 30 GiB
                ),
                ec2.BlockDevice(
                    device_name="/dev/sdb",
                    volume=ec2.BlockDeviceVolume.ebs(15, volume_type=ec2.EbsDeviceVolumeType.GP3)
                ),
                ec2.BlockDevice(
                    device_name="/dev/sdc",
                    volume=ec2.BlockDeviceVolume.ebs(20, volume_type=ec2.EbsDeviceVolumeType.GP3)
                )
            ]
        )