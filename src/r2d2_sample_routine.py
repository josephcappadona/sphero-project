from r2d2_client import R2D2Client
r2d2 = R2D2Client()

r2d2.animate(10)
r2d2.set_stance(2)  # transition to bipod

from maneuver import follow_path
path = [(0,0), (0,1), (1,1), (1,2), (2,2), (2,3), (3,3), (3,0), (0,0)]
follow_path(r2d2, path, 0x88, scale_dist=0.5)

r2d2.turn(0)
r2d2.sleep()
r2d2.quit()
