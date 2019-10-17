# Copyright (C) 2019 by Daniel Shapero <shapero@uw.edu>
#
# This file is part of icepack.
#
# icepack is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# The full text of the license can be found in the file LICENSE in the
# icepack source directory or at <http://www.gnu.org/licenses/>.

r"""Routines for fetching the glaciological data sets used in the demos"""

import os
from getpass import getpass
import requests
import pooch

def _earthdata_downloader(url, output_file, dataset):
    username = os.environ.get('EARTHDATA_USERNAME')
    if username is None:
        username = input('EarthData username: ')

    password = os.environ.get('EARTHDATA_PASSWORD')
    if password is None:
        password = getpass('EarthData password: ')

    login = requests.get(url)
    downloader = pooch.HTTPDownloader(auth=(username, password))
    downloader(login.url, output_file, dataset)


measures_antarctica = pooch.create(
    path=pooch.os_cache('icepack'),
    base_url='https://n5eil01u.ecs.nsidc.org/MEASURES/NSIDC-0484.002/1996.01.01/',
    registry={
        'antarctica_ice_velocity_450m_v2.nc':
        '268be94e3827b9b8137b4b81e3642310ca98a1b9eac48e47f91d53c1b51e4299'
    }
)

def fetch_measures_antarctica():
    return measures_antarctica.fetch('antarctica_ice_velocity_450m_v2.nc',
                                     downloader=_earthdata_downloader)


bedmap2 = pooch.create(
    path=pooch.os_cache('icepack'),
    base_url='https://secure.antarctica.ac.uk/data/bedmap2/',
    registry={
        'bedmap2_tiff.zip':
        'f4bb27ce05197e9d29e4249d64a947b93aab264c3b4e6cbf49d6b339fb6c67fe'
    }
)

def fetch_bedmap2():
    filenames = bedmap2.fetch('bedmap2_tiff.zip', processor=pooch.Unzip())
    return [f for f in filenames if os.path.splitext(f)[1] == '.tif']


outlines_url = 'https://raw.githubusercontent.com/icepack/glacier-meshes/'
outlines_commit = '9306972327a127c4c4bdd3b5f61d2102307c2baa'
larsen_outline = pooch.create(
    path=pooch.os_cache('icepack'),
    base_url=outlines_url + outlines_commit + '/glaciers/',
    registry={
        'larsen.geojson':
        '74a632fcb7832df1c2f2d8c04302cfcdb3c1e86e027b8de5ba10e98d14d94856'
    }
)

def fetch_larsen_outline():
    return larsen_outline.fetch('larsen.geojson')


moa = pooch.create(
    path=pooch.os_cache('icepack'),
    base_url='https://daacdata.apps.nsidc.org/pub/DATASETS/nsidc0593_moa2009/geotiff/',
    registry={
        'moa750_2009_hp1_v01.1.tif.gz':
        '90d1718ea0971795ec102482c47f308ba08ba2b88383facb9fe210877e80282c'
    }
)

def fetch_mosaic_of_antarctica():
    return moa.fetch('moa750_2009_hp1_v01.1.tif.gz',
                     downloader=_earthdata_downloader,
                     processor=pooch.Decompress())
