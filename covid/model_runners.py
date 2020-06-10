from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model
from django.conf import settings

import json
import time
import boto3
s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY_ID)

User = get_user_model()


class ModelRunner:
    """
    Class to run the model using Fargate, Fargate Spot, or Onboard Compute
    """

    def __init__(self, serialized_data, sim_run_data, request):
        self.serialized_data = serialized_data
        # if needed in the future, extraneous at this point
        # self.timestamp = serialized_data['timestamp']
        # self.model_input = serialized_data['model_input']
        # self.model_output = None
        self.id = sim_run_data.id
        self.webhook_token = str(sim_run_data.webhook_token)
        self.webhook_url = reverse(
            'simulations-webhook', args=[self.id], request=request)
        self.capacity_provider = self.determineJobType(request)
        self.s3_object = self.createS3Object()

        # can be submitted with just the constructor
        # remove submitJob in views.py
        # self.submitJob()

    def submitJob(self):
        # currently no difference between FARGATE/FARGATE_SPOT
        if self.capacity_provider == 'FARGATE':
            Fargate(self.s3_object)
        elif self.capacity_provider == 'FARGATE_SPOT':
            FargateSpot(self.s3_object)
        # need to implement onboard computes
        # else:
        #     OnboardCompute(self.serialized_data)

    def determineJobType(self, request):
        user = User.objects.get(id=request.user.id)
        if user.groups.filter(name='Fargate').exists():
            return 'FARGATE'
        elif user.groups.filter(name='Fargate Spot').exists():
            return'FARGATE_SPOT'
        else:
            return 'FARGATE'

    def createS3Object(self):
        if self.capacity_provider != 'onboard_compute':
            s3_dict = {'webhook_url': self.webhook_url,
                       'capacity_provider': self.capacity_provider, 'webhook_token': self.webhook_token}
            s3_dict.update(self.serialized_data)
            return s3_dict
        else:
            return -1


class Fargate(ModelRunner):
    """
    Subclass of ModelRunner to submit a Fargate job
    """

    def __init__(self, s3_object):
        self.s3_object = s3_object
        self.submitJob()

    def submitJob(self):
        s3_data = str(json.dumps(self.s3_object))
        key_name = time.strftime("%Y%m%d-%H%M%S") + "-ndcovid.json"
        # put in s3
        response = s3_client.put_object(
            Body=s3_data,
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=key_name
        )


class FargateSpot(ModelRunner):
    """
    Subclass of ModelRunner to submit a Fargate Spot job
    """

    def __init__(self, s3_object):
        self.s3_object = s3_object
        self.submitJob()

    def submitJob(self):
        s3_data = str(json.dumps(self.s3_object))
        key_name = time.strftime("%Y%m%d-%H%M%S") + "-ndcovid.json"
        # put in s3
        response = s3_client.put_object(
            Body=s3_data,
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=key_name
        )


# class OnboardCompute(ModelRunner):
#     def submitJob(self):
#         print('Onboard!!!')
#         print(self.s3_object)
