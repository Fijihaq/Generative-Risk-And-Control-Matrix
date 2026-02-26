import json
import boto3

bedrock = boto3.client("bedrock-runtime")

def lambda_handler(event, context):
    body = json.loads(event["body"])

    prompt = f"""
You are an Internal Audit Risk & Control Matrix Generator.

Inputs:
- Control Testing Type: {body.get("controlType")}
- Framework: {body.get("framework")}
- Priority: {body.get("priority")}
- Number of Tests: {body.get("numTests")}
- Business Process: {body.get("userInput")}

Generate a structured JSON Risk & Control Matrix with fields:
risk_id, risk_description, control_id, control_description,
control_objective, frequency, control_owner, testing_steps.
"""

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
        contentType="application/json",
        accept="application/json",
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2000,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        })
    )

    result = json.loads(response["body"].read())

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result)
    }