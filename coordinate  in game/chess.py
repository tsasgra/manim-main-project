from manim import *

class FullChessBoard(Scene):
    def construct(self):
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
            lbl_bottom = Text(cols_letters[col], font="Arial", font_size=12, weight=BOLD, color=WHITE)
            lbl_bottom.move_to(np.array([x_pos, -4 * square_size - border_width / 2, 0]))
            labels.add(lbl_bottom)

        for row in range(8):
            y_pos = (row - 3.5) * square_size
            lbl_left = Text(str(row + 1), font="Arial", font_size=12, weight=BOLD, color=WHITE)
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
            except FileNotFoundError:
                return Text("?", font_size=30, color=RED)

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

        # ---------------------------------------------------------
        # ĐỒNG BỘ ANIMATION VỚI KỊCH BẢN (image_fdd88a.png)
        # ---------------------------------------------------------

        # Thoại: "Một ví dụ quen thuộc khác là trò chơi cờ vua." (~3s)
        self.play(FadeIn(board_group), FadeIn(all_pieces, shift=DOWN * 0.3), run_time=2)
        self.wait(1)

        # Thoại: "Nếu bạn để ý, trên hai cạnh của bàn cờ thường có đánh số và chữ cái tương ứng." (~4.5s)
        self.play(FadeIn(labels), run_time=2)
        self.wait(2.5)

        # Thoại: "Các chữ cái (A, B, C, D, E, F, G, H) được sắp theo hàng ngang, còn các con số (1 đến 8) theo cột dọc." (~5s)
        self.wait(5)

        # 5. Vẽ trục tọa độ Oxy
        origin_x = -4 * square_size - border_width - 0.4
        origin_y = -4 * square_size - border_width - 0.4
        h_edge_x = 4 * square_size + border_width + 0.3
        v_edge_y = 4 * square_size + border_width + 0.3
        axis_color = BLUE_C

        ox_arrow = Arrow(np.array([origin_x - 0.2, origin_y, 0]), np.array([h_edge_x, origin_y, 0]), buff=0, color=axis_color, stroke_width=3, tip_length=0.15)
        oy_arrow = Arrow(np.array([origin_x, origin_y - 0.2, 0]), np.array([origin_x, v_edge_y, 0]), buff=0, color=axis_color, stroke_width=3, tip_length=0.15)
        ox_label = Text("Ox", font="Arial", font_size=16, color=axis_color).next_to(ox_arrow, RIGHT, buff=0.1)
        oy_label = Text("Oy", font="Arial", font_size=16, color=axis_color).next_to(oy_arrow, UP, buff=0.1)

        axes_group = VGroup(ox_arrow, oy_arrow, ox_label, oy_label)
        for col in range(8):
            x_pos = (col - 3.5) * square_size
            tick = Text("|", font="Arial", font_size=14, color=axis_color).move_to(np.array([x_pos, origin_y, 0]))
            axes_group.add(tick)
        for row in range(8):
            y_pos = (row - 3.5) * square_size
            tick = Text("|", font="Arial", font_size=14, color=axis_color).rotate(90 * DEGREES).move_to(np.array([origin_x, y_pos, 0]))
            axes_group.add(tick)

        # Thoại: "Như vậy, mỗi ô trên bàn cờ có thể xem như một điểm tọa độ trên mặt phẳng Oxy, trong đó trục Ox biểu diễn theo chữ cái, còn trục Oy biểu diễn theo số thứ tự" (~9s)
        self.play(FadeIn(axes_group), run_time=2)
        self.wait(7)

        # Thoại: "Bằng cách này, ta có thể xác định chính xác vị trí của từng ô và từng quân cờ trên bàn." (~4s)
        # Ẩn trục Oxy đi để chuẩn bị di chuyển quân cờ
        self.play(FadeOut(axes_group), run_time=1.5)
        self.wait(2.5)

        # Thoại: "Ví dụ, khi nói 'quân Tốt trắng đi tới ô D4', nghĩa là quân Tốt đó được di chuyển đến vị trí nằm ở giao điểm giữa cột D và hàng 4." (~8s)
        pawn_d2 = pieces_dict[(3, 1)]
        target_square = squares[(3, 3)]
        
        self.play(
            pawn_d2.animate.move_to(target_square.get_center()),
            run_time=2.0,
            rate_func=smooth 
        )
        pieces_dict[(3, 3)] = pawn_d2
        del pieces_dict[(3, 1)]
        self.wait(6)

        # Thoại: "Như vậy, trong trò chơi, hệ trục tọa độ Oxy giúp ta xác định vị trí và tính toán đường đi ngắn nhất cho nhân vật. Còn trong cờ vua, nó giúp định vị trí và tính toán nước đi hợp lý cho từng quân cờ." (~10s)
        self.wait(8)