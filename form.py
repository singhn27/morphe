#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Morphe - Modular Forms Library
Navtej Singh <singhnav@umich.edu>
'''

# Imports #

from __future__ import print_function

import requests
from   time     import sleep

# Parameters #

ps = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 
    47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 
    107, 109, 113, 127, 131, 137, 139, 149]

# Functions #

# Utilities

def get_form_params(space=False,verbose=False,debug=True,**parameters):
    req = 'https://www.lmfdb.org/api/mf_newforms?_format=json&' + '&'.join('{}={}'.format(k,
        v) for k,v in parameters.items())
    if verbose: print(req)
    response = requests.get(req)
    if response.ok or debug:
        json_data = response.json()
        if 'data' not in json_data or len(json_data['data']) == 0:
            raise Exception('No such form found')
        return json_data['data'][0] if not space else json_data['data']
    else:
        raise Exception('Request failed')

def test_example_form():
    form = Form(weight=1,level=(3**3)*(7**2),artin_degree=6)
    assert (form.traces[:10] == [1, 0, 0, 1, 0, 0, 0, 0, 0, 0])

def test_example_formspace():
    formspace = Formspace(weight=1,level=(3**3)*(7**2))
    assert (formspace.form113746_traces[:10] == formspace.findone(artin_field_label='3.1.1323.1')['traces'][:10])

# Classes #

class Form(object):
    def __init__(self,verbose=False,**params):
        if verbose: print('Instantiated Form of {}'.format(', '.join(['{} {}'.format(k.capitalize(), 
            v) for k, v in sorted(params.items())])))
        params = get_form_params(**params)
        for k,v in params.items():
            setattr(self,k,v)

    def trace(self,n):
        try:
            return self.traces[n-1]
        except Exception as e:
            raise NotImplementedError

class Formspace(object):
    def __init__(self,verbose=False,**params):
        self.forms = get_form_params(space=True,**params)
        form_methods = []
        for form in self.forms:
            for k,v in form.items():
                setattr(self,'form{}_{}'.format(form['id'], k), v)
                form_methods.append('form{}_{}'.format(form['id'], k))
        self.form_methods = form_methods
        self.number_of_forms = len([attr for attr in dir(self) if 'form' in attr])
        if verbose: print('Found {} Forms of {}'.format(self.number_of_forms, 
            ', '.join(['{} {}'.format(k.capitalize(), 
            v) for k, v in sorted(params.items())])))

    def find(self, **kwargs):
        candidates = [form for form in self.forms if all([form[k] == v for k, v in kwargs.items()])]
        if len(candidates) == 0:
            raise Exception('None found')
        return candidates

    def findone(self, **kwargs):
        candidates = [form for form in self.forms if all([form.get(k) == v for k, v in kwargs.items()])]
        if len(candidates) == 0:
            raise Exception('None found')
        return candidates[0]

if __name__ == '__main__':
    test_example_form()
    test_example_formspace()
