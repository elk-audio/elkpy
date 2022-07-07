import os
import sys
from elkpy.sushicontroller import SushiController
from elkpy import sushi_info_types as sushi
from elkpy import grpc_gen
from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import *
from enum import IntEnum
from pathlib import Path

SUSHI_ADDRESS = ('localhost:51051')
#SUSHI_ADDRESS = ('192.168.1.90:51051')
# Get protofile to generate grpc library
proto_file = os.environ.get('SUSHI_GRPC_ELKPY_PROTO')
if proto_file is None:
    print('Environment variable SUSHI_GRPC_ELKPY_PROTO not defined, set it to point the .proto definition')
    sys.exit(-1)

SYNCMODES = ['Internal', 'Midi', 'Link']
PLUGIN_TYPES = ['Internal', 'Vst2x', 'Vst3x', 'LV2']
MODE_PLAYING = 2

# Number of columns of parameters to display per processor
# 1-3 works reasonably well
MAX_COLUMNS              = 1

PROCESSOR_WIDTH          = 300
PARAMETER_VALUE_WIDTH    = 80
ICON_BUTTON_WIDTH        = 30
SLIDER_HEIGHT            = 15
SLIDER_MIN_WIDTH         = 100
PAN_SLIDER_WIDTH         = 60
FILE_BUTTON_WIDTH        = 40

# Slider values are ints in QT, so we need to scale with an integer factor to get 0-1 floats
SLIDER_MAX_VALUE         = 1024

sushi_grpc_types, _ = grpc_gen.modules_from_proto(proto_file)


class Direction(IntEnum):
    UP = 1
    DOWN = 2


