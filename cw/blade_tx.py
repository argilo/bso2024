#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Blade Tx
# GNU Radio version: 3.10.11.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import iqbalance
from gnuradio import soapy
from morse_table import morse_seq
import math
import threading



class blade_tx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Blade Tx", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Blade Tx")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "blade_tx")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1000000
        self.interpolation = interpolation = 80
        self.wpm = wpm = 15
        self.tune = tune = 100
        self.rf_gain = rf_gain = 60
        self.q_off = q_off = 0.015
        self.phase = phase = 0.066
        self.offset = offset = 200000
        self.mag = mag = 0.035
        self.i_off = i_off = 0.045
        self.cw_vector = cw_vector = morse_seq("ve3irr   the flag is cucumber   ")*1000
        self.correction = correction = 0
        self.band = band = 926.900
        self.audio_rate = audio_rate = samp_rate / interpolation

        ##################################################
        # Blocks
        ##################################################

        self._q_off_range = qtgui.Range(-0.2, 0.2, 0.0005, 0.015, 200)
        self._q_off_win = qtgui.RangeWidget(self._q_off_range, self.set_q_off, "'q_off'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._q_off_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._phase_range = qtgui.Range(-0.2, 0.2, 0.001, 0.066, 200)
        self._phase_win = qtgui.RangeWidget(self._phase_range, self.set_phase, "'phase'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._phase_win, 4, 0, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._mag_range = qtgui.Range(-0.2, 0.2, 0.001, 0.035, 200)
        self._mag_win = qtgui.RangeWidget(self._mag_range, self.set_mag, "'mag'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._mag_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._i_off_range = qtgui.Range(-0.2, 0.2, 0.0005, 0.045, 200)
        self._i_off_win = qtgui.RangeWidget(self._i_off_range, self.set_i_off, "'i_off'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._i_off_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.soapy_bladerf_sink_0 = None
        dev = 'driver=bladerf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_bladerf_sink_0 = soapy.sink(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_bladerf_sink_0.set_sample_rate(0, samp_rate)
        self.soapy_bladerf_sink_0.set_bandwidth(0, 0.0)
        self.soapy_bladerf_sink_0.set_frequency(0, ((band * 1e6 + 100000 - offset) * (1 + correction*1e-6)))
        self.soapy_bladerf_sink_0.set_frequency_correction(0, 0)
        self.soapy_bladerf_sink_0.set_gain(0, min(max(rf_gain, 17.0), 73.0))
        self.resamp = filter.rational_resampler_ccc(
                interpolation=interpolation,
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.iqbalance_fix_cc_0 = iqbalance.fix_cc(mag, phase)
        self.cw_vector_source = blocks.vector_source_c(cw_vector, False, 1, [])
        self.cw_repeat = blocks.repeat(gr.sizeof_gr_complex*1, (int(1.2 * audio_rate / wpm)))
        self.click_filter = filter.single_pole_iir_filter_cc((1e-2), 1)
        self.blocks_rotator_cc_0 = blocks.rotator_cc((2 * math.pi * (tune * 1000 + 100000) / samp_rate), False)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(0.8)
        self.blocks_add_const_vxx_0_0 = blocks.add_const_cc(i_off + q_off * 1j)
        self.blocks_add_const_vxx_0 = blocks.add_const_cc(0.000001)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_const_vxx_0, 0), (self.resamp, 0))
        self.connect((self.blocks_add_const_vxx_0_0, 0), (self.soapy_bladerf_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.cw_repeat, 0))
        self.connect((self.blocks_rotator_cc_0, 0), (self.iqbalance_fix_cc_0, 0))
        self.connect((self.click_filter, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.cw_repeat, 0), (self.click_filter, 0))
        self.connect((self.cw_vector_source, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.iqbalance_fix_cc_0, 0), (self.blocks_add_const_vxx_0_0, 0))
        self.connect((self.resamp, 0), (self.blocks_rotator_cc_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "blade_tx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_audio_rate(self.samp_rate / self.interpolation)
        self.blocks_rotator_cc_0.set_phase_inc((2 * math.pi * (self.tune * 1000 + 100000) / self.samp_rate))
        self.soapy_bladerf_sink_0.set_sample_rate(0, self.samp_rate)

    def get_interpolation(self):
        return self.interpolation

    def set_interpolation(self, interpolation):
        self.interpolation = interpolation
        self.set_audio_rate(self.samp_rate / self.interpolation)

    def get_wpm(self):
        return self.wpm

    def set_wpm(self, wpm):
        self.wpm = wpm
        self.cw_repeat.set_interpolation((int(1.2 * self.audio_rate / self.wpm)))

    def get_tune(self):
        return self.tune

    def set_tune(self, tune):
        self.tune = tune
        self.blocks_rotator_cc_0.set_phase_inc((2 * math.pi * (self.tune * 1000 + 100000) / self.samp_rate))

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.soapy_bladerf_sink_0.set_gain(0, min(max(self.rf_gain, 17.0), 73.0))

    def get_q_off(self):
        return self.q_off

    def set_q_off(self, q_off):
        self.q_off = q_off
        self.blocks_add_const_vxx_0_0.set_k(self.i_off + self.q_off * 1j)

    def get_phase(self):
        return self.phase

    def set_phase(self, phase):
        self.phase = phase
        self.iqbalance_fix_cc_0.set_phase(self.phase)

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self.soapy_bladerf_sink_0.set_frequency(0, ((self.band * 1e6 + 100000 - self.offset) * (1 + self.correction*1e-6)))

    def get_mag(self):
        return self.mag

    def set_mag(self, mag):
        self.mag = mag
        self.iqbalance_fix_cc_0.set_mag(self.mag)

    def get_i_off(self):
        return self.i_off

    def set_i_off(self, i_off):
        self.i_off = i_off
        self.blocks_add_const_vxx_0_0.set_k(self.i_off + self.q_off * 1j)

    def get_cw_vector(self):
        return self.cw_vector

    def set_cw_vector(self, cw_vector):
        self.cw_vector = cw_vector
        self.cw_vector_source.set_data(self.cw_vector, [])

    def get_correction(self):
        return self.correction

    def set_correction(self, correction):
        self.correction = correction
        self.soapy_bladerf_sink_0.set_frequency(0, ((self.band * 1e6 + 100000 - self.offset) * (1 + self.correction*1e-6)))

    def get_band(self):
        return self.band

    def set_band(self, band):
        self.band = band
        self.soapy_bladerf_sink_0.set_frequency(0, ((self.band * 1e6 + 100000 - self.offset) * (1 + self.correction*1e-6)))

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.cw_repeat.set_interpolation((int(1.2 * self.audio_rate / self.wpm)))




def main(top_block_cls=blade_tx, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
