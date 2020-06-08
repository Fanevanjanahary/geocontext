import os
import unittest
from datetime import datetime
from unittest.mock import patch

from django.test import TestCase

from base.management.commands.utilities import import_data
from geocontext.models.cache import Cache
from geocontext.models.service import Service
from geocontext.models.utilities import (
    create_cache,
    retrieve_cache,
    ServiceUtils,
    retrieve_external_service,
    UtilArg
)
from geocontext.tests.models.model_factories import ServiceF
from geocontext.utilities import ServiceDefinitions


test_data_directory = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '../data')


@patch.object(ServiceUtils, 'get_service')
class TestCRSUtils(TestCase):

    def test_retrieve_value1(self, mock_get_service):
        """Test retrieving value from a point with same CRS."""
        x = 18.42
        y = -29.71

        service = ServiceF.create()
        service.url = 'https://maps.kartoza.com/geoserver/wfs'
        service.query_type = ServiceDefinitions.WFS
        service.layer_typename = 'kartoza:water_management_areas'
        service.service_version = '1.0.0'
        service.result_regex = 'gml:name'
        service.save()
        mock_get_service.return_value = service

        service_util = ServiceUtils(service.key, x, y, service.srid)
        util_arg = UtilArg(group_key=service.key, service_util=service_util)
        new_util_arg = retrieve_external_service(util_arg)
        self.assertIsNotNone(new_util_arg)
        result = create_cache(new_util_arg.service_util)

        expected_value = '14 - Lower Orange'
        self.assertEqual(result.value, expected_value)
        self.assertIsNotNone(result.geometry)
        self.assertEqual(result.geometry.geom_type, 'Polygon')
        self.assertTrue(result.geometry.valid)

        caches = Cache.objects.filter(service=service)
        self.assertIsNotNone(caches)
        cache = caches[0]
        self.assertEqual(cache.value, expected_value)
        self.assertEqual(cache.geometry.geom_type, 'Polygon')
        self.assertEqual(cache.geometry.srid, 4326)

    @unittest.skip("Please fix this")
    def test_retrieve_value2(self, mock_get_service):
        """Test retrieving value from a point with different CRS."""
        x = 18.42
        y = -29.71

        service = ServiceF.create()
        service.url = 'http://maps.kartoza.com/geoserver/wfs'
        service.query_type = ServiceDefinitions.WFS
        service.layer_typename = 'sa_provinces'
        service.service_version = '1.0.0'
        service.srid = 3857
        service.result_regex = 'kartoza:sa_provinces'
        service.save()
        mock_get_service.return_value = service

        service_util = ServiceUtils(service.key, x, y, srid=4326)
        util_arg = UtilArg(group_key=service.key, service_util=service_util)
        new_util_arg = retrieve_external_service(util_arg)
        self.assertIsNotNone(new_util_arg)
        result = new_util_arg.service_util.create_cache()

        expected_value = 'Northern Cape'
        self.assertEqual(result.value, expected_value)
        self.assertIsNotNone(result.value)
        self.assertEqual(result.geometry.geom_type, 'MultiPolygon')
        self.assertTrue(result.geometry.valid)

        caches = Cache.objects.filter(service=service)
        self.assertIsNotNone(caches)
        cache = caches[0]
        self.assertEqual(cache.value, expected_value)
        self.assertEqual(cache.geometry.geom_type, 'MultiPolygon')
        # Automatically projected to 4326
        self.assertEqual(cache.geometry.srid, 4326)

    @unittest.skip("Please fix this")
    def test_retrieve_value_geoserver(self, mock_get_service):
        """Test retrieving value from a geoserver service."""
        x = 18.42
        y = -29.71

        service = ServiceF.create()
        service.url = 'http://maps.kartoza.com/geoserver/wfs'
        service.query_type = ServiceDefinitions.WFS
        service.layer_typename = 'sa_provinces'
        service.service_version = '1.0.0'
        service.result_regex = 'kartoza:sa_provinces'
        service.save()
        mock_get_service.return_value = service

        service_util = ServiceUtils(service.key, x, y, service.srid)
        util_arg = UtilArg(group_key=service.key, service_util=service_util)
        new_util_arg = retrieve_external_service(util_arg)
        self.assertIsNotNone(new_util_arg)
        result = new_util_arg.service_util.create_cache()

        expected_value = 'Northern Cape'
        self.assertEqual(result.value, expected_value)
        self.assertIsNotNone(result.value)
        self.assertEqual(result.geometry.geom_type, 'MultiPolygon')
        self.assertTrue(result.geometry.valid)

        caches = Cache.objects.filter(service=service)
        self.assertIsNotNone(caches)
        cache = caches[0]
        self.assertEqual(cache.value, expected_value)
        self.assertEqual(cache.geometry.geom_type, 'MultiPolygon')
        # Automatically projected to 4326
        self.assertEqual(cache.geometry.srid, 4326)

    def test_retrieve_value_wms(self, mock_get_service):
        """Test retrieving value from a point with WMS source."""
        x = 27.8231
        y = -32.1231
        srid = 4326

        service = ServiceF.create()
        service.url = 'https://maps.kartoza.com/geoserver/wms'
        service.query_type = ServiceDefinitions.WMS
        service.layer_typename = 'kartoza:south_africa'
        service.service_version = '1.3.0'
        service.result_regex = 'kartoza:GRAY_INDEX'
        service.save()
        mock_get_service.return_value = service

        service_util = ServiceUtils(service.key, x, y, srid)

        util_arg = UtilArg(group_key=service.key, service_util=service_util)
        new_util_arg = retrieve_external_service(util_arg)
        self.assertIsNotNone(new_util_arg)
        result = new_util_arg.service_util.create_cache()

        expected_value = '1009.0'
        self.assertEqual(result.value, expected_value)
        self.assertIsNotNone(result.value)

        caches = Cache.objects.filter(service=service)
        self.assertIsNotNone(caches)
        cache = caches[0]
        self.assertEqual(cache.value, expected_value)

    def test_retrieve_value_arcrest(self, mock_get_service):
        """Test retrieving value from a point with ArcRest source.
        """
        x = 19.14
        y = -32.32

        service = ServiceF.create()
        service.url = (
            'https://portal.environment.gov.za/server/rest/services/Corp/'
            'ProtectedAreas/MapServer/')
        service.srid = 4326
        service.query_type = ServiceDefinitions.ARCREST
        service.layer_typename = 'all:10'
        service.service_version = 'ArcRest 1.0.0'
        service.result_regex = 'value'
        service.save()
        mock_get_service.return_value = service

        service_util = ServiceUtils(service.key, x, y, service.srid)
        util_arg = UtilArg(group_key=service.key, service_util=service_util)
        new_util_arg = retrieve_external_service(util_arg)
        self.assertIsNotNone(new_util_arg)
        result = new_util_arg.service_util.create_cache()

        expected_value = (
            'Cape Floral Region Protected Areas: Cederberg Wilderness Area')
        self.assertEqual(result.value, expected_value)
        self.assertIsNotNone(result.value)

        caches = Cache.objects.filter(service=service)
        self.assertIsNotNone(caches)
        cache = caches[0]
        self.assertEqual(cache.value, expected_value)

    def test_retrieve_value_placename(self, mock_get_service):
        """Test retrieving value from a point with ArcRest source.
        """
        x = 19.14
        y = -32.32

        service = ServiceF.create()
        service.url = (
            'http://api.geonames.org/findNearbyPlaceNameJSON')
        service.srid = 4326
        service.query_type = ServiceDefinitions.PLACENAME
        service.layer_typename = 'Find Nearby Place Name'
        service.service_version = 'Version 1.0.0'
        service.result_regex = 'toponymName'
        service.api_key = 'christiaanvdm'
        service.save()
        mock_get_service.return_value = service

        service_util = ServiceUtils(service.key, x, y, service.srid)
        util_arg = UtilArg(group_key=service.key, service_util=service_util)
        new_util_arg = retrieve_external_service(util_arg)
        self.assertIsNotNone(new_util_arg)
        result = new_util_arg.service_util.create_cache()

        expected_value = 'Wuppertal'
        self.assertEqual(result.value, expected_value)
        self.assertIsNotNone(result.value)

        caches = Cache.objects.filter(service=service)
        self.assertIsNotNone(caches)
        cache = caches[0]
        self.assertEqual(cache.value, expected_value)

    @unittest.skip("Please fix this")
    def test_retrieve_value_invalid(self, mock_get_service):
        """Test retrieving value from a point with different CRS.

        The CRS is 4326 (query), 3857 (service)
        """
        x = 0
        y = 0

        service = ServiceF.create()
        service.url = 'https://maps.kartoza.com/geoserver/wfs'
        service.query_type = ServiceDefinitions.WFS
        service.layer_typename = 'kartoza:sa_provinces'
        service.service_version = '1.0.0'
        service.result_regex = 'gml:name'
        service.srid = 3857
        service.save()
        mock_get_service.return_value = service

        service_util = ServiceUtils(service.key, x, y, service.srid)
        util_arg = UtilArg(group_key=service.key, service_util=service_util)
        new_util_arg = retrieve_external_service(util_arg)

        self.assertIsNone(new_util_arg)

    def test_parse_request_value(self, mock_get_service):
        """Test parse value for WMS response."""
        service = ServiceF.create()
        service.url = 'https://maps.kartoza.com/geoserver/wms'
        service.srid = 3857
        service.query_type = ServiceDefinitions.WMS
        service.layer_typename = 'kartoza:south_africa'
        service.service_version = '1.1.1'
        service.result_regex = 'kartoza:GRAY_INDEX'
        service.save()
        mock_get_service.return_value = service

        wms_response_file = os.path.join(test_data_directory, 'wms.xml')
        with open(wms_response_file) as f:
            response = f.read()

        service_util = ServiceUtils(service.key, 0, 0, service.srid)
        value = service_util.parse_request_value(response)

        self.assertIsNotNone(value)
        self.assertEqual('746.0', value)


class TestGeoContextView(TestCase):
    """Test for geocontext view."""

    def setUp(self):
        """Setup test data."""
        test_geocontext_file = os.path.join(
            test_data_directory, 'test_geocontext.json')
        import_data(test_geocontext_file)
        pass

    def tearDown(self):
        """Delete all service data."""
        services = Service.objects.all()
        for service in services:
            service.delete()

    def test_cache_retrieval(self):
        """Test for retrieving from service and cache."""
        x = 27.8
        y = -32.1
        service_key = 'quaternary_catchment_area'

        start_direct = datetime.now()
        service_util = ServiceUtils(service_key, x, y)
        retrieve_cache(service_util)

        end_direct = datetime.now()

        start_cache = datetime.now()
        retrieve_cache(service_util)
        end_cache = datetime.now()

        duration_direct = end_direct - start_direct
        duration_cache = end_cache - start_cache
        direct_time = duration_direct.total_seconds()
        cache_time = duration_cache.total_seconds()
        message = f'Direct: {direct_time:.5f}. Cache: {cache_time:.5f}'
        self.assertGreater(duration_direct, duration_cache, message)
