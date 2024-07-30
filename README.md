<!--
title: 'AWS Python User Data Ingestion Pipeline'
description: 'This template demonstrates how to deploy a Python-based user data ingestion pipeline running on AWS using the Serverless Framework. The data is sourced from https://randomuser.me.'
layout: Doc
framework: v4
platform: AWS
language: python
priority: 2
authorLink: 'https://github.com/Aphexlog'
authorName: 'Aaron West'
authorAvatar: ''
-->

# Serverless Framework AWS Python User Data Ingestion Pipeline

Welcome to the AWS Python User Data Ingestion Pipeline project! This template showcases how to deploy a robust and scalable data ingestion pipeline on AWS Lambda via the Serverless Framework. The pipeline sources user data from [RandomUser.me](https://randomuser.me), processes it through Kinesis Data Stream, and finally stores it in an S3 target bucket. For more advanced configurations, explore our [examples repo](https://github.com/serverless/examples/), which includes additional integrations with services like SQS, DynamoDB, or examples of event-triggered functions. For details about specific event configurations, please refer to our [documentation](https://www.serverless.com/framework/docs/providers/aws/events/).

## Usage

### Deployment

Deploying the pipeline is straightforward. Simply run the following command:

```
serverless deploy
```

After executing the deploy command, you should see an output akin to:

```
Deploying "aws-python" to stage "dev" (us-east-1)

✔ Service deployed to stack aws-python-dev (90s)

functions:
  hello: aws-python-dev-hello (1.9 kB)
```

### Invocation

Post successful deployment, you can invoke the deployed function using this command:

```
serverless invoke --function hello
```

You should receive a response similar to:

```json
{
  "statusCode": 200,
  "body": "{\"message\": \"Go Serverless v4.0! Your function executed successfully!\"}"
}
```

### Local development

For local testing and development, you can invoke your function locally via:

```
serverless invoke local --function hello
```

This command should yield a response similar to:

```
{
  "statusCode": 200,
  "body": "{\"message\": \"Go Serverless v4.0! Your function executed successfully!\"}"
}
```

### Bundling dependencies

In order to include third-party dependencies, you need to use the `serverless-python-requirements` plugin. Install it with the following command:

```
serverless plugin install -n serverless-python-requirements
```

This command will automatically add `serverless-python-requirements` to the `plugins` section in your `serverless.yml` file and register it as a `devDependency` in the `package.json` file. If `package.json` does not exist, it will be generated for you. Now, you can specify your dependencies in the `requirements.txt` file (support for `Pipfile` and `pyproject.toml` is available with additional configuration) and they will be included in the Lambda package during the build process. More details about plugin configuration can be found in the [official documentation](https://github.com/UnitedIncome/serverless-python-requirements).
