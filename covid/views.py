import requests
import json
import csv

from oauth2_provider.views.generic import ProtectedResourceView
from rest_framework import status, viewsets
from rest_framework.reverse import reverse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.conf import settings
from django.forms.models import model_to_dict

from .models import County, State, SimulationRun, HashValue, HashFile
from .serializers import CountySerializer, SimulationRunSerializer, HashValueSerializer, HashFileSerializer


from django.contrib.auth import get_user_model
from django.db import models
# from urls import urlpatterns
import boto3
import time
import urllib.parse
from datetime import datetime, timedelta
from django.utils.timezone import utc
from rest_framework import serializers
from .model_runners import ModelRunner, OnboardCompute
s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY_ID)

# Create your views here.

# Pass Through View to Flask API
User = get_user_model()


class ProxyToModelAPIView(APIView):

    def get(self, request, format=None):
        # Convert the Django path to an appropriate flask path
        api_path = request.get_full_path().replace(
            settings.MODEL_API_SUBPATH, settings.MODEL_API_BASE_URL)
        r = requests.get(api_path)
        return Response(r.json(), status=r.status_code)

# Proxy Routes that require authentication.


class ProtectedProxyToModelAPIView(ProtectedResourceView, ProxyToModelAPIView):
    pass


class SystemConfigurationAPIView(APIView):

    def get(self, request, format=None):
        data = {
            'country': settings.MODEL_API_COUNTRY,
            'state': settings.MODEL_API_STATE,
            'state_abbreviation': settings.MODEL_API_STATE_ABBREVIATION,
            'model_defaults': {
                'counties': settings.API_DEFAULT_COUNTIES,
                'shelter_date': settings.API_DEFAULT_SHELTER_DATE,
                'shelter_release_start_date': settings.API_DEFAULT_SHELTER_RELEASE_START_DATE,
                'shelter_release_end_date': settings.API_DEFAULT_SHELTER_RELEASE_END_DATE,
                'social_distancing': settings.API_DEFAULT_SOCIAL_DISTANCING,
                'social_distancing_end_date': settings.API_DEFAULT_SOCIAL_DISTANCING_END_DATE,
                'quarantine_start_date': settings.API_DEFAULT_QUARANTINE_START_DATE,
                'quarantine_percent': settings.API_DEFAULT_QUARANTINE_PERCENT,
                'high_risk_quarantine_percent': settings.API_DEFAULT_HIGH_RISK_QUARANTINE_PERCENT,
                'sim_length': settings.API_DEFAULT_SIM_LENGTH,
                'nDraws': settings.API_DEFAULT_NDRAWS
            },
            'default_counties': settings.API_DEFAULT_COUNTIES,
            'map': {
                'center': [
                    float(settings.API_DEFAULT_MAP_X_COORD),
                    float(settings.API_DEFAULT_MAP_Y_COORD)
                ],
                'zoom': settings.API_DEFAULT_MAP_ZOOM_LEVEL
            },
            'default_state': settings.API_DEFAULT_STATE,
            'states': [model_to_dict(state, fields=[field.name for field in state._meta.fields], exclude=['id']) for state in State.objects.all().order_by('name')]
        }

        return Response(data)


class CountyResourcesAPIView(ListAPIView):
    queryset = County.objects.all().order_by('name')
    serializer_class = CountySerializer


