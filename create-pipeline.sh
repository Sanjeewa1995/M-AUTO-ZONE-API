#!/bin/bash

# AWS CodePipeline Setup Script for Vehicle Parts API
# This script creates a complete CI/CD pipeline

echo "🚀 Creating AWS CodePipeline for Vehicle Parts API..."

# Configuration
PROJECT_NAME="vehicle-parts-api"
PIPELINE_NAME="vehicle-parts-pipeline"
SERVICE_ROLE_NAME="CodePipelineServiceRole"
BUILD_ROLE_NAME="CodeBuildServiceRole"
GITHUB_REPO="https://github.com/dewapathi/M-AUTO-ZONE-API.git"
EC2_HOST="3.107.165.131"
EC2_USER="ec2-user"

# Create IAM roles for CodePipeline
echo "🔧 Creating IAM roles..."

# Create CodePipeline service role
aws iam create-role \
  --role-name $SERVICE_ROLE_NAME \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "codepipeline.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  }' \
  --profile vehicle_parts

# Attach policies to CodePipeline role
aws iam attach-role-policy \
  --role-name $SERVICE_ROLE_NAME \
  --policy-arn arn:aws:iam::aws:policy/AWSCodePipelineServiceRole \
  --profile vehicle_parts

aws iam attach-role-policy \
  --role-name $SERVICE_ROLE_NAME \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess \
  --profile vehicle_parts

# Create CodeBuild service role
aws iam create-role \
  --role-name $BUILD_ROLE_NAME \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "codebuild.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  }' \
  --profile vehicle_parts

# Attach policies to CodeBuild role
aws iam attach-role-policy \
  --role-name $BUILD_ROLE_NAME \
  --policy-arn arn:aws:iam::aws:policy/CloudWatchLogsFullAccess \
  --profile vehicle_parts

aws iam attach-role-policy \
  --role-name $BUILD_ROLE_NAME \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess \
  --profile vehicle_parts

# Create S3 bucket for artifacts
BUCKET_NAME="vehicle-parts-artifacts-$(date +%s)"
echo "📦 Creating S3 bucket: $BUCKET_NAME"

aws s3 mb s3://$BUCKET_NAME --profile vehicle_parts

# Create CodeBuild project
echo "🔨 Creating CodeBuild project..."

aws codebuild create-project \
  --name $PROJECT_NAME \
  --source '{
    "type": "GITHUB",
    "location": "'$GITHUB_REPO'",
    "buildspec": "buildspec.yml"
  }' \
  --artifacts '{
    "type": "S3",
    "location": "'$BUCKET_NAME'",
    "path": "artifacts",
    "name": "vehicle-parts-api",
    "packaging": "ZIP"
  }' \
  --environment '{
    "type": "LINUX_CONTAINER",
    "image": "aws/codebuild/standard:7.0",
    "computeType": "BUILD_GENERAL1_SMALL",
    "privilegedMode": true
  }' \
  --service-role arn:aws:iam::142881765270:role/$BUILD_ROLE_NAME \
  --profile vehicle_parts

# Create CodePipeline
echo "🚀 Creating CodePipeline..."

aws codepipeline create-pipeline \
  --pipeline '{
    "name": "'$PIPELINE_NAME'",
    "roleArn": "arn:aws:iam::142881765270:role/'$SERVICE_ROLE_NAME'",
    "artifactStore": {
      "type": "S3",
      "location": "'$BUCKET_NAME'"
    },
    "stages": [
      {
        "name": "Source",
        "actions": [
          {
            "name": "SourceAction",
            "actionTypeId": {
              "category": "Source",
              "owner": "ThirdParty",
              "provider": "GitHub",
              "version": "1"
            },
            "configuration": {
              "Owner": "dewapathi",
              "Repo": "M-AUTO-ZONE-API",
              "Branch": "main",
              "OAuthToken": "your-github-token-here"
            },
            "outputArtifacts": [
              {
                "name": "SourceOutput"
              }
            ]
          }
        ]
      },
      {
        "name": "Build",
        "actions": [
          {
            "name": "BuildAction",
            "actionTypeId": {
              "category": "Build",
              "owner": "AWS",
              "provider": "CodeBuild",
              "version": "1"
            },
            "configuration": {
              "ProjectName": "'$PROJECT_NAME'"
            },
            "inputArtifacts": [
              {
                "name": "SourceOutput"
              }
            ],
            "outputArtifacts": [
              {
                "name": "BuildOutput"
              }
            ]
          }
        ]
      },
      {
        "name": "Deploy",
        "actions": [
          {
            "name": "DeployAction",
            "actionTypeId": {
              "category": "Deploy",
              "owner": "AWS",
              "provider": "S3",
              "version": "1"
            },
            "configuration": {
              "BucketName": "'$BUCKET_NAME'",
              "Extract": "true",
              "ObjectKey": "artifacts/vehicle-parts-api.zip"
            },
            "inputArtifacts": [
              {
                "name": "BuildOutput"
              }
            ]
          }
        ]
      }
    ]
  }' \
  --profile vehicle_parts

echo "✅ Pipeline created successfully!"
echo "🔗 View your pipeline at: https://console.aws.amazon.com/codesuite/codepipeline/pipelines/$PIPELINE_NAME/view"
echo "📝 Note: You need to configure GitHub OAuth token in the pipeline settings"
