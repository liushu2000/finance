__author__ = 'shu'
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from finance.import_data import *
class Command(BaseCommand):
    help = 'Import Data from excel'

    def add_arguments(self, parser):
        """
        Retrieve all existing product types from a ZODB.
        """
        option_list = BaseCommand.option_list + (
            make_option(
                '-i',
                '--userid',
                default='claimcore25',
                dest='user_id',
                help='User id for authentication',
                metavar='USERID'
            ),
            make_option(
                '-p',
                '--password',
                default='m@gg0t13#',
                dest='password',
                help='Password for URL',
                metavar='PASSWORD'
            )

        )

    def handle(self, *args, **options):
        # dialy_rf_rm_rf()
        dialy_price_returns()



        # monthly_market_value()
        # monthly_book_value()
        # monthly_sales()
        # monthly_return()

        self.stdout.write('Successfully Import Data')
