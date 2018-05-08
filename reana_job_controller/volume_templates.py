# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2017 CERN.
#
# REANA is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# REANA is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# REANA; if not, write to the Free Software Foundation, Inc., 59 Temple Place,
# Suite 330, Boston, MA 02111-1307, USA.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization or
# submit itself to any jurisdiction.

"""Volume template generation."""

import json
from string import Template

CEPHFS_SECRET_NAME = 'ceph-secret'

REANA_STORAGE_PATHS = {
    'alice': '/reana/alice',
    'atlas': '/reana/atlas',
    'cms': '/reana/cms',
    'lhcb': '/reana/lhcb',
    'default': '/reana/default'
}

CVMFS_REPOSITORIES = {
    'alice': 'alice.cern.ch',
    'alice-ocdb': 'alice-ocdb.cern.ch',
    'atlas': 'atlas.cern.ch',
    'atlas-condb': 'atlas-condb.cern.ch',
    'cms': 'cms.cern.ch',
    'lhcb': 'lhcb.cern.ch',
    'na61': 'na61.cern.ch',
    'boss': 'boss.cern.ch',
    'grid': 'grid.cern.ch',
    'sft': 'sft.cern.ch',
    'geant4': 'geant4.cern.ch'
}

REANA_STORAGE_MOUNT_PATH = '/data'

K8S_CEPHFS_TEMPLATE = Template("""{
    "name": "$experiment-shared-volume",
    "cephfs": {
        "monitors": [
            "128.142.36.227:6790",
            "128.142.39.77:6790",
            "128.142.39.144:6790"
        ],
        "path": "$path",
        "user": "k8s",
        "secretRef": {
            "name": "$secret_name",
            "readOnly": false
        }
    }
}""")

K8S_CVMFS_TEMPLATE = Template("""{
    "name": "cvmfs-$experiment",
    "flexVolume": {
        "driver": "cern/cvmfs",
        "options": {
            "repository": "$repository"
        }
    }
}""")

K8S_HOSTPATH_TEMPLATE = Template("""{
    "name": "$experiment-shared-volume",
    "hostPath": {
        "path": "$path"
    }
}""")


def get_cvmfs_mount_point(repository_name):
    """Generate mount point for a given CVMFS repository.

    :param repository_name: CVMFS repository name.
    :returns: The repository's mount point.
    """
    return '/cvmfs/{repository}'.format(
        repository=CVMFS_REPOSITORIES[repository_name]
    )


def get_k8s_cephfs_volume(experiment):
    """Render k8s CephFS volume template.

    :param experiment: Experiment name.
    :returns: k8s CephFS volume spec as a dictionary.
    """
    return json.loads(
        K8S_CEPHFS_TEMPLATE.substitute(experiment=experiment,
                                       path=REANA_STORAGE_PATHS[experiment],
                                       secret_name=CEPHFS_SECRET_NAME)
    )


def get_k8s_cvmfs_volume(experiment, repository):
    """Render k8s CVMFS volume template.

    :param experiment: Experiment name.
    :returns: k8s CVMFS volume spec as a dictionary.
    """
    if repository in CVMFS_REPOSITORIES:
        return json.loads(K8S_CVMFS_TEMPLATE.substitute(experiment=experiment,
                                                        repository=repository))
    else:
        raise ValueError('The provided repository doesn\'t exist')


def get_k8s_hostpath_volume(experiment):
    """Render k8s HostPath volume template.

    :param experiment: Experiment name.
    :returns: k8s HostPath spec as a dictionary.
    """
    return json.loads(
        K8S_HOSTPATH_TEMPLATE.substitute(experiment=experiment,
                                         path=REANA_STORAGE_PATHS[experiment])
    )