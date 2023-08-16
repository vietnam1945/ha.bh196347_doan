import math

class Tracker:
    def __init__(self):
        # Lưu trữ vị trí tâm của các đối tượng
        self.center_points = {}
        # Giữ số lượng các ID
        # Mỗi khi phát hiện một ID đối tượng mới, số lượng sẽ tăng lên một
        self.id_count = 0

        self.prev_frame = None
        # Đặt số khung hình bỏ qua giữa các cập nhật
        self.num_frames_skip = 5
        # Khởi tạo bộ đếm để theo dõi các khung hình đã bị bỏ qua
        self.frame_counter = 0

        # Bộ đếm để theo dõi đối tượng qua nhiều khung hình
        self.object_counter = {}

    
    
    def update(self, objects_rect):
        # Hộp đối tượng và các ID
        objects_bbs_ids = []

        # Lấy điểm tâm của đối tượng mới
        for rect in objects_rect:
            x, y, w, h, clas, conf = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2
            name = clas

            # Xác định xem đối tượng đó đã được phát hiện hay chưa
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 30:
                    # Kiểm tra xem khoảng cách giữa điểm tâm hiện tại và điểm tâm trước đó có quá lớn hay không
                    if self.frame_counter > self.num_frames_skip:
                        self.center_points[id] = (cx, cy)
                        objects_bbs_ids.append([x, y, w, h, id, name, conf])
                    else:
                        self.center_points[id] = (cx, cy)
                        objects_bbs_ids.append([x, y, w, h, id, name, conf])
                    same_object_detected = True
                    break

            # Nếu phát hiện đối tượng mới, chúng ta gán ID cho đối tượng đó
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count, name,conf])
                self.id_count += 1


        # Xóa các ID không còn được sử dụng khỏi từ điển tọa độ tâm
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id, _, _,  = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Loại bỏ các ID không còn được sử dụng nữa
        self.center_points = new_center_points.copy()

        #  Kiểm tra xem có bất kỳ đối tượng nào đã được phát hiện trong nhiều khung hình 
        for id, count in self.object_counter.items():
            if count >= 3:
                #  Đặt lại bộ đếm cho đối tượng này
                self.object_counter[id] = 0

                # Cập nhật tất cả các mục nhập trước đó của đối tượng này với ID hiện tại
                for i in range(len(objects_bbs_ids)):
                    if objects_bbs_ids[i][4] == id:
                        objects_bbs_ids[i][4] = self.id_count - 1

        # Tăng bộ đếm khung hình và cập nhật khung hình trước đó
        self.frame_counter += 1
        self.prev_frame = self.center_points.copy()

        return objects_bbs_ids