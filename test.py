# 추적박스안에 선수를 다시 추적하기
# 다중객체 추적 test
import cv2
import numpy as np

# open video file
video_path = '영상1.mp4'
cap = cv2.VideoCapture(video_path)

output_size = (200, 400) # (width, height)
fit_to = 'height'

# initialize writing video
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
out = cv2.VideoWriter('%s_output.mp4' % (video_path.split('.')[0]), fourcc, cap.get(cv2.CAP_PROP_FPS), output_size)

# check file is opened
if not cap.isOpened():
  exit()

# initialize tracker
OPENCV_OBJECT_TRACKERS = {
  "csrt": cv2.TrackerCSRT_create,
  "kcf": cv2.TrackerKCF_create,
  "boosting": cv2.TrackerBoosting_create,
  "mil": cv2.TrackerMIL_create,
  "tld": cv2.TrackerTLD_create,
  "medianflow": cv2.TrackerMedianFlow_create,
  "mosse": cv2.TrackerMOSSE_create
}




tracker = OPENCV_OBJECT_TRACKERS['csrt']()
# tracker2 = OPENCV_OBJECT_TRACKERS['csrt']()
# tracker3 = OPENCV_OBJECT_TRACKERS['csrt']()
# tracker4 = OPENCV_OBJECT_TRACKERS['csrt']()

# main
ret, img = cap.read()

cv2.namedWindow('Select Window')
cv2.imshow('Select Window', img)

# select ROI
rect = cv2.selectROI('Select Window', img, fromCenter=False, showCrosshair=True)
# rect = cv2.selectROI('Select Window', img, fromCenter=False, showCrosshair=True)

# rect2 = cv2.selectROI('Select Window', img, fromCenter=False, showCrosshair=True)
# rect3 = cv2.selectROI('Select Window', img, fromCenter=False, showCrosshair=True)
# rect4 = cv2.selectROI('Select Window', img, fromCenter=False, showCrosshair=True)
cv2.destroyWindow('Select Window')

# initialize tracker
tracker.init(img, rect)

# tracker2.init(img, rect2)
# tracker3.init(img, rect3)
# tracker4.init(img, rect4)

tracker_check = 0

blue_threshold = 200
green_threshold = 200
red_threshold = 200
bgr_threshold = [blue_threshold, green_threshold, red_threshold]


while True:

  # read frame from video
  ret, img = cap.read()

  if not ret:
    exit()

  # update tracker and get position from new frame
  success, box = tracker.update(img)
  # if success:
  left, top, w, h = [int(v) for v in box]
  right = left + w
  bottom = top + h

  center_x = left + w / 2
  center_y = top + h /2

  # success2, box2 = tracker2.update(img)
  # # if success:
  # left2, top2, w2, h2 = [int(v) for v in box2]
  # right2 = left2 + w2
  # bottom2 = top2 + h2
  #
  # center_x2 = left2 + w2 / 2
  # center_y2 = top2 + h2 / 2
  #
  # success3, box3 = tracker3.update(img)
  # # if success:
  # left3, top3, w3, h3= [int(v) for v in box3]
  # right3 = left3 + w3
  # bottom3 = top3 + h3
  #
  # center_x3 = left3 + w3 / 2
  # center_y3 = top3 + h3 / 2
  #
  # success4, box4 = tracker4.update(img)
  # # if success:
  # left4, top4, w4, h4 = [int(v) for v in box4]
  # right4 = left4 + w4
  # bottom4 = top4 + h4
  #
  # center_x4 = left4 + w4 / 2
  # center_y4 = top4 + h4 / 2


  cv2.rectangle(img, pt1=(left,top), pt2=(left+w, top+h), color=(255,255,255), thickness=3)
  # cv2.rectangle(img, pt1=(left2, top2), pt2=(left2 + w2, top2 + h2), color=(255, 0, 255), thickness=3)
  # cv2.rectangle(img, pt1=(left3, top3), pt2=(left3 + w3, top3 + h3), color=(0, 0, 255), thickness=3)
  # cv2.rectangle(img, pt1=(left4, top4), pt2=(left4 + w4, top4 + h4), color=(255, 0, 0), thickness=3)

  cv2.imshow('img', img)

  # write video

  if cv2.waitKey(1) == ord('q'):
    break

# release everything
cap.release()
out.release()
cv2.destroyAllWindows()
def perstpective(perspect_map, pointList, onepixel):
  perspect_map =0

