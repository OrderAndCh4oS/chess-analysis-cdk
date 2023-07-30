import * as cdk from 'aws-cdk-lib';
import {Construct} from 'constructs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ecsPatterns from 'aws-cdk-lib/aws-ecs-patterns';
import * as logs from "aws-cdk-lib/aws-logs";
import {ContainerImage} from "aws-cdk-lib/aws-ecs";
import {Platform} from "aws-cdk-lib/aws-ecr-assets";
import * as path from "path";


export class ChessAnalysisCdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const vpc = new ec2.Vpc(this, "ChessAnalysisVpc", {
      natGateways: 1,
      subnetConfiguration: [
        {cidrMask: 24, subnetType: ec2.SubnetType.PUBLIC, name: "Public"},
        {cidrMask: 24, subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS, name: "Private"}
      ],
      maxAzs: 3
    });

    const cluster = new ecs.Cluster(this, 'ChessAnalysisCluster', {
      vpc,
      containerInsights: true
    });

    const image = ContainerImage.fromAsset(
        path.join(__dirname, '../src'),
        {
          platform: Platform.LINUX_ARM64,
        }
    );

    const fargate = new ecsPatterns.ApplicationLoadBalancedFargateService(this, 'ChessAnalysisAlbFargate', {
      cluster,
      taskImageOptions: {
        image,
        containerPort: 80,
        logDriver: ecs.LogDrivers.awsLogs({
          streamPrefix: id,
          logRetention: logs.RetentionDays.ONE_MONTH,
        }),
      },
      assignPublicIp: true,
      memoryLimitMiB: 8192,
      cpu: 2048,
      desiredCount: 1,
      deploymentController: {type: ecs.DeploymentControllerType.ECS},
    });
  }
}
