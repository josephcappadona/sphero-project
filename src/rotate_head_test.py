from client import DroidClient
droid = DroidClient()
droid.connect_to_R2D2()

#check that the robot is connected
droid.animate(10)
droid.set_stance(2)  # transition to bipod

#check if the robot will turn its head
droid.rotate_head(30)
droid.rotate_head(60)
droid.rotate_head(90)
droid.rotate_head(120)
droid.rotate_head(150)
droid.rotate_head(180)
droid.rotate_head(-30)
droid.rotate_head(-60)
droid.rotate_head(-90)
droid.rotate_head(-120)
droid.rotate_head(-150)

droid.rotate_head(-160)

droid.rotate_head(200)
droid.rotate_head(-180)

droid.rotate_head(0)

#shutdown
droid.sleep()
droid.quit()
