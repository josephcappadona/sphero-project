from client import DroidClient
droid = DroidClient()
droid.connect_to_R2D2()

#check that the robot is connected
droid.animate(10)
droid.set_stance(2)  # transition to bipod

#check if the main lights change color
droid.set_front_LED_colors(254, 127, 156) #pink
droid.set_front_LED_colors(255, 165, 0)  #orange
droid.set_front_LED_colors(255, 255, 255)  #white
droid.set_front_LED_colors(255, 211, 0)  #yellow
droid.set_front_LED_colors(255, 0, 0) #red
droid.set_front_LED_colors(0, 255, 0) #green
droid.set_front_LED_colors(0, 0, 255) #blue

#color should override rgb values
# droid.main_light_color(254, 127, 156, "red") 
# droid.main_light_color(255, 165, 0, "blue")  
# droid.main_light_color(255, 255, 255, "green")  

#back light intensity check

droid.set_back_LED_colors(254, 127, 156) #pink
droid.set_back_LED_colors(255, 165, 0)  #orange
droid.set_back_LED_colors(255, 255, 255)  #white
droid.set_back_LED_colors(255, 211, 0)  #yellow
droid.set_back_LED_colors(255, 0, 0) #red
droid.set_back_LED_colors(0, 255, 0) #green
droid.set_back_LED_colors(0, 0, 255) #blue

droid.sleep()
droid.quit()
