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

    # 4. Khởi tạo quân cờ và lưu vào pieces_dict để dễ dàng di chuyển sau này
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
      # Hàng 1
      p_main_w = make_piece(back_rank[col], is_white=True)
      p_main_w.move_to(squares[(col, 0)].get_center())
      all_pieces.add(p_main_w)
      pieces_dict[(col, 0)] = p_main_w

      # Hàng 2
      p_pawn_w = make_piece("P", is_white=True)
      p_pawn_w.move_to(squares[(col, 1)].get_center())
      all_pieces.add(p_pawn_w)
      pieces_dict[(col, 1)] = p_pawn_w

      # Hàng 8
      p_main_b = make_piece(back_rank[col], is_white=False)
      p_main_b.move_to(squares[(col, 7)].get_center())
      all_pieces.add(p_main_b)
      pieces_dict[(col, 7)] = p_main_b

      # Hàng 7
      p_pawn_b = make_piece("P", is_white=False)
      p_pawn_b.move_to(squares[(col, 6)].get_center())
      all_pieces.add(p_pawn_b)
      pieces_dict[(col, 6)] = p_pawn_b

    # Xuất hiện bàn cờ và quân cờ
    self.play(FadeIn(board_group), FadeIn(labels), FadeIn(all_pieces, shift=DOWN * 0.3), run_time=1.5)
    self.wait(0.5)

    # 5. Vẽ trục tọa độ Oxy dóng song song
    origin_x = -4 * square_size - border_width - 0.4
    origin_y = -4 * square_size - border_width - 0.4
    h_edge_x = 4 * square_size + border_width + 0.3
    v_edge_y = 4 * square_size + border_width + 0.3
    axis_color = BLUE_C

    ox_arrow = Arrow(
        np.array([origin_x - 0.2, origin_y, 0]),
        np.array([h_edge_x, origin_y, 0]),
        buff=0, color=axis_color, stroke_width=3, tip_length=0.15,
    )
    oy_arrow = Arrow(
        np.array([origin_x, origin_y - 0.2, 0]),
        np.array([origin_x, v_edge_y, 0]),
        buff=0, color=axis_color, stroke_width=3, tip_length=0.15,
    )

    ox_label = Text("Ox", font="Arial", font_size=16, color=axis_color).next_to(ox_arrow, RIGHT, buff=0.1)
    oy_label = Text("Oy", font="Arial", font_size=16, color=axis_color).next_to(oy_arrow, UP, buff=0.1)

    axes_group = VGroup(ox_arrow, oy_arrow, ox_label, oy_label)

    for col in range(8):
      x_pos = (col - 3.5) * square_size
      tick = Text("|", font="Arial", font_size=14, color=axis_color)
      tick.move_to(np.array([x_pos, origin_y, 0]))
      axes_group.add(tick)

    for row in range(8):
      y_pos = (row - 3.5) * square_size
      tick = Text("|", font="Arial", font_size=14, color=axis_color)
      tick.rotate(90 * DEGREES)
      tick.move_to(np.array([origin_x, y_pos, 0]))
      axes_group.add(tick)

    self.play(FadeIn(axes_group), run_time=1.2)
    self.wait(2)

    # 6. MỚI: Xóa trục Oxy khỏi màn hình
    self.play(FadeOut(axes_group), run_time=1)
    self.wait(0.5)

    # 7. MỚI: Di chuyển quân Tốt Trắng từ D2 lên D4
    # Cột D tương ứng index 3, hàng 2 tương ứng index 1, hàng 4 tương ứng index 3
    pawn_d2 = pieces_dict[(3, 1)]
    target_square = squares[(3, 3)]
    
    self.play(
        pawn_d2.animate.move_to(target_square.get_center()),
        run_time=1.0,
        rate_func=smooth # Hiệu ứng di chuyển mượt mà
    )
    
    # Cập nhật vị trí trong từ điển (nếu bạn muốn code các nước đi tiếp theo)
    pieces_dict[(3, 3)] = pawn_d2
    del pieces_dict[(3, 1)]
    
    self.wait(2)