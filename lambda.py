import boto3
import os
import json

asg_client = boto3.client('autoscaling')

filter_asg_list_names = asg_client.get_paginator('describe_auto_scaling_groups').paginate(
    PaginationConfig={'PageSize': 100}).search('AutoScalingGroups[].[AutoScalingGroupName]')

list_start_desired = list(
    asg_client.get_paginator('describe_auto_scaling_groups').paginate(PaginationConfig={'PageSize': 100})
        .search('AutoScalingGroups[].[Tags[?Key ==`{}`].Value[]]'
        .format('Desired')))

list_start_min = list(
    asg_client.get_paginator('describe_auto_scaling_groups').paginate(PaginationConfig={'PageSize': 100})
        .search('AutoScalingGroups[].[Tags[?Key ==`{}`].Value[]]'
        .format('Minimum')))


def lambda_handler(event, context):
    global cloudwatchvalue
    cloudwatchvalue = event.get('action')

    for asg_item, desired, minimum in zip(filter_asg_list_names, list_start_desired, list_start_min):
        if 'start' == cloudwatchvalue:
            print("####### starting scale out instances #######")

            print("ASG: {asg_name}; Desired: {desired_count}; Minimum: {minimum_size}"
                  .format(asg_name=asg_item[0], desired_count=desired[0][0], minimum_size=minimum[0][0]))
            update_asg_desired_count(asg_item[0], desired[0][0], minimum[0][0])

        elif 'stop' == cloudwatchvalue:
            print("####### stopping instances - scale in ########")
            print("ASG: {asg_name} set desired: 0".format(asg_name=asg_item[0]))
            update_asg_desired_count(asg_item[0], 0, 0)


def update_asg_desired_count(asg, new_desired_count, minimum):
    # para cada instancia atualizar o valor de desired
    asg_client.update_auto_scaling_group(
        AutoScalingGroupName=asg,
        DesiredCapacity=int(new_desired_count),
        MinSize=int(minimum),
    )
