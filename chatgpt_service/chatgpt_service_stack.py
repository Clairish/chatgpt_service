from aws_cdk import (
    # Duration,
    Stack,
    aws_codecommit as codecommit,
    aws_iam as iam,
    pipelines as pipelines,
    # aws_sqs as sqs,
)
from constructs import Construct

class ChatgptServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        repo = codecommit.Repository(self, "Quincare", repository_name="Quincare")

        odic_provider = iam.OpenIdConnectProvider(
            self,
            "GithubODIC",
            url="https://token.actions.githubusercontent.com",
            client_ids=["sts.amazonaws.com"],
        )

        policy_statement = iam.PolicyStatement(
            actions=["codecommit:GitPush"],
            resources=[repo.repository_arn],
        )

        policy_statement.effect = iam.Effect.ALLOW

        role = iam.Role(
            self,
            id="GitHubActionsRole",
            role_name="Quincare_role",
            path="/github-actions/",
            assumed_by=iam.FederatedPrincipal(
                federated="arn:aws:iam::1235:odic-provider/token.actions.githubusercontent.com",
                conditions={
                    "StringEquals": {
                        "token.actions.githubusercontent.com:aud": "sts:amazonaws.com"
                    },
                    "StringLike": {
                        "token.actions.githubusercontent.com:sub": "repo:Quintic-Solutions/Quincare:ref:refs/heads/develop"
                    },
                },
                assume_role_action="sts:AssumeRoleWithWebIdentity",
            ),
            inline_policies={
                "quincare-repo-access": iam.PolicyDocument(
                    statements=[policy_statement]
                )
            },
        )

        pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.code_commit(repo, "develop"),
                commands=[
                    "npm install -g aws_cdk",
                    "pip install -r requirements.txt",
                    "cdk synth",
                ],
            ),
            docker_enabled_for_synth=True,
        )