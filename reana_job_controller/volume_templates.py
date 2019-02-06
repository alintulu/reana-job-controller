# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2017, 2018 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Volume template generation."""

import json
from string import Template

from reana_job_controller.config import SHARED_FS_MAPPING

CEPHFS_SECRET_NAME = 'ceph-secret'

K8S_CEPHFS_TEMPLATE = """{
    "name": "reana-shared-volume",
    "persistentVolumeClaim": {
        "claimName": "manila-cephfs-pvc"
    },
    "readOnly": "false"
}"""

K8S_CVMFS_TEMPLATE = Template("""{
    "name": "$experiment-cvmfs-volume",
    "persistentVolumeClaim": {
        "claimName": "csi-cvmfs-$experiment-pvc"
    },
    "readOnly": "true"
}""")

K8S_HOSTPATH_TEMPLATE = Template("""{
    "name": "$experiment-shared-volume",
    "hostPath": {
        "path": "$path"
    }
}""")


def get_k8s_cephfs_volume():
    """Return k8s CephFS volume template.

    :returns: k8s CephFS volume spec as a dictionary.
    """
    return json.loads(
        K8S_CEPHFS_TEMPLATE
    )


def get_k8s_cvmfs_volume(experiment):
    """Render k8s CVMFS volume template.

    :param experiment: Experiment name.
    :returns: k8s CVMFS volume spec as a dictionary.
    """
    return json.loads(K8S_CVMFS_TEMPLATE.substitute(
        experiment=experiment))


def get_k8s_hostpath_volume(experiment):
    """Render k8s HostPath volume template.

    :param experiment: Experiment name.
    :returns: k8s HostPath spec as a dictionary.
    """
    return json.loads(
        K8S_HOSTPATH_TEMPLATE.substitute(
            experiment=experiment,
            path=SHARED_FS_MAPPING['MOUNT_SOURCE_PATH'])
    )
