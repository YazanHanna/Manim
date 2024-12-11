from manim import *

class TrapRule(Scene):
    def construct(self):
        def func(x):
            return 0.05 * x**3 - 0.55 * x**2 + x + 7

        axes = Axes(
            x_range=[0, 10, 1], 
            y_range=[0, 20, 5], 
            axis_config={"color": BLUE}
        )

        graph = axes.plot(func, color=RED)

        title = MathTex("Trapezoidal \\ Rule", font_size=64, color=WHITE).to_edge(UP)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))
        self.play(FadeOut(title))

        self.play(Create(axes))
        self.play(Create(graph))

        # Show the function and step-by-step integration
        func_text = MathTex("f(x) = 0.05x^3 - 0.55x^2 + x + 7", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(func_text))
        area_text = MathTex(r"\text{Area under the curve} = \int_{0}^{10} (0.05x^3 - 0.55x^2 + x + 7) \,dx", font_size=36, color=WHITE).next_to(func_text, DOWN)
        self.play(Write(area_text))

        integral_func_text = MathTex(
            r"= \left[\frac{0.05}{4}x^4 - \frac{0.55}{3}x^3 + \frac{1}{2}x^2 + 7x \right]_0^{10}", font_size=36, color=WHITE
        ).next_to(area_text, DOWN)
        self.play(Write(integral_func_text))

        integral_value_text = MathTex(
            r"= \left[\frac{0.05}{4}(10)^4 - \frac{0.55}{3}(10)^3 + \frac{1}{2}(10)^2 + 7(10) \right] - \left[0 \right]", font_size=36, color=WHITE
        ).next_to(integral_func_text, DOWN)
        self.play(Write(integral_value_text))

        integral_value = (0.05/4 * 10**4 - 0.55/3 * 10**3 + 0.5 * 10**2 + 7 * 10) - (0.05/4 * 0**4 - 0.55/3 * 0**3 + 0.5 * 0**2 + 7 * 0)
        final_value_text = MathTex(f"= {integral_value:.2f}", font_size=36, color=WHITE).next_to(integral_value_text, DOWN)
        self.play(Write(final_value_text))
        self.wait()
        self.play(*[FadeOut(mob) for mob in self.mobjects if mob != axes and mob != graph and mob != final_value_text])
        self.play(final_value_text.animate.move_to(axes.c2p(5, 2)))


        # Show the Trapezoidal rule formula
        formula = MathTex(
            r"\frac{\Delta x}{2} \left[ y_1 + y_n + 2(y_2 + y_3 + \ldots + y_{n-1}) \right]", font_size=24
        ).to_edge(UP)
        self.play(Write(formula))
        self.wait()

        def create_trapezoids(delta_x):
            trapezoids = VGroup()
            x_values = np.arange(0, 10, delta_x)
            for x in x_values:
                x_next = x + delta_x
                trapezoid = Polygon(
                    axes.c2p(x, 0), axes.c2p(x, func(x)),
                    axes.c2p(x_next, func(x_next)), axes.c2p(x_next, 0),
                    fill_color=BLUE, fill_opacity=0.5, stroke_color=WHITE
                )
                trapezoids.add(trapezoid)
            return trapezoids

        measure_line = Line(axes.c2p(0, 0), axes.c2p(10, 0), color=PURPLE).shift(DOWN * 0.5)
        delta_x_label = MathTex("\\Delta x = 10", font_size=36, color=WHITE).next_to(measure_line, DOWN*0.2)
        self.play(Create(measure_line), Write(delta_x_label))
        self.wait()

        # Trapezoid visualization for Δx = 10
        trapezoids_10 = create_trapezoids(10)
        self.play(Create(trapezoids_10), run_time=4)
        self.wait()

        # Show y1 and y10 on the graph and their values
        y1 = func(0)
        y10 = func(10)
        y1_dot = Dot(axes.c2p(0, y1), color=GREEN)
        y10_dot = Dot(axes.c2p(10, y10), color=GREEN)
        y1_label = MathTex(f"y_1 = {y1:.0f}", font_size=20, color=WHITE).next_to(y1_dot, UP+RIGHT)
        y10_label = MathTex(r"y_{10} = ", f"{y10:.0f}", font_size=20, color=WHITE).next_to(y10_dot, UP)
        self.play(FadeIn(y1_dot), FadeIn(y10_dot), Write(y1_label), Write(y10_label))
        self.wait()

        # Show Trapezoidal rule formula for Δx = 10 and animate the values
        trap_formula_sub_10 = MathTex( r"\frac{10}{2} \left[ \,", r" y_1", r" +", r" y_{10}", r"\, \right]", font_size=20, color=WHITE ).next_to(formula, DOWN)
        self.play(Write(trap_formula_sub_10))
        self.wait()


        # Create texts for the numerical parts
        y1_value_text = MathTex(f"{y1:.0f}", font_size=15, color=WHITE)
        y10_value_text = MathTex(f"{y10:.0f}", font_size=15, color=WHITE)

        # Position the numerical parts at the initial positions
        y1_value_text.move_to(y1_label.get_part_by_tex(f"{y1:.0f}").get_center())
        y10_value_text.move_to(y10_label.get_part_by_tex(f"{y10:.0f}").get_center())

        # Animate the numerical parts moving to the respective positions in the formula and Replace y_1 and y_{10} in the formula with the respective values
        self.play(y1_value_text.animate.move_to(trap_formula_sub_10[1].get_center()))
        self.play(Transform(trap_formula_sub_10.get_part_by_tex("y_1"), y1_value_text))

        self.play(y10_value_text.animate.move_to(trap_formula_sub_10[3].get_center()))
        self.play(Transform(trap_formula_sub_10.get_part_by_tex("y_{10}"), y10_value_text))

        self.wait()

        trap_area_10 = (y1 + y10) * 10 / 2
        trap_area_10_Text = MathTex(f"= {trap_area_10:.2f}", font_size=20)
        self.play(Write(trap_area_10_Text.next_to(trap_formula_sub_10, RIGHT)))
        self.wait()

        # Calculate the percent error
        percent_error_10 = ((trap_area_10 - integral_value) / integral_value) * 100

        # Percent error text
        percent_error_text_10 = MathTex(
            r"\text{Percent Error} = \left( \frac{\text{trap\_area\_10} - \text{integral\_value}}{\text{integral\_value}} \right) \times 100\%", font_size=16, color=WHITE
        ).next_to(trap_formula_sub_10, DOWN)

        # Percent error text with substituted values
        percent_error_equation_10 = MathTex(
            r"\text{Percent Error} = \left( \frac{" + f"{trap_area_10:.2f} - {integral_value:.2f}" + r"}{" + f"{integral_value:.2f}" + r"} \right) \times 100\%", font_size=16, color=WHITE
        ).next_to(percent_error_text_10, DOWN)

        # Percent error value
        percent_error_value_10 = MathTex(
            f"= {percent_error_10:.2f}\%", font_size=16, color=WHITE
        ).next_to(percent_error_equation_10, DOWN)

        # Animate the text
        self.play(Write(percent_error_text_10))
        self.wait()

        self.play(Write(percent_error_equation_10))
        self.wait()

        self.play(Write(percent_error_value_10))
        self.wait()


        self.play(
            Uncreate(trapezoids_10),
            FadeOut(measure_line),
            FadeOut(delta_x_label),
            FadeOut(trap_formula_sub_10),
            FadeOut(y1_value_text),
            FadeOut(y10_value_text),
            FadeOut(trap_area_10_Text),
            FadeOut(percent_error_text_10),
            FadeOut(percent_error_equation_10),
            FadeOut(percent_error_value_10)
        )
        # Setting up Δx = 5 visualization
        measure_line = Line(axes.c2p(0, 0), axes.c2p(5, 0), color=PURPLE).shift(DOWN * 0.5)
        delta_x_label = MathTex("\\Delta x = 5", font_size=36, color=WHITE).next_to(measure_line, DOWN * 0.2)
        self.play(Create(measure_line), Write(delta_x_label))
        self.wait()

        # Setting up Δx = 5 visualization
        measure_line = Line(axes.c2p(0, 0), axes.c2p(5, 0), color=PURPLE).shift(DOWN * 0.5)
        delta_x_label = MathTex("\\Delta x = 5", font_size=36, color=WHITE).next_to(measure_line, DOWN * 0.2)
        self.play(Create(measure_line), Write(delta_x_label))
        self.wait()

        # Trapezoid visualization for Δx = 5
        trapezoids_5 = create_trapezoids(5)
        self.play(Create(trapezoids_5), run_time=4)
        self.wait()

        # Show y5 on the graph and its value
        y5 = func(5)
        y5_dot = Dot(axes.c2p(5, y5), color=GREEN)
        y5_label = MathTex(f"y_5 = {y5:.1f}", font_size=20, color=WHITE).next_to(y5_dot, UP)
        self.play(FadeIn(y5_dot), Write(y5_label))
        self.wait()

        # Show Trapezoidal rule formula for Δx = 5 and animate the values
        trap_formula_sub_5 = MathTex( r"\frac{5}{2} \left[ \,", r"y_1", r"\,", r" +", r"\,", r"y_{10}", r"\,", r"+ 2(", r"y_5", r") \, \right]", font_size=20, color=WHITE ).next_to(formula, DOWN)
        self.play(Write(trap_formula_sub_5))
        self.wait()

        # Create texts for the numerical parts
        y5_value_text = MathTex(f"{y5:.1f}", font_size=15, color=WHITE)
        y1_value_text.move_to(y1_label.get_part_by_tex(f"{y1:.0f}").get_center())
        y10_value_text.move_to(y10_label.get_part_by_tex(f"{y10:.0f}").get_center())


        # Position the numerical parts at the initial positions
        y5_value_text.move_to(y5_label.get_part_by_tex(f"{y5:.1f}").get_center())

        # Animate the numerical parts moving to the respective positions in the formula and Replace y_1, y_5, and y_{10} in the formula with the respective values
        self.play(y1_value_text.animate.move_to(trap_formula_sub_5[1].get_center()))
        self.play(Transform(trap_formula_sub_5.get_part_by_tex("y_1"), y1_value_text))

        self.play(y10_value_text.animate.move_to(trap_formula_sub_5[5].get_center()))
        self.play(Transform(trap_formula_sub_5.get_part_by_tex("y_{10}"), y10_value_text))

        self.play(y5_value_text.animate.move_to(trap_formula_sub_5[8].get_center()))
        self.play(Transform(trap_formula_sub_5.get_part_by_tex("y_5"), y5_value_text))

        self.wait()

        trap_area_5 = ((y1 + y10 + 2 * y5) * 5 / 2)
        trap_area_5_Text = MathTex(f"= {trap_area_5:.2f}", font_size=20)
        # Calculate the percent error
        percent_error_5 = ((trap_area_5 - integral_value) / integral_value) * 100

        # Percent error text
        percent_error_text_5 = MathTex(
            r"\text{Percent Error} = \left( \frac{\text{trap\_area\_5} - \text{integral\_value}}{\text{integral\_value}} \right) \times 100\%", font_size=16, color=WHITE
        ).next_to(trap_formula_sub_5, DOWN)

        # Percent error text with substituted values
        percent_error_equation_5 = MathTex(
            r"\text{Percent Error} = \left( \frac{" + f"{trap_area_5:.2f} - {integral_value:.2f}" + r"}{" + f"{integral_value:.2f}" + r"} \right) \times 100\%", font_size=16, color=WHITE
        ).next_to(percent_error_text_5, DOWN)

        # Percent error value
        percent_error_value_5 = MathTex(
            f"= {percent_error_5:.2f}\%", font_size=16, color=WHITE
        ).next_to(percent_error_equation_5, DOWN)
        self.play(Write(trap_area_5_Text.next_to(trap_formula_sub_5, RIGHT)))
        self.wait()
        self.play(Write(percent_error_text_5))
        self.wait()

        self.play(Write(percent_error_equation_5))
        self.wait()

        self.play(Write(percent_error_value_5))
        self.wait()

        self.play(
            Uncreate(trapezoids_5),
            FadeOut(measure_line),
            FadeOut(delta_x_label),
            FadeOut(trap_formula_sub_5),
            FadeOut(y1_value_text),
            FadeOut(y5_value_text),
            FadeOut(y10_value_text),
            FadeOut(trap_area_5_Text),
            FadeOut(percent_error_text_5),
            FadeOut(percent_error_equation_5),
            FadeOut(percent_error_value_5)
        )

        self.play(*[FadeOut(mob) for mob in self.mobjects if mob != axes and mob != graph and mob != formula])

        measure_line2 = Line(axes.c2p(0, 0), axes.c2p(2, 0), color=PURPLE).shift(DOWN * 0.5)
        measure_line1 = Line(axes.c2p(0, 0), axes.c2p(1, 0), color=PURPLE).shift(DOWN * 0.5)
        measure_line = Line(axes.c2p(0, 0), axes.c2p(0.5, 0), color=PURPLE).shift(DOWN * 0.5)


        delta_x_label = MathTex("\\Delta x = 2", font_size=36, color=WHITE).next_to(measure_line2, DOWN*0.2)
        self.play(Create(measure_line2), Write(delta_x_label))
        self.wait()

        # Trapezoid visualization for Δx = 2
        trapezoids_2 = create_trapezoids(2)
        self.play(Create(trapezoids_2),run_time=6)
        self.wait()
        self.play(Uncreate(trapezoids_2))

        # Update measure line and label for Δx = 1
        self.play(ReplacementTransform(measure_line2,measure_line1))
        self.play(Transform(delta_x_label, MathTex("\\Delta x = 1", font_size=24, color=WHITE).next_to(measure_line1, DOWN*0.2)))

        # Trapezoid visualization for Δx = 1
        trapezoids_1 = create_trapezoids(1)
        self.play(Create(trapezoids_1),run_time=8)
        self.wait()
        self.play(Uncreate(trapezoids_1))

        # Update measure line and label for Δx = 0.5
        self.play(ReplacementTransform(measure_line1,measure_line))

        self.play(Transform(delta_x_label, MathTex("\\Delta x = 0.5", font_size=12, color=WHITE).next_to(measure_line, DOWN*0.2)))

        # Trapezoid visualization for Δx = 0.5
        trapezoids_0_5 = create_trapezoids(0.5)
        self.play(Create(trapezoids_0_5),run_time=12)
        self.wait(4)