fps =0
# fir_top 을 각 선수마다 넣어준다.
class Player():
  fir_top, pre_top = 0
  right, bottom, center_x, center_x = 0
  left, top, w, h =0
  f_t_h_cal, t_p_h_cal = 0
  adj_center_x, adj_center_y = 0
  # 경로를 그리기 위한 변수들
  nowPoint,  point_sum,  point_mean = [0,0]
  pointList =[]
  route_pointList = []
  mean_avg_list_size = int(fps / 2)  # 이동평균 리스트 크기
  mean_avg_list = []
  for i in range(mean_avg_list_size):  # 개수만큼 만듬
    mean_avg_list.append([0, 0])

  route_pers_distance = 0
  pre_route_pers_distance = 0
  pre_time =0
  cur_time =0
  line_count=1

  length = 0.0
  pix_num_move = 0.0

  def box(self, box):
    Player.left, Player.top, Player.w, Player.h = [int(v) for v in box]
    Player.right = left + w
    Player.bottom = top + h
    Player.center_x = int(left + w / 2)
    Player.center_y = int(top + h)

  def draw_box(self):
      pt1 = (int(Player.left), int(Player.top))
      pt2 = (int(Player.right), int(Player.bottom))
      return cv2.rectangle(img, pt1, pt2, (255, 255, 255), 3)

  def constant(self,slope_13,slope_h2, point_list_y_ratio):
    constant_b1 = player1.center_y - slope_13 * player1.center_x  # 1, 3루
    constant_b2 = player1.center_y - slope_h2 * player1.center_x  # h, 2루
    if (constant_b1 > 0 and constant_b2 < 0) or (constant_b1 < 0 and constant_b2 > 0) or (
            constant_b1 == 0 and constant_b2 >= 0):  # 2,4면이랑 각 선에 있을때
      Player.f_t_h_cal = (h * (abs(Player.fir_top - Player.top) / int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))  # 초기위치 - 현재위치
    if (constant_b1 > 0 and constant_b2 > 0) or (constant_b1 < 0 and constant_b2 < 0):  # 1,3면에 있을때
      Player.f_t_h_cal = (h * (abs(Player.fir_top - Player.top) / int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))) * point_list_y_ratio)

  def positional_correction(self):  #위치에 따른 점의 보정을 위한 함수
    Player.t_p_h_cal = (Player.h * (abs(Player.top - Player.pre_top) / int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    if Player.fir_top > Player.top:  # 초기위치보다 멀때
        if Player.top < Player.pre_top:  # 위쪽움직임
            Player.adj_center_y = int(Player.top + Player.h - Player.f_t_h_cal - Player.t_p_h_cal)
        if Player.top > Player.pre_top:  # 아래쪽움직임
            Player.adj_center_y = int(Player.top + Player.h - Player.f_t_h_cal + Player.t_p_h_cal)
        if Player.top == Player.pre_top:
            Player.adj_center_y = int(Player.top + Player.h - Player.f_t_h_cal)

    if Player.fir_top < Player.top:  # 초기위치보다 가까워질때
        if Player.top < Player.pre_top:
            Player.adj_center_y = int(Player.top + Player.h + Player.f_t_h_cal - Player.t_p_h_cal)
        if Player.top > Player.pre_top:
            Player.adj_center_y = int(Player.top + Player.h + Player.f_t_h_cal + Player.t_p_h_cal)
        if Player.top == Player.pre_top:
            Player.adj_center_y = int(Player.top + Player.h + Player.f_t_h_cal)

    if Player.fir_top == Player.top:
        if Player.top < Player.pre_top:
            Player.adj_center_y = int(Player.top + Player.h - Player.t_p_h_cal)
        if Player.top > Player.pre_top:
            Player.adj_center_y = int(Player.top + Player.h + Player.t_p_h_cal)
        if Player.top == Player.pre_top:
            Player.adj_center_y = int(Player.top + Player.h)

    Player.pre_top = Player.top

  # 이동평균 계산하여 경로 그리기 보정 & 속도별 칼라추가 작업
  def mean_avg(self,start_a):
    Player.adj_center_x = int(Player.left + Player.w / 2)

    Player.nowPoint[0] = Player.adj_center_x
    Player.nowPoint[1] = Player.adj_center_y
    if start_a == 1 or start_a == 2:
        Player.point_sum[0] -= Player.mean_avg_list[0][0]
        Player.point_sum[1] -= Player.mean_avg_list[0][1]

        Player.mean_avg_list.pop(0)

        if start_a == 1:
            Player.point_sum[0] += Player.nowPoint[0]
            Player.point_sum[1] += Player.nowPoint[1]

        if start_a == 1:
            Player.mean_avg_list.append(Player.nowPoint[0:2])
        if start_a == 2:
            Player.mean_avg_list.append([0, 0])

        if Player.mean_avg_list.count([0, 0]) < Player.mean_avg_list_size:
            Player.point_mean[0] = int(Player.point_sum[0] / (Player.mean_avg_list_size - Player.mean_avg_list.count([0, 0])))
            Player.point_mean[1] = int(Player.point_sum[1] / (Player.mean_avg_list_size - Player.mean_avg_list.count([0, 0])))

            Player.pointList.append(Player.point_mean[0:2])

  def route_color(self, frame, frame1, perspect_map, onepixel): # 이동경로를 색상으로 표현하기 위하여 구간별 속도 계산
    if frame1 + 1 == frame:
        Player.pre_route_pers_distance = Player.route_pers_distance
        Player.pre_time = Player.cur_time

        Player.cur_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        route_run_time = round(player1.cur_time - player1.pre_time, 2)
        print("시간 ", route_run_time)
        player1.pre_time = player1.cur_time

        Player.route_pers_distance = round(perstpective(perspect_map, Player.pointList, onepixel), 2)
        print("거리", Player.route_pers_distance)
        route_v = round(abs(Player.route_pers_distance - Player.pre_route_pers_distance) / route_run_time * 3.6, 2)
        print("속도 ", route_v)
        Player.pre_route_pers_distance = Player.route_pers_distance

        Player.route_pointList.append(route_v)

  def draw_route(self):
      temp_x , temp_y =0
      color_cal = 0
      route_pointList_i = 0
      for [x, y] in Player.pointList:
          # print("x: ",x,y)
          if temp_x != 0 and temp_y != 0:
              route_pointList_index = Player.route_pointList[route_pointList_i]
              if Player.line_count == 1:
                  Player.pre_route_pointList_index = route_pointList_index
                  Player.line_count += 1

              route_pointList_index_div = abs(route_pointList_index - Player.pre_route_pointList_index) / 2
              pre_route_pointList_index = route_pointList_index

              color_cal1 = 0
              if route_pointList_index >= Player.pre_route_pointList_index:
                  color_cal1 = abs(Player.pre_route_pointList_index + route_pointList_index_div - 20) * 10
              if route_pointList_index < pre_route_pointList_index:
                  color_cal1 = abs(pre_route_pointList_index - route_pointList_index_div - 20) * 10
              color_cal2 = abs(route_pointList_index - 20) * 10

              if route_pointList_index - 20 >= 0:
                  large_color1_255 = 127 - color_cal1
                  if large_color1_255 <= 0:
                      large_color1_255 = 0
                  large_color2_255 = 127 - color_cal2
                  if large_color2_255 <= 0:
                      large_color2_255 = 0
                  cv2.line(img, (x, y), (int((temp_x + x) / 2), int((temp_y + y) / 2)), (0, large_color1_255, 255), 2)
                  cv2.line(img, (int((temp_x + x) / 2), int((temp_y + y) / 2)), (temp_x, temp_y),
                           (0, large_color2_255, 255), 2)
              if route_pointList_index - 20 < 0:
                  little_color1_255 = 127 + color_cal1
                  if little_color1_255 >= 255:
                      little_color1_255 = 255
                  little_color2_255 = 127 + color_cal2
                  if little_color2_255 >= 255:
                      little_color2_255 = 255
                  cv2.line(img, (x, y), (int((temp_x + x) / 2), int((temp_y + y) / 2)), (0, little_color1_255, 255), 2)
                  cv2.line(img, (int((temp_x + x) / 2), int((temp_y + y) / 2)), (temp_x, temp_y),
                           (0, little_color2_255, 255), 2)

              route_pointList_i += 1
          temp_x = x
          temp_y = y

  def print_imformation(self,perspect_map,  onepixel, run_time):
      pers_distance = round(perstpective(perspect_map, Player.pointList, onepixel), 2)
      print("변환된 물리적 거리는", pers_distance, "M 입니다")
      v = round(pers_distance / run_time * 3.6, 2)
      a = round(v / run_time, 2)
      print("선수의 평균가속도는 ", a, "km/h^2 입니다")
      print("시간"+ run_time +"입니다.")

      file = open("결과파일.txt", 'w')
      file.write("영상 이름: ")
      file.write(video_path)
      file.write("\n")
      file.write("선수 기록\n")
      file.write("뛴거리: %f M \n" % pers_distance)
      file.write("속도: %f km/h\n" % v)
      file.write("가속도: %f km/h^2\n" % a)
      file.close()




player1 = Player()
player1.fir_top = 1
player1.constant(1,1,)

success, box = tracker.update(img)
player1.box(box)

if count % frame_num == 0:
  player1.mean_avg(start_a)

temp_x = 0
temp_y = 0

for