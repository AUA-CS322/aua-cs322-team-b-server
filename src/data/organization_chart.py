import json
from os import path

from src.data.user_repository import UserRepository

class OrganizationChart:
    __slots__ = '_chart'

    def __init__(self):
        base_dir = path.abspath(path.dirname(__file__))
        with open(path.join(base_dir, 'source', 'org-tree.json')) as f:
            self._chart = list(json.loads(f.read()))

    def _normalize(self):
        user_repository = UserRepository()
        chart_nodes_list = []
        # The parent of the first element of _chart is assumed to be the root
        root_node_id = self._chart[0]['parent']
        self._chart.insert(0, {'id': root_node_id, 'parent': None})
        for user_info in self._chart:
            user = user_repository.get_by_id(user_info['id'])
            parent_user = user_repository.get_by_id(user_info['parent'])
            if user is None:
                raise Exception('The id provided does not exist in data.')
            chart_node = {}
            chart_node['nodeId'] = user['id']
            if parent_user is None:
                chart_node['parentNodeId'] = None
            else:
                chart_node['parentNodeId'] = parent_user['id']
            chart_node['fullName'] = '{}, {}'.format(user['firstName'], user['lastName'])
            chart_node['position'] = user['position']
            chart_node['photoUrl'] = user['photoUrl']
            chart_nodes_list.append(chart_node)
        return chart_nodes_list

    def get_chart(self):
        return self._normalize()