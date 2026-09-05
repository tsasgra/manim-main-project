from manim import *
import numpy as np

class CombinedCoordinateScene(Scene):
    def construct(self):
        # Thiết lập phông chữ hỗ trợ tiếng Việt (Arial, Tahoma, hoặc Times New Roman)
        self.vn_font = "Arial"
        
        # ==========================================
        # Thêm 4 giây nền đen ở đoạn mở đầu video
        # ==========================================
        self.wait(4)
        
        # Chạy Phần 1: Mê cung
        self.play_maze_part()
        
        # Chuyển cảnh 1 -> 2
        self.transition_between_parts()
        
        # Chạy Phần 2: Bàn cờ vua
        self.play_chess_part()
        
        # Chuyển cảnh 2 -> 3
        self.transition_between_parts()
        
        # Chạy Phần 3: Hệ tọa độ Oxy
        self.play_oxy_grid_part()

    def transition_between_parts(self):
        """Hiệu ứng chuyển cảnh: Xóa mờ toàn bộ vật thể đang có trên màn hình"""
        if self.mobjects:
            self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.5)
        self.wait(0.5)

    # ==========================================
    # PHẦN 1: TÌM ĐƯỜNG TRONG MÊ CUNG
    # ==========================================
    def play_maze_part(self):
        board = VGroup()
        square_size = 0.7 
        
        path_color = "#334155"   
        wall_color = "#22C55E"   
        border_color = "#475569" 
        start_color = "#3B82F6"  
        end_color = "#EF4444"    

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
                sq.set_fill(path_color, opacity=1) 
                
                x = (col - 4) * square_size
                y = (row - 4) * square_size
                sq.move_to(RIGHT * x + UP * y)
                
                board.add(sq)
                squares_2d[row][col] = sq

        origin_pt = np.array([-4.5 * square_size, -4.5 * square_size, 0])

        # 2. TẠO TRỤC TỌA ĐỘ VÀ ĐÁNH SỐ
        label_0 = Text("0", font=self.vn_font, font_size=22, color=WHITE).next_to(origin_pt, DL, buff=0.15)
        labels.add(label_0)

        for i in range(1, 10):
            x_pos = origin_pt + RIGHT * ((i - 0.5) * square_size)
            x_label = Text(str(i), font=self.vn_font, font_size=22, color=WHITE).next_to(x_pos, DOWN, buff=0.15)
            labels.add(x_label)
            
            y_pos = origin_pt + UP * ((i - 0.5) * square_size)
            y_label = Text(str(i), font=self.vn_font, font_size=22, color=WHITE).next_to(y_pos, LEFT, buff=0.15)
            labels.add(y_label)

        x_arrow = Arrow(start=origin_pt, end=origin_pt + RIGHT * (9.8 * square_size), buff=0, stroke_width=2, max_tip_length_to_length_ratio=0.04, color=WHITE)
        x_text = Text("x", font=self.vn_font, font_size=24, slant=ITALIC, color=WHITE).next_to(x_arrow, RIGHT, buff=0.1)
        
        y_arrow = Arrow(start=origin_pt, end=origin_pt + UP * (9.8 * square_size), buff=0, stroke_width=2, max_tip_length_to_length_ratio=0.04, color=WHITE)
        y_text = Text("y", font=self.vn_font, font_size=24, slant=ITALIC, color=WHITE).next_to(y_arrow, UP, buff=0.1)
        
        axes.add(x_arrow, x_text, y_arrow, y_text)

        board.sort(lambda p: p[0] - p[1])
        self.play(DrawBorderThenFill(board, lag_ratio=0.05), run_time=3)
        self.play(FadeIn(labels, shift=UP*0.2), FadeIn(axes), run_time=2)
        self.wait(2)
        
        # 3. CHUYỂN MÀU CHƯỚNG NGẠI VẬT
        wall_animations = []
        for row in range(9):
            for col in range(9):
                if maze_map[row][col] == 1:
                    wall_animations.append(squares_2d[row][col].animate.set_fill(wall_color))
        
        self.play(*wall_animations, run_time=2)
        self.wait(1)

        # 4. XUẤT HIỆN A VÀ B
        squares_2d[0][0].set_fill(start_color)
        squares_2d[8][8].set_fill(end_color)
        
        label_a = Text("A", font=self.vn_font, font_size=32, color=WHITE, weight=BOLD).move_to(squares_2d[0][0].get_center())
        label_b = Text("B", font=self.vn_font, font_size=32, color=WHITE, weight=BOLD).move_to(squares_2d[8][8].get_center())
        
        self.play(FadeIn(label_a), FadeIn(label_b), run_time=1.5)
        self.wait(1)

        # 5. DÒ ĐƯỜNG NGẮN NHẤT (BFS)
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

        # 6. DI CHUYỂN
        if shortest_path:
            path_points = [squares_2d[r][c].get_center() for r, c in shortest_path]
            route_path = VMobject()
            route_path.set_points_as_corners(path_points)
            self.play(MoveAlongPath(label_a, route_path), run_time=5, rate_func=linear)
            
        self.wait(2)


    # ==========================================
    # PHẦN 2: BÀN CỜ VUA
    # ==========================================
    def play_chess_part(self):
        square_size = 0.75
        border_width = 0.22 
        light_color = "#E6D4A7" 
        dark_color = "#A87F47"   
        border_color = "#59267c" 

        board_group = VGroup()
        squares = {}

        # 1. Tạo viền ngoài (Border)
        total_board_size = 8 * square_size
        outer_board = Square(side_length=total_board_size + 2 * border_width)
        outer_board.set_fill(border_color, opacity=1)
        outer_board.set_stroke(color=WHITE, width=1)
        board_group.add(outer_board)

        # 2. Tạo 64 ô cờ
        for row in range(8):
            for col in range(8):
                is_dark = (row + col) % 2 == 0
                color = dark_color if is_dark else light_color
                
                sq = Square(side_length=square_size)
                sq.set_fill(color, opacity=1)
                sq.set_stroke(color="#333333", width=0.2)

                x = (col - 3.5) * square_size
                y = (row - 3.5) * square_size
                sq.move_to(np.array([x, y, 0]))

                squares[(col, row)] = sq
                board_group.add(sq)

        # 3. Đánh tọa độ A-H và 1-8
        labels = VGroup()
        cols_letters = ["A", "B", "C", "D", "E", "F", "G", "H"]

        for col in range(8):
            x_pos = (col - 3.5) * square_size
            lbl_bottom = Text(cols_letters[col], font=self.vn_font, font_size=12, weight=BOLD, color=WHITE)
            lbl_bottom.move_to(np.array([x_pos, -4 * square_size - border_width / 2, 0]))
            labels.add(lbl_bottom)

        for row in range(8):
            y_pos = (row - 3.5) * square_size
            lbl_left = Text(str(row + 1), font=self.vn_font, font_size=12, weight=BOLD, color=WHITE)
            lbl_left.move_to(np.array([-4 * square_size - border_width / 2, y_pos, 0]))
            labels.add(lbl_left)

        # 4. Khởi tạo quân cờ
        def make_piece(piece_type, is_white=True):
            color_prefix = "white" if is_white else "black"
            file_name = f"picture/{color_prefix}_{piece_type}.svg"
            try:
                p = SVGMobject(file_name)
                p.scale(0.285)
                return p
            except:
                return Text("?", font=self.vn_font, font_size=30, color=RED)

        back_rank = ["R", "N", "B", "Q", "K", "B", "N", "R"]
        all_pieces = VGroup()
        pieces_dict = {}

        for col in range(8):
            p_main_w = make_piece(back_rank[col], is_white=True)
            p_main_w.move_to(squares[(col, 0)].get_center())
            all_pieces.add(p_main_w)
            pieces_dict[(col, 0)] = p_main_w

            p_pawn_w = make_piece("P", is_white=True)
            p_pawn_w.move_to(squares[(col, 1)].get_center())
            all_pieces.add(p_pawn_w)
            pieces_dict[(col, 1)] = p_pawn_w

            p_main_b = make_piece(back_rank[col], is_white=False)
            p_main_b.move_to(squares[(col, 7)].get_center())
            all_pieces.add(p_main_b)
            pieces_dict[(col, 7)] = p_main_b

            p_pawn_b = make_piece("P", is_white=False)
            p_pawn_b.move_to(squares[(col, 6)].get_center())
            all_pieces.add(p_pawn_b)
            pieces_dict[(col, 6)] = p_pawn_b

        # Hoạt ảnh bàn cờ
        self.play(FadeIn(board_group), FadeIn(all_pieces, shift=DOWN * 0.3), run_time=2)
        self.wait(1)
        self.play(FadeIn(labels), run_time=1.5)
        self.wait(2)

        # 5. Vẽ trục tọa độ Oxy
        origin_x = -4 * square_size - border_width - 0.4
        origin_y = -4 * square_size - border_width - 0.4
        h_edge_x = 4 * square_size + border_width + 0.3
        v_edge_y = 4 * square_size + border_width + 0.3
        axis_color = BLUE_C

        ox_arrow = Arrow(np.array([origin_x - 0.2, origin_y, 0]), np.array([h_edge_x, origin_y, 0]), buff=0, color=axis_color, stroke_width=3, tip_length=0.15)
        oy_arrow = Arrow(np.array([origin_x, origin_y - 0.2, 0]), np.array([origin_x, v_edge_y, 0]), buff=0, color=axis_color, stroke_width=3, tip_length=0.15)
        ox_label = Text("Ox", font=self.vn_font, font_size=16, color=axis_color).next_to(ox_arrow, RIGHT, buff=0.1)
        oy_label = Text("Oy", font=self.vn_font, font_size=16, color=axis_color).next_to(oy_arrow, UP, buff=0.1)

        axes_group = VGroup(ox_arrow, oy_arrow, ox_label, oy_label)
        for col in range(8):
            x_pos = (col - 3.5) * square_size
            tick = Text("|", font=self.vn_font, font_size=14, color=axis_color).move_to(np.array([x_pos, origin_y, 0]))
            axes_group.add(tick)
        for row in range(8):
            y_pos = (row - 3.5) * square_size
            tick = Text("|", font=self.vn_font, font_size=14, color=axis_color).rotate(90 * DEGREES).move_to(np.array([origin_x, y_pos, 0]))
            axes_group.add(tick)

        self.play(FadeIn(axes_group), run_time=2)
        self.wait(3)

        self.play(FadeOut(axes_group), run_time=1.5)
        self.wait(1)

        # Di chuyển quân tốt D2 -> D4
        if (3, 1) in pieces_dict:
            pawn_d2 = pieces_dict[(3, 1)]
            target_square = squares[(3, 3)]
            self.play(
                pawn_d2.animate.move_to(target_square.get_center()),
                run_time=2.0,
                rate_func=smooth 
            )
            pieces_dict[(3, 3)] = pawn_d2
            del pieces_dict[(3, 1)]
            
        self.wait(3)


    # ==========================================
    # PHẦN 3: HỆ TỌA ĐỘ TRONG GAME
    # ==========================================
    def play_oxy_grid_part(self):
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
        
        self.play(Create(plane), run_time=1.5)
        self.play(Write(axes_labels), run_time=0.5)
        self.wait(0.5)

        # 2. Tạo một điểm (mô phỏng nhân vật)
        character = Dot(plane.c2p(3, 2), color=RED, radius=0.15)
        
        # Hàm tự động cập nhật hiển thị tọa độ
        coord_label = always_redraw(
            lambda: Text(
                f"({int(round(plane.p2c(character.get_center())[0]))}, {int(round(plane.p2c(character.get_center())[1]))})",
                font=self.vn_font, font_size=24, color=RED
            ).next_to(character, UP)
        )

        self.play(FadeIn(character, scale=0.5), Write(coord_label))
        self.wait(0.5)

        self.play(character.animate.move_to(plane.c2p(-4, 1)), run_time=1.5)
        self.wait(0.5)
        self.play(character.animate.move_to(plane.c2p(-2, -3)), run_time=1.5)
        self.wait(0.5)

        # 3. Tô sáng các ô vuông trên lưới tọa độ
        square_1 = Square(side_length=1, color=YELLOW, fill_opacity=0.6)
        square_1.move_to(plane.c2p(-2, -3)) 
        
        square_2 = Square(side_length=1, color=PURPLE, fill_opacity=0.6)
        square_2.move_to(plane.c2p(4, 2))

        self.play(Create(square_1))
        self.play(TransformFromCopy(square_1, square_2))
        self.wait(2)

        # Fade out để nhường chỗ cho hình ảnh cuối
        self.play(FadeOut(Group(*self.mobjects)))

        # 4. Hiển thị hình ảnh kết thúc
        image_path = r"C:\Users\ASUS\manimations\coordinate  in game\picture\thinking_emotion.jpg"
        
        try:
            final_image = ImageMobject(image_path)
            self.play(FadeIn(final_image))
            self.wait(8)
            self.play(FadeOut(final_image))
        except:
            err_text = Text("Không tìm thấy đường dẫn ảnh kết thúc", font=self.vn_font, color=RED)
            self.play(Write(err_text))
            self.wait(2)
            self.play(FadeOut(err_text))