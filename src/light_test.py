from client import DroidClient
droid = DroidClient()
droid.connect_to_R2D2()

#check that the robot is connected
droid.animate(10)
droid.set_stance(2)  # transition to bipod

droid.light_color(254, 127, 156) #pink
droid.light_color(255, 165, 0)  #orange
droid.light_color(255, 255, 255)  #white
droid.light_color(255, 211, 0)  #yellow
droid.light_color(255, 0, 0) #red
droid.light_color(0, 255, 0) #green
droid.light_color(0, 0, 255) #blue

droid.sleep()
droid.quit()
