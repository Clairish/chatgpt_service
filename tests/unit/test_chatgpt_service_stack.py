import aws_cdk as core
import aws_cdk.assertions as assertions

from chatgpt_service.chatgpt_service_stack import ChatgptServiceStack

# example tests. To run these tests, uncomment this file along with the example
# resource in chatgpt_service/chatgpt_service_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ChatgptServiceStack(app, "chatgpt-service")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
