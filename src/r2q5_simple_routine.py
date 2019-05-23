from r2q5_client import R2Q5Client
r2q5 = R2Q5Client()

r2q5.animate(10)
r2q5.set_stance(2)  # transition to bipod

from maneuver import follow_path
path = [(0,0), (0,1), (1,1), (1,2), (2,2), (2,3), (3,3), (3,0), (0,0)]
follow_path(r2q5, path, 0x88, scale_dist=0.5)

r2q5.turn(0)
r2q5.sleep()
r2q5.quit()
