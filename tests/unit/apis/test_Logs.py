import sys; sys.path.append('..')

from pbx_gs_python_utils.utils.Misc import Misc
from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from osbot_aws.apis.Logs import Logs


class test_Logs(TestCase):

    log_group   = '/unit-tests/test_log_group'
    stream_name = '/tmp_stream'
    logs      = Logs(log_group,stream_name)

    @classmethod
    def setUpClass(cls):
        assert test_Logs.logs.group_create() is True

    @classmethod
    def tearDownClass(cls):
        assert test_Logs.logs.group_delete() is True

    def setUp(self):
        self.logs = Logs(test_Logs.log_group,test_Logs.stream_name)
        self.logs.stream_create()


    def test_log_group_create_delete_exists_info(self):
        tmp_log_group = Misc.random_string_and_numbers(prefix='/unit-tests/test_log_group_')
        temp_logs     = Logs(tmp_log_group,'')
        assert temp_logs.group_exists () is False
        assert temp_logs.group_create () is True
        assert temp_logs.group_exists () is True
        assert temp_logs.group_info   ().get('logGroupName') == tmp_log_group
        assert temp_logs.group_delete () == True
        assert temp_logs.group_exists () is False

    def test_groups(self):
        assert len(list(self.logs.groups())) > 1
        assert len(self.logs.groups()) > 100

    # def test_logs(self):
    #     group_name  = 'awslogs-temp_task_on_temp_cluster_X29B3K'
    #     stream_name = 'awslogs-example/gs-docker-codebuild/f8ccf213-b642-466c-8458-86af9933eca9'
    #     messages    = self.logs.get_messages(group_name, stream_name)
    #     assert len(messages) > 10
    #
    def test_streams__exists_delete_create(self):
        assert self.logs.stream_exists() is True                                        # log stream is created by setUpClass
        assert self.logs.streams().pop().get('logStreamName') == test_Logs.stream_name
        assert self.logs.stream_delete() is True
        assert self.logs.stream_delete() is False
        assert self.logs.streams() == []
        assert self.logs.stream_create() is True
        assert self.logs.stream_create() is False