from time import sleep
#import pygro
from ELKpy import sushicontroller as sc
import tkinter as tk

SLEEP_PERIOD = 0.0001# increase to limit the number of simultaneous set requests (Re's don't like that)
COLUMN_HEIGHT = 15 # max widgets before starting a new column
SLIDER_WIDTH = 150
SLIDER_HEIGHT = 50

class App(tk.Frame):
    def __init__(self, controller, master=None):
        super().__init__(master)
        self.cont = controller
        self.master = master
        self.widgets = []
        self.processor_params = {}
        self.pack(fill="both")
        self.create_widgets()

    def set_parameter(self, processor_id, parameter_id, value):
        # self.cont.SetParameterValue(parameter={"processor_id": processor_id, "parameter_id": parameter_id}, value=value) 
        self.cont.set_parameter_value(processor_id, parameter_id, value)
        sleep(SLEEP_PERIOD )
        # txt_val = self.cont.GetParameterValueAsString(parameter={"processor_id": processor_id, "parameter_id":parameter_id})
        txt_val = self.cont.get_parameter_value_as_string(processor_id, parameter_id)
        self.value_display.delete(0, tk.END)
        self.value_display.insert(0, str(value) + " ("+str(txt_val)+")")

    def set_program(self, processor_id, program, programs):
        program_id = programs.index(program)
        #self.cont.SetProcessorProgram(processor= processor_id, program=program_id)
        self.cont.set_processor_program(processor_id, program_id)
        sleep(SLEEP_PERIOD)
        self.refresh_param_values(processor_id)

    def set_bypass(self, processor_id, bypassed):
        print("Setting bypass "+str(bypassed) + " on proc: " + str(processor_id))
        #self.cont.SetProcessorBypassState(processor= processor_id, value=bypassed)
        self.cont.set_processor_bypass_state(processor_id, bypassed)

    def get_parameter(self, processor_id, parameter_id):
        try:
            #return self.cont.GetParameterValue(parameter={"processor_id": processor_id, "parameter_id":parameter_id}).value
            return self.cont.get_parameter_value(processor_id, parameter_id)
        except:
            return 0
        #return val.value

    def refresh_param_values(self, processor_id):
        for i in self.processor_params[processor_id]:
            value = self.cont.get_parameter_value(processor_id, i['id'])
            i['widget'].set(value)

    def create_widgets(self):
        entry = tk.Entry(self)
        entry.pack()
        entry.insert(0, "Text")
        self.value_display = entry

        #tracks = self.cont.GetTracks()
        tracks = self.cont.get_tracks()
        #for t in tracks.tracks:
        for t in tracks:
            self.create_track(t)
            separator = tk.Frame(self, height=2, width=2, bd=1, relief="sunken")
            separator.pack(fill="y", side="left", padx=5, pady=5)

    def create_track(self, track):
        #processors = self.cont.GetTrackProcessors(TrackId={"id": track.id})
        processors = self.cont.get_track_processors(track.id)
        frame = tk.Frame(self)
        frame.pack(fill="both", side="left")
        processor_count = 0

        #for p in processors.processors:
        for p in processors:
            if processor_count > 1:
                 new_frame = tk.Frame(self)
                 new_frame.pack(fill="both", side="left")
                 frame = new_frame
                 processor_count = 0

            processor_count += 1

            label = tk.Label(frame, text=p.label)
            label.pack(side="top")
            self.create_processor(frame, p)
            separator = tk.Frame(frame, self, height=2, width=2, bd=1, relief="sunken")
            separator.pack(fill="x", side="top", padx=5, pady=5)

        pan_vol_frame = tk.Frame(frame)
        #params = self.cont.GetTrackParameters(TrackId={"id": track.id})
        params = self.cont.get_track_parameters(track.id)
        #for p in params.parameters:
        for p in params:
            l = tk.Label(pan_vol_frame, text=p.name)
            l.pack(side="top")
            def_val = self.get_parameter(track.id, p.id)
            w = tk.Scale(pan_vol_frame, from_=p.min_range, to_=p.max_range, resolution=0.001, \
                 showvalue=False, orient=tk.HORIZONTAL,  length=SLIDER_WIDTH, \
                 command=lambda v,p=track.id,a=p.id: self.set_parameter(p, a, float(v)))
            w.pack(side="top")
            w.set(def_val)
            sleep(SLEEP_PERIOD)

        pan_vol_frame.pack(fill="y", side="bottom")

    def create_processor(self, parent, proc):
        #params = self.cont.GetProcessorParameters(ProcId={"id": proc.id})
        params = self.cont.get_processor_parameters(proc.id)
        proc_frame = tk.Frame(parent) 
        proc_frame.pack(fill="both", side="top")
        frame = tk.Frame(proc_frame, width=SLIDER_WIDTH) 
        frame.pack(fill="y", side="left")
        self.create_program_selector(frame, proc)
        self.processor_params[proc.id] = []
        count = 0
        
        #for p in params.parameters:
        for p in params:
            if count > COLUMN_HEIGHT:
                new_frame = tk.Frame(proc_frame) 
                new_frame.pack(fill="y", side="left")
                count = 0
                frame = new_frame

            l = tk.Label(frame, text=p.name)
            l.pack(side="top")
            def_val = self.get_parameter(proc.id, p.id)
            w = tk.Scale(frame, from_=p.min_range, to_=p.max_range, resolution=0.001, \
                showvalue=False, orient=tk.HORIZONTAL, length=SLIDER_WIDTH, \
                command=lambda v,p=proc.id,a=p.id: self.set_parameter(p, a, float(v)))
            w.pack(side="top", fill="none")
            w.set(def_val)
            self.processor_params[proc.id].append({'id':p.id, 'widget':w})
            sleep(SLEEP_PERIOD)
            count += 1

        self.create_program_selector(frame, proc)
        self.create_bypass_button(frame, proc)
        #self.processor_params[proc.id] = []
    
    def create_program_selector(self, parent, proc):
        try:
            #programs = self.cont.GetProcessorPrograms(ProcId={"id": proc.id})
            programs = self.cont.get_processor_programs(proc.id)
            program_names = [p.name for p in programs.programs]
            label = tk.Label(parent, text="Programs")
            label.pack(side="top")
            variable = tk.StringVar(parent)
            variable.set(program_names[0])
            selector = tk.OptionMenu(parent, variable, *program_names)
            selector.config(width=2)
            variable.trace('w', lambda v,a,b,p=proc.id,n=program_names,var=variable: self.set_program(p, var.get(), n))
            selector.pack(side="top", fill="both", expand=0)

        except:
            pass

    def create_bypass_button(self, frame, proc):
        var = tk.IntVar()
        button = tk.Checkbutton(frame, text = "Enabled", variable = var,
                 command=lambda v=var,p=proc.id: self.set_bypass(p, not bool(v.get())))
        button.pack(side="top", fill="both", expand=0)

def main():
    SushiController = sc.SushiController('192.168.1.136:51051')
    root = tk.Tk()
    app = App(SushiController, master=root)
    app.mainloop()

if __name__ == "__main__": main()
