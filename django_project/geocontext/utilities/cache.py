from datetime import datetime, timedelta
import pytz

from django.contrib.gis.db.models.functions import Distance

from geocontext.models.service import Service
from geocontext.models.cache import Cache
from geocontext.utilities.geometry import transform, flatten
from geocontext.utilities.service import ServiceUtil


# We use pseudo-mercator projection for cache for efficient distance queries
cache_srid = 3857


def retrieve_cache(service_util: ServiceUtil) -> Cache:
    """Retrieve closest valid cache from point. Filters for cache expiry and service key.

    :param service_util: ServiceUtil instance
    :type service_util: ServiceUtil
    :returns: cache on None
    :rtype: cache or None
    """
    point = transform(service_util.point, cache_srid)
    return Cache.objects.filter(
                        geometry__dwithin=(point, service_util.search_dist)
                    ).filter(
                        service=Service.objects.get(key=service_util.key),
                        expired_time__gte=datetime.utcnow().replace(tzinfo=pytz.UTC),
                    ).annotate(
                        distance=Distance('geometry', point)
                    ).order_by(
                        'distance'
                    ).first()


def create_caches(service_util: ServiceUtil) -> Cache:
    """Add cache entries for all values+geometries and return closest cache to query.

    :param service_util: ServiceUtil instance
    :type service_util: ServiceUtil
    :return: Cache instance
    :rtype: Cache
    """
    for result in service_util.results:
        expired_time = datetime.utcnow() + timedelta(seconds=service_util.cache_duration)
        cache = Cache(
            service=Service.objects.get(key=service_util.key),
            name=service_util.key,
            value=result['value'],
            expired_time=expired_time.replace(tzinfo=pytz.UTC),
            source_uri=service_util.source_uri
        )
        if result['geometry'] is not None:
            geometry = transform(result['geometry'], cache_srid)
            geometry = flatten(geometry)
            cache.geometry = geometry

        cache.save()

    if len(service_util.results) > 1:
        return retrieve_cache(service_util)
    else:
        return cache
