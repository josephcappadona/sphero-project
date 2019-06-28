from r2d2_client import R2D2Client
r2d2 = R2D2Client()

#check that the robot is connected
r2d2.animate(10)
r2d2.set_stance(2)  # transition to bipod

#check if the robot will turn its head
r2d2.rotate_head(30)
r2d2.rotate_head(60)
r2d2.rotate_head(90)
r2d2.rotate_head(120)
r2d2.rotate_head(150)
r2d2.rotate_head(180)
r2d2.rotate_head(-30)
r2d2.rotate_head(-60)
r2d2.rotate_head(-90)
r2d2.rotate_head(-120)
r2d2.rotate_head(-150)

r2d2.rotate_head(-160)

r2d2.rotate_head(200)
r2d2.rotate_head(-180)

r2d2.rotate_head(0)

#shutdown
r2d2.sleep()
r2d2.quit()
