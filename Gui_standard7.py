import tkinter as tk
import numpy as np
import time
import const

class Gui(tk.Frame):

    def __init__(self, const, master):
        super().__init__(master)
        self.__const = const
        self.__make_canvas()
        self.__make_regions()
        self.__make_dots()
        self.__writeLilypondGraphic()

    def __euler_to_coords(self, i, j, k):
        x = int(
                (
                    (i + 0.5)
                  + j * 0.5
                  + k * 0.5
                ) * self.__const["EULERNET_DISTANCE"] * 1.3
            )
        y = int(
                (- k) * self.__const["EULERNET_DISTANCE"] * 1.3 * (0.5 / np.sqrt(3))
              + (self.__const["EULER_ROWS"] - j)
              * np.sqrt(3) * 0.5
              * self.__const["EULERNET_DISTANCE"] * 1.3
            )
        return (x, y)

    def __make_canvas(self):
        (w, h) = self.__euler_to_coords(
            self.__const["EULER_PEDALS"] + 3,
            0,
            0
        )
        w += self.__const["EULERNET_DISTANCE"]
        h += self.__const["EULERNET_DISTANCE"]
        self.__canvas = tk.Canvas(
            self,
            width=w,
            height=h,
            bg=self.__const["BACKGROUND_COLOR"]
        )
        self.__canvas.pack()

    def __make_regions(self):
        self.__regions = []
        for i in range(self.__const["EULER_PEDALS"]):
            (x0, y0) = self.__euler_to_coords(
                i-0.3,
                -0.5,
                0
            )

            (x3, y3) = self.__euler_to_coords(
                i-0.3,
                self.__const["EULER_ROWS"] - 0.25,
                0
            )
            (x4, y4) = self.__euler_to_coords(
                i+1.7,
                self.__const["EULER_ROWS"] - 0.25,
                0
            )

            (x7, y7) = self.__euler_to_coords(
                i+1.7,
                -0.5,
                0
            )
            self.__regions.append(
                self.__canvas.create_polygon(
                    x0, y0, x3, y3, x4, y4, x7, y7,
                    fill=self.__const["REGION_COLOR"],
                    width=
                        self.__const["REGION_BORDER_WIDTH"],
                    outline=
                        self.__const["REGION_BORDER_COLOR"],
                    state=tk.HIDDEN
                )
            )
        self.set_region(4)

    def __getNoteName(self, i, j, k):
        index_init = self.__const["NOTE_NAMES"].index(
            self.__const["INIT_NAME"]
        )
        i_init = self.__const["INIT_POS"][0]
        j_init = self.__const["INIT_POS"][1]
        k_init = self.__const["INIT_POS"][2]
        index = index_init - i_init + i - (j_init - j)*4 + (k_init - k)*2
        if (0 <= index < len(self.__const["NOTE_NAMES"])):
            return self.__const["NOTE_NAMES"][index]
        else:
            return "o"

    def __make_dots(self):
        self.__dots_small = []
        self.__dots_big = []
        self.__images = [] # preventing garbage
                           # collection
        self.__playing = []
        for k in range(self.__const["EULER_LAYERS"]):
            self.__playing.append([])
            for j in range(self.__const["EULER_ROWS"]):
                self.__playing[-1].append([])
                for i in range(self.__const["EULER_PEDALS"] + 3):
                    self.__playing[-1][-1].append(0)
        for k in range(self.__const["EULER_LAYERS"]):
            self.__dots_small.append([])
            self.__dots_big.append([])
            for j in range(self.__const["EULER_ROWS"]):
                self.__dots_small[-1].append([])
                self.__dots_big[-1].append([])
                for i in range(self.__const["EULER_PEDALS"] + 1):
                    name = self.__getNoteName(i, j, k)
                    if k == 0:
                        image = tk.PhotoImage(
                            file="figs/%s_small.png"%(name)
                        )
                    else:
                        image = tk.PhotoImage(
                            file="figs/%s_small_gray.png"%(name)
                        )
                    self.__images.append(image)
                    (x, y) = self.__euler_to_coords(
                        i, j, k
                    )
                    self.__dots_small[-1][-1].append(
                        self.__canvas.create_image(
                            x,
                            y,
                            image=image,
                            anchor=tk.CENTER
                        )
                    )
                    if k == 0:
                        image = tk.PhotoImage(
                            file="figs/%s_big.png"%(name)
                        )
                    else:
                        image = tk.PhotoImage(
                            file="figs/%s_big_gray.png"%(name)
                        )
                    self.__images.append(image)
                    (x, y) = self.__euler_to_coords(
                        i, j, k
                    )
                    self.__dots_big[-1][-1].append(
                        self.__canvas.create_image(
                            x,
                            y,
                            image=image,
                            anchor=tk.CENTER,
                            state=tk.HIDDEN
                        )
                    )



    def set_region(self, index):
        for i in range(self.__const["EULER_PEDALS"]):
            if i == index:
                value = tk.NORMAL
            else:
                value = tk.HIDDEN
            self.__canvas.itemconfigure(
                self.__regions[i],
                state=value
            )

    def note_on(self, position):
        [i, j, k] = [int(word) for word in position.split(",")]
        self.__playing[k][j][i] += 1
        if self.__playing[k][j][i] > 0:
            self.__canvas.itemconfigure(
                self.__dots_small[k][j][i],
                state=tk.HIDDEN
            )
            self.__canvas.itemconfigure(
                self.__dots_big[k][j][i],
                state=tk.NORMAL
            )

    def note_off(self, position):
        [i, j, k] = [int(word) for word in position.split(",")]
        self.__playing[k][j][i] -= 1
        if self.__playing[k][j][i] == 0:
            self.__canvas.itemconfigure(
                self.__dots_small[k][j][i],
                state=tk.NORMAL
            )
            self.__canvas.itemconfigure(
                self.__dots_big[k][j][i],
                state=tk.HIDDEN
            )

    def reset(self):
        for k in range(self.__const["EULER_LAYERS"]):
            for j in range(self.__const["EULER_ROWS"]):
                for i in range(self.__const["EULER_PEDAlS"] + 1):
                    self.__playing[k][j][i] = 0
                    self.__canvas.itemconfigure(
                        self.__dots_small[k][j][i],
                        state=tk.NORMAL
                    )
                    self.__canvas.itemconfigure(
                        self.__dots_big[k][j][i],
                        state=tk.HIDDEN
                    )
  
    def __writeLilypondGraphic(self):
        pedalsToPlot = range(8)
        columnsToPlot = []
        for p in pedalsToPlot:
            for c in [p, p + 1]:
                if c not in columnsToPlot:
                     columnsToPlot.append(c)
        shift = min(columnsToPlot)
        with open("/tmp/eulerizerplot.txt", "w") as f:
            f.write("\\version \"2.22.1\"\n")
            f.write("\\book {\n")
            f.write("\\markup {\n")
            scaling = 0.07
            pedalNames = [
                "\\fontsize #3 \\italic \\concat { \\raise #0.35 \\char ##x2212 \\char ##x2163 }",
                "\\fontsize #3 \\italic \\concat { \\raise #0.35 \\char ##x2212 \\char ##x2162 }",
                "\\fontsize #3 \\italic \\concat { \\raise #0.35 \\char ##x2212 \\char ##x2161 }",
                "\\fontsize #3 \\italic \\concat { \\raise #0.35 \\char ##x2212 \\char ##x2160 }",
                "\\fontsize #3 \\italic \\sans \"O\"",
                "\\fontsize #3 \\italic \\concat { \\raise #0.35 \"+\" \\char ##x2160 }",
                "\\fontsize #3 \\italic \\concat { \\raise #0.35 \"+\" \\char ##x2161 }",
                "\\fontsize #3 \\italic \\concat { \\raise #0.35 \"+\" \\char ##x2162 }",
            ]
            for k in range(self.__const["EULER_LAYERS"]):
                for j in range(self.__const["EULER_ROWS"]):
                    for i in columnsToPlot:
                         (x, y) = self.__euler_to_coords(i - shift, j, k)
                         (x, y) = (x*scaling, y*scaling)
                         notename = self.__getNoteName(i, j, k)
                         f.write("\\combine ")
                         if True:
                             if len(notename) == 1:
                                 notename = "\\fontsize #3 " + notename[0]
                             elif len(notename) == 2:
                                 if notename[1] == "#":
                                     notename = "\\fontsize #3 " + notename[0] + " \\fontsize #0.3 \\raise #1.2 \\sharp"
                                 elif notename[1] == "b":
                                     notename = "\\fontsize #3 " + notename[0] + " \\fontsize #0.5 \\raise #0.3 \\flat"
                         elif k == 1:
                             if len(notename) == 1:
                                 notename = "\\fontsize #1 " + notename[0]
                             elif len(notename) == 2:
                                 if notename[1] == "#":
                                     notename = "\\fontsize #0.5 " + notename[0] + " \\fontsize #0.05 \\raise #1.2 \\sharp"
                                 elif notename[1] == "b":
                                     notename = "\\fontsize #0.5 " + notename[0] + " \\fontsize #0.07 \\raise #0.3 \\flat"
                         f.write("\\translate #'(%f . %f) \\concat \\center-align { %s }"%(x, -y, notename))
            f.write("\n")                       
            for i in pedalsToPlot: 
                n = i - shift
                m = max(pedalsToPlot)
                (x0, y0) = self.__euler_to_coords(-0.3 + n, -0.3 - n * 0.1, 0)
                (x1, y1) = self.__euler_to_coords(-0.3 + n, self.__const["EULER_ROWS"] - 0.2 + (m - i) * 0.1, 0)
                (x2, y2) = self.__euler_to_coords(-0.3 + n + 1.9, self.__const["EULER_ROWS"] - 0.2 + (m - i) * 0.1, 0)
                (x3, y3) = self.__euler_to_coords(-0.3 + n + 1.9, -0.3 - n * 0.1, 0)
                (x0, y0) = (x0 * scaling, y0 * scaling)
                (x1, y1) = (x1 * scaling, y1 * scaling)
                (x2, y2) = (x2 * scaling, y2 * scaling)
                (x3, y3) = (x3 * scaling, y3 * scaling)
                f.write("\\combine ")
                f.write("\path #0.2 #'((moveto %f %f) (lineto %f %f) (lineto %f %f) (lineto %f %f) (lineto %f %f))\n"
                %(x0, -y0, x1, -y1, x2, -y2, x3, -y3, x0, -y0))
                (x, y) = self.__euler_to_coords(n, -0.8 - n * 0.1, 0)
                (x, y) = (x * scaling, y * scaling)
                pedalName = pedalNames[i]
                f.write("\\combine")
                f.write("\\translate #'(%f . %f) \\concat \\center-align { %s }"%(x, -y, pedalName))
            f.write(" \" \"\n")
            f.write("}\n")
            f.write("}\n")                         
                                  
