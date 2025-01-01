from manim import *
import numpy as np
import sympy as sp

class SimpsonRule(Scene):
    def construct(self):

        def create_axes():
            axes = Axes(
                x_range=[0, 11, 1],
                y_range=[0, 450, 50],
                axis_config={"color": BLUE, "include_numbers": True},
            )
            axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
            return axes, axes_labels
        
        def set_function(f, f_expr):
            def create_graph(axes):
                return axes.plot(lambda x: sp.lambdify(sp.Symbol('x'), f_expr)(x), color=RED)

            def get_function_label():
                return MathTex(rf"f(x) = {sp.latex(f_expr)}", font_size=14).shift(LEFT * 2)

            def create_quadratic_function(axes, x0, x1, x2):
                f_lambdified = sp.lambdify(sp.Symbol('x'), f_expr)
                y0, y1, y2 = f_lambdified(x0), f_lambdified(x1), f_lambdified(x2)

                points = [Dot(axes.coords_to_point(x0, y0)), Dot(axes.coords_to_point(x1, y1)), Dot(axes.coords_to_point(x2, y2))]
                point_labels = [
                    MathTex(f"({x0}, {y0:.2f})").scale(0.5).next_to(points[0], UP),
                    MathTex(f"({x1}, {y1:.2f})").scale(0.5).next_to(points[1], UP),
                    MathTex(f"({x2}, {y2:.2f})").scale(0.5).next_to(points[2], UP)
                ]

                h = x1 - x0
                c = y1
                a = (y0 + y2 - 2 * y1) / (2 * h ** 2)
                b = ((y0 + y2 - 2 * y1) / 2 - y0 + y1) / h

                quad_func = lambda x: a * (x - x1) ** 2 + b * (x - x1) + c
                quad_graph = axes.plot(quad_func, color=GREEN, x_range=[x0 - 1, x2 + 1])
                quad_group = VGroup(*points, *point_labels)
                return quad_group, quad_graph, y0, y1, y2

            return create_graph, get_function_label, create_quadratic_function
        
        def display_substitution(self, y_values, x_values, n):
            h = (x_values[-1] - x_values[0]) / n
            f_values = [f"{y:.2f}" for y in y_values]

            # Generate strings for odd and even indices
            odd_indices = " + ".join([f"4f({x_values[i]:.2f})" for i in range(1, n, 2)])
            even_indices = " + ".join([f"2f({x_values[i]:.2f})" for i in range(2, n, 2)])

            # Create the general expression
            general_expr = MathTex(
                rf"\int_{{{x_values[0]:.2f}}}^{{{x_values[-1]:.2f}}} f(x) \, dx \approx \frac{{h}}{3} \left[ f({x_values[0]:.2f}) + {odd_indices} + {even_indices} + f({x_values[-1]:.2f}) \right]",
                font_size=14
            ).next_to(simple_simpson_expr, DOWN, aligned_edge=LEFT)

            # Substitute values into the expression
            odd_values = " + ".join([f"4({f_values[i]})" for i in range(1, n, 2)])
            even_values = " + ".join([f"2({f_values[i]})" for i in range(2, n, 2)])

            substituted_expr = VGroup(
                MathTex(
                    rf"\int_{{{x_values[0]:.2f}}}^{{{x_values[-1]:.2f}}} f(x) \, dx \approx \frac{{h}}{3} \left[ {f_values[0]} + {odd_values} + {even_values} + {f_values[-1]} \right]",
                    font_size=14
                ),
                MathTex(
                    rf"= \frac{{{h:.2f}}}{{3}} \left[ {y_values[0]} + {sum(4*y_values[i] for i in range(1, n, 2))} + {sum(2*y_values[i] for i in range(2, n, 2))} + {y_values[-1]} \right]",
                    font_size=14
                ),
                MathTex(
                    rf"= {h / 3 * (y_values[0] + sum(4*y_values[i] for i in range(1, n, 2)) + sum(2*y_values[i] for i in range(2, n, 2)) + y_values[-1]):.2f}",
                    font_size=14
                ),
            ).arrange(DOWN).next_to(general_expr, DOWN, aligned_edge=LEFT)
            
            self.play(Write(general_expr))
            self.wait(1)
            self.play(Write(substituted_expr),run_time=4)
            self.wait(3)
            self.play(FadeOut(VGroup(general_expr, substituted_expr)))

        axes, axes_labels = create_axes()
        self.play(Create(axes), Write(axes_labels))
        self.wait(1)

        x = sp.Symbol('x')
        f_expr = sp.exp(x / 2) - x**3 + 100 * x
        create_graph, get_function_label, create_quadratic_function = set_function(f_expr, f_expr)

        graph = create_graph(axes)
        func_label = get_function_label()
        self.play(Create(graph))
        self.play(Write(func_label))
        self.wait(2)

        simple_simpson_expr = MathTex(
            r"\int_{a}^{b} f(x) \, dx \approx \frac{h}{3} [f(x_0) + 4f(x_1) + f(x_2)]",
            font_size=14
        ).next_to(func_label, DOWN, aligned_edge=LEFT)
        self.play(Write(simple_simpson_expr))
        self.wait(2)

        # Example quadratic functions
        quad_group, quad_graph, y0, y1, y2 = create_quadratic_function(axes, 1, 2, 3)
        self.play(Create(quad_group), run_time=1)
        self.play(Create(quad_graph), run_time=2)
        self.wait(4)
        display_substitution(self, [y0, y1, y2], [1, 2, 3], 2)
        self.play(FadeOut(quad_group, quad_graph))

        quad_group, quad_graph, y0, y1, y2 = create_quadratic_function(axes, 0, 5, 10)
        self.play(Create(quad_group), run_time=1)
        self.play(Create(quad_graph), run_time=2)
        self.wait(4)
        display_substitution(self, [y0, y1, y2], [0, 5, 10], 2)
        self.play(FadeOut(quad_group, quad_graph))


        # Fade out the Simple Simpson's Rule
        general_simpson_expr = MathTex( r"\int_{a}^{b} f(x) \, dx \approx \frac{h}{3} \left[ f(x_0) + 4 \sum_{\text{odd} \, i} f(x_i) + 2 \sum_{\text{even} \, i} f(x_i) + f(x_n) \right]", font_size=14 ).next_to(func_label, DOWN, aligned_edge=LEFT)
        self.play(Transform(simple_simpson_expr, general_simpson_expr),run_time=2)
        self.wait(1)

        # General Simpson's Rule for n = 4
        n = 4
        x_values = np.linspace(0, 10, n + 1)
        y_values = [sp.lambdify(x, f_expr)(x_val) for x_val in x_values]

        # Create and display quadratic functions for each pair of intervals
        quads_group = VGroup()
        graph_group = VGroup()
        for i in range(0, len(x_values) - 2, 2):
            quad_group, quad_graph, y0, y1, y2 = create_quadratic_function(axes, x_values[i], x_values[i + 1], x_values[i + 2])
            quads_group.add(*quad_group)
            self.play(Create(quad_group), run_time=2)
            self.wait(1)
            graph_group.add(quad_graph)
            self.play(Create(quad_graph), run_time=3)
            self.wait(2)


        # Display the substitution in the General Simpson's Rule
        display_substitution(self, y_values, x_values, n)
        self.play(FadeOut(quads_group, graph_group))
        
        # General Simpson's Rule for n = 8
        n = 8
        x_values = np.linspace(0, 10, n + 1)
        y_values = [sp.lambdify(x, f_expr)(x_val) for x_val in x_values]

        quads_group = VGroup()
        graph_group = VGroup()

        # Create and display quadratic functions for each pair of intervals
        quads_group = VGroup()
        for i in range(0, len(x_values) - 2, 2):
            quad_group, quad_graph, y0, y1, y2 = create_quadratic_function(axes, x_values[i], x_values[i + 1], x_values[i + 2])
            quads_group.add(*quad_group)
            self.play(Create(quad_group), run_time=3)
            self.wait(1)
            graph_group.add(quad_graph)
            self.play(Create(quad_graph), run_time=6)
            self.wait(2)

        self.wait(3)
        # Display the substitution in the General Simpson's Rule
        display_substitution(self, y_values, x_values, n)
        self.play(FadeOut(quads_group, graph_group))
