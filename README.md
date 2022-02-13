# lambda-finops-asg-ec2
Simple Lambda to stop and start EC2 instances with attached Auto Scaling Group, this lambda is trigger by Cloud Watch Event Bridge based on cron expression and execute a script to set MinSize and DesiredCapacity of ASG to 0. I create 2 tags Minimum and Desired to store values to start.

So the instances will terminate, and start based in Event Bridge Schedule Expression:       
start: "cron(0 10 ? * MON-FRI *)"
stop: "cron(55 23 ? * MON-FRI *)"

i.e. start instances Monday to Friday during business hours

![Diagram](https://github.com/viborotto/lambda-finops-asg-ec2/blob/main/lambda-ec2-asg.jpg?raw=true)
    
    
    
Another way to do that is creating an Scheduled Action attached to Auto Scaling Group
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client.put_scheduled_action


#### References:
https://aws.plainenglish.io/aws-lambda-best-practices-7454da49314d
https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html
https://medium.com/platform-engineer/aws-lambda-functions-best-practices-f40b60596a0c