class MainWindow(QMainWindow):

    track_notification_received = Signal(sushi_grpc_types.TrackUpdate)
    processor_notification_received = Signal(sushi_grpc_types.ProcessorUpdate)
    parameter_notification_received = Signal(sushi_grpc_types.ParameterValue)
    transport_notification_received = Signal(sushi_grpc_types.TransportUpdate)
    timing_notification_received = Signal(sushi_grpc_types.CpuTimings)
    property_notification_received = Signal(sushi_grpc_types.PropertyValue)

    def __init__(self, controller):
        super().__init__()
        self._controller = controller
        self.setWindowTitle('Sushi')

        self._window_layout = QVBoxLayout()
        self._central_widget = QWidget(self)
        self._central_widget.setLayout(self._window_layout)
        self.setCentralWidget(self._central_widget)

        # Menu / actions
        self.file_menu = self.menuBar().addMenu("&File")
        self.settings_menu = self.menuBar().addMenu("&Settings")
        self.tools_menu = self.menuBar().addMenu("&Tools")
        self.help_menu = self.menuBar().addMenu("&Info")

        save = QAction('Save', self)
        save.triggered.connect(controller.save_session)
        load = QAction('Load', self)
        load.triggered.connect(controller.restore_session)

        self.file_menu.addAction(save)
        self.file_menu.addAction(load)

        about = QAction('About Sushi', self)
        about.triggered.connect(self.show_about_sushi)
        processors = QAction('Show all processors', self)
        processors.triggered.connect(self.show_all_processors)
        tracks = QAction('Show all tracks', self)
        tracks.triggered.connect(self.show_all_tracks)
        inputs = QAction('Show input connections', self)
        inputs.triggered.connect(self.show_inputs)

        self.help_menu.addAction(about)
        self.help_menu.addAction(processors)
        self.help_menu.addAction(tracks)
        self.help_menu.addAction(inputs)

        self.tpbar = TransportBarWidget(self._controller)
        self._window_layout.addWidget(self.tpbar)
        self.tracks = {}
        self._track_layout = QHBoxLayout(self)
        self._window_layout.addLayout(self._track_layout)

        self.track_notification_received.connect(self.process_track_notification)
        self.processor_notification_received.connect(self.process_processor_notification)
        self.parameter_notification_received.connect(self.process_parameter_notification)
        self.transport_notification_received.connect(self.process_transport_notification)
        self.timing_notification_received.connect(self.process_timing_notification)
        self.property_notification_received.connect(self.process_property_notification)

        self._create_tracks()

    def delete_track(self, track_id):
        track = self.tracks.pop(track_id)
        track.deleteLater() # Otherwise traces are left hanging
        self._track_layout.removeWidget(track)

    def create_track(self, track_info):
        if (track_info.id not in self.tracks):
            track = TrackWidget(self._controller, track_info, self)
            self._track_layout.addWidget(track)
            self.tracks[track_info.id] = track

    def create_processor_on_track(self, plugin_info, track_id):
        self.tracks[track_id].create_processor(plugin_info)

    def _create_tracks(self):
        tracks = self._controller.audio_graph.get_all_tracks()
        for t in tracks:
            self.create_track(t)

    def show_about_sushi(self):
        version = self._controller.system.get_sushi_version()
        build_info = self._controller.system.get_build_info()
        audio_inputs = self._controller.system.get_input_audio_channel_count()
        audio_outputs = self._controller.system.get_output_audio_channel_count()

        about = QMessageBox()
        about.setText(f"Sushi version: {version}\n"
                      f"Buidl info: {build_info}\n"
                      f"Audio input count: {audio_inputs}\n"
                      f"Audio output count: {audio_outputs}")
        about.exec_()

    def show_all_processors(self):
        r = self._controller.audio_graph.get_all_processors()
        info = QMessageBox()
        info.setText(f"{r}")
        info.exec_()

    def show_all_tracks(self):
        r = self._controller.audio_graph.get_all_tracks()
        info = QMessageBox()
        info.setText(f"{r}")
        info.exec_()

    def show_inputs(self):
        r = self._controller.audio_routing.get_all_input_connections()
        info = QMessageBox()
        info.setText(f"{r}")
        info.exec_()

    def process_track_notification(self, n):
        if n.action == 1:   # TRACK_ADDED
            for t in self._controller.audio_graph.get_all_tracks():
                if t.id == n.track.id:
                    self.create_track(t)
                    break
        elif n.action == 2:  # TRACK_DELETED
            self.delete_track(n.track.id)

    def process_processor_notification(self, n):
        if n.action == 1:  # PROCESSOR_ADDED
            for t in self._controller.audio_graph.get_track_processors(n.parent_track.id):
                if t.id == n.processor.id:
                    self.create_processor_on_track(t, n.parent_track.id)
                    break
        elif n.action == 2:  # PROCESSOR_DELETED
            self.tracks[n.parent_track.id].delete_processor(n.processor.id)

    def process_parameter_notification(self, n):
        for id, track in self.tracks.items():
            if n.parameter.processor_id == id:
                track.handle_parameter_notification(n)

            elif n.parameter.processor_id in track.processors:
                track.processors[n.parameter.processor_id].handle_parameter_notification(n)

    def process_transport_notification(self, n):
        if n.HasField('tempo'):
            self.tpbar.set_tempo(n.tempo)

        elif n.HasField('playing_mode'):
            self.tpbar.set_playing(n.playing_mode.mode == MODE_PLAYING)

    def process_timing_notification(self, n):
        self.tpbar.set_cpu_value(n.average)

    def process_property_notification(self, n):
        for t, v in self.tracks.items():
            if n.property.processor_id in v.processors:
                v.processors[n.property.processor_id].handle_property_notification(n)

class TransportBarWidget(QGroupBox):
    def __init__(self, controller):
        super().__init__()
        self._controller = controller
        self._layout = QHBoxLayout(self)
        self.setLayout(self._layout)
        self._create_widgets()

    def _create_widgets(self):
        self._syncmode_label = QLabel('Sync mode', self)
        self._layout.addWidget(self._syncmode_label)
        self._syncmode = QComboBox(self)
        for mode in SYNCMODES:
            self._syncmode.addItem(mode)

        self._layout.addWidget(self._syncmode)
        self._tempo_label = QLabel('Tempo', self)
        self._layout.addWidget(self._tempo_label)

        self._tempo = QDoubleSpinBox(self)
        self._tempo.setRange(20, 999)
        self._tempo.setValue(self._controller.transport.get_tempo())
        self._layout.addWidget(self._tempo)

        self._stop_button = QPushButton('', self)
        self._stop_button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_MediaStop')))
        self._stop_button.setCheckable(True)
        self._layout.addWidget(self._stop_button)

        self._play_button = QPushButton('', self)
        self._play_button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_MediaPlay')))
        self._play_button.setCheckable(True)
        self._layout.addWidget(self._play_button)

        self._add_track_button = QPushButton('New Track', self)
        self._layout.addWidget(self._add_track_button)

        self._cpu_meter = QLabel("Cpu: -", self)
        self._layout.addWidget(self._cpu_meter)

        self._layout.addStretch(0)
        self._connect_signals()

    def _connect_signals(self):
        self._play_button.clicked.connect(self._controller.set_playing)
        self._stop_button.clicked.connect(self._controller.set_stopped)
        self._syncmode.currentTextChanged.connect(self._controller.set_sync_mode_txt)
        self._tempo.valueChanged.connect(self._controller.transport.set_tempo)
        self._add_track_button.clicked.connect(self._controller.add_track)

    def set_playing(self, playing):
        self._play_button.setChecked(playing)
        self._stop_button.setChecked(not playing)

    def set_tempo(self, tempo):
        self._tempo.setValue(tempo)

    def set_cpu_value(self, value):
        self._cpu_meter.setText(f"Cpu: {value * 100:.1f}%")


