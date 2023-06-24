from typing import Callable, Optional, Tuple, Union
from customtkinter.windows.widgets.font import CTkFont
from customtkinter.windows.widgets.image import CTkImage
import numpy as np
import math
import customtkinter as ctk
from typing import *


class App(ctk.CTk):
    def __init__(self, fg_color: Optional[Union[str, Tuple[str, str]]] = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.title("Fun With Concrete")
        ctk.set_default_color_theme("blue")
        ctk.set_appearance_mode("dark")
        self.iconbitmap(r"images\towelie.ico")

        # Set up the tabs for the program
        TabHolder(self).pack()


class TabHolder(ctk.CTkTabview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Constants
        self.textFont = ("Consolas", 18)
        self.resFont = ("Consolas", 14)
        self.resTxtFont = ("Consolas", 14)
        self.barsizes_US = [3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 18]

        # Variables
        self.fcEntry = ctk.StringVar(value="4.5")
        self.wcEntry = ctk.StringVar(value="0.150")
        self.fyEntry = ctk.StringVar(value="60.0")
        self.MuEntry = ctk.StringVar(value="15.0")
        self.dEntry = ctk.StringVar(value="12.5")
        self.trialBEntry = ctk.StringVar(value="6")
        self.EcResult = ctk.StringVar()
        self.a1Result = ctk.StringVar()
        self.B1Result = ctk.StringVar()
        self.lResult = ctk.StringVar()
        self.frResult = ctk.StringVar()
        self.AsOptimalResult = ctk.StringVar()
        self.AsRequiredResult = ctk.StringVar()
        self.AsRequestedResult = ctk.StringVar()

        # Define the tabs for various features
        self.tab1 = self.add("Sectional Properties")
        self.tab2 = self.add("Optimal Bar Size/Spacing")

        # Build the tabs
        self.sectionPropertiesTab()
        self.optimalRebarTab()

    def sectionPropertiesTab(self):
        # Initialize the row and column counters
        r = 0
        c = 0

        # Concrete strength & weight entry
        ctk.CTkLabel(self.tab1, text="Enter Concrete Strength in ksi",
                     font=("Consolas", 18)).grid(row=r, column=c)
        c += 1
        ctk.CTkEntry(self.tab1, textvariable=self.fcEntry,
                     font=self.textFont).grid(row=r, column=c, columnspan=2)
        r += 1
        c = 0
        ctk.CTkLabel(self.tab1, text="Unit weight (kcf)",
                     font=("Consolas", 18)).grid(row=r, column=c)
        c += 1
        ctk.CTkEntry(self.tab1, textvariable=self.wcEntry,
                     font=self.textFont).grid(row=r, column=c, columnspan=2)
        r += 1
        c = 0

        # Calculate button
        ctk.CTkButton(self.tab1, width=300, height=50, font=(
            "Consolas", 20), text="Calculate", command=self.calcSectionProperties).grid(row=r, column=c, columnspan=3, sticky="NSEW")
        r += 1
        c = 0

        HorizLine(self.tab1, r, c, 3)
        r += 1

        ctk.CTkLabel(self.tab1, font=("Consolas", 20, "bold"),
                     text="Results").grid(row=r, column=c, columnspan=3, sticky="EW")
        r += 2

        # Output - Ec
        ctk.CTkLabel(self.tab1, font=self.resTxtFont,
                     text="Modulus of Elasticity, Ec = ").grid(row=r, column=c, sticky="E")
        c += 1
        ctk.CTkEntry(self.tab1, font=self.resFont, textvariable=self.EcResult,
                     state="readonly").grid(row=r, column=c, sticky="EW")
        c += 1
        ctk.CTkLabel(self.tab1, font=self.resTxtFont,
                     text="ksi").grid(row=r, column=c)
        r += 1
        c = 0

        # Output - a1
        ctk.CTkLabel(self.tab1, font=self.resTxtFont,
                     text="Stress block parameter a1 = ").grid(row=r, column=c, sticky="E")
        c += 1
        ctk.CTkEntry(self.tab1, font=self.resFont, textvariable=self.a1Result,
                     state="readonly").grid(row=r, column=c, sticky="EW")
        r += 1
        c = 0

        # Output - B1
        ctk.CTkLabel(self.tab1, font=self.resTxtFont,
                     text="Stress block parameter B1 = ").grid(row=r, column=c, sticky="E")
        c += 1
        ctk.CTkEntry(self.tab1, font=self.resFont, textvariable=self.B1Result,
                     state="readonly").grid(row=r, column=c, sticky="EW")
        r += 1
        c = 0

        # Output - lambda
        ctk.CTkLabel(self.tab1, font=self.resTxtFont,
                     text="Lightweight mod. factor lambda = ").grid(row=r, column=c, sticky="E")
        c += 1
        ctk.CTkEntry(self.tab1, font=self.resFont, textvariable=self.lResult,
                     state="readonly").grid(row=r, column=c, sticky="EW")
        r += 1
        c = 0

        # Output - fr
        ctk.CTkLabel(self.tab1, font=self.resTxtFont,
                     text="Modulus of Rupture, fr = ").grid(row=r, column=c, sticky="E")
        c += 1
        ctk.CTkEntry(self.tab1, font=self.resFont, textvariable=self.frResult,
                     state="readonly").grid(row=r, column=c, sticky="EW")
        c += 1
        ctk.CTkLabel(self.tab1, font=self.resTxtFont,
                     text="ksi").grid(row=r, column=c)

    def optimalRebarTab(self):
        # Initialize the row and column counters
        r = 0
        c = 0

        # Concrete strength & weight entry
        ctk.CTkLabel(self.tab2, text="Enter Concrete Strength in ksi",
                     font=("Consolas", 18)).grid(row=r, column=c)
        c += 1
        ctk.CTkEntry(self.tab2, textvariable=self.fcEntry,
                     font=self.textFont).grid(row=r, column=c, columnspan=2)
        r += 1
        c = 0
        ctk.CTkLabel(self.tab2, text="Unit weight (kcf)",
                     font=("Consolas", 18)).grid(row=r, column=c)
        c += 1
        ctk.CTkEntry(self.tab2, textvariable=self.wcEntry,
                     font=self.textFont).grid(row=r, column=c, columnspan=2)
        r += 1
        c = 0
        ctk.CTkLabel(self.tab2, text="Enter Rebar Strength in ksi",
                     font=("Consolas", 18)).grid(row=r, column=c)
        c += 1
        ctk.CTkEntry(self.tab2, textvariable=self.fyEntry,
                     font=self.textFont).grid(row=r, column=c, columnspan=2)
        r += 1
        c = 0
        ctk.CTkLabel(self.tab2, text="Ultimate Moment (kip*ft)",
                     font=("Consolas", 18)).grid(row=r, column=c)
        c += 1
        ctk.CTkEntry(self.tab2, textvariable=self.MuEntry,
                     font=self.textFont).grid(row=r, column=c, columnspan=2)
        r += 1
        c = 0
        ctk.CTkLabel(self.tab2, text="Depth to centroid of tension steel (in)",
                     font=("Consolas", 18)).grid(row=r, column=c)
        c += 1
        ctk.CTkEntry(self.tab2, textvariable=self.dEntry,
                     font=self.textFont).grid(row=r, column=c, columnspan=2)

        r += 1
        c = 0
        ctk.CTkLabel(self.tab2, text="Design for Bar Size",
                     font=("Consolas", 18)).grid(row=r, column=c)
        c += 1
        ctk.CTkEntry(self.tab2, textvariable=self.trialBEntry,
                     font=self.textFont).grid(row=r, column=c, columnspan=2)

        r += 1
        c = 0
        ctk.CTkLabel(self.tab2, text="Design for Spacing",
                     font=("Consolas", 18)).grid(row=r, column=c)
        c += 1
        self.trialsEntry = ctk.StringVar()
        self.trialsEntry.set("8.0")
        ctk.CTkEntry(self.tab2, textvariable=self.trialsEntry,
                     font=self.textFont).grid(row=r, column=c, columnspan=2)

        r += 1
        c = 0

        # Calculate button
        ctk.CTkButton(self.tab2, width=300, height=50, font=(
            "Consolas", 20), text="Calculate", command=self.calcOptimalRebar).grid(row=r, column=c, columnspan=3, sticky="NSEW")
        r += 1
        c = 0

        HorizLine(self.tab2, r, c, 3)
        r += 1

        ctk.CTkLabel(self.tab2, font=("Consolas", 20, "bold"),
                     text="Results").grid(row=r, column=c, columnspan=3, sticky="EW")
        r += 2

        # Output - As Optimal
        ctk.CTkLabel(self.tab2, font=self.resTxtFont,
                     text="Required Reinforcement").grid(row=r, column=c, sticky="EW")
        r += 1
        ctk.CTkEntry(self.tab2, font=self.resFont, textvariable=self.AsRequiredResult,
                     state="readonly").grid(row=r, column=c, columnspan=3, sticky="EW")

        r += 1
        c = 0
        # Output - As Provided
        ctk.CTkLabel(self.tab2, font=self.resTxtFont,
                     text="Optimal reinforcement").grid(row=r, column=c, sticky="E")
        r += 1
        self.AsOptimal1 = ctk.StringVar()
        ctk.CTkEntry(self.tab2, font=self.resFont, textvariable=self.AsOptimal1,
                     state="readonly").grid(row=r, column=c, columnspan=3, sticky="EW")
        r += 1
        self.AsOptimal2 = ctk.StringVar()
        ctk.CTkEntry(self.tab2, font=self.resFont, textvariable=self.AsOptimal2,
                     state="readonly").grid(row=r, column=c, columnspan=3, sticky="EW")
        r += 1
        self.AsOptimal3 = ctk.StringVar()
        ctk.CTkEntry(self.tab2, font=self.resFont, textvariable=self.AsOptimal3,
                     state="readonly").grid(row=r, column=c, columnspan=3, sticky="EW")
        r += 1
        self.AsOptimal4 = ctk.StringVar()
        ctk.CTkEntry(self.tab2, font=self.resFont, textvariable=self.AsOptimal4,
                     state="readonly").grid(row=r, column=c, columnspan=3, sticky="EW")
        r += 1
        c = 0
        # Output - As Provided
        ctk.CTkLabel(self.tab2, font=self.resTxtFont,
                     text="Requested reinforcement").grid(row=r, column=c, sticky="E")
        r += 1
        ctk.CTkEntry(self.tab2, font=self.resFont, textvariable=self.AsRequestedResult,
                     state="readonly").grid(row=r, column=c, columnspan=3, sticky="EW")

        r += 1
        c = 0

    def calcSectionProperties(self):
        _fc = float(self.fcEntry.get())
        _wc = float(self.wcEntry.get())
        self.EcResult.set("{}".format(calcEc(_fc, _wc)))
        self.a1Result.set("{:.2f}".format(calcA1(_fc)))
        self.B1Result.set("{:.2f}".format(calcB1(_fc)))
        self.lResult.set("{:.2f}".format(calcL(_wc)))
        self.frResult.set("{:.3f}".format(calcFr(_fc, calcL(_wc))))

    def calcOptimalRebar(self):
        _fc = float(self.fcEntry.get())  # ksi
        _fy = float(self.fyEntry.get())  # ksi
        _Mu = float(self.MuEntry.get()) * 12.  # kip*ft to kip*in
        _d = float(self.dEntry.get())  # inches
        _a1 = calcA1(_fc)
        _b1 = calcB1(_fc)
        _b = 12.  # inches; represents a unit width design
        _f = 0.9  # Resistance factor; tension controlled section assumed

        # I Mathcad'd a built expression for the values below.  It's basically solving the following:
        # Mu = f * Mn
        # f * Mn = 0.9 * T * (d - a / 2)
        # T = As * fy
        # Mu = 0.9 * As * fy * (d - a / 2)
        # As * fy = alpha1 * f'c * 12in * aa
        # aa = As * fy / (alpha1 * f'c * 12in)
        # Mu = 0.9 * As * fy * (d - (As * fy / (alpha1 * f'c * 12in)) / 2)
        # Then solved for As.  It was a 2nd order express, therefore the 2 results.

        _As1 = (math.sqrt((_fc**2 * _fy**2 * _a1**2 * _f**2 * _b**2 * _d**2) - (2 * _Mu *
                _fc * _fy**2 * _a1 * _f * _b)) + (_fc * _fy * _a1 * _f * _b * _d)) / (_fy**2 * _f)
        _As2 = (-1*math.sqrt((_fc**2 * _fy**2 * _a1**2 * _f**2 * _b**2 * _d**2) - (2 * _Mu *
                _fc * _fy**2 * _a1 * _f * _b)) + (_fc * _fy * _a1 * _f * _b * _d)) / (_fy**2 * _f)

        # Calculate the required steel area per unit width
        _AsRequired = min(_As1, _As2)

        # Initialize an empty array to hold bar size, num req'd, spacing, and total area, and score
        _results = np.zeros([len(self.barsizes_US), 5])

        for nb, bar in enumerate(self.barsizes_US):
            _abar = calcBarArea(bar)
            _nreq = ceil(_AsRequired / _abar, 1)
            _atot = _abar * _nreq
            _sp = floor(12. / (_nreq), 0.5) if _nreq != 1. else 6.
            _score = 1 / (_atot / _AsRequired)
            _results[nb, :] = [bar, _nreq, _sp, _atot, _score]

        # Return the top 4 most economical selections
        sorted_results = np.argsort(_results[:, -2])
        sorted_array = _results[sorted_results]

        outputStringArray = []
        for i in range(4):
            outputStringArray.append("#{} bars @ {:.1f}\" sp. = {:.2f} in2/ft ({:.2%} Efficient)".format(
                int(sorted_array[i, 0]), sorted_array[i, 2], sorted_array[i, 3], sorted_array[i, 4]))

        self.AsRequiredResult.set("{:.2f} in2/ft Required".format(_AsRequired))
        self.AsOptimal1.set(outputStringArray[0])
        self.AsOptimal2.set(outputStringArray[1])
        self.AsOptimal3.set(outputStringArray[2])
        self.AsOptimal4.set(outputStringArray[3])

        # # Oh yeah, check the requested
        # _asquest = calcBarArea(int(self.trialBEntry.get()))
        # _squest = float(self.trialsEntry.get())
        # _Asquest = _asquest / (_squest / 12)

        # _rbar = float(self.trialBEntry)
        # _rspa = float(self.trialsEntry)

        # _questString = "#{} bars @ {}\" spa. = {:.2f} in2/ft".format(
        #     _rbar, _rspa, _Asquest)
        # self.AsRequestedResult.set(_questString)

# Additional standalone functions


def floor(n, m):
    return n // m * m


def ceil(n, m):
    return (n // m + 1) * m


def calcBarArea(s):
    return math.pi/4 * (s / 8)**2


def calcEc(fc: float = None, wc: float = 0.150):
    _fc = fc if not None else 4.5
    return floor(120000. * (wc)**2 * (_fc)**(0.33), 10)


def calcB1(fc: float = None):
    _fc = fc if not None else 4.5
    if _fc <= 4.:
        return 0.85
    else:
        return max(0.65, 0.85 - 0.05 * (_fc - 4.))


def calcA1(fc: float = None):
    _fc = fc if not None else 4.5
    if _fc <= 10.:
        return 0.85
    else:
        return max(0.75, 0.85 - 0.02 * (_fc - 10.))


def calcL(wc: float = None):
    _wc = wc if not None else 0.150
    if _wc <= 0.100:
        return 0.75
    elif _wc < 0.135:
        return round(0.75 + 0.25 * (_wc - 0.100), 2)
    else:
        return 1.00


def calcFr(fc: float = None, lam: float = None):
    _fc = fc if not None else 4.5
    _lam = lam if not None else 1.0
    return floor(0.24 * _lam * math.sqrt(_fc), 0.005)


class AddSpace(ctk.CTkLabel):
    """
    This class will generate a blank space horizontally

    Args:
        ctk (_type_): _description_
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configure(text=" ")
        self.pack(fill="x")


class HorizLine(ctk.CTkFrame):
    """
    This class will generate a thin horizontal line.  Riveting.

    Args:
        ctk (_type_): _description_
    """

    def __init__(self, master: any, r, c, n, width: int = 200, height: int = 2, corner_radius: Optional[Union[int, str]] = None, border_width: Optional[Union[int, str]] = None, bg_color: Union[str, Tuple[str, str]] = "#dce4ee", fg_color: Optional[Union[str, Tuple[str, str]]] = None, border_color: Optional[Union[str, Tuple[str, str]]] = None, background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None, overwrite_preferred_drawing_method: Union[str, None] = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color,
                         border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.configure(fg_color="#1F6AA5",
                       border_color="#1F6AA5",
                       bg_color="#1F6AA5")
        self.grid(row=r, column=c, columnspan=n, sticky="EW")


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
