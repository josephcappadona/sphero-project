from r2d2_client import R2D2Client
r2d2 = R2D2Client('127.0.0.1', 1337)

#check that the robot is connected
r2d2.animate(10)
r2d2.set_stance(2)  # transition to bipod

r2d2.light_color(254, 127, 156) #pink
r2d2.light_color(255, 165, 0)  #orange
r2d2.light_color(255, 255, 255)  #white
r2d2.light_color(255, 211, 0)  #yellow
r2d2.light_color(255, 0, 0) #red
r2d2.light_color(0, 255, 0) #green
r2d2.light_color(0, 0, 255) #blue

#back_light_led
r2d2.back_light_intensity(156) 
r2d2.back_light_intensity(0)  
r2d2.back_light_intensity(255)  
r2d2.back_light_intensity(211)  

r2d2.sleep()
r2d2.quit()
