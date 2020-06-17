from django.core.management.base import BaseCommand, CommandError
from covid.models import HashValue
import requests
import datetime
import ssl


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
        return 1
    except HashValue.DoesNotExist:
        # ensure that model files exist to ensure this is a valid hash
        resp = str(requests.get(model_base_location + data_hash + '/' +
                                model_file_list))
        # failed or succeeded
        if '404' in resp:
            self.stdout.write("No data available")
            return -1
        elif '200' in resp:
            self.stdout.write("Data is available")
            return 0


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
                                if commmit_date > current_time:

                                    ret = download_precomputes(
                                        self, data_point['sha'])

                                    # if downloaded add hash
                                    if ret == 0:
                                        # add data_point['sha'] to database with timestamp
                                        # if hash not currently in database
                                        self.stdout.write(
                                            "Adding Hash: "+data_point['sha'] + " with time: "+data_point['commit']['committer']['date'])

                                        try:
                                            # create hash
                                            new_hash = HashValue.create(data_point['sha'],
                                                                        data_point['commit']['committer']['date'])
                                            self.stdout.write(
                                                "Created Hash: "+data_point['sha'] + " with time: "+data_point['commit']['committer']['date'])
                                            # save hash
                                            new_hash.save()
                                            self.stdout.write(
                                                "Saved Hash: "+data_point['sha'] + " with time: "+data_point['commit']['committer']['date'] + " to database.")
                                        except:
                                            self.stdout.write(
                                                "Failed to add hash (could already exist): "+data_point['sha'])
                                            pass
                                    # used only if you have existing hashes in db and only want most recent to be added
                                    elif not options['all'] and ret == 1:
                                        # this has already been added and so have all after (timeordered)
                                        previously_added = True

                                break  # need to exit as ordered in time

            else:
                self.stdout.write("Hourly API rate limit exceeded!")
