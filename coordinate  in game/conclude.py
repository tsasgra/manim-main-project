from manim import *

class OxyToGameGrid(Scene):
    def construct(self):
        # 1. Tạo và vẽ hệ lưới trục tọa độ
        plane = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 2,
                "stroke_opacity": 0.5
            }
        )
        axes_labels = plane.get_axis_labels(x_label="x", y_label="y")
        
        # Vẽ hệ trục tọa độ nhanh hơn (run_time = 1)
        self.play(Create(plane), run_time=1)
        self.play(Write(axes_labels), run_time=0.5)
        self.wait(0.5)

        # 2. Tạo một điểm (mô phỏng nhân vật hoặc vật thể)
        character = Dot(plane.c2p(3, 2), color=RED, radius=0.15)
        
        # Hàm tự động cập nhật hiển thị tọa độ (x, y) khi điểm di chuyển
        coord_label = always_redraw(
            lambda: Text(
                f"({int(round(plane.p2c(character.get_center())[0]))}, {int(round(plane.p2c(character.get_center())[1]))})",
                font_size=24, color=RED
            ).next_to(character, UP)
        )

        self.play(FadeIn(character, scale=0.5), Write(coord_label))
        self.wait(0.5)

        # Mô phỏng sự di chuyển của nhân vật trên bản đồ
        self.play(character.animate.move_to(plane.c2p(-4, 1)), run_time=1.5)
        self.wait(0.5)
        self.play(character.animate.move_to(plane.c2p(-2, -3)), run_time=1.5)
        self.wait(0.5)

        # 3. Tô sáng các ô vuông trên lưới tọa độ
        square_1 = Square(side_length=1, color=YELLOW, fill_opacity=0.6)
        square_1.move_to(plane.c2p(-2, -3)) # Vị trí hiện tại của nhân vật
        
        square_2 = Square(side_length=1, color=PURPLE, fill_opacity=0.6)
        square_2.move_to(plane.c2p(4, 2))

        self.play(Create(square_1))
        self.play(TransformFromCopy(square_1, square_2))
        
        self.wait(2)

        # Fade out để kết thúc video
        self.play(FadeOut(Group(*self.mobjects)))