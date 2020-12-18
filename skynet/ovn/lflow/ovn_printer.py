import pandas
from skynet.ovn.lflow.data import LFlowData


class OVNFLowPrinter():
    """
    Experimental OVN Flow Printer. Try to mimic how ovn-sbctl prints logical flows
    """
    MAXINT = 65535

    def __init__(self):
        pass

    def fformat(self, flow: pandas.Series) -> str:
        """
        Formats one flow to be printed.
        Returns the formatted string
        """
        fstr = " table={table:<2d} ({stage:<19s}), priority={prio:<5d}, match=({match}), action=({act})\n".format(
            table=int(flow.fillna(0).get('Table')),
            stage=flow.get('Stage'),
            prio=int(flow.fillna(self.MAXINT).get('Priority')),
            match=flow.get('Match'),
            act=flow.get('Actions'))
        return fstr

    def fformat_all(self, flows: LFlowData) -> str:
        """
        Format all the flows.
        Returns formatted string
        """
        df = flows.data()
        fstr = ""
        for datapath in set(df.get('Datapath').values):
            for pipeline in set(df.get('Pipeline').values):
                fstr += "Datapath: ({data}), Pipleine: {pipe}\n".format(
                    data=datapath, pipe=pipeline)

                data = df[(df['Datapath'] == datapath)
                          & (df['Pipeline'] == pipeline)]
                for _, series in data.iterrows():
                    fstr += self.fformat(series)

        return fstr

    def fprint(self, flow: pandas.Series) -> None:
        """
        Print one flow in OVN format
        """
        print(self.fformat(flow))

    def fprint_all(self, flows: LFlowData) -> None:
        """
        Print all the flows in OVN format
        """
        print(self.fformat_all(flows))
