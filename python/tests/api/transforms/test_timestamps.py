# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from iceberg.api.expressions import Literal
from iceberg.api.transforms import Transforms
from iceberg.api.types import TimestampType
import pytest


@pytest.mark.parametrize("lit,type_var", [
    (Literal.of("2017-12-01T10:12:55.038194-08:00"), TimestampType.with_timezone()),
    (Literal.of("2017-12-01T18:12:55.038194"), TimestampType.without_timezone())])
@pytest.mark.parametrize("transform_gran,expected", [
    (Transforms.year, "2017"),
    (Transforms.month, "2017-12"),
    (Transforms.day, "2017-12-01"),
    (Transforms.hour, "2017-12-01-18")])
def test_ts_to_human_string(lit, type_var, transform_gran, expected):
    date_var = lit.to(type_var)
    assert (transform_gran(type_var)
            .to_human_string(transform_gran(type_var)
                             .apply(date_var.value))) == expected


@pytest.mark.parametrize("transform_gran", [
    Transforms.year,
    Transforms.month,
    Transforms.day,
    Transforms.hour])
def test_null_human_string(transform_gran):
    type_var = TimestampType.with_timezone()
    assert "null" == transform_gran(type_var).to_human_string(None)
