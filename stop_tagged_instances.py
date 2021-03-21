import boto3
import json
import os

# Parse Region Name from Environment Variable
region_name = os.environ["region"]


def lambda_handler(event, context):

    # Parse Tag from Environment Variable or event
    tags = os.environ.get("tags") or event["tags"]
    tags = json.loads(tags)
    print("Target Instance Tags:", tags)

    filters = []
    for key, value in tags.items():
        describe_filter = {}
        describe_filter["Name"] = "tag:"+key
        describe_filter["Values"] = [value]
        filters.append(describe_filter)

    ec2 = boto3.client('ec2', region_name=region_name)

    # Find All Instances with the given tags
    describe_paginatgor = ec2.get_paginator("describe_instances")
    paginated_response = describe_paginatgor.paginate(Filters=filters)
    target_instances = []
    for response in paginated_response:
        for reservation in response["Reservations"]:
            instances = reservation.get("Instances", [])
            for instance in instances:
                instance_id = instance.get("InstanceId")
                # Only Stop Running Instances
                state = instance.get("State", {}).get("Name")
                if state is not None and state == "running":
                    target_instances.append(instance_id)

    print("Preparing to Stop:", target_instances)

    # Stop All Found Instances
    stoping_instances = target_instances[:]
    for instance_id in target_instances:
        try:
            response = ec2.stop_instances(
                InstanceIds=[instance_id]
            )
        except Exception as e:
            print("Stop Instance error: "+format(e))
            stoping_instances.remove(instance_id)

    print("Stoping:", stoping_instances)
