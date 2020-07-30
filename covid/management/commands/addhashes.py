from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from covid.models import HashValue, HashFile
import requests
import datetime
import ssl
import json
import os
import shutil


def create_save_hash_file(content, path):
    hash_file = HashFile()
    file_content = ContentFile(content)
    hash_file.file.save(path, file_content)
    hash_file.save()
    return hash_file


def remove_current_dir(path):
    """
    Removes all current hash files from the directory
    """
    if os.path.exists(path):
        shutil.rmtree(path)


def remove_files():
    """ 
    Removes all current hash files from the database
    """
    queryset = HashFile.objects.all().order_by('id')
    for file in queryset:
        file.delete()


def download_precomputes(self, data_hash):
        # filename info
    model_base_location = 'http://www.crc.nd.edu/~csweet1/covid_pre_compute/'
    model_file_list = 'model_files.txt'
    model_local = 'output/'
    # fix ssl?
    ssl._create_default_https_context = ssl._create_unverified_context

    # check to see if we already did this
    # if hash not already in database
    try:
        HashValue.objects.get(hash_value=data_hash)
        self.stdout.write(
            "Most recent hash and associated files have already been added.")
        return 1
    except HashValue.DoesNotExist:
        # ensure that model files exist to ensure this is a valid hash
        resp = requests.get(model_base_location + data_hash + '/' +
                            model_file_list)

        # failed or succeeded
        if resp.status_code == 400:
            self.stdout.write("No data available")
            return -1
        elif resp.status_code == 200:
            self.stdout.write("Data is available")
            # remove all current files from db
            remove_files()
            # remove output folder to replace with new content
            remove_current_dir('app/hash_files/output')
          
            path = model_local+'/'+model_file_list
            hash_file = create_save_hash_file(resp.text, path)

            # get current path to the file object
            hash_file_obj = hash_file.file.path

            # check if files in filename
            files_listed = True
            # get file
            with open(hash_file_obj) as model_files:
                files = model_files.readlines()

                files = [x.strip() for x in files]
                # check file has models
                if 'model_' not in files[0]:
                    self.stdout.write("no data available")

                    # flag
                    files_listed = False

                    # return
                    return -1

            # data is available
            # do not need to download
            if files_listed:
                return 0



def download_inputs(self, data_hash):
    confirmed_filename = 'time_series_covid19_confirmed_US.csv'
    deaths_filename = 'time_series_covid19_deaths_US.csv'
    base_address = 'http://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'
    base_folder = 'input/'

    # remove output folder to replace with new content
    if os.path.exists('app/hash_files/input'):
        shutil.rmtree('app/hash_files/input')

    resp_conf = requests.get(base_address + confirmed_filename)
    resp_death = requests.get(base_address + deaths_filename)

    path = base_folder+confirmed_filename
    create_save_hash_file(resp_conf.text, path)

    path = base_folder+deaths_filename
    create_save_hash_file(resp_death.text, path)


class Command(BaseCommand):
    help = 'Adds any new hashes added to github API'

    def add_arguments(self, parser):
        # used to delete all hash values in the databse
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete hashes instead of adding',
        )

        # used to add all the hashes to the database the first time the command is run
        # after this has been run one time, run normally
        parser.add_argument(
            '--all',
            action='store_true',
            help='Add all hashes, to ensure older hashes get added'
        )

    def handle(self, *args, **options):
        if options['delete']:
            # delete all hashes in database
            all_hashes = HashValue.objects.all()
            for hash in all_hashes:
                hash.delete()
            self.stdout.write("deleted all hashes")
        else:
            self.stdout.write("Starting the script")
            confirmed_filename = 'time_series_covid19_confirmed_US.csv'
            # dont beleive this is necessary anymore
            try:
                current_time = float(datetime.datetime.utcfromtimestamp(
                    HashValue.objects.all().order_by('timestamp')[0]).strftime("%s"))
            except:
                # some past time if no files
                current_time = 1088058000.0

            # api-endpoint
            URL = "http://api.github.com/repos/CSSEGISandData/COVID-19/commits"

            # defining a params dict for the parameters to be sent to the API
            PARAMS = {}

            # sending get request and saving the response as response object
            r = requests.get(url=URL, params=PARAMS)

            # extracting data in json format
            data = r.json()

            previously_added = False

            # data is a list if we get commit data
            if isinstance(data, list):
                # run through commits to see if there is a new one with our data
                previously_added = False
                for data_point in data:
                    # only check commits with message "automated update"
                    if data_point['commit']['message'] == "automated update":

                        # break if we hit hash in database already, rest will already be added
                        # only used if --all NOT specified
                        if previously_added == True:
                            break
                        # sending get request and saving the response as response object
                        rc = requests.get(
                            url=URL + '/' + data_point['sha'], params=PARAMS)

                        # extracting data in json format
                        commit_data = rc.json()

                        # find commit date in UTC
                        commmit_date = float(datetime.datetime.strptime(
                            data_point['commit']['committer']['date'], '%Y-%m-%dT%H:%M:%SZ').strftime("%s"))

                        # break? Commits are in time ordered, so if this is old then all subsequent are
                        if commmit_date < current_time:
                            break

                        # check to see if our file was updated
                        for file in commit_data['files']:
                            if confirmed_filename in file['filename']:
                                # is the commit newer?
                                # add data_point['sha'] to database with timestamp
                                # if hash not currently in database
                                self.stdout.write(
                                    "Adding Hash: "+data_point['sha'] + " with time: "+data_point['commit']['committer']['date'])

                                try: 
                                    HashValue.objects.get(hash_value=data_point['sha'])
                                    self.stdout.write(
                                        "Hash already exists: "+data_point['sha'])
                                except ObjectDoesNotExist:

                                    new_hash = HashValue.create(data_point['sha'],
                                                                data_point['commit']['committer']['date'])
                                    
                                    self.stdout.write(
                                        "Created Hash: "+data_point['sha'] + " with time: "+data_point['commit']['committer']['date'])

                                    confirmed_filename = 'time_series_covid19_confirmed_US.csv'
                                    deaths_filename = 'time_series_covid19_deaths_US.csv'
                                    base_address = 'http://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'

                                    resp_conf = requests.get(base_address + confirmed_filename)
                                    confirmed_file_content = ContentFile(resp_conf.text)
                                    new_hash.timeseries_confirmed.save(confirmed_filename, confirmed_file_content)


                                    resp_death = requests.get(base_address + deaths_filename)
                                    deaths_file_content = ContentFile(resp_conf.text)
                                    new_hash.timeseries_deaths.save(deaths_filename, deaths_file_content)

                                    new_hash.save()
                                    self.stdout.write(
                                        "Saved Hash: "+data_point['sha'] + " with time: "+data_point['commit']['committer']['date'] + " to database.")

                                    if not options['all']:
                                        previously_added = True
                                    
                                    break
                    if previously_added:
                        break                
            else:
                self.stdout.write("Hourly API rate limit exceeded!")
