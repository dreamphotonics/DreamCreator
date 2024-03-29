from sequences.core.laser_sweep import LaserSweep

class SetVoltageWavelengthSweepIda(LaserSweep):
    """
    Sets the voltage and then performs a laser sweep.

    Args:
        ps (Dreams Lab probe station object): the probe station performing the sweep.
    """
    def __init__(self, ps):

        self.variables = {
            'Start': 1480,
            'Start_info': 'unit nm',
            'Stop': 1580,
            'Stop_info': 'unit nm',
            'Step': 1,
            'Step_info': 'unit nm, can also use wavl_pts, if both filled Step will take priority',
            'Power': 1,
            'Power_info': 'unit dBm',
            'Sweep Speed': 'auto',
            'Sweep Speed_info': 'controls the speed of the sweep, if yaml fails time execution test increase this, options are 20nm, 10nm, auto',
            'Laser Output': 'High Power',
            'Laser Output_info': 'Set to High Power or Low SSE',
            'Numscans': 1,
            'Numscans_info': 'choose how many scans for each device, default 1, max 3',
            'RangeDec': 20,
            'RangeDec_info': 'default 20',
            'Initialrange': '-20',
            'Initialrange_info': 'default -20',
            'Channel A': 'True',
            'Channel A_info': 'Please enter True to use Channel A if not enter False',
            'Channel B': 'False',
            'Channel B_info': 'Please enter True to use Channel B if not enter False',
            'Voltages': '0, 1, 2',
            'Voltages_info': 'Please enter voltages in units (V) in the form x1, x2, x3',
        }
        

        self.resultsinfo = {
            'num_plots': 1,
            'visual': True,
            'saveplot': True,
            'plottitle': 'Set Voltage Wavelength Sweep',
            'save_location': '',
            'foldername': '',
            'xtitle': 'Wavelength (nm)',
            'ytitle': 'Power (dBm)',
            'xscale': 1,
            'yscale': 1,
            'legend': True,
            'csv': True,
            'pdf': True,
            'mat': True,
            'pkl': False
        }
        super().__init__(variables=self.variables, resultsinfo=self.resultsinfo, ps=ps)

    def run(self, routine=False):
        self.set_results(variables=self.variables, resultsinfo = self.resultsinfo, routine=routine)
        """Executes a wavelength sweep for each given voltage."""

        settings = self.ps.get_settings(self.verbose)
        
        for volt in self.variables['voltages']:
            self.ps.elecprobe.smuchannels[0].set_current_mode()
            self.ps.elecprobe.smuchannels[0].set_voltage(volt)
            self.ps.elecprobe.smuchannels[0].set_output(True)
        
            self.external_parameters = volt
            self.external_unit = 'V'
            self.execute()

            self.ps.elecprobe.smuchannels[0].set_output(False)

        self.ps.set_settings(settings)