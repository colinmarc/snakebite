# -*- coding: utf-8 -*-
# Copyright (c) 2013 Spotify AB
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
from minicluster import MiniClusterTestBase
from spotify.snakebite.errors import FileNotFoundException
from spotify.snakebite.errors import InvalidInputException


class ChgrpTest(MiniClusterTestBase):

    def test_onepath(self):
        self.client.chgrp(['/dir1'], "onepathgroup")
        client_output = self.client.ls(['/dir1'], include_toplevel=True, include_children=False)
        self.assertEqual(client_output[0]["group"], "onepathgroup")

    def test_multipath(self):
        self.client.chgrp(['/dir1', '/zerofile'], "multipathgroup")
        client_output = self.client.ls(['/dir1', '/zerofile'], include_toplevel=True, include_children=False)
        for node in client_output:
            self.assertEqual(node["group"], "multipathgroup")

    def test_recursive(self):
        self.client.chgrp(['/'], 'recursivegroup', recurse=True)
        expected_output = self.cluster.ls(["/"], ["-R"])
        for node in expected_output:
            self.assertEqual(node["group"], "recursivegroup")

    def test_unknown_file(self):
        self.assertRaises(FileNotFoundException, self.client.chgrp, ['/nonexistent'], 'myOnwer', recurse=True)

    def test_invalid_input(self):
        self.assertRaises(InvalidInputException, self.client.chgrp, '/doesnotexist', 'myOnwer')