class TrackWidget(QGroupBox):
    def __init__(self, controller, track_info, parent):
        super().__init__(track_info.name, parent)
        self._id = track_info.id
        self._parent = parent
        self._controller = controller
        self._layout = QVBoxLayout(self)
        self.setLayout(self._layout)
        self.processors = {}
        self._create_processors(track_info)
        self._create_common_controls(track_info)
        self._connect_signals()

    def create_processor(self, proc_info):
        if proc_info.id not in self.processors:
            processor = ProcessorWidget(self._controller, proc_info, self._id, self)
            self._proc_layout.insertWidget(self._proc_layout.count() - 1, processor)
            self.processors[proc_info.id] = processor

    def _create_processors(self, track_info):
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        scroll.setFrameShape(QFrame.NoFrame)

        self._proc_layout = QVBoxLayout(self)
        frame = QWidget(self)
        frame.setLayout(self._proc_layout)
        frame.setContentsMargins(0,0,0,0)
        frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        scroll.setWidget(frame)
        self._layout.addWidget(scroll)

        processors = self._controller.audio_graph.get_track_processors(track_info.id)
        for p in processors:
            processor = ProcessorWidget(self._controller, p, track_info.id, self)
            self._proc_layout.addWidget(processor, 0)
            self.processors[p.id] = processor

        self._proc_layout.addStretch()

    def _create_common_controls(self, track_info):
        pan_gain_layout = QHBoxLayout(self)
        pan_gain_layout.setContentsMargins(0,0,0,0)
        pan_gain_box = QGroupBox('Master', self)
        pan_gain_box.setMaximumHeight(220)
        pan_gain_box.setLayout(pan_gain_layout)
        self._layout.addWidget(pan_gain_box)
        self._pan_gain = [PanGainWidget(self._id, 'Main Bus', 0, 1, self._controller, self)]
        pan_gain_layout.addWidget(self._pan_gain[0], 0, Qt.AlignLeft)

        # Create 1 pan/gain control per extra output bus
        for bus in range(1, track_info.output_busses):
            gain_id = self._controller.parameters.get_parameter_id(track_info.id, 'gain_sub_' + str(bus))
            pan_id = self._controller.parameters.get_parameter_id(track_info.id, 'pan_sub_' + str(bus))
            pan_gain = PanGainWidget(self._id, 'Sub Bus ' + str(bus), gain_id, pan_id, self._controller, self)
            pan_gain_layout.addWidget(pan_gain)
            self._pan_gain.append(pan_gain)

        self._track_buttons = QHBoxLayout(self)
        self._layout.addLayout(self._track_buttons)
        
        self._mute_button = QPushButton('Mute', self)
        self._track_buttons.addWidget(self._mute_button)
        self._mute_button.setCheckable(True)
        self._mute_id = self._controller.parameters.get_parameter_id(track_info.id, 'mute')
        self._mute_button.setChecked(self._controller.parameters.get_parameter_value(self._id, self._mute_id) == 1)

        self._delete_button = QPushButton('Delete', self)
        self._track_buttons.addWidget(self._delete_button)
        self._add_plugin_button = QPushButton('Add Plugin', self)
        self._track_buttons.addWidget(self._add_plugin_button)
        self._track_buttons.addStretch(0)

    def _connect_signals(self):
        self._mute_button.clicked.connect(self.mute_track)
        self._delete_button.clicked.connect(self.delete_track)
        self._add_plugin_button.clicked.connect(self.add_plugin)

    def handle_parameter_notification(self, notif):
        for pan_gain in self._pan_gain:
            if notif.parameter.parameter_id == pan_gain.pan_id:
                pan_gain.set_pan_slider(notif.normalized_value)
                pan_gain.set_pan_label(notif.formatted_value)

            elif notif.parameter.parameter_id == pan_gain.gain_id:
                pan_gain.set_gain_slider(notif.normalized_value)
                pan_gain.set_gain_label(notif.formatted_value)

        if notif.parameter.parameter_id == self._mute_id:
            self._mute_button.blockSignals(True)
            self._mute_button.setChecked(True if notif.normalized_value > 0.5 else False)
            self._mute_button.blockSignals(False)

    def mute_track(self, arg):
        state = self._mute_button.isChecked()
        muted = self._controller.parameters.set_parameter_value(self._id, self._mute_id, 1 if state == True else 0)

    def delete_track(self, arg):
        self._controller.audio_graph.delete_track(self._id)

    def add_plugin(self, arg):
        self._controller.add_plugin(self._id)

    def delete_processor(self, processor_id):
        p = self.processors.pop(processor_id)
        p.deleteLater() # Otherwise traces are left hanging
        self._proc_layout.removeWidget(p)

    def move_processor(self, processor_id, direction):
        p = self.processors[processor_id]
        index = self._proc_layout.indexOf(p)
        
        if direction == Direction.UP and index > 0:
            self._proc_layout.removeWidget(p)
            self._proc_layout.insertWidget(index - 1, p)

        # There is a 'hidden' stretch element that should always remain at the end
        # for layout purposes, so never move the processor past that element.
        elif direction == Direction.DOWN and index < self._proc_layout.count() - 2:
            self._proc_layout.removeWidget(p)
            self._proc_layout.insertWidget(index + 1, p)


