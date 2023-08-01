#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { ChessAnalysisCdkStack } from '../lib/chess-analysis-cdk-stack';
import 'dotenv/config'

const app = new cdk.App();
new ChessAnalysisCdkStack(app, 'ChessAnalysisCdkStack', {
    certificateDomainName: process.env.CERTIFICATE_DOMAIN_NAME!,
    hostedZoneId: process.env.HOSTED_ZONE_ID!,
    hostedZoneName: process.env.HOSTED_ZONE_NAME!,
    aRecordName: process.env.A_RECORD_NAME!,
});