class HardCodedModelOutputAPIView(ProtectedResourceView, APIView):

    def get(self, request, format=None):
        hard_coded_response_json = {"Cumulative": [[1.7261521407235438, 3.2688168500007171, 4.271571665127003], [9.1679151421131522, 14.135934407609934, 19.7277523579864], [19.615619232566274, 28.461461271413722, 38.512638119072882], [31.319863751502844, 44.406065194884988, 58.509215912196623], [45.245453863299076, 62.734701698623454, 80.5110552481515], [61.546537885414921, 83.7077494134092, 106.08581819802666], [81.19284244240589, 108.98881682169416, 136.45096554876238], [105.6407042678471, 139.48501726543913, 172.48572563771782], [136.45387502219282, 175.44230955058748, 215.44926563540224], [175.3115556266323, 217.71108446169256, 266.96069090568233], [221.5806755139505, 269.05595387112976, 327.49376370922664], [281.15376227228734, 329.909663641058, 404.58566167711217], [353.667426220871, 403.08851341953516, 497.56124825939889], [441.91760189281723, 492.07250672666908, 607.02439201900381], [545.50834116201213, 596.34453932202973, 732.64555389284556], [659.04577268082244, 718.18063950128158, 874.44940911366325], [774.25208017411558, 850.10714549059753, 1027.0251343645007], [891.66913425802409, 983.45191466134747, 1176.6962977184423], [1009.2425630362795, 1116.6320540197748, 1329.295448224342], [1122.0046768570805, 1248.0654671580019, 1474.4914891066308], [1226.0885934406062, 1376.899445244977, 1606.1388525009793], [1324.1811968027193, 1499.2455457760329, 1726.0372547008387], [1411.6224889821037, 1614.3138508054712, 1838.5742481902855], [1490.5063669859951, 1721.8464453832808, 1937.0700890998498], [1558.9983101909952, 1822.0340387140218, 2042.2383172933971], [1612.5971610451111, 1912.5894006413423, 2149.6311483771819], [1660.6699928726894, 1999.9339059734705, 2263.906217723732], [1696.6503323961927, 2093.1112881900854, 2382.5720003264614], [1730.1949818197854, 2173.3690438503636, 2518.79034513657], [1758.777514809339, 2232.31963286083, 2650.4320877598443], [1787.7517860069656, 2295.5335453651032, 2780.5628802428005], [1804.6584016123247, 2348.9130336693943, 2918.062540810638], [1818.0837767660437, 2404.0084561903786, 3063.7342201343586], [1837.9127352722257, 2456.8976076569634, 3207.4375291034812], [1851.0752911390182, 2511.9944365108468, 3351.6479301724657], [1861.3070254185184, 2549.1066166928322, 3503.9591537888787], [1869.2297660384424, 2588.1461455082108, 3647.2488796782759], [1877.3610369559394, 2637.2204966604727, 3783.9349588219879], [1884.65767431685, 2682.7339206651832, 3933.3403360793518], [1891.2224229885526, 2722.1858053291389, 4084.3087366640016], [1897.1399378984681, 2752.2016039227428, 4236.8688896078365]], "Epidemic": [[27.999999999999993, 27.999999999999993, 27.999999999999993], [47.843862601913962, 60.072434545008875, 66.617032268379432], [65.926193140818711, 85.659643346766558, 96.6252805685103], [84.5390574606069, 109.12252646458231, 124.67090561102259], [104.72135837880307, 133.97838557642717, 156.97832442517554], [127.85806291999194, 162.51405484131141, 197.6318649660021], [155.01608351544175, 195.57970328761854, 245.69140598214605], [183.14679198037396, 235.02125458794211, 305.10491913529069], [219.54106635274235, 283.57274131480324, 380.18490900970261], [261.66591188233133, 340.56212896690732, 475.03565275396204], [310.17853214208981, 408.61898506884961, 592.16801453249036], [368.43212720949009, 491.40122671468464, 746.74357521556237], [436.32882749836722, 589.22383236919825, 937.25621086279216], [516.51938110741764, 708.48190271482736, 1169.5724388760659], [605.18569181536407, 846.30937673160679, 1448.3992011812109], [695.674201638552, 988.7625919091538, 1737.5899762635117], [782.63932317252772, 1121.83123067188, 1995.4818485321366], [848.7581037032752, 1236.2688758844652, 2209.500398039444], [906.53907214795538, 1329.6108461746592, 2386.1588337950238], [938.47032300965327, 1392.0982841798082, 2538.4620848924724], [949.97796336001272, 1438.7487821799373, 2615.0673870068372], [940.61989275376357, 1469.3058100543331, 2624.8982307953183], [934.2913472681247, 1476.4041799036559, 2614.0129316430125], [899.55868383549807, 1468.0294805523376, 2572.9172794694255], [855.51346914890212, 1445.2114363619853, 2518.8273135998493], [808.345853773949, 1422.1936884754591, 2475.98733717393], [759.57403926605059, 1374.5718117785955, 2435.8493620771824], [697.18562231401336, 1336.573588840829, 2390.90093539838], [623.15949679163509, 1283.4092319907518, 2327.8525105581925], [562.70735100026263, 1235.4265393354558, 2270.1224726069859], [500.11153576513533, 1184.767369677334, 2247.4964386709312], [443.45316871284524, 1135.5056585515849, 2251.3044940161208], [391.92985617053478, 1074.5314943484618, 2233.0157665827596], [346.90591980167079, 1020.5976848575779, 2212.4998115481985], [307.83981357379093, 973.06933339921625, 2189.4618776429033], [272.9765609262181, 933.8386098202767, 2229.7995071784967], [236.27951975980898, 888.0621741842732, 2213.0542718508127], [205.89593859044359, 846.90321939433284, 2202.1203655785225], [180.67307108361319, 808.23659921576927, 2237.5073868352542], [158.55956015041156, 775.28292465494383, 2266.3719305407508], [139.39068475346929, 736.36324305449955, 2267.6862425309218]], "Hospitalized": [[1.9999999999999998, 1.9999999999999998, 1.9999999999999998], [1.9154198673863871, 2.3346982634742623, 2.8785402563306093], [2.4929813730425892, 4.1051495563924032, 6.4790141248872546], [
            3.4583428580296305, 6.7632742226866451, 11.764860563757521], [4.9869211908888378, 10.533119470466495, 18.542748706758182], [7.0304704794173647, 15.148557047063932, 26.252730256460481], [9.4062520487212922, 20.601775624279338, 35.096235714598166], [12.296927572022236, 26.819923073617531, 44.266381142007639], [15.758789823749387, 33.9717179491011, 55.424615184936442], [19.505484272934208, 42.143074090388041, 68.67061270300097], [24.33125955691931, 52.203120559608465, 83.7347042855616], [29.697110049103319, 64.17482583839066, 101.68111418987634], [36.086737569282278, 77.680547605347982, 122.96648144834975], [43.264999045217706, 94.3747724545927, 148.06578687878658], [52.134993119319766, 113.42929927348175, 178.7197357681161], [62.191673221688923, 137.08751097575535, 217.18189953252929], [73.284204586035969, 164.53656392204829, 262.50828045347413], [85.51721954857679, 192.42100787081336, 311.22552556939712], [98.092001085009926, 221.80770663893077, 363.22531159348858], [110.36810560839911, 249.24016099874751, 416.41292438980935], [121.82219612627814, 274.35913642562491, 460.561205781467], [132.0193734532854, 295.79101284749521, 493.86002691039334], [140.32095874692467, 313.25907623499177, 530.98074903318616], [146.93077494004547, 327.29578199878165, 566.87221473988859], [152.07142500392644, 338.02724010012457, 603.05915215347375], [156.613952868736, 347.98988326766823, 628.07590904205381], [154.85800140377529, 349.88526179275692, 641.15147489446474], [150.58757928884827, 350.69220834319572, 652.29213373185075], [148.76546691766984, 346.63557408090446, 659.86560588121415], [141.18039059035286, 342.59396480847914, 660.082853484326], [135.86480427234613, 333.71623367183827, 667.76275244452768], [125.52464536210476, 325.26452876908189, 667.29364620406091], [120.62710852825855, 314.64866034877059, 666.65171514309156], [107.08405753835039, 301.82556762362151, 669.61279911564327], [98.167211250345019, 292.47589128809835, 671.26458517434514], [87.63466407000729, 284.46988487076521, 677.97372672468964], [78.038750325251073, 271.83371789215335, 679.41580005965159], [69.356300989391372, 263.33147292287413, 673.02526081114377], [60.346635609754451, 254.57094767644304, 678.50684665110714], [52.608183678040831, 246.7439899000336, 687.41235051361446], [44.759283374922617, 235.35140023614204, 698.16842580325658]], "ICU": [[0.99999999999999989, 0.99999999999999989, 0.99999999999999989], [0.94719277726947593, 1.316228091955657, 1.6375562704862712], [0.9897408271386342, 1.7524649812292339, 2.8724446597577185], [1.2327824495338986, 2.9520848923563863, 5.7780153767995772], [1.6687425924461954, 4.59864525990203, 9.8226777350781127], [2.2807438762226435, 6.966006267410469, 14.806262022002787], [3.1264936618084502, 9.84556234822563, 20.610513870283096], [4.1859660197088981, 13.158157789645992, 27.589900545951107], [5.4986187156636772, 17.325343946971643, 35.503578565461879], [7.08677889023935, 22.262603195699981, 44.132703618821985], [8.9900135317817025, 27.657989710435011, 53.520171722151126], [11.271909077050443, 34.36019223090392, 66.95130324289768], [13.981618898626905, 42.568651798800488, 82.417914948404672], [17.170696663987773, 52.329805990397148, 99.335261509165917], [20.951772793920242, 63.2841618282084, 120.92741966200362], [25.427027226630752, 76.257414616922176, 148.266003298235], [30.670375181051661, 91.732879413223969, 177.91338616090974], [36.285098228096658, 109.0809370005521, 209.72137695904937], [41.697961366914122, 127.87797302038045, 251.13965060432341], [48.209801179982385, 148.08472983316665, 293.60193239009214], [55.425265684277022, 167.87798098873415, 333.18406802948664], [62.580216303634423, 187.7421190131775, 372.62283081370634], [68.834628367836729, 203.9043850185181, 405.64252667389678], [72.6592640114448, 220.010189128128, 435.96632810348621], [75.960283428077133, 235.11329719725853, 465.54901979423545], [77.9534633539758, 244.18786336292476, 490.66193742480107], [78.880724634837918, 250.72929388205068, 507.07070240171919], [82.9238105161268, 253.73078664325365, 515.92189172794735], [85.966481768616617, 253.33694230788365, 522.36481535020425], [81.1960356813987, 252.28618512225034, 531.96949094986564], [77.8939776023272, 247.95410176497117, 530.22315727372677], [78.332708678926991, 240.59524573964023, 533.875380959472], [75.679438480626175, 236.12621048201339, 539.35406906281776], [69.519536263284564, 231.06348292210592, 545.31638257851273], [67.013050830209309, 226.04287331800077, 537.72220045027359], [63.117560906013935, 217.66125820004669, 534.52679079543987], [57.221566589434026, 209.57582930712576, 544.92016688216], [50.25957719011361, 203.46885109416675, 547.6178807222318], [45.991324661059814, 195.166685448884, 556.19568306394763], [40.787219072523811, 189.89531800230489, 558.72161704059886], [37.002693593979039, 180.86299078395149, 557.78670030344881]], "sim_time": 14, "start_date": "20-Mar-2020", "real_time": 27, "Confirmed": [70, 94, 118, 143, 164, 187, 242, 293, 351, 404, 472, 585, 598, 846, 984, 1071, 1154, 1219, 1305, 1351, 1397, 1477, 1524, 1628, 1731, 1769, 1854], "Deaths": [0, 1, 1, 1, 1, 1, 3, 3, 4, 8, 9, 11, 11, 15, 16, 18, 19, 19, 20, 23, 27, 29, 36, 40, 41, 44, 45], "Git_hash": "e0f2ce559af52aa6adcadf21875c6d027b6e6711"}

        return Response(hard_coded_response_json)


