import importlib
import DreamTalk.imports
importlib.reload(DreamTalk.imports)
from DreamTalk.imports import *

class Emergence(CustomObject):

    def __init__(self, shapes=None, **kwargs):
        self.shapes = shapes
        super().__init__()

    def specify_parts(self):
        self.spherical_field = SphericalField(invert=True)
        self.plain_effector = PlainEffector(fields=[self.spherical_field], scale=-1)
        self.spline_mask = SplineMask(*self.shapes, mode="union", axis="xz")
        self.circle = Circle(radius=3.46, color=RED, plane="xz", creation=True, stroke_width=1)
        self.cloner = Cloner(
            clones=[self.circle],
            effectors=[self.plain_effector],
            mode="honeycomb",
            honeycomb_form="spline",
            honeycomb_spline_form=self.spline_mask,
            honeycomb_step_size_width=3,
            honeycomb_step_size_height=3.464102,
            honeycomb_count_height=50,
            honeycomb_count_width=50,
            )
        self.parts += [self.spherical_field, self.plain_effector, self.spline_mask, self.circle, self.cloner]

if __name__ == "__main__":
    
    emergence = Emergence(shapes=[Circle(radius=30, color=WHITE, plane="xz")])