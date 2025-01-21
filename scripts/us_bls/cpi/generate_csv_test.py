# Copyright 2025 Google LLC
# Author: Shamim Ansari
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import unittest
import os
from absl import logging
import pandas as pd
from generate_csv import process
from pathlib import Path

_MODULE_DIR = os.path.dirname(__file__)
TEST_DATA_DIR = os.path.join(_MODULE_DIR, 'test_data')
output_dir = os.path.join(TEST_DATA_DIR, 'output_dir')
Path(output_dir).mkdir(parents=True, exist_ok=True)
series_id = "CUSR0000SA0"
series_name = "cpi_u_1913_2024"
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
class TestGenerateCSV(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def test_GenerateCSV_data(self):
        #Calling process method
        process(TEST_DATA_DIR, series_id, series_name, output_dir, int(1946))
        expected_df = pd.read_csv(output_dir + "/" + series_name + ".csv",
                                  sep=r"\s+",
                                  dtype="str")
        actual_df = pd.read_csv(TEST_DATA_DIR + "/" + series_name + "_output" +
                                ".csv",
                                sep=r"\s+",
                                dtype="str")
        #Comparing both data frame which is generated from process method
        pd.testing.assert_frame_equal(actual_df, expected_df)


if __name__ == '__main__':
    unittest.main()