class ProcessorWidget(QGroupBox):
    def __init__(self, controller, processor_info, track_id, parent):
        super().__init__(processor_info.name, parent)
        self.setFixedWidth(PROCESSOR_WIDTH * MAX_COLUMNS)
        # Make sure the ProcessorWidget doesn't expand to much, as that looks ugly
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self._controller = controller
        self._id = processor_info.id
        self._track_id = track_id
        self._parameters = {}
        self._properties = {}
        self._layout = QVBoxLayout(self)
        self.setLayout(self._layout)

        self._create_common_controls(processor_info)
        self._create_parameters()
        self._create_properties()
        self._connect_signals()

    def _create_parameters(self):
        parameters = self._controller.parameters.get_processor_parameters(self._id)
        param_count = len(parameters)
        param_layout = QHBoxLayout()
        self._layout.addLayout(param_layout)
        for col in range(0, MAX_COLUMNS):
            col_layout = QVBoxLayout()
            param_layout.addLayout(col_layout)
            for p in parameters[col::MAX_COLUMNS]:
                parameter = ParameterWidget(p, self._id, self._controller, self)
                col_layout.addWidget(parameter)
                self._parameters[p.id] = parameter

            col_layout.addStretch()
        self._layout.addStretch()

    def _create_properties(self):
        properties = self._controller.parameters.get_processor_properties(self._id)
        prop_count = len(properties)
        prop_layout = QVBoxLayout()
        self._layout.addLayout(prop_layout)

        for p in properties:
            property = PropertyWidget(p, self._id, self._controller, self)
            prop_layout.addWidget(property)
            self._properties[p.id] = property

        self._layout.addStretch()

    def _create_common_controls(self, processor_info):
        common_layout = QHBoxLayout(self)
        self._layout.addLayout(common_layout)

        self._mute_button = QPushButton(self)
        self._mute_button.setCheckable(True)
        self._mute_button.setChecked(self._controller.audio_graph.get_processor_bypass_state(self._id))
        self._mute_button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_MediaVolumeMuted')))
        self._mute_button.setFixedWidth(ICON_BUTTON_WIDTH)
        self._mute_button.setToolTip('Mute processor')
        common_layout.addWidget(self._mute_button)

        self._delete_button = QPushButton(self)
        self._delete_button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_DialogCloseButton')))
        self._delete_button.setFixedWidth(ICON_BUTTON_WIDTH)
        self._delete_button.setToolTip('Delete processor')
        common_layout.addWidget(self._delete_button)

        self._up_button = QPushButton('', self)
        self._up_button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_ArrowUp')))
        self._up_button.setToolTip('Move processor up')
        self._up_button.setFixedWidth(ICON_BUTTON_WIDTH)
        common_layout.addWidget(self._up_button)

        self._down_button = QPushButton('', self)
        self._down_button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_ArrowDown')))
        self._down_button.setToolTip('Move processor down')
        self._down_button.setFixedWidth(ICON_BUTTON_WIDTH)
        common_layout.addWidget(self._down_button)
    

        self._program_selector = QComboBox(self)
        common_layout.addWidget(self._program_selector)
        if processor_info.program_count > 0:
            for program in self._controller.programs.get_processor_programs(self._id):
                self._program_selector.addItem(program.name)
            current_program =self._controller.programs.get_processor_current_program(self._id)
            self._program_selector.setCurrentIndex(current_program)
            
        else:
            self._program_selector.addItem('No programs')
    
    def _connect_signals(self):
        self._mute_button.clicked.connect(self.mute_processor_clicked)
        self._program_selector.currentIndexChanged.connect(self.program_selector_changed)
        self._delete_button.clicked.connect(self.delete_processor_clicked)
        self._up_button.clicked.connect(self.up_clicked)
        self._down_button.clicked.connect(self.down_clicked)

    def handle_parameter_notification(self, notif):
        self._parameters[notif.parameter.parameter_id].set_slider_value(notif.normalized_value)
        self._parameters[notif.parameter.parameter_id].set_label_value(notif.formatted_value)

    def handle_property_notification(self, notif):
        self._properties[notif.property.property_id].set_value(notif.value)

    def delete_processor_clicked(self):
        self._controller.delete_processor(self._track_id, self._id)

    def up_clicked(self):
        self._controller.move_processor(self._track_id, self._id, Direction.UP)

    def down_clicked(self):
        self._controller.move_processor(self._track_id, self._id, Direction.DOWN)

    def mute_processor_clicked(self, arg):
        state = self._mute_button.isChecked()
        self._controller.audio_graph.set_processor_bypass_state(self._id, state)        

    def program_selector_changed(self, program_id):
        self._controller.programs.set_processor_program(self._id, program_id)

