from manim import *

class FullChessBoard(Scene):
    def construct(self):
        title = Text("Bàn cờ vua (Sử dụng SVG)", font="Arial", font_size=36, color=BLUE)
        title.to_edge(UP, buff=0.2)
        self.play(Write(title))

        square_size = 0.75
        light_color = "#EBECD0"
        dark_color = "#739552"

        board_group = VGroup()
        squares = {}

        for row in range(8):
            for col in range(8):
                color = light_color if (row + col) % 2 == 0 else dark_color
                sq = Square(side_length=square_size)
                sq.set_fill(color, opacity=1)
                sq.set_stroke(color="#333333", width=0.5)

                x = (col - 3.5) * square_size
                y = (row - 3.5) * square_size - 0.2
                sq.move_to(np.array([x, y, 0]))

                squares[(col, row)] = sq
                board_group.add(sq)

        labels = VGroup()
        cols_letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
        for col in range(8):
            lbl = Text(cols_letters[col], font="Arial", font_size=20, color=GRAY)
            lbl.next_to(squares[(col, 0)], DOWN, buff=0.1)
            labels.add(lbl)

        for row in range(8):
            lbl = Text(str(row + 1), font="Arial", font_size=20, color=GRAY)
            lbl.next_to(squares[(0, row)], LEFT, buff=0.1)
            labels.add(lbl)

        self.play(FadeIn(board_group), FadeIn(labels), run_time=1.5)

        # Sử dụng SVGMobject để gọi file ảnh
        def make_piece(piece_type, is_white=True):
            color_prefix = "white" if is_white else "black"
            # Thêm "picture/" vào trước tên file
            file_name = f"picture/{color_prefix}_{piece_type}.svg"

            try:
                p = SVGMobject(file_name)
                # Đã giảm tỷ lệ từ 0.35 xuống 0.28 để quân cờ nằm gọn trong ô
                p.scale(0.28) 
                return p
            except FileNotFoundError:
                return Text("?", font_size=40, color=RED)

        back_rank = ["R", "N", "B", "Q", "K", "B", "N", "R"]
        all_pieces = VGroup()

        for col in range(8):
            p_main_w = make_piece(back_rank[col], is_white=True)
            p_main_w.move_to(squares[(col, 0)].get_center())
            all_pieces.add(p_main_w)
            
            p_pawn_w = make_piece("P", is_white=True)
            p_pawn_w.move_to(squares[(col, 1)].get_center())
            all_pieces.add(p_pawn_w)

        for col in range(8):
            p_main_b = make_piece(back_rank[col], is_white=False)
            p_main_b.move_to(squares[(col, 7)].get_center())
            all_pieces.add(p_main_b)
            
            p_pawn_b = make_piece("P", is_white=False)
            p_pawn_b.move_to(squares[(col, 6)].get_center())
            all_pieces.add(p_pawn_b)

        self.play(FadeIn(all_pieces, shift=DOWN*0.5), run_time=2)
        self.wait(2)