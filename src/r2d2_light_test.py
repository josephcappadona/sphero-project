from r2d2_client import R2D2Client
r2d2 = R2D2Client()

#check that the robot is connected
r2d2.animate(10)
r2d2.set_stance(2)  # transition to bipod

#check if the front and back lights change color
r2d2.main_light_color(254, 127, 156) #pink
r2d2.main_light_color(255, 165, 0)  #orange
r2d2.main_light_color(255, 255, 255)  #white
r2d2.main_light_color(255, 211, 0)  #yellow
r2d2.main_light_color(255, 0, 0) #red
r2d2.main_light_color(0, 255, 0) #green
r2d2.main_light_color(0, 0, 255) #blue

r2d2.front_light_color(254, 127, 156) #pink
r2d2.front_light_color(255, 165, 0)  #orange
r2d2.front_light_color(255, 255, 255)  #white
r2d2.front_light_color(255, 211, 0)  #yellow
r2d2.front_light_color(255, 0, 0) #red
r2d2.front_light_color(0, 255, 0) #green
r2d2.front_light_color(0, 0, 255) #blue

#color should override rgb values
r2d2.main_light_color(254, 127, 156, "red") 
r2d2.main_light_color(255, 165, 0, "blue")  
r2d2.main_light_color(255, 255, 255, "green")  

r2d2.front_light_color(255, 0, 0, "yellow") 
r2d2.front_light_color(0, 255, 0, "purple") 
r2d2.front_light_color(0, 0, 255, "orange") 

r2d2.sleep()
r2d2.quit()
