from qcodes import VisaInstrument


def parse_output(s):
    parts = s.split(',')[1:-1]

    if len(parts) == 1:
        return float(parts[0])
    else:
        return list(map(float, parts))


class F70(VisaInstrument):
    """
    Driver for the Sumitomo (SHI) F-70 helium compressor.

    Command structure: $<COMMAND><DATA><CRC-16><cr>
    Response: $<COMMAND>,<DATA>,<DATA>,<CRC-16><cr>
    """
    def __init__(self, name, address, reset=False, **kwargs):
        super().__init__(name, address, **kwargs)

        self.add_parameter('temp_helium_gas',
                           get_cmd='$TE140B8\r',
                           get_parser=parse_output,
                           unit='deg C')

        self.add_parameter('temp_water_outlet',
                           get_cmd='$TE241F8\r',
                           get_parser=parse_output,
                           unit='deg C')

        self.add_parameter('temp_water_inlet',
                           get_cmd='$TE38139\r',
                           get_parser=parse_output,
                           unit='deg C')

        self.add_parameter('return_pressure',
                           get_cmd='$PR171F6\r',
                           get_parser=parse_output,
                           unit='psig')

        self.add_function('on', call_cmd='$ON177CF\r')
        self.add_function('off', call_cmd='$OFF9188\r')
        self.add_function('reset', call_cmd='$RS1')

        self.add_function('cold_head_pause', call_cmd='$CHP')
        self.add_function('cold_head_run', call_cmd='$CHR')
        self.add_function('cold_head_pause_off', call_cmd='$POF')