class ParameterWidget(QWidget):
    def __init__(self, parameter_info, processor_id, controller, parent):
        super().__init__(parent)
        self._controller = controller
        self._id = parameter_info.id
        self._processor_id = processor_id
        self._unit = parameter_info.unit
        self._layout = QHBoxLayout(self)
        self.setLayout(self._layout)

        self._name_label = QLabel(parameter_info.name, self)
        self._name_label.setFixedWidth(PARAMETER_VALUE_WIDTH)
        self._layout.addWidget(self._name_label)

        self._value_slider = QSlider(Qt.Orientation.Horizontal, self)
        self._value_slider.setFixedWidth(SLIDER_MIN_WIDTH)
        self._value_slider.setRange(0, SLIDER_MAX_VALUE)
        self._layout.addWidget(self._value_slider)

        self._value_label = QLabel('0.0' + parameter_info.unit, self)
        self._value_label.setFixedWidth(PARAMETER_VALUE_WIDTH)
        self._value_label.setAlignment(Qt.AlignRight)
        self._layout.addWidget(self._value_label)
        self._layout.setContentsMargins(0,0,0,0)

        value = self._controller.parameters.get_parameter_value(self._processor_id, self._id)
        self.set_slider_value(value)
        txt_value = self._controller.parameters.get_parameter_value_as_string(self._processor_id, self._id)
        self.set_label_value(txt_value)

        if parameter_info.automatable:
            self._connect_signals()
        else:
            # It an output only parameter, it's not meant to be set by the user
            self._value_slider.setEnabled(False)


    def _connect_signals(self):
        self._value_slider.valueChanged.connect(self.value_changed)

    def value_changed(self):
        value = float(self._value_slider.value()) / SLIDER_MAX_VALUE
        self._controller.parameters.set_parameter_value(self._processor_id, self._id, value)

    def set_slider_value(self, value):
        ## Set value without triggering a signal
        self._value_slider.blockSignals(True)
        self._value_slider.setValue(value * SLIDER_MAX_VALUE)
        self._value_slider.blockSignals(False)

    def set_label_value(self, value):
        self._value_label.setText(value + ' ' + self._unit)