# class RunModelProtectedAPIView(ProtectedResourceView, APIView):
class SimulationRunViewSet(viewsets.ModelViewSet):
    """
    Simulation run viewset to handle webhook, create simulation runs, and get status updates
    for the simulation runs
    """
    queryset = SimulationRun.objects.all()
    serializer_class = SimulationRunSerializer
    webhook_url = serializers.CharField(max_length=100)
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(methods=['put'], detail=True, permission_classes=[AllowAny],
            url_path='webhook', url_name='webhook')
    def handle_webhook(self, request, pk=None):
        sim_run = self.get_object()
        print(request.data)
        # validate webhook
        if str(sim_run.webhook_token) == request.data['webhook_token']:
            if not request.data.get('output'):
                return Response({'status': "webhook payload must contain an 'output' key."}, status=status.HTTP_400_BAD_REQUEST)
            # ensure model is not complete
            elif sim_run.model_output != None and type(sim_run.model_output) is dict and sim_run.model_output.get('status', None) == 'complete':
                return Response({'status': 'model completed'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # update model output and save
                sim_run.model_output = request.data['output']
                sim_run.save()
                serializer = self.get_serializer(sim_run)
                headers = self.get_success_headers(serializer.data)
                # Return the actual object with updated values
                return Response(serializer.data, headers=headers)

        else:
            return Response({'status': 'invalid webhook token'}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        # retrieve latest hash value
        latest_hash = HashValue.objects.all().order_by(
            '-timestamp')[0].hash_value
        model_input_dict = request.data
        model_input_dict['model_input'].update({'data_hash': latest_hash})
        # look for existing run with same inputs
        serializer = SimulationRunSerializer(
            data=model_input_dict)
        try:
            # get existing run
            existing_run_results = SimulationRun.objects.get(
                model_input=model_input_dict['model_input'])
            # check onboard and not finsihed
            if existing_run_results.capacity_provider == 'onboard' and (existing_run_results.model_output == None or existing_run_results.model_output['status'] != 'complete'):
                # create onboard model runner to check for status
                model_runner = OnboardCompute(existing_run_results.model_input)
                try:
                    # get status update and save to model output
                    existing_run_results.model_output = model_runner.status()
                    existing_run_results.save()
                except:
                    return Response({'error': 'Model Failed to retreive status'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            now = datetime.utcnow().replace(tzinfo=utc)
            max_time = existing_run_results.timestamp+timedelta(hours=1)
            # check to ensure model has returned results within 1 hour, exception resubmits the job after deletion
            if now > max_time and (existing_run_results.model_output == None or existing_run_results.model_output.get('status', 'none') != 'complete'):
                existing_run_results.delete()
                raise Exception("model failed to complete within 1 hour")

            # get most recent status update for model
            serializer = self.get_serializer(existing_run_results)
            return Response(serializer.data)
        except:
            # validate data
            serializer.is_valid(raise_exception=True)
            sim_run = self.perform_create(serializer)
            # create model runner class for either Fargate, Spot, or Onboard depending on capacity provider
            model_run = ModelRunner(serializer.data, sim_run, request)

            # submit job for newly created model runner
            submit_job = model_run.submit()
            # only dict type is failed submissions, rest are Requests
            if type(submit_job) is dict:
                delete_run = SimulationRun.objects.get(pk=sim_run.id)
                delete_run.delete()
                return Response(submit_job, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # put user in
        user = self.request.user
        # add capacity provider
        user_cp = User.objects.get(id=user.id)
        # filter users by group and add appropriate capacity provider to validated data to ensure
        # it only gets added one time on creation
        # default to FARGATE if user is not in a group
        if user_cp.groups.filter(name='Fargate').exists():
            serializer.validated_data.update({'capacity_provider': 'FARGATE'})
        elif user_cp.groups.filter(name='Fargate Spot').exists():
            serializer.validated_data.update(
                {'capacity_provider': 'FARGATE_SPOT'})
        elif user_cp.groups.filter(name='Onboard Compute').exists():
            serializer.validated_data.update(
                {'capacity_provider': 'onboard'})
        else:# Azure
            serializer.validated_data.update(
                {'capacity_provider': 'AZURE'})
        obj = serializer.save(user=user)

        return obj

    @action(methods=['get'], detail=False, permission_classes=[AllowAny],
            url_path='status', url_name='find_simulation')
    def status(self, request, pk=None):
        query_str = request.META['QUERY_STRING']
        model_input_vals = dict(urllib.parse.parse_qs(query_str))
        # convert list items to string values, except county
        for key, val in model_input_vals.items():
            if key != 'county':
                model_input_vals[key] = val[0]
        # convert quarantine percent to int and social_distancing to bool
        model_input_vals['quarantine_percent'] = int(
            model_input_vals['quarantine_percent'])
        if model_input_vals['social_distancing'] == 'false':
            model_input_vals['social_distancing'] = False
        else:
            model_input_vals['social_distancing'] = True

        # get the max age of the model input and remove from model input
        if 'max_age' in model_input_vals:
            max_age = int(model_input_vals['max_age'])
            model_input_vals.pop('max_age')
        else:
            max_age = -1
        model_input_dict = {'model_input': model_input_vals}

        # get all available hashes
        hash_queryset = HashValue.objects.all().order_by('-timestamp')

        # check for model inputs with every hash until one is found. The hashes after will contain older data
        for hash in hash_queryset:
            model_input_dict['model_input'].update(
                {'data_hash': hash.hash_value})
            # try to find existing runs with hash values
            try:
                existing_run_results = SimulationRun.objects.get(
                    model_input=model_input_dict['model_input'])
                # update model output if onboard compute
                if existing_run_results.capacity_provider == 'onboard' and (existing_run_results.model_output == None or existing_run_results.model_output['status'] != 'complete'):
                    model_runner = OnboardCompute(
                        existing_run_results.model_input)
                    try:
                        existing_run_results.model_output = model_runner.status()
                        existing_run_results.save()
                    except:
                        return Response({'error': 'Model failed to retrieve status'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                # check timeframe if given maximum time for data
                if max_age > 0:
                    now = datetime.utcnow().replace(tzinfo=utc)
                    max_time = existing_run_results.timestamp + \
                        timedelta(days=max_age)
                    if now > max_time:
                        return Response({'error': 'No model within this timeframe found'}, status=status.HTTP_404_NOT_FOUND)
                serializer = self.get_serializer(existing_run_results)
                return Response(serializer.data['model_output'])
            except:
                # max_age == 0 indicates only the current hash is acceptable, no second chance
                if max_age == 0:
                    return Response({'error': 'Model does not exist with current hash'}, status=status.HTTP_404_NOT_FOUND)
                pass

        # no model with any existing hashes
        return Response({'error': 'Model does not exist'}, status=status.HTTP_404_NOT_FOUND)


class HashResourceAPIView(APIView):
    """
    A simple ViewSet for viewing and posting hashvalues in the database.
    """

    def get(self, request, format=None):
        queryset = HashValue.objects.all().order_by('id')
        hash_value = request.query_params.get('hash_value', None)
        if hash_value is not None:
            queryset = queryset.filter(hash_value=hash_value)
        serializer = HashValueSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = HashValueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HashFileAPIView(APIView):
    """
    A simple ViewSet for viewing and posting hashvalues in the database.
    """

    def get(self, request, format=None):
        queryset = HashFile.objects.all().order_by('id')
        serializer = HashFileSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = HashFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StateCountyAPIView(APIView):
    """
    A simple get API View to return all the states and their respected counties
    """

    def get(self, request, format=None):
        confirmed_filename = HashValue.objects.all().order_by(
            '-timestamp')[0].timeseries_confirmed.path

        # filters for extra data in JH dataset
        state_filter = ['Diamond Princess', 'Grand Princess']
        county_filter = ['Out of ', 'Unassigned']

        # store states and their counties
        states = []
        counties = {}

        # try and get data
        try:
            # loop through data
            with open(confirmed_filename) as csvfile:
                spamreader = csv.reader(csvfile)
                # skip headers
                next(spamreader)

                # get every row
                for row in spamreader:
                    # print("test")
                    # reject non states
                    if row[6] in state_filter:
                        continue

                    # add new state
                    if row[6] not in states:
                        states.append(row[6])
                        counties[row[6]] = []

                    # add counties to states
                    save_county = True
                    for cfilt in county_filter:
                        if cfilt in row[5]:
                            save_county = False

                    # add
                    if save_county:
                        counties[row[6]].append(row[5])

            # return results
            return Response({"states": states, "counties": counties}, status=status.HTTP_201_CREATED)

        except:
            return Response({"states": "None", "counties": "None"}, status=status.HTTP_400_BAD_REQUEST)
