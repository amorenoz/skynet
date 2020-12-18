from typing import Any, Dict, List

from skynet.context import SkyNetCtxt
from skynet.common.data import SkyDiveDataProvider, SkyDiveData, Metadata


class OvSBridgeData(SkyDiveData):
    """
    OvsBridgeData represents OvS bridge
    """
    METADATA = [
        Metadata('Type'),
        Metadata('Name'),
        Metadata('ExtID.bridge-id', None, 'BridgeID'),
        Metadata('ExtID.bridge-uplink', None, 'BridgeUplink'),
        Metadata('ExtID', None, 'ExtID'),
    ]

    def __init__(self, data: List[Dict[str, Any]]):
        """
        OvSBridgeData Constructor
        """
        super(OvSBridgeData, self).__init__(data=data,
                                            meta=self.METADATA,
                                            index="ID")


class OvSSystemData(SkyDiveData):
    """
    OvSSystemData represents OvS System Configuration
    """
    METADATA = [
        Metadata('Type'),
        Metadata('ExtID.hostname', None, 'Host'),
        Metadata('ExtID.ovn-encap-type', None, 'EncapType'),
        Metadata('ExtID.ovn-encap-ip', None, 'EncapIP'),
        Metadata('FDB'),
    ]

    def __init__(self, data: List[Dict[str, Any]]):
        """
        OvSSystemData constructor
        """
        super(OvSSystemData, self).__init__(data=data,
                                            meta=self.METADATA,
                                            index="ID")


class OvSPortData(SkyDiveData):
    """
    OvsPortData represents OvS ports data from Skydive
    """
    METADATA = [
        Metadata('Type'),
        Metadata('Name'),
        Metadata('ExtID'),
        Metadata('ExtID.ovn-chassis-id', None, 'ChassisID'),
    ]

    def __init__(self, data: List[Dict[str, Any]]):
        """
        OvSPortData constructor from skydive data
        """
        super(OvSPortData, self).__init__(data=data,
                                          meta=self.METADATA,
                                          index="ID")


class OvSIfaceData(SkyDiveData):
    """
    OvSIfaceData represets OvS Interfaces
    """
    COMMON_METADATA = [
        Metadata('Type'),
        Metadata('Name'),
        Metadata('ExtID'),
        Metadata('MAC'),
        Metadata('Ovs'),
        Metadata('OfPort'),
    ]
    PATCH_METADATA = [
        Metadata('Ovs.Options.peer', None, "Peer"),
        Metadata('ExtID.ovn-local-port', None, 'LocalPort'),
    ]
    GENEVE_METADATA = [
        Metadata('RemoteIP'),
        Metadata('IfIndex'),
        Metadata('MTU'),
        Metadata('EncapType'),
        Metadata('TunEgressIfaceCarrier'),
        Metadata('TunEgressIface'),
        Metadata('Ovs.Options', None, 'Options'),
    ]
    INTERNAL_METADATA = [
        Metadata('Neighbours'),
        Metadata('EncapType'),
        Metadata('IPV4'),
        Metadata('MTU'),
        Metadata('EncapType'),
        Metadata('RoutingTables'),
        Metadata('Metric'),
        Metadata('FDB'),
        Metadata('LinkFlags'),
        Metadata('Features'),
    ]
    VETH_METADATA = [
        Metadata('PeerIFIndex'),
        Metadata('Features'),
        Metadata('State'),
        Metadata('LinkNetNsID'),
        Metadata('Metric'),
        Metadata('LinkNetNsName'),
        Metadata('LinkFlags'),
        Metadata('Speed'),
        Metadata('IfIndex'),
        Metadata('FDB'),
        Metadata('MasterIndex'),
        Metadata('ParentIndex'),
        Metadata('ExtID.ip_address', None, 'IPAddress'),
        Metadata('ExtID.attached_mac', None, 'AttachedMAC'),
        Metadata('ExtID.sandbox', None, 'Sandbox'),
        Metadata('ExtID.iface-id', None, 'IfaceID')
    ]

    def __init__(self, data: List[Dict[str, Any]]):
        """
        OvSIfaceData constructor from skydive data
        """
        # Assume all interfaces are the same type
        meta = self.COMMON_METADATA
        if len(data) > 0:
            iface_type = data[0]['Metadata']['Type']
            if iface_type == "patch":
                meta.extend(self.PATCH_METADATA)
            elif iface_type == "geneve":
                meta.extend(self.GENEVE_METADATA)
            elif iface_type == "internal":
                meta.extend(self.INTERNAL_METADATA)
            elif iface_type == "veth":
                meta.extend(self.VETH_METADATA)
            else:
                raise Exception('Unknown Interface type %s' % iface_type)

        super(OvSIfaceData, self).__init__(data=data, meta=meta, index="ID")


