from manim import *
import numpy as np

class ArrowMazePath(Scene):
    def construct(self):
        board = VGroup()
        square_size = 0.7 
        
        # Bảng màu
        path_color = "#334155"   # Màu xám cho đường đi
        wall_color = "#22C55E"   # Màu xanh lá cây chuẩn cho tường
        border_color = "#475569" 
        start_color = "#3B82F6"  
        end_color = "#EF4444"    

        # Bản đồ mê cung tự nhiên
        maze_map = [
            [0, 0, 1, 0, 0, 0, 0, 1, 0],
            [1, 0, 1, 0, 1, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 1, 1, 0, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 1],
            [1, 1, 0, 1, 1, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 1, 0, 0, 0, 1, 0] 
        ]

        squares_2d = [[None for _ in range(9)] for _ in range(9)]
        labels = VGroup()
        axes = VGroup()
        
        # 1. KHỞI TẠO LƯỚI
        for row in range(9):
            for col in range(9):
                sq = Square(side_length=square_size)
                sq.set_stroke(width=1.5, color=border_color)
                
                # Ban đầu tất cả các ô đều mang màu xám (vùng có thể đi)
                sq.set_fill(path_color, opacity=1) 
                
                x = (col - 4) * square_size
                y = (row - 4) * square_size
                sq.move_to(RIGHT * x + UP * y)
                
                board.add(sq)
                squares_2d[row][col] = sq

        # Tọa độ gốc tọa độ (góc dưới bên trái của bảng)
        origin_pt = np.array([-4.5 * square_size, -4.5 * square_size, 0])

        # 2. TẠO TRỤC TỌA ĐỘ OX, OY VÀ ĐÁNH SỐ
        # Thêm số 0 ở gốc tọa độ
        label_0 = Text("0", font_size=22, color=WHITE).next_to(origin_pt, DL, buff=0.15)
        labels.add(label_0)

        # Đánh số 1 đến 9 căn giữa phía ngoài các ô vuông
        for i in range(1, 10):
            # Số trục X (Dịch (i - 0.5) để vào chính giữa cột)
            x_pos = origin_pt + RIGHT * ((i - 0.5) * square_size)
            x_label = Text(str(i), font_size=22, color=WHITE).next_to(x_pos, DOWN, buff=0.15)
            labels.add(x_label)
            
            # Số trục Y (Dịch (i - 0.5) để vào chính giữa hàng)
            y_pos = origin_pt + UP * ((i - 0.5) * square_size)
            y_label = Text(str(i), font_size=22, color=WHITE).next_to(y_pos, LEFT, buff=0.15)
            labels.add(y_label)

        # Vẽ trục mũi tên Ox, Oy
        x_arrow = Arrow(start=origin_pt, end=origin_pt + RIGHT * (9.8 * square_size), buff=0, stroke_width=2, max_tip_length_to_length_ratio=0.04, color=WHITE)
        x_text = Text("x", font_size=24, slant=ITALIC, color=WHITE).next_to(x_arrow, RIGHT, buff=0.1)
        
        y_arrow = Arrow(start=origin_pt, end=origin_pt + UP * (9.8 * square_size), buff=0, stroke_width=2, max_tip_length_to_length_ratio=0.04, color=WHITE)
        y_text = Text("y", font_size=24, slant=ITALIC, color=WHITE).next_to(y_arrow, UP, buff=0.1)
        
        axes.add(x_arrow, x_text, y_arrow, y_text)

        # Sắp xếp lại thứ tự các ô trong board từ Trái-Trên xuống Phải-Dưới
        board.sort(lambda p: p[0] - p[1])

        # Bảng xuất hiện trước trong 1.7 giây
        self.play(DrawBorderThenFill(board, lag_ratio=0.05), run_time=3)
        
        # Sau đó hệ trục và các con số mới xuất hiện 
        self.play(FadeIn(labels, shift=UP*0.2), FadeIn(axes), run_time=4.5)
        
        # Chờ đúng 10 giây trước khi chuyển màu chướng ngại vật
        self.wait(10)
        
        # 3. CHUYỂN MÀU CÁC Ô CHƯỚNG NGẠI VẬT SANG XANH LÁ
        wall_animations = []
        for row in range(9):
            for col in range(9):
                if maze_map[row][col] == 1:
                    wall_animations.append(squares_2d[row][col].animate.set_fill(wall_color))
        
        self.play(*wall_animations, run_time=2)
        self.wait(5)

        # 4. XUẤT HIỆN A VÀ B
        squares_2d[0][0].set_fill(start_color)
        squares_2d[8][8].set_fill(end_color)
        
        label_a = Text("A", font_size=32, color=WHITE, weight=BOLD).move_to(squares_2d[0][0].get_center())
        label_b = Text("B", font_size=32, color=WHITE, weight=BOLD).move_to(squares_2d[8][8].get_center())
        
        self.play(
            FadeIn(label_a, shift=UP),
            FadeIn(label_b, shift=UP),
            run_time=3
        )
        self.wait(6)

        # 5. AI DÒ ĐƯỜNG NGẮN NHẤT (BFS)
        queue = [[(0, 0)]]
        visited = set([(0, 0)])
        shortest_path = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while queue:
            path = queue.pop(0)
            curr_r, curr_c = path[-1]
            if (curr_r, curr_c) == (8, 8):
                shortest_path = path
                break
            for dr, dc in directions:
                nr, nc = curr_r + dr, curr_c + dc
                if 0 <= nr < 9 and 0 <= nc < 9 and maze_map[nr][nc] == 0:
                    if (nr, nc) not in visited:
                        visited.add((nr, nc))
                        queue.append(path + [(nr, nc)])

        # 6. CHỮ A DI CHUYỂN ĐẾN B
        path_points = [squares_2d[r][c].get_center() for r, c in shortest_path]
        route_path = VMobject()
        route_path.set_points_as_corners(path_points)

        self.play(MoveAlongPath(label_a, route_path), run_time=12, rate_func=linear)
        
        self.wait(2)