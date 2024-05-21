from manim import *
from manim_physics import *
import random

RED = "#FF644E"
BLUE = "#00a2ff"

class PoincareFlower(MovingCameraScene):
    GRAVITY = 0, -0  # Set gravity to 0 to create a zero-gravity environment
    
    def construct(self):
        # Create the main circle with radius 3
        main_circle = Circle(radius=3)
        #self.add(main_circle)

        # Create the overlay of small circles with a honeycomb arrangement
        uniform_circle_overlay = self.create_uniform_circle_overlay(main_circle, grid_size=0.4)
        circle_overlay = self.create_circle_overlay(main_circle, grid_size=0.4)

        # zoom in camera
        self.camera.frame.scale(0.1)
        self.add(uniform_circle_overlay)

        # animate camera zoom out while circles stroke width is set to 1.5
        stroke_width_animations = []
        for circle in uniform_circle_overlay:
            stroke_width_animation = circle.animate.set_stroke(width=1.5)
            stroke_width_animations.append(stroke_width_animation)


        self.play(
            self.camera.frame.animate.scale(10),
            *stroke_width_animations,
            run_time=3,
        )


        # Add the circle overlay to the scene
        self.play(ReplacementTransform(uniform_circle_overlay, circle_overlay), run_time=3)

        self.play(
            circle_overlay.animate.apply_function(
                self.poincare_transform
            ),
            run_time=3,
        )

        # Wait for the physics simulation to run
        #self.wait(5)

    def create_circle_overlay(self, mobject, grid_size=0.2):
        square_size_x = grid_size
        square_size_y = square_size_x * np.sqrt(3) / 2

        center_point = mobject.get_center()

        # Determine the width and height of the mobject
        width = mobject.width*2
        height = mobject.height*2

        # Calculate the number of circles in each dimension
        circles_x = int(width / square_size_x)
        circles_y = int(height / square_size_y)

        # Create a grid of circles in a honeycomb arrangement
        circles = VGroup()
        for i in range(circles_x + 1):
            for j in range(circles_y + 1):
                circle = Circle(radius=square_size_x, color=RED, stroke_width=1.5)
                circle.move_to(center_point + np.array([square_size_x * (i - circles_x / 2), square_size_y * (j - circles_y / 2), 0]))
                offset = square_size_x / 2 if j % 2 == 0 else 0
                circle.shift(offset * RIGHT)

                distance_from_center = np.linalg.norm(circle.get_center() - center_point)

                # Modify the circle's radius based on the distance from the center
                if distance_from_center > 1.5 and distance_from_center < 3.0:  # Within big circle radius to 1.5 times big circle radius
                    lerp_factor = (distance_from_center - 1.5) / (3.0 - 1.5)
                    new_radius = np.interp(lerp_factor, [0, 1], [square_size_x, square_size_x / 2])
                    circle.scale(new_radius / square_size_x/2)
                elif distance_from_center >= 3.0:  # Beyond 1.5 times big circle radius
                    circle.scale((square_size_x / 2) / square_size_x/2)


                # Check if the circle intersects with the object
                intersection = Intersection(mobject, circle)
                if True:#len(intersection) > 0:
                    circles.add(circle)

        return circles

    def create_uniform_circle_overlay(self, mobject, grid_size=0.2):
        square_size_x = grid_size
        square_size_y = square_size_x * np.sqrt(3) / 2

        center_point = mobject.get_center()

        # Determine the width and height of the mobject
        width = mobject.width*2
        height = mobject.height*2

        # Calculate the number of circles in each dimension
        circles_x = int(width / square_size_x)
        circles_y = int(height / square_size_y)

        # Create a grid of circles in a honeycomb arrangement
        circles = VGroup()
        for i in range(circles_x + 1):
            for j in range(circles_y + 1):
                circle = Circle(radius=square_size_x, color=RED, stroke_width=.5)
                circle.move_to(center_point + np.array([square_size_x * (i - circles_x / 2), square_size_y * (j - circles_y / 2), 0]))
                offset = square_size_x / 2 if j % 2 == 0 else 0
                circle.shift(offset * RIGHT)

                distance_from_center = np.linalg.norm(circle.get_center() - center_point)

                circle.scale(1/4)


                # Check if the circle intersects with the object
                intersection = Intersection(mobject, circle)
                if True:#len(intersection) > 0:
                    circles.add(circle)

        return circles

    def poincare_transform(self, point):
        x, y = point[:2]
        r, theta = np.sqrt(x**2 + y**2), np.arctan2(y, x)
        new_r = 2*np.tanh(r)
        return np.array([new_r * np.cos(theta), new_r * np.sin(theta), 0])