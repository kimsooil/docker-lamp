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

s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY_ID)

User = get_user_model()


class ModelRunner:
    """
    Class to run the model using Fargate, Fargate Spot, or Onboard Compute
    """

    def __init__(self, serialized_data, sim_run_data, request):
        self.serialized_data = serialized_data
        self.request = request
        # if needed in the future, extraneous at this point
        # self.timestamp = serialized_data['timestamp']
        self.model_input = serialized_data['model_input']
        # self.model_output = None
        self.id = sim_run_data.id
        self.webhook_token = str(sim_run_data.webhook_token)
        self.webhook_url = reverse(
            'simulations-webhook', args=[self.id], request=request)
        self.capacity_provider = serialized_data['capacity_provider']
        self.s3_object = self.createS3Object()

        # can be submitted with just the constructor
        # remove submitJob in views.py
        # self.submitJob()

    def submit(self):
        # currently no difference between FARGATE/FARGATE_SPOT
        if self.capacity_provider == 'FARGATE':
            Fargate(self.s3_object)
        elif self.capacity_provider == 'FARGATE_SPOT':
            FargateSpot(self.s3_object)
        elif self.capacity_provider == 'onboard':
            model = OnboardCompute(self.model_input)
            model.submit()
    # moved to the view
    # def determineJobType(self):
    #     user = User.objects.get(id=request.user.id)
    #     if user.groups.filter(name='Fargate').exists():
    #         return 'FARGATE'
    #     elif user.groups.filter(name='Fargate Spot').exists():
    #         return'FARGATE_SPOT'
    #     elif user.groups.filter(name='Onboard Compute').exists():
    #         return'onboard_compute'
    #     # default currently if not in group
    #     else:
    #         return 'onboard_compute'

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
        self.submit()

    def submit(self):
        s3_data = str(json.dumps(self.s3_object))
        key_name = time.strftime("%Y%m%d-%H%M%S") + "-ndcovid.json"
        print('FARGATE')
        # put in s3
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
    Subclass of ModelRunner to submit a Fargate Spot job
    """

    def __init__(self, s3_object):
        self.s3_object = s3_object
        self.submit()

    def submit(self):
        # No progress updates to the webhook for spot
        self.s3_object.update({'progress_delay': 0})
        s3_data = str(json.dumps(self.s3_object))
        key_name = time.strftime("%Y%m%d-%H%M%S") + "-ndcovid.json"
        print('FARGATE SPOT')
        # put in s3
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
        encode_params = urllib.parse.urlencode(self.model_input, True)
        api_path = settings.MODEL_API_BASE_URL + \
            settings.MODEL_API_START + str(encode_params)
        r = requests.get(api_path)
        r.raise_for_status()
        return Response(r.json(), status=r.status_code)

    def status(self):
        encode_params = urllib.parse.urlencode(self.model_input, True)
        api_path = settings.MODEL_API_BASE_URL + \
            settings.MODEL_API_STATUS + str(encode_params)
        r = requests.get(api_path)
        r.raise_for_status()
        return r.json()


# https://seircast.org/backend/model/api/v3/prediction_status/?sim_length=60&shelter_date=2020-03-27&shelter_release_start_date=2020-05-04&shelter_release_end_date=2020-06-29&social_distancing=true&quarantine_percent=0&social_distancing_end_date=2020-06-15&quarantine_start_date=2020-08-01&country=US&state=Florida&nDraws=50000&county=Hillsborough&county=Pasco&county=Pinellas&county=Polk
# /model/api/v3/prediction_status/?sim_length=62&shelter_date=2020-03-27&shelter_release_start_date=2020-05-04&shelter_release_end_date=2020-06-29&social_distancing=True&quarantine_percent=0&social_distancing_end_date=2020-06-15&quarantine_start_date=2020-08-01&country=US&state=Florida&nDraws=50000&county=%5B%27Hillsborough%27%2C+%27Pasco%27%2C+%27Pinellas%27%2C+%27Polk%27%5D
# /model/api/v3/prediction_status/?country=US&state=Florida&shelter_date=2020-03-27&shelter_release_start_date=2020-05-04&shelter_release_end_date=2020-06-29&county=%5B%27Hillsborough%27%2C+%27Pasco%27%2C+%27Pinellas%27%2C+%27Polk%27%5D&sim_length=61&nDraws=50000&social_distancing=True&social_distancing_end_date=2020-06-15&quarantine_percent=0&quarantine_start_date=2020-08-01
