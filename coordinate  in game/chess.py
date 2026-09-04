from manim import *


class ChessOpeningScene(Scene):

  def construct(self):
    # 1. Tiêu đề
    title = Text("Khai cuộc Cờ Vua (King's Knight)", font_size=32, color=BLUE)
    title.to_edge(UP, buff=0.4)
    self.play(Write(title))

    # 2. Tạo bàn cờ 8x8
    square_size = 0.65
    light_color = "#F0D9B5"  # Màu ô sáng
    dark_color = "#B58863"  # Màu ô tối

    board_group = VGroup()
    squares = {}

    for row in range(8):
      for col in range(8):
        color = light_color if (row + col) % 2 == 0 else dark_color
        sq = Square(side_length=square_size)
        sq.set_fill(color, opacity=1)
        sq.set_stroke(color="#4a3728", width=0.5)

        # Căn giữa bàn cờ
        x = (col - 3.5) * square_size
        y = (row - 3.5) * square_size - 0.2
        sq.move_to(np.array([x, y, 0]))

        squares[(col, row)] = sq
        board_group.add(sq)

    # Thêm nhãn cột (A-H) và hàng (1-8)
    labels = VGroup()
    cols_letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
    for col in range(8):
      lbl = Text(cols_letters[col], font_size=18, color=GRAY)
      lbl.next_to(squares[(col, 0)], DOWN, buff=0.1)
      labels.add(lbl)

    for row in range(8):
      lbl = Text(str(row + 1), font_size=18, color=GRAY)
      lbl.next_to(squares[(0, row)], LEFT, buff=0.1)
      labels.add(lbl)

    self.play(FadeIn(board_group), FadeIn(labels), run_time=1.2)

    # 3. Hàm tạo quân cờ bằng ký tự Unicode
    def make_piece(symbol, is_white=True):
      color = "#FFFFFF" if is_white else "#1A1A1A"
      stroke_color = "#333333" if is_white else "#AAAAAA"
      p = Text(symbol, font_size=38, color=color)
      p.set_stroke(color=stroke_color, width=1)
      return p

    # Khởi tạo một số quân cờ chính cho khai cuộc
    # Ký hiệu: ♟: Tốt, ♞: Mã, ♝: Tượng, ♜: Xe, ♛: Hậu, ♚: Vua
    white_pawn_e = make_piece("♟", is_white=True)
    black_pawn_e = make_piece("♟", is_white=False)
    white_knight_g = make_piece("♞", is_white=True)
    black_knight_b = make_piece("♞", is_white=False)

    # Đặt quân cờ vào vị trí xuất phát
    white_pawn_e.move_to(squares[(4, 1)].get_center())  # e2
    black_pawn_e.move_to(squares[(4, 6)].get_center())  # e7
    white_knight_g.move_to(squares[(6, 0)].get_center())  # g1
    black_knight_b.move_to(squares[(1, 7)].get_center())  # b8

    pieces_group = VGroup(
        white_pawn_e, black_pawn_e, white_knight_g, black_knight_b
    )
    self.play(FadeIn(pieces_group), run_time=0.8)

    # 4. Hiển thị bảng ký hiệu nước đi
    move_tracker = Text(
        "Nước đi: --", font_size=24, color=YELLOW
    ).next_to(board_group, RIGHT, buff=0.8)
    self.play(Write(move_tracker))

    # Hàm di chuyển quân cờ và tạo hiệu ứng highlight
    def move_piece(piece, from_pos, to_pos, notation_str):
      # Highlight ô đi và ô đến
      hl_from = (
          squares[from_pos]
          .copy()
          .set_fill("#F6F669", opacity=0.5)
          .set_stroke(width=0)
      )
      hl_to = (
          squares[to_pos]
          .copy()
          .set_fill("#BAFA44", opacity=0.5)
          .set_stroke(width=0)
      )

      new_notation = Text(
          f"Nước đi: {notation_str}", font_size=24, color=YELLOW
      ).move_to(move_tracker)

      self.add(hl_from, hl_to, piece)
      self.play(
          piece.animate.move_to(squares[to_pos].get_center()),
          Transform(move_tracker, new_notation),
          run_time=1.0,
      )
      self.wait(0.4)
      self.remove(hl_from, hl_to)

    # 5. Thực hiện chuỗi nước đi
    # 1. e4 (Trắng đi tốt e2 -> e4)
    move_piece(white_pawn_e, (4, 1), (4, 3), "1. e4")

    # 1... e5 (Đen đi tốt e7 -> e5)
    move_piece(black_pawn_e, (4, 6), (4, 4), "1... e5")

    # 2. Nf3 (Trắng đi mã g1 -> f3)
    move_piece(white_knight_g, (6, 0), (5, 2), "2. Nf3")

    # 2... Nc6 (Đen đi mã b8 -> c6)
    move_piece(black_knight_b, (1, 7), (2, 5), "2... Nc6")

    # Kết thúc hoạt cảnh
    ending_text = Text(
        "Thế cờ cân bằng!", font_size=26, color=GREEN
    ).next_to(move_tracker, DOWN, buff=0.5)
    self.play(Write(ending_text))
    self.wait(2)