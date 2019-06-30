from client import DroidClient
droid = DroidClient()
droid.connect_to_R2D2()

droid.animate(10)
droid.set_stance(2)  # transition to bipod

from maneuver import follow_path
path = [(0,0), (0,1), (1,1), (1,2), (2,2), (2,3), (3,3), (3,0), (0,0)]
follow_path(droid, path, 0x88, scale_dist=0.5)

droid.turn(0)
droid.sleep()
droid.quit()
