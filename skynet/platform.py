from enum import Enum
import logging
from typing import Dict, Any, List

from skynet.context import SkyNetCtxt
from skynet.common.data import SkyDiveDataProvider, Metadata, Field, \
    SkyDiveData


class Platform(Enum):
    """
    Enum to represent supported platforms
    """
    K8S = 'K8S'
    Unknown = 'Unknown'


class K8sConfig(SkyDiveData):
    """
    K8s Configuration
    """
    METADATA: List[Field] = [
        Metadata('K8s.Extra.Data.mtu', int, 'MTU'),
        Metadata('K8s.Extra.Data.net_cidr', None, 'NetCIDR'),
        Metadata('K8s.Extra.Data.svc_cidr', None, 'SvcCIDR'),
    ]

    def __init__(self, data: List[Dict[str, Any]]):
        """
        K8sConfig constructor
        """
        super(K8sConfig, self).__init__(data=data,
                                        meta=self.METADATA,
                                        index="ID")


class PlatformProvider(SkyDiveDataProvider):
    """
    PlatformProvider is a provider for platform configuration
    """
    def __init__(self, ctxt: SkyNetCtxt):
        """
        PlatformProvider constructor
        """
        super(PlatformProvider, self).__init__(ctxt=ctxt)

    def get_k8s_conf(self) -> K8sConfig:
        """
        Returns tne ovn-conf object
        """
        ovn = self._run_query("V().Has('Manager', 'k8s','Name', 'ovn-config')")

        return K8sConfig(ovn)

    def platform_type(self) -> Platform:
        """
        Determine the platform type
        """
        k8s_count = self._run_query("V().Has('Manager', 'k8s').Count()")

        if k8s_count > 0:
            logging.getLogger("Platform").debug(
                "k8s count is %i. Plafrom type is k8s" % k8s_count)
            return Platform.K8S

        return Platform.Unknown
