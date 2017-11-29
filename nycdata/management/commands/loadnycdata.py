from importlib import import_module
import traceback

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = 'dataset_name'
    help = 'Loads NYC data (addresses, buildings, parcels, ...)'

    datasets = {
        'landmarks': 'nycdata.landmarks',
        'libraries': 'nycdata.libraries',
        'nycha': 'nycdata.nycha',
        'parcels': 'nycdata.parcels',
        'parks': 'nycdata.parks',
        'postoffices': 'nycdata.postoffices',
        'shoreline': 'nycdata.shoreline',
        'urbanrenewal': 'nycdata.urbanrenewal',
        'waterfront': 'nycdata.waterfront',
    }

    def add_arguments(self, parser):
        parser.add_argument('dataset_name', type=str)

    def handle(self, dataset_name, *args, **options):
        try:
            load_module = import_module('%s.load' % self.datasets[dataset_name])
            load_module.load()
        except KeyError:
            traceback.print_exc()
            raise CommandError('Could not find dataset %s' % dataset_name)
        except Exception:
            traceback.print_exc()
            raise CommandError('There was a problem loading data')