def find_childs(parent: str, data: List[Dict[str, Any]],
                edges: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Given a list of Nodes and Edges, find the children of a specific Node
    """
    out_edges = list(filter(lambda e: e['Parent'] == parent, edges))
    return list(
        filter(lambda d: d['ID'] in [edge['Child'] for edge in out_edges],
               data))


class OvSPort():
    """
    OvSPort encapsulates the detail information of a OvS Port
    It has two properties:
        port: The port information (OvSPortData)
        ifaces: The interfaces (OvSIfaceData)
    """
    def __init__(self, data: List[Dict[str, Any]]):
        """
        It is expected to receive both the port data and the interface data
        """
        iface_types = ['geneve', 'patch', 'internal', 'veth']
        self._port = OvSPortData(
            list(filter(lambda d: d['Metadata']['Type'] == 'ovsport', data)))

        ifaces = list(
            filter(lambda d: d['Metadata']['Type'] in iface_types, data))
        if len(ifaces) == 0:
            raise Exception('Port without interfaces: %s' % str(data))

        self._ifaces = OvSIfaceData(ifaces)

    @property
    def port(self) -> OvSPortData:
        return self._port

    @property
    def ifaces(self) -> OvSIfaceData:
        return self._ifaces


class OvSBridge():
    """
    OvSBridge encapsulates the detail information of an OvS Bridge
    It has two properties:
        bridge: The bridge information (OvSBridgeData)
        ports: The port information (List of OvSPort)
    """
    def __init__(self, graph: Dict[str, List[Dict[str, Any]]]):
        """
        It is expected to receive an ovs bridge and all its descendents as a subgraph
        The output of:

        G.V('61f44ac8-c5e3-457b-64dc-c7dbf0a7c1a5').Descendants().HasEither('Type', 'ovsport','Type', 'ovsbridge').OutE().Has('RelationType', 'layer2').Subgraph()

        should be enough to build this.
        """

        self._bridge = OvSBridgeData([
            next(
                filter(lambda d: d['Metadata']['Type'] == 'ovsbridge',
                       graph['Nodes']))
        ])

        self._ports: List[OvSPort] = []
        for port in filter(lambda d: d['Metadata']['Type'] == 'ovsport',
                           graph['Nodes']):
            port_data = [port]
            childs = find_childs(port['ID'], graph['Nodes'], graph['Edges'])
            port_data.extend(childs)
            self._ports.append(OvSPort(port_data))

    @property
    def bridge(self) -> OvSBridgeData:
        return self._bridge

    @property
    def ports(self) -> List[OvSPort]:
        return self._ports


class OvSDataProvider(SkyDiveDataProvider):
    """
    Data Provider for OvS Bridges
    """
    def __init__(self, ctxt: SkyNetCtxt):
        super(OvSDataProvider, self).__init__(ctxt=ctxt)

    def list_ports(self, bridge) -> OvSPortData:
        """
        List all the bridges by name or ID
        """
        query = "V()"

        if bridge:
            query += ".Has('Type', 'ovsbridge').HasEither('ID', '{bridge}', 'Name', '{bridge}').Out()".format(
                bridge=bridge)

        query += ".Has('Type', 'ovsport')"

        data = self._run_query(query)
        return OvSPortData(data)

    def get_port(self, port: str) -> OvSPort:
        """
        Get port from detail from ID
        """
        query = "V('{}')".format(port)

        query += ".Descendants()"

        data = self._run_query(query)
        return OvSPort(data)

    def get_bridge(self, bridge: str) -> OvSBridge:
        """
        Get port detail from UID
        """
        query = "V('{}')".format(bridge)

        query += ".Descendants().HasEither('Type', 'ovsport','Type', 'ovsbridge').OutE().Has('RelationType', 'layer2').Subgraph()"

        data = self._run_query(query)
        if len(data) == 0:
            raise Exception('Bridge not found %s' % bridge)

        return OvSBridge(data[0])

    def list_bridges(self, host) -> OvSBridgeData:
        """
        List all bridges from given host
        """
        query = "V()"

        if host:
            query += ".Has('Type', 'host').HasEither('ID', '{host}', 'Name', '{host}').Out()".format(
                host=host)

        query += ".Has('Type', 'ovsbridge')"

        data = self._run_query(query)
        return OvSBridgeData(data)

    def get_bridges_by_host(self, host: str) -> List[OvSBridge]:
        """
        Get Bridge detail by host
        """
        bridges = []

        bridge_data = self.list_bridges(host)

        if bridge_data.is_empty():
            raise Exception("No bridges found in host: %s" % host)

        for uuid, _ in bridge_data.data().iterrows():
            bridges.append(self.get_bridge(uuid))

        return bridges

    def get_num_ports(self, bridge) -> int:
        """
        Get Nubmer of ports of a bridge
        """
        query = "V().Has('Type', 'ovsbridge', 'ID', '{id}')".format(id=bridge)
        query += ".Out().Has('Type','ovsport').Count()"
        return self._run_query(query)

    def get_num_flows(self, bridge) -> int:
        """
        Get Nubmer of flows of a bridge
        """
        query = "V().Has('Type', 'ovsbridge', 'ID', '{id}')".format(id=bridge)
        query += ".Out().Has('Type','ofrule').Count()"
        return self._run_query(query)
