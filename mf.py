#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Morphe - Modular Forms Library
Navtej Singh <singhnav@umich.edu>
'''

# Imports #

from __future__ import print_function

import requests

# Functions #

# Utilities

def get_form_params(verbose=False,debug=True,**parameters):
    req = 'https://www.lmfdb.org/api/mf_newforms?_format=json&' + '&'.join('{}={}'.format(k,
        v) for k,v in parameters.items())
    if verbose: print(req)
    response = requests.get(req)
    if response.ok or debug:
        json_data = response.json()
        if 'data' not in json_data or len(json_data['data']) == 0:
            raise Exception('No such form found')
        return json_data['data'][0]
    else:
        raise Exception('Request failed')

# Classes #

class Form(object):
    def __init__(self,**params):
        print('Instantiated Form of {}'.format(', '.join(['{} {}'.format(k.capitalize(), 
            v) for k, v in sorted(params.items())])))
        params = get_form_params(**params)
        for k,v in params.items():
            setattr(self,k,v)

    def trace(self,n):
        try:
            return self.traces[n-1]
        except Exception as e:
            raise NotImplementedError

# Execution #

if __name__ == '__main__':
    ps = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 
        43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 
        103, 107, 109, 113, 127, 131, 137, 139, 149]
    form = Form(weight=1,level=(3**3)*(7**2),artin_degree=6)
    print('p,a_p')
    for p in ps:
        print('{},{}'.format(p, form.trace(p)))
