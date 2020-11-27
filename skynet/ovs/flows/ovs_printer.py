import pandas
from typing import Dict, List, Any


class OVSFlowPrinter():
    """
    (Experimental) OVSFlowPrinter is a class that is able to print OFFLowData in the same sytanx used by ovs-ofctl
    """
    def __init__(self):
        self.action_printers = {'resubmit': self.resubmit_action_printer}

        self.filter_printers = {
            'conn_tracking_state_masked': self.ct_state_filter_printer,
            'conn_tracking_label_masked': self.ct_label_filter_printer
        }

        self.state_str = {
            "Established": "est",
            "Tracked": "trk",
            "New": "new",
            "Related": "rel",
            "ReplyDir": "rpl",
            "Invalid": "inv",
            "SrcNat": "snat",
            "DstNat": "dnat",
        }

    def ct_state_filter_printer(self, filter_obj: Dict[str, Any]):
        ct_str = "ct_state="
        for state in filter_obj["Mask"]:
            ct_str += "{sign}{state}".format(
                sign=("+" if filter_obj["Value"].get(state) == True else "-"),
                state=(self.state_str.get(state) or "UNKNOWN!:%s" % state))
        return ct_str

    @classmethod
    def ct_label_filter_printer(self, filter_obj: Dict[str, Any]):
        return "ct_flag=0x{vh}{vl}/0x{mh}{ml}".format(
            vh=filter_obj['Value']['Hi'],
            vl=filter_obj['Value']['Lo'],
            mh=filter_obj['Mask']['Hi'],
            ml=filter_obj['Mask']['Lo'])

    @classmethod
    def resubmit_action_printer(self, action_obj: Dict[str, Any]):
        return "resubmit(,%s)" % action_obj['Arguments']['Table']

    @classmethod
    def dict2str(self, dictionary: Dict[str, Any]):
        if not dictionary:
            return ""
        return ",".join(
            ["=".join([k, str(dictionary[k])]) for k in dictionary.keys()])

    @classmethod
    def default_action_printer(self, action_obj):
        return ":".join(
            [action_obj["Type"],
             self.dict2str(action_obj.get('Arguments'))])

    def printFilter(self, filter_data: List[Dict[str, Any]]):
        import pdb
        #pdb.set_trace()
        filter_str = ""
        filter_str = ','.join([
            self.filter_printer(filter_obj["Type"])(filter_obj)
            for filter_obj in filter_data
        ])
        return filter_str

    def printActions(self, action_data: List[Dict[str, Any]]):
        action_str = ','.join([
            self.action_printer(action_obj["Type"])(action_obj)
            for action_obj in action_data
        ])
        return action_str

    def default_filter_printer(self, filter_obj: Dict[str, Any]):
        return "=".join([filter_obj["Type"], str(filter_obj["Value"])])

    def filter_printer(self, filter_type: str):
        return self.filter_printers.get(
            filter_type) or self.default_filter_printer

    def action_printer(self, action_type: str):
        return self.action_printers.get(
            action_type) or self.default_action_printer

    def fformat(self, flow: pandas.Series) -> str:
        fstr = ""
        fstr += "cookie={cookie}, duration=TBD, table={table:d}, n_packets={packets}, n_bytes={bytes}, priority={prio},".format(
            cookie=flow.get('Cookie'),
            table=flow.get('Table'),
            packets=flow.get('Metric').get('RxPackets') or 0,
            bytes=flow.get('Metric').get('RxBytes') or 0,
            prio=flow.get('Priority'))

        fstr += self.printFilter(flow['Filters'])
        fstr += " actions={act}".format(act=self.printActions(flow['Actions']))

        return fstr

    def fprint(self, flow: pandas.Series) -> None:
        print(self.fformat(flow))
