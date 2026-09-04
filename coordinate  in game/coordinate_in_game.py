from manim import *

class ArrowMazePath(Scene):
    def construct(self):
        # 1. ĐỔI MÀU NỀN ĐỂ TẠO CHIỀU SÂU
        self.camera.background_color = "#1E1E2E" 
        
        board = VGroup()
        square_size = 0.7 
        
        # Bảng màu
        path_color = "#334155"   
        wall_color = "#2DD4BF"   
        route_color = "#FBBF24"  # Màu vàng cho mũi tên
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
        
        # 2. KHỞI TẠO LƯỚI
        for row in range(9):
            for col in range(9):
                sq = Square(side_length=square_size)
                sq.set_stroke(width=1.5, color=border_color)
                
                if (row, col) == (0, 0):
                    target_color = start_color
                elif (row, col) == (8, 8):
                    target_color = end_color
                else:
                    target_color = wall_color if maze_map[row][col] == 1 else path_color
                    
                sq.set_fill(target_color, opacity=1) 
                
                x = (col - 4) * square_size
                y = (row - 4) * square_size
                sq.move_to(RIGHT * x + UP * y)
                
                board.add(sq)
                squares_2d[row][col] = sq

        # Hiệu ứng vẽ lưới
        self.play(DrawBorderThenFill(board, lag_ratio=0.01), run_time=3)
        
        # Gắn chữ A, B 
        label_a = Text("A", font_size=32, color=WHITE, weight=BOLD).move_to(squares_2d[0][0].get_center())
        label_b = Text("B", font_size=32, color=WHITE, weight=BOLD).move_to(squares_2d[8][8].get_center())
        self.play(Write(label_a), Write(label_b))
        self.wait(0.5)

        # 3. AI DÒ ĐƯỜNG NGẮN NHẤT (BFS)
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

        # 4. VẼ ĐƯỜNG ĐI BẰNG CÁC MŨI TÊN TO HƠN
        arrows = VGroup()
        for i in range(len(shortest_path) - 1):
            r1, c1 = shortest_path[i]
            r2, c2 = shortest_path[i+1]
            
            start_point = squares_2d[r1][c1].get_center()
            end_point = squares_2d[r2][c2].get_center()
            
            # Tinh chỉnh thông số mũi tên để to và rõ hơn
            arrow = Arrow(
                start=start_point, 
                end=end_point, 
                color=route_color, 
                stroke_width=8,                          # Tăng độ dày thân (từ 5 lên 8)
                max_tip_length_to_length_ratio=0.35,     # Tỷ lệ đầu mũi tên to hơn (từ 0.25 lên 0.35)
                max_stroke_width_to_length_ratio=10,     # Giúp thân không bị teo lại khi khoảng cách ngắn
                buff=0.15                                # Giảm khoảng hở một chút để mũi tên dài hơn
            )
            arrows.add(arrow)

        # Hiệu ứng các mũi tên xuất hiện nối tiếp nhau
        self.play(Create(arrows, lag_ratio=1), run_time=4.5)
        self.wait(2)