class PropertyWidget(QWidget):
    def __init__(self, property_info, processor_id, controller, parent):
        super().__init__(parent)
        self._controller = controller
        self._id = property_info.id
        self._processor_id = processor_id
        self._layout = QHBoxLayout(self)
        self.setLayout(self._layout)

        self._name_label = QLabel(property_info.name, self)
        self._name_label.setFixedWidth(PARAMETER_VALUE_WIDTH)
        self._layout.addWidget(self._name_label)

        self._edit_box = QLineEdit(self)
        self._layout.addWidget(self._edit_box)

        self._file_button = QPushButton('', self)
        self._file_button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_DirIcon')))
        self._file_button.setToolTip("Set to a file location")
        self._layout.addWidget(self._file_button)
        self._file_button.clicked.connect(self.open_file_dialog)

        self._layout.setContentsMargins(0,0,0,0)

        value = self._controller.parameters.get_property_value(self._processor_id, self._id)
        self._edit_box.setText(value)
        self._connect_signals()

    def _connect_signals(self):
        self._edit_box.returnPressed.connect(self.value_changed)

    def value_changed(self):
        value = self._edit_box.text()
        self._controller.parameters.set_property_value(self._processor_id, self._id, value)

    def set_value(self, value):
        self._edit_box.blockSignals(True)
        self._edit_box.setText(value)
        self._edit_box.blockSignals(False)

    def open_file_dialog(self):
        dialog = QFileDialog(self)
        if dialog.exec_():
            filename = dialog.selectedFiles()[0]
            self._edit_box.setText(filename)
            self._controller.parameters.set_property_value(self._processor_id, self._id, filename)


class PanGainWidget(QWidget):
    def __init__(self, processor_id, name, gain_id, pan_id, controller, parent):
        super().__init__(parent)
        self._processor_id = processor_id
        self.gain_id = gain_id
        self.pan_id = pan_id
        self._controller = controller
        self.setFixedWidth(SLIDER_MIN_WIDTH)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0,0,0,0)

        bus_label = QLabel(name, self)
        self._layout.addWidget(bus_label, 0, Qt.AlignHCenter)

        self._gain_slider = QSlider(Qt.Orientation.Vertical, self)
        self._gain_slider.setFixedHeight(80)
        self._gain_slider.setRange(0, SLIDER_MAX_VALUE)
        self._gain_slider.setValue(SLIDER_MAX_VALUE / 2)
        self._layout.addWidget(self._gain_slider, 0, Qt.AlignHCenter)

        self._gain_label = QLabel('', self)
        self._layout.addWidget(self._gain_label, 0, Qt.AlignHCenter)

        self._pan_slider = QSlider(Qt.Orientation.Horizontal, self)
        self._pan_slider.setFixedWidth(PAN_SLIDER_WIDTH)
        self._pan_slider.setRange(0, SLIDER_MAX_VALUE)
        self._pan_slider.setValue(SLIDER_MAX_VALUE / 2)
        self._layout.addWidget(self._pan_slider, 0, Qt.AlignHCenter)

        self._pan_label = QLabel('', self)
        self._layout.addWidget(self._pan_label, 0, Qt.AlignHCenter)

        value = self._controller.parameters.get_parameter_value(self._processor_id, pan_id)
        self.set_pan_slider(value)
        txt_value = self._controller.parameters.get_parameter_value_as_string(self._processor_id, self.pan_id)
        self.set_pan_label(txt_value)

        value = self._controller.parameters.get_parameter_value(self._processor_id, gain_id)
        self.set_gain_slider(value)
        txt_value = self._controller.parameters.get_parameter_value_as_string(self._processor_id, self.gain_id)
        self.set_gain_label(txt_value)
        
        self._connect_signals()

    def _connect_signals(self):
        self._pan_slider.valueChanged.connect(self.pan_changed)
        self._gain_slider.valueChanged.connect(self.gain_changed)

    def pan_changed(self):
        value = float(self._pan_slider.value()) / SLIDER_MAX_VALUE
        self._controller.parameters.set_parameter_value(self._processor_id, self.pan_id, value)

    def gain_changed(self):
        value = float(self._gain_slider.value()) / SLIDER_MAX_VALUE
        self._controller.parameters.set_parameter_value(self._processor_id, self.gain_id, value)

    def set_pan_slider(self, value):
        self._pan_slider.blockSignals(True)
        self._pan_slider.setValue(value * SLIDER_MAX_VALUE)
        self._pan_slider.blockSignals(False)

    def set_pan_label(self, txt_value):
        self._pan_label.setText(txt_value)

    def set_gain_slider(self, value):
        self._gain_slider.blockSignals(True)
        self._gain_slider.setValue(value * SLIDER_MAX_VALUE)
        self._gain_slider.blockSignals(False)

    def set_gain_label(self, txt_value):
        self._gain_label.setText(txt_value + ' ' + 'dB')


class AddTrackDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setModal(True)
        self.setWindowTitle('Add new track')

        self._layout = QGridLayout(self)
        self.setLayout(self._layout)

        self.name_label = QLabel('Name', self)
        self._layout.addWidget(self.name_label, 0,0)
        self._name_entry = QLineEdit(self)
        self._layout.addWidget(self._name_entry,0,1)

        nr_of_channels = QLabel('Track type:')
        self._layout.addWidget(nr_of_channels, 2, 0)
        self._track_type = QComboBox(self)
        self._track_type.addItem('Mono')
        self._track_type.addItem('Stereo')
        self._track_type.addItem('Multibus')
        self._track_type.setCurrentIndex(1)
        self._layout.addWidget(self._track_type, 2, 1)

        self._inputs_lbl = QLabel('Inputs:')
        self._inputs_sb = QSpinBox()
        self._inputs_sb.setMinimum(1)
        self._inputs_sb.setMaximum(8)
        self._layout.addWidget(self._inputs_lbl, 3, 0)
        self._layout.addWidget(self._inputs_sb, 3, 1)
        self._inputs_lbl.hide()
        self._inputs_sb.hide()

        self._outputs_lbl = QLabel('Outputs:')
        self._outputs_lbl.hide()
        self._outputs_sb = QSpinBox()
        self._outputs_sb.hide()
        self._outputs_sb.setMinimum(1)
        self._outputs_sb.setMaximum(8)
        self._layout.addWidget(self._outputs_lbl, 4, 0)
        self._layout.addWidget(self._outputs_sb, 4, 1)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.button(QDialogButtonBox.Ok).setDefault(True)
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(True)
        self._layout.addWidget(self.button_box, 5, 1)

        self._connect_signals()

    def _connect_signals(self):
        self._track_type.currentIndexChanged.connect(self._update_nr_of_channels)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def _update_nr_of_channels(self, idx: int):
        if idx == 2:
            self._inputs_sb.show()
            self._inputs_lbl.show()
            self._outputs_sb.show()
            self._outputs_lbl.show()
        else:
            self._inputs_sb.hide()
            self._inputs_lbl.hide()
            self._outputs_sb.hide()
            self._outputs_lbl.hide()


class AddPluginDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Add new plugin')

        self._layout = QGridLayout(self)
        self.setLayout(self._layout)

        self._type = None

        type_label = QLabel('Type', self)
        self._layout.addWidget(type_label, 0, 0)
        self._type_box = QComboBox(self)
        self._layout.addWidget(self._type_box, 0, 1)
        for t in PLUGIN_TYPES:
            self._type_box.addItem(t)

        name_label = QLabel('Name', self)
        self._layout.addWidget(name_label, 1,0)
        self._name_entry = QLineEdit(self)
        self._name_entry.setMinimumWidth(200)
        self._layout.addWidget(self._name_entry,1,1)

        self._uid_label = QLabel('Uid', self)
        self._layout.addWidget(self._uid_label, 2,0)
        self._uid_entry = QLineEdit(self)
        self._layout.addWidget(self._uid_entry,2,1)

        self._path_label = QLabel('Path', self)
        self._layout.addWidget(self._path_label, 3,0)
        self._path_entry = QLineEdit(self)
        self._path_entry.setEnabled(False)
        self._layout.addWidget(self._path_entry,3,1)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok |
                                               QDialogButtonBox.Cancel)
        self.button_box.button(QDialogButtonBox.Ok).setDefault(True)
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(True)
        self._layout.addWidget(self.button_box, 4, 1)
        
        self._connect_signals()

    def _connect_signals(self):
        self._type_box.currentIndexChanged.connect(self.type_changed)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def type_changed(self, type_index):
        type = type_index + 1
        self._type = type
        if (type == sushi.PluginType.INTERNAL):
            self._path_entry.setEnabled(False)
            self._uid_entry.setEnabled(True)

        elif (type == sushi.PluginType.VST2X):
            self._path_entry.setEnabled(True)
            self._uid_entry.setEnabled(False)

        elif (type == sushi.PluginType.VST3X):
            self._path_entry.setEnabled(True)
            self._uid_entry.setEnabled(True)

        elif (type == sushi.PluginType.LV2):
            self._path_entry.setEnabled(True)
            self._uid_entry.setEnabled(False)


