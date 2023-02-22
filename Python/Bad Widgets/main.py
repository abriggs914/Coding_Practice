import re
import subprocess
import tkinter

from time import sleep

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math

from tkinter_utility import *

import phone_number_guess
# import orbiting_date_picker
from utility import *


# gsm_showing_dae_picker = (True, False), 0


#	Class outlining a Game-State-Machine (GSM).
#	Version............1.1
#	Date........2022-06-30
#	Author....Avery Briggs
from test_suite import TestSuite


class GSM:

    def __init__(self, options, name=None, idx=None, max_cycles=None):
        """Game State Machine. Simulates state switches for an object.
        Required:   options     -   list of states.
        Optional:   name        -   GSM name
                    idx         -   starting index for a state
                    max_cycles  -   maximum number of cycles allowed. (Think generators)"""
        if idx is None:
            idx = 0
        if not isinstance(idx, int) or (0 < idx < len(options)):
            raise TypeError("Error param 'idx' needs to be an integer corresponding to a list index.")

        if not isinstance(options, list) and not isinstance(options, tuple):
            raise TypeError("Error param 'options' needs to be an ordered iterable object. (supported: list, tuple)")
        if len(options) == 0:
            raise ValueError("Error param 'options' needs to have at least 1 element.")
        if max_cycles == 0:
            raise ValueError("Error you can not create a GSM that does not have at least 1 cycle")

        self.name = name
        self.idx = idx
        self.options = options
        self.cycles = 0

        self.max_cycles = -1
        if max_cycles is not None:
            if isinstance(max_cycles, bool) and max_cycles:
                # use this for 1 iteration
                self.max_cycles = 1
            elif isinstance(max_cycles, int):
                self.max_cycles = max_cycles

    def __iter__(self):
        """Generator of upcoming states. ONLY 1 CYCLE"""
        # return self.options[:self.idx] + self.options[self.idx:]
        for op in self.queue():
            yield op

    def __next__(self):
        """Call this like a generator would. Simulates 'walking' states and checks against max_cycles."""
        self.idx += 1
        if self.idx >= len(self):
            self.cycles += 1
            self.restart()
            if not self.can_recycle():
                raise StopIteration(f"Error max cycles have been reached for this GSM object. cycles={self.cycles}")
            # if self.max_cycles >= 0:
            #     if self.cycles >= self.max_cycles:
            #         raise StopIteration(f"Error max cycles have been reached for this GSM object. cycles={self.cycles}")
        return self.state()

    def __len__(self):
        """Return length of states list"""
        return len(self.options)

    def queue(self):
        """List of states in pending order, beginning with the current."""
        rest = self.options[self.idx:]
        if self.can_recycle():
            rest += self.options[:self.idx]
        return rest

    def opposite(self, round_up=False):
        """Viewing options cyclically, return the state opposite to the current. Use round_up to handle odd length state lists"""
        off = 0 if not round_up else len(self) % 2
        return self.options[(self.idx + ((len(self) // 2) + off)) % len(self)]

    def state(self, idx=None):
        """Return the state at a given index. If none given, defaults to own index."""
        return self.options[self.idx] if idx is None else self.options[idx]

    def peek(self, n_ahead=1):
        """Peek ahead to the nth state. Default next state."""
        return self.state((self.idx + n_ahead) % len(self))

    def add_state(self, state, idx=None):
        """Add a state. By default, appended, but can be altered using idx param."""
        if idx is None:
            if isinstance(self.options, list):
                self.options.append(state)
            else:
                self.options = (*self.options, state)
        else:
            if isinstance(self.options, list):
                self.options.insert(idx, state)
            else:
                self.options = (*self.options[:idx], state, self.options[idx:])

    def remove_state(self, state):
        """Remove a state. Beware ValueError"""
        if isinstance(self.options, list):
            self.options.remove(state)
        else:
            temp = list(self.options)
            temp.remove(state)
            self.options = tuple(temp)

    def restart(self):
        """Restart from idx=0, same cycle."""
        self.idx = 0

    def reset(self):
        """Reset from index=0 and cycle=0."""
        self.restart()
        self.cycles = 0

    def can_recycle(self):
        """Can this GSM cycle again or will it raise a StopIteration."""
        return self.max_cycles < 0 or self.cycles < self.max_cycles - 1

    def __repr__(self):
        a = f" name={self.name}," if self.name is not None else ""
        b = f", cycle_num/max_cycles={self.cycles} / {self.max_cycles}" if self.max_cycles >= 0 else ""
        r = (self.cycles * len(self)) + self.idx
        f = (self.max_cycles * len(self)) if len(self) != 0 and self.max_cycles != 0 else 1
        p = ("%.2f" % ((100 * r) / f)) + " %"
        c = f", #state_idx/ttl_states={r} / {f} = {p}" if b else ""
        return f"<GSM{a} state={self.state()}, options={self.queue()}{b}{c}>"


class BooleanGSM(GSM):

    # Binary switch

    def __init__(self, name=None, idx=None, max_cycles=None, t_first=True):
        super().__init__(options=[True, False] if t_first else [False, True], name=name, idx=idx, max_cycles=max_cycles)


class YesNoCancelGSM(GSM):

    # Triple state switch

    def __init__(self, name=None, idx=None, max_cycles=None):
        super().__init__(options=["Yes", "No", "Cancel"], name=name, idx=idx, max_cycles=max_cycles)


def calc_bounds(center, width, height=None):
    assert (isinstance(center, list) or isinstance(center, tuple)) and len(center) == 2 and all([isnumber(x) for x in center]), f"Error param 'center' must be a tuple or list representing center coordinates (x, y). Got: {center}"
    assert isnumber(width), f"Error param 'width' must be a number. Got: {width}"
    if height is not None:
        assert isnumber(height), f"Error param 'height' if not omitted, must be a number. Got: {height}"
    w = width / 2
    h = w if height is None else (height / 2)
    return (
        center[0] - w,
        center[1] - h,
        center[0] + w,
        center[1] + h
    )


# def get_speaker_output_volume():
#     """
#     Get the current speaker output volume from 0 to 100.
#
#     Note that the speakers can have a non-zero volume but be muted, in which
#     case we return 0 for simplicity.
#
#     Note: Only runs on macOS.
#     """
#     cmd = "osascript -e 'get volume settings'"
#     process = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
#     output = process.stdout.strip().decode('ascii')
#
#     print(f"{output=}")
#
#     pattern = re.compile(r"output volume:(\d+), input volume:(\d+), "
#                          r"alert volume:(\d+), output muted:(true|false)")
#     volume, _, _, muted = pattern.match(output).groups()
#
#     volume = int(volume)
#     muted = (muted == 'true')
#
#     return 0 if muted else volume


class DecreasingVolumeControl(tkinter.Frame):

    def __init__(self, master, auto_grid=False, auto_pack=False, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.auto_grid = auto_grid
        self.auto_pack = auto_pack

        if self.auto_grid and self.auto_pack:
            raise ValueError("Error params 'self.auto_grid' and 'self.auto_pack' cannot both be true")

        self.audio_controller = AudioController()

        self.frame_controls = tkinter.Frame(self)

        self.tv_scale = tkinter.IntVar(self, value=self.audio_controller.volume)
        self.scale_volume = ttk.Scale(self.frame_controls, cursor="crosshair", variable=self.tv_scale, from_=0, to=100)

        self.tv_label = tkinter.StringVar(self, value=self.gen_label())
        self.label = tkinter.Label(self, textvariable=self.tv_label)

        self.tv_button_decrease, self.button_decrease = button_factory(
            self.frame_controls,
            tv_btn="-"
            # ,
            # kwargs_btn={
            #     "command": self.click_decrease_volume
            # }
        )
        self.tv_button_increase, self.button_increase = button_factory(
            self.frame_controls,
            tv_btn="+"
            # ,
            # kwargs_btn={
            #     "command": self.click_increase_volume
            # }
        )

        self.button_decrease.bind("<Button-1>", self.click_decrease_volume)
        self.button_increase.bind("<Button-1>", self.click_increase_volume)

        if self.auto_grid:
            self.grid()
            self.label.grid(row=0, column=0, columnspan=3, rowspan=1)
            self.frame_controls.grid(row=1, column=0, columnspan=3, rowspan=1)
            self.button_decrease.grid(row=0, column=0, columnspan=1, rowspan=1)
            self.scale_volume.grid(row=0, column=1, columnspan=1, rowspan=1)
            self.button_increase.grid(row=0, column=2, columnspan=1, rowspan=1)
        elif self.auto_pack:
            self.pack()
            self.label.pack()
            self.frame_controls.pack()
            self.button_decrease.pack(side=tkinter.LEFT)
            self.scale_volume.pack(side=tkinter.LEFT)
            self.button_increase.pack(side=tkinter.LEFT)

    def get_objects(self):
        """
        frame
        label
        frame_controls
        (
            button_decrease
            scale_volume
            button_increase
        )
        """
        return \
            self,\
            self.label,\
            self.frame_controls, \
            (
                self.button_decrease,
                self.scale_volume,
                self.button_increase
            )

    def gen_label(self):
        return f"Volume\t\t{self.tv_scale.get()}"

    def click_decrease_volume(self, event):
        print(f"click_decrease_volume")

    def click_increase_volume(self, event):
        print(f"click_increase_volume")


def test_decreasing_volume():

    win = tkinter.Tk()
    width = 600
    ratio = 16 / 9
    win.geometry(f"{width}x{int(width / ratio)}")
    win.title("Decreasing Volume")

    dvc_00 = DecreasingVolumeControl(win)
    dvc_00_frame,\
    dvc_00_label,\
    dvc_00_frame_controls,\
    dvc_00_control_data=\
        dvc_00.get_objects()

    print(f"{dvc_00=}\n{dvc_00_frame=}\n{dvc_00_label=}\n{dvc_00_frame_controls=}\n{dvc_00_control_data=}")

    dvc_00_button_decrease,\
    dvc_00_scale_colume,\
    dvc_00_button_increase=\
        dvc_00_control_data

    dvc_00.pack()
    dvc_00_frame.pack()
    dvc_00_label.pack()
    dvc_00_frame_controls.pack()
    dvc_00_button_decrease.pack(side=tkinter.LEFT)
    dvc_00_scale_colume.pack(side=tkinter.LEFT)
    dvc_00_button_increase.pack(side=tkinter.LEFT)

    # dvc_10 = DecreasingVolumeControl(win, auto_grid=True)
    # # dvc_10_frame,\
    # # dvc_10_label,\
    # # dvc_10_frame_controls,\
    # # *dvc_10_control_data=\
    # #     dvc_10.get_objects()
    #
    # dvc_01 = DecreasingVolumeControl(win, auto_pack=True)
    # # dvc_01_frame,\
    # # dvc_01_label,\
    # # dvc_01_frame_controls,\
    # # *dvc_01_control_data=\
    # #     dvc_01.get_objects()

    win.mainloop()


class AudioController:
    def __init__(self):
        # self.process_name = process_name
        self.volume = self.process_volume()

    def mute(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process:
                interface.SetMute(1, None)
                print(session.Process.name(), "has been muted.")  # debug

    def unmute(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process:
                interface.SetMute(0, None)
                print(session.Process.name(), "has been unmuted.")  # debug

    def standardize_decibels(self, decibels):
        # print(f"{decibels=}, {-96 - decibels=}, {100/-96=}, {(-96 - decibels) * 100 / -96=}")
        a = decibels / -96
        b = 1 - a
        c = 100 * b
        print(f"{decibels=}, {a=}, {b=}, {c=}")
        return (1 - (decibels / -96)) * 100

    def process_volume(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        # Get current volume
        currentVolumeDb = volume.GetMasterVolumeLevel()
        # -96.0 -- 0
        print(f"{currentVolumeDb=}, {type(currentVolumeDb)=}")
        return self.standardize_decibels(currentVolumeDb)

        # sessions = AudioUtilities.GetAllSessions()
        #
        # speakers = AudioUtilities.GetSpeakers()
        # Speaker_face = speakers.SimpleAudioVolume
        #
        # vol = 0
        # for session in sessions:
        #     interface = session.SimpleAudioVolume
        #     if session.Process or 1:
        #         print("Volume:", interface.GetMasterVolume())  # debug
        #         # return interface.GetMasterVolume()
        #         vol = max(vol, interface.GetMasterVolume())
        # return vol * 100

    def set_volume(self, decibels):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process:
                # only set volume in the range 0.0 to 1.0
                self.volume = min(1.0, max(0.0, decibels))
                interface.SetMasterVolume(self.volume, None)
                print("Volume set to", self.volume)  # debug

    def decrease_volume(self, decibels):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process:
                # 0.0 is the min value, reduce by decibels
                self.volume = max(0.0, self.volume - decibels)
                interface.SetMasterVolume(self.volume, None)
                print("Volume reduced to", self.volume)  # debug

    def increase_volume(self, decibels):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process:
                # 1.0 is the max value, raise by decibels
                self.volume = min(1.0, self.volume + decibels)
                interface.SetMasterVolume(self.volume, None)
                print("Volume raised to", self.volume)  # debug


def test_volume():
    # class AudioController:
    #     def __init__(self):
    #         # self.process_name = process_name
    #         self.process_volume()
    #
    #     def mute(self):
    #         session = AudioUtilities.GetSpeakers()
    #         interface = session.SimpleAudioVolume
    #         if session.Process:
    #             interface.SetMute(1, None)
    #             print("Speaker have been muted.")  # debug
    #
    #         # sessions = AudioUtilities.GetAllSessions()
    #         # for session in sessions:
    #         #     interface = session.SimpleAudioVolume
    #         #     if session.Process and session.Process.name() == self.process_name:
    #         #         interface.SetMute(1, None)
    #         #         print(self.process_name, "has been muted.")  # debug
    #
    #     def unmute(self):
    #         session = AudioUtilities.GetSpeakers()
    #         interface = session.SimpleAudioVolume
    #         if session.Process:
    #             interface.SetMute(0, None)
    #             print("Speaker have been unmuted.")  # debug
    #
    #         # sessions = AudioUtilities.GetAllSessions()
    #         # for session in sessions:
    #         #     interface = session.SimpleAudioVolume
    #         #     if session.Process and session.Process.name() == self.process_name:
    #         #         interface.SetMute(0, None)
    #         #         print(self.process_name, "has been unmuted.")  # debug
    #
    #     def process_volume(self):
    #         # sessions = AudioUtilities.GetAllSessions()
    #         devices = AudioUtilities.GetSpeakers()
    #         interface = devices.Activate(
    #             IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    #         volume = cast(interface, POINTER(IAudioEndpointVolume))
    #         return volume.GetMasterVolumeLevel()
    #
    #         # for session in sessions:
    #         #     interface = session.SimpleAudioVolume
    #         #     if session.Process and session.Process.name() == self.process_name:
    #         #         print("Volume:", interface.GetMasterVolume())  # debug
    #         #         return interface.GetMasterVolume()
    #
    #     def set_volume(self, decibels):
    #         # session = AudioUtilities.GetSpeakers()
    #         # print(f"{session=}, {type(session)=}, {dir(session)=}")
    #         # for i, d in enumerate(dir(session)):
    #         #     print(f"\t{i=}\t{d=}\t{getattr(session, d, 'N/A')=}")
    #         # interface = session.SimpleAudioVolume
    #
    #
    #         session = AudioUtilities.GetSpeakers()
    #         print(f"1 - {session=}\n\t{type(session)=}\n\t{dir(session)=}")
    #         for i, d in enumerate(dir(session)):
    #             print(f"1.5 - \t{i=}\t\t{d=}\t\t{getattr(session, d, 'N/A')=}")
    #         sessions = AudioUtilities.GetAllSessions()
    #         print(f"2 - {sessions=}\n\t{type(sessions)=}\n\t{dir(sessions)=}\n\n###\n")
    #         # for i, d in enumerate(dir(sessions)):
    #         #     print(f"\t{i=}\t\t{d=}\t\t{getattr(sessions, d, 'N/A')=}")
    #         for session in sessions:
    #             interface = session.SimpleAudioVolume
    #             print(f"\t3 - {session=}\n\t\t{type(session)=}\n\t\t{dir(session)=}")
    #             for i, d in enumerate(dir(session)):
    #                 print(f"3.5 - \t{i=}\t\t{d=}\t\t{getattr(session, d, 'N/A')=}")
    #             # print(f"{session=}\n{interface=}")
    #             if session.Process:
    #                 print(f"\t\t{session.Process.name()=}")
    #             else:
    #                 print(f"ELSE A")
    #             # if session.Process and session.Process.name() == self.process_name:
    #             #     # only set volume in the range 0.0 to 1.0
    #             #     self.volume = min(1.0, max(0.0, decibels))
    #             #     interface.SetMasterVolume(self.volume, None)
    #             #     print("Volume set to", self.volume)  # debug
    #
    #
    #         # if session.Process:
    #         self.volume = min(1.0, max(0.0, decibels))
    #         devices = AudioUtilities.GetSpeakers()
    #         interface = devices.Activate(
    #             IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    #         interface.SetMasterVolume(self.volume, None)
    #         print("Volume set to", self.volume)  # debug
    #
    #         # sessions = AudioUtilities.GetAllSessions()
    #         # for session in sessions:
    #         #     interface = session.SimpleAudioVolume
    #         #     if session.Process and session.Process.name() == self.process_name:
    #         #         # only set volume in the range 0.0 to 1.0
    #         #         self.volume = min(1.0, max(0.0, decibels))
    #         #         interface.SetMasterVolume(self.volume, None)
    #         #         print("Volume set to", self.volume)  # debug
    #
    #     def decrease_volume(self, decibels):
    #         # session = AudioUtilities.GetSpeakers()
    #         # interface = session.SimpleAudioVolume
    #         # if session.Process:
    #         self.volume = max(0.0, self.volume - decibels)
    #         interface.SetMasterVolume(self.volume, None)
    #         print("Volume reduced to", self.volume)  # debug
    #
    #         # sessions = AudioUtilities.GetAllSessions()
    #         # for session in sessions:
    #         #     interface = session.SimpleAudioVolume
    #         #     if session.Process and session.Process.name() == self.process_name:
    #         #         # 0.0 is the min value, reduce by decibels
    #         #         self.volume = max(0.0, self.volume - decibels)
    #         #         interface.SetMasterVolume(self.volume, None)
    #         #         print("Volume reduced to", self.volume)  # debug
    #
    #     def increase_volume(self, decibels):
    #
    #         # session = AudioUtilities.GetSpeakers()
    #         # interface = session.SimpleAudioVolume
    #         # if session.Process:
    #         self.volume = min(1.0, self.volume + decibels)
    #         interface.SetMasterVolume(self.volume, None)
    #         print("Volume raised to", self.volume)  # debug
    #
    #         # sessions = AudioUtilities.GetAllSessions()
    #         # for session in sessions:
    #         #     interface = session.SimpleAudioVolume
    #         #     if session.Process and session.Process.name() == self.process_name:
    #         #         # 1.0 is the max value, raise by decibels
    #         #         self.volume = min(1.0, self.volume + decibels)
    #         #         interface.SetMasterVolume(self.volume, None)
    #         #         print("Volume raised to", self.volume)  # debug
    #
    # def main():
    #     audio_controller = AudioController()
    #     audio_controller.set_volume(1.0)
    #     audio_controller.mute()
    #     audio_controller.decrease_volume(0.25)
    #     audio_controller.increase_volume(0.05)
    #     audio_controller.unmute()
    #
    # main()

    def main():
        audio_controller = AudioController()
        audio_controller.set_volume(1.0)
        sleep(1.5)
        audio_controller.mute()
        sleep(1.5)
        audio_controller.decrease_volume(0.25)
        sleep(1.5)
        audio_controller.increase_volume(0.05)
        sleep(1.5)
        audio_controller.unmute()
        sleep(1.5)

    # if __name__ == "__main__":
    #     main()


    # main()

    # Get default audio device using PyCAW
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # Get current volume
    currentVolumeDb = volume.GetMasterVolumeLevel()
    # -96.0 -- 0
    print(f"{currentVolumeDb=}, {type(currentVolumeDb)=}")
    # volume.SetMasterVolumeLevel(currentVolumeDb - 6.0, None)


class HexCircles(tkinter.Canvas):
    def __init__(
            self,
            master,
            radius_in,
            width=600,
            height=600,
            pitch=None,
            colour_circles="#000031",
            *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.radius = radius_in

        self.width = self.height = max(width, height)
        self.configure(width=self.width, height=self.height)
        self.pitch = pitch
        if pitch is not None:
            width = height = (2 * pitch) + ((2 * radius_in) + 1)
            print(f"Width adjusted to {self.width} -> {width}.\nHeight adjusted to {self.height} -> {height}.\nBecause Pitch was passed {pitch}.")
        else:
            # self.pitch = (self.width - ((2 * self.radius) + 1)) / 2
            # self.pitch = ((2 * self.width) - self.radius) / 3
            # self.pitch = (self.width - self.radius) / (self.radius + 1)
            self.pitch = self.width / ((2 * self.radius) + 1)
            print(f"Pitch calculated to be {self.pitch}.")

        self.colour_circles = colour_circles

        self.cw = 2
        self.gw = 2
        self.mt = 100
        self.ct = 0

        print(f"{self.width=}\n{self.height=}\n{self.pitch=}")
        self.circles = self.init_circles()
        self.animate()

    def animate(self):
        # print(f"animate # {self.ct}")
        if self.ct == self.mt:
            self.gw *= -1
            self.ct = 0
            # print(f"flip!")
        for k, v in self.circles.items():
            tag = v["tag"]
            dims = v["dims"]
            # iw = self.itemcget(v, "width")
            # ih = self.itemcget(v, "height")
            # x = self.itemcget(v, "x1")
            # y = self.itemcget(v, "y1")
            # self.itemconfigure(v, width=iw + 2, height=ih + 2)
            # self.moveto(v, x - 1, y - 1)
            x1, y1, x2, y2 = dims
            x1 -= self.gw
            y1 -= self.gw
            x2 += self.gw
            y2 += self.gw
            self.coords(tag, x1, y1, x2, y2)
            self.circles[k]["dims"] = (x1, y1, x2, y2)
        self.ct += 1
        self.after(60, self.animate)

    def init_circles(self):
        p = self.pitch
        w = self.width
        r = self.radius

        h = self.cw
        d = (2 * r) + 1
        o = (d - (r + 1)) / 2

        circles = {}

        for i in range(d):
            # ro =
            for j in range(d):
                x1, y1, x2, y2 = \
                    (p / 2) + (i * p) - h,\
                    (p / 2) + (j * p) - h,\
                    (p / 2) + (i * p) + h,\
                    (p / 2) + (j * p) + h
                print(f"\t{x1=}, {y1=}, {x2=}, {y2=}")
                mii, mai, mij, maj = o - 1, d - o, o - 1, d - o
                if any([
                    (mii < i < mai),
                    (mij < j < maj)
                ]):
                    circles[(i, j)] = {
                        "tag": self.create_oval(
                        x1, y1, x2, y2,
                        fill="",
                        outline=self.colour_circles,
                        width=2
                        ),
                        "dims": (x1, y1, x2, y2)
                    }
                # else:
                #     circles[(i, j)] = self.create_oval(
                #         x1, y1, x2, y2,
                #         fill="",
                #         outline="#0000ff",
                #         width=2
                #     )
        return circles


def test_hexagon_circles():
    win = tkinter.Tk()
    w, h = 700, 700
    win.geometry(f"{w}x{h}")

    colour_background = "#de9d5b"
    radius = 6

    frame = tkinter.Frame(win)
    hc = HexCircles(frame, radius_in=radius, background=colour_background)

    hc.pack(anchor=tkinter.CENTER, expand=True)
    frame.pack(anchor=tkinter.CENTER, expand=True)

    win.mainloop()


if __name__ == '__main__':
    # phone_number_guess.main()
    # orbiting_date_picker.main()
    # gsma = GSM(options=list(range(100)), name="GSM3")
    # gsm1 = GSM(options=list(range(100)))
    # gsm2 = BooleanGSM()
    # gsm3 = YesNoCancelGSM()
    # gsm4 = YesNoCancelGSM(max_cycles=True)
    #
    # to_print = [
    #     gsm3.opposite(round_up=True),
    #     gsm2.add_state("There"),
    #     gsm2.__next__(),
    #     gsm4.__next__(),
    #     gsm4.__next__(),
    #     gsm4.can_recycle(),
    #     gsm4.__next__()
    # ]
    #
    # for i, test in enumerate(to_print):
    #     print(f"i: {i}, test=<{test}>")

    # print(f"res: {calc_bounds((0, 0), 10)}")
    # print(f"res: {calc_bounds((0, 0), 10, 20)}")
    #
    # ts = TestSuite(test_func=calc_bounds)
    # # ts.set_func(calc_bounds)
    # ts.add_test("test1", [[(0, 0), 10], (-5, -5, 5, 5)])
    # ts.add_test("test2", [[(0, 0), 10, 20], (-5, -10, 5, 10)])
    # ts.add_test("test3", [[(None, 0), 10, 20], AssertionError])
    # ts.execute()

    # test_volume()
    # test_decreasing_volume()

    test_hexagon_circles()