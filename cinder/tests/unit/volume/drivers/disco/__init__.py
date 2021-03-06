# Copyright (c) 2015 Industrial Technology Research Institute.
#
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Parent class for the DISCO driver unit test."""

import mock
from suds import client

from os_brick.initiator import connector

from cinder import context
from cinder import test
from cinder.tests.unit import fake_volume
from cinder.volume import configuration as conf
import cinder.volume.drivers.disco.disco as driver


class TestDISCODriver(test.TestCase):
    """Generic class for the DISCO test case."""

    DETAIL_OPTIONS = {
        'success': 1,
        'pending': 2,
        'failure': 3
    }

    ERROR_STATUS = 1

    def setUp(self):
        """Initialise variable common to all the test cases."""
        super(TestDISCODriver, self).setUp()

        mock_exec = mock.Mock()
        mock_exec.return_value = ('', '')
        self.cfg = mock.Mock(spec=conf.Configuration)
        self.cfg.disco_client = '127.0.0.1'
        self.cfg.disco_client_port = '9898'
        self.cfg.disco_wsdl_path = 'somewhere'
        self.cfg.volume_name_prefix = 'openstack-'
        self.cfg.num_volume_device_scan_tries = 1
        self.cfg.snapshot_check_timeout = 3600
        self.cfg.restore_check_timeout = 3600
        self.cfg.clone_check_timeout = 3600
        self.cfg.snapshot_reserve_days = -1
        self.cfg.retry_interval = 1

        self.FAKE_SOAP_RESPONSE = {
            'standard': {
                'success': {'status': 0, 'result': 'a normal message'},
                'fail': {'status': 1, 'result': 'an error message'}}
        }

        mock.patch.object(client,
                          'Client',
                          self.create_client).start()

        mock.patch.object(connector.InitiatorConnector,
                          'factory',
                          self.get_mock_connector).start()

        mock.patch.object(driver.DiscoDriver,
                          '_get_connector_identifier',
                          self.get_mock_attribute).start()

        self.driver = driver.DiscoDriver(execute=mock_exec,
                                         configuration=self.cfg)
        self.driver.do_setup(None)

        self.ctx = context.RequestContext('fake', 'fake', auth_token=True)
        self.volume = fake_volume.fake_volume_obj(self.ctx)
        self.volume['volume_id'] = '1234567'

        self.requester = self.driver.client.service

    def create_client(self, *cmd, **kwargs):
        """Mock the suds client."""
        return FakeClient()

    def get_mock_connector(self, *cmd, **kwargs):
        """Mock the os_brick connector."""
        return None

    def get_mock_attribute(self, *cmd, **kwargs):
        """Mock the os_brick connector."""
        return 'DISCO'


class FakeClient(object):
    """Fake class to mock suds.Client."""

    def __init__(self, *args, **kwargs):
        """Create a fake service attribute."""
        self.service = FakeMethod()


class FakeMethod(object):
    """Fake class recensing some of the method of the suds client."""

    def __init__(self, *args, **kwargs):
        """Fake class to mock the suds client."""

    def volumeCreate(self, *args, **kwargs):
        """"Mock function to create a volume."""

    def volumeDelete(self, *args, **kwargs):
        """"Mock function to delete a volume."""

    def snapshotCreate(self, *args, **kwargs):
        """"Mock function to create a snapshot."""

    def snapshotDetail(self, *args, **kwargs):
        """"Mock function to get the snapshot detail."""

    def snapshotDelete(self, *args, **kwargs):
        """"Mock function to delete snapshot."""

    def restoreFromSnapshot(self, *args, **kwargs):
        """"Mock function to create a volume from a snasphot."""

    def restoreDetail(self, *args, **kwargs):
        """"Mock function to detail the restore operation."""

    def volumeDetailByName(self, *args, **kwargs):
        """"Mock function to get the volume detail from its name."""

    def volumeClone(self, *args, **kwargs):
        """"Mock function to clone a volume."""

    def cloneDetail(self, *args, **kwargs):
        """Mock function to get the clone detail."""

    def volumeExtend(self, *args, **kwargs):
        """Mock function to extend a volume."""

    def systemInformationList(self, *args, **kwargs):
        """Mock function to get the backend properties."""
