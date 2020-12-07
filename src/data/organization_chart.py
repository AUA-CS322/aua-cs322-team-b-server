import json
from os import path

from src.data.user_repository import UserRepository

class OrganizationChart:
    __slots__ = '_chart', '_user_repository'

    def __init__(self):
        base_dir = path.abspath(path.dirname(__file__))
        with open(path.join(base_dir, 'source', 'org-tree.json')) as f:
            self._chart = json.loads(f.read())
            self._user_repository = UserRepository()

    def _normalize(self):
        chart_nodes_list = []
        # The parent of the first element of _chart is assumed to be the root
        root_node_id = self._chart[0]['parent']
        self._chart.insert(0, {'id': root_node_id, 'parent': None})
        for user_info in self._chart:
            user, parent_user = self.get_user_with_parent(user_info['id'], user_info)
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

    def find_user_info_by_id(self, id):
        for user_info in self._chart:
            if user_info['id'] == id:
                return user_info            

    def get_user_with_manager(self, id):
        user_info = self.find_user_info_by_id(id)                    
        return self.get_user_with_parent(id, user_info)        

    def get_user_with_parent(self, user_id, user_info):
        user = self._user_repository.get_by_id(user_id)
        parent_user = None    

        if user_info is not None:  
            parent_user = self._user_repository.get_by_id(user_info['parent'])

        return user, parent_user        