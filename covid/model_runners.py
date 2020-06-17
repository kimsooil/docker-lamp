import json
import time
import boto3
import urllib
import requests

from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.conf import settings

# used to upload objects to s3 bucket
s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY_ID)


class ModelRunner:
    """
    Class to run the model using Fargate, Fargate Spot, or Onboard Compute
    """

    def __init__(self, serialized_data, sim_run_data, request):
        self.serialized_data = serialized_data
        self.request = request
        self.model_input = serialized_data['model_input']
        self.id = sim_run_data.id
        # get webhook token
        self.webhook_token = str(sim_run_data.webhook_token)
        #  create webhook url
        self.webhook_url = reverse(
            'simulations-webhook', args=[self.id], request=request)
        #  determine capacity provider from the model
        self.capacity_provider = serialized_data['capacity_provider']
        self.s3_object = self.createS3Object()

        # can be submitted with just the constructor
        # remove submitJob in views.py
        # self.submitJob()

    def submit(self):
        # submit job depending on capacity provider
        # fargate and spot submit are called in the initialization of the object
        # onboard submit needs to be called explicitly, as it is created to get status as well
        if self.capacity_provider == 'FARGATE':
            Fargate(self.s3_object)
        elif self.capacity_provider == 'FARGATE_SPOT':
            FargateSpot(self.s3_object)
        elif self.capacity_provider == 'onboard':
            model = OnboardCompute(self.model_input)
            model.submit()

    def createS3Object(self):
        # create object to upload to S3 for fargate and spot which include additional data created in constructor
        # onboard does not need s3 object
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
        # submit the job on initialization of the instance
        self.submit()

    def submit(self):
        # convert to string for put_object formatting
        s3_data = str(json.dumps(self.s3_object))
        # add timestamp as object name for anything uploaded to S3
        key_name = time.strftime("%Y%m%d-%H%M%S") + "-ndcovid.json"
        # put in s3 to trigger lambda
        try:
            s3_client.put_object(
                Body=s3_data,
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=key_name
            )
        except:
            return Response({'error': 'Failed to upload object to s3 - fargate'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FargateSpot(ModelRunner):
    """
    Subclass of ModelRunner to submit a Fargate Spot job with no progress to webhook
    """

    def __init__(self, s3_object):
        self.s3_object = s3_object
        # submit the job on initialization of the instance
        self.submit()

    def submit(self):
        # No progress updates to the webhook for spot
        self.s3_object.update({'progress_delay': 0})
        # convert to string for put_object formatting
        s3_data = str(json.dumps(self.s3_object))
        # add timestamp as object name for anything uploaded to S3
        key_name = time.strftime("%Y%m%d-%H%M%S") + "-ndcovid.json"
        # put in s3 to trigger lambda
        try:
            s3_client.put_object(
                Body=s3_data,
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=key_name
            )
        except:
            return Response({'error': 'Failed to upload object to s3 - spot'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OnboardCompute(ModelRunner):
    """
    Subclass of ModelRunner to submit a Onboard Compute job
    """

    def __init__(self, model_input):
        self.model_input = model_input

    def submit(self):
        print('onboard')
        # encode model input, True used for list object (county)
        encode_params = urllib.parse.urlencode(self.model_input, True)
        # create url from settings and encoded paramaters to submit job
        api_path = settings.MODEL_API_BASE_URL + \
            settings.MODEL_API_START + str(encode_params)
        # send get request to start the job and get response
        r = requests.get(api_path)
        r.raise_for_status()
        return Response(r.json(), status=r.status_code)

    def status(self):
        # encode model input, True used for list object (county)
        encode_params = urllib.parse.urlencode(self.model_input, True)
        # create url from settings and encoded paramaters to get status of job
        api_path = settings.MODEL_API_BASE_URL + \
            settings.MODEL_API_STATUS + str(encode_params)
        # send get request to receive satatus for job and get response
        r = requests.get(api_path)
        r.raise_for_status()
        return r.json()