# Expand the controller with a few convinience functions that better match our use case
class Controller(SushiController):

    def __init__(self, address, proto_file):
        super().__init__(address, proto_file)
        self._view = None
        
    def emit_notification(self, notif):
        try:
            if type(notif) == sushi_grpc_types.TrackUpdate:
                self._view.track_notification_received.emit(notif)
            elif type(notif) == sushi_grpc_types.ProcessorUpdate:
                self._view.processor_notification_received.emit(notif)
            elif type(notif) == sushi_grpc_types.ParameterUpdate:
                self._view.parameter_notification_received.emit(notif)
            elif type(notif) == sushi_grpc_types.TransportUpdate:
                self._view.transport_notification_received.emit(notif)
            elif type(notif) == sushi_grpc_types.CpuTimings:
                self._view.timing_notification_received.emit(notif)
            elif type(notif) == sushi_grpc_types.PropertyValue:
                self._view.property_notification_received.emit(notif)
            else:
                print(type(notif))

        ## Note, if an exception in a notification handler is not caught, that notification stops working 
        except Exception as e:
            print(e)


    def subscribe_to_notifications(self):
        self.notifications.subscribe_to_track_changes(self.emit_notification)
        self.notifications.subscribe_to_processor_changes(self.emit_notification)
        self.notifications.subscribe_to_parameter_updates(self.emit_notification)
        self.notifications.subscribe_to_transport_changes(self.emit_notification)
        self.notifications.subscribe_to_timing_updates(self.emit_notification)
        self.notifications.subscribe_to_property_updates(self.emit_notification)
        self.timings.set_timings_enabled(True)
        self.timings.reset_all_timings();

    def set_playing(self):
        self.transport.set_playing_mode(2)

    def set_stopped(self):
        self.transport.set_playing_mode(1)

    def delete_processor(self, track_id, processor_id):
        self.audio_graph.delete_processor_from_track(processor_id, track_id)

    def delete_track(self, track_id):
        super().audio_graph.delete_track(track_id)

    def add_track(self):
        dialog = AddTrackDialog(self._view)
        if dialog.exec_():
            track_type = dialog._track_type.currentText()
            inputs = dialog._inputs_sb.value()
            outputs = dialog._outputs_sb.value()
            name = dialog._name_entry.text().strip()

            if track_type == 'Multibus':
                self.audio_graph.create_multibus_track(name, outputs, inputs)
            elif track_type == 'Stereo':
                self.audio_graph.create_track(name, 2)
            elif track_type == 'Mono':
                self.audio_graph.create_track(name, 1)

    def add_plugin(self, track_id):
        dialog = AddPluginDialog(self._view)
        if dialog.exec_():
            name = dialog._name_entry.text().strip()
            uid = dialog._uid_entry.text().strip()
            path = dialog._path_entry.text().strip()
            p_type = dialog._type
            try:
                self.audio_graph.create_processor_on_track(name, uid, path, p_type, track_id, 0, True)
            except Exception as e:
                print('Error creating plugin: {}'.format(e))   

    def move_processor(self, track_id, processor_id, direction):
        track_info = self.audio_graph.get_track_info(track_id)
        index = track_info.processors.index(processor_id)

        proc_count = len(track_info.processors)
        if (direction == Direction.UP and index == 0) or (direction == direction.DOWN and index == proc_count - 1):
            # Processor is not in a place where it can be moved
            return

        # only true if moving down and processor position is second to last
        add_to_back = direction == Direction.DOWN and index == proc_count - 2
        before_processor = 0 
        if direction == Direction.UP:
            before_processor = track_info.processors[index - 1] 
        elif not add_to_back:
            before_processor = track_info.processors[index + 2]

        self.audio_graph.move_processor_on_track(processor_id, track_id, track_id, add_to_back, before_processor)

        self._view.tracks[track_id].move_processor(processor_id, direction)

    def set_sync_mode_txt(self, txt_mode):
        if txt_mode == 'Internal':
            self.transport.set_sync_mode(sushi.SyncMode.INTERNAL)
        elif txt_mode == 'Link':
            self.transport.set_sync_mode(sushi.SyncMode.LINK)
        if txt_mode == 'Midi':
            self.transport.set_sync_mode(sushi.SyncMode.MIDI)

    def save_session(self):
        filename, _ = QFileDialog.getSaveFileName(self._view, 'Save Session As', '', '')

        if filename:
            if not filename.endswith('.sushi'):
                filename += '.sushi'

            saved_session = self.session.save_binary_session();
            with open(filename, 'wb') as f:
                f.write(saved_session)

    def restore_session(self):
        filename, _ = QFileDialog.getOpenFileName(self._view, 'Load Session', '', "Sushi Files (*.sushi)")

        if filename:
            with open(filename, 'rb') as f:
                saved_session = f.read()

            self.session.restore_binary_session(saved_session)

    def set_view(self, view):
        self._view = view


# Client code
def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    controller = Controller(SUSHI_ADDRESS, proto_file)
    window = MainWindow(controller)
    window.show()
    controller.set_view(window)
    controller.subscribe_to_notifications()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
