from rest_framework import views
from rest_framework.response import Response

from geocontext.serializers.utilities import GroupValues
from geocontext.serializers.group import GroupValueSerializer


class GroupAPIView(views.APIView):
    """Retrieving value based on a point (x, y, srid) and a group key."""
    def get(self, request, x, y, group_key, srid=4326):
        group_values = GroupValues(x, y, group_key, srid)
        try:
            group_values.populate_group_values()
        except Exception as e:
             return Response(f"Server exception: {e}")
        group_value_serializer = GroupValueSerializer(group_values)
        return Response(group_value_serializer.data)
