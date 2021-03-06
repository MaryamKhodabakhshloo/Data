import os
import pygame
import numpy as np
import time
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
#################################################################################
class EGO_Car:
    def __init__(self, x, y, angle=90.0, length=4, max_steering=30, max_acceleration=5.0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0,0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 10
        self.brake_deceleration = 10
        self.free_deceleration = 1
        self.acceleration = 0.0
        self.steering = 0.0

    def update(self,dt):
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))#vehical velocity if it's in allowable range
        #print(self.velocity.x)
        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0
        self.position += self.velocity.rotate(-self.angle) * dt

        self.angle += degrees(angular_velocity) * dt
################################################################################
class O_Car:
    def __init__(self, x, y, length=4):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.length = length
        self.max_velocity = 10

    def update(self,dt):
        self.velocity=(0,10)
        self.position += np.array(self.velocity) * dt
       # print(np.array(self.velocity) * dt)
################################################################################
class Start:
    def __init__(self):
        pygame.init()
        width = 500
        height = 1000
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False

    def run(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, "car.png")
        path1 = os.path.join(current_dir, "car1.png")
        path2 = os.path.join(current_dir, "car2.png")
        path3 = os.path.join(current_dir, "car3.png")
        car_image = pygame.image.load(path)
        car_image1 = pygame.image.load(path1) 
        car_image2 = pygame.image.load(path2)
        car_image3 = pygame.image.load(path3)
        car = EGO_Car(11,19,angle=90.0)
        car1=O_Car(5,5)
        car2=O_Car(5,12)
        car3=O_Car(5,19)
        ppu = 32
        
        while not self.exit:
            dt = self.clock.get_time() / 1000
            
            # Event queue
            for event in pygame.event.get():
                pressed = pygame.key.get_pressed()
                if event.type == pygame.QUIT or pressed[pygame.K_ESCAPE] :
                    self.exit = True
            # User input
            

            if pressed[pygame.K_UP]:
                if car.velocity.x < 0:
                    car.acceleration = car.brake_deceleration
                else:
                    car.acceleration += 1 * dt
            elif pressed[pygame.K_DOWN]:
                if car.velocity.x > 0:
                    car.acceleration = -1*car.brake_deceleration
                else:
                    car.acceleration -= 1 * dt
            else:
                if abs(car.velocity.x) > dt * car.free_deceleration:
                    car.acceleration = -copysign(car.free_deceleration, car.velocity.x)
                else:
                    if dt != 0:
                        car.acceleration = -car.velocity.x / dt
            car.acceleration = max(-car.max_acceleration, min(car.acceleration, car.max_acceleration))
            

            if pressed[pygame.K_RIGHT]:
                car.steering -= 30 * dt
            elif pressed[pygame.K_LEFT]:
                car.steering += 30 * dt
            else:
                car.steering = 0
            car.steering = max(-car.max_steering, min(car.steering, car.max_steering))
            # Logic
            car.update(dt)
            car1.update(-.5*dt)
            car2.update(-.25*dt)
            car3.update(-.2*dt)
           
            bias = 10

            
            car.position_disp = np.array((car.position[0], car.position[1]+bias) )
            car1.position_disp = np.array((car1.position[0], car1.position[1]+bias) )
            car2.position_disp = np.array((car2.position[0], car2.position[1]+bias) )
            car3.position_disp = np.array((car3.position[0], car3.position[1]+bias))
            outFile = open('/home/m/Desktop/file','a')
            outFile.write(str(car.position_disp[0]))
            outFile.write(",") 
            outFile.write(str(car.velocity.rotate(-car.angle)[0]))
            outFile.write(",") 
            outFile.write(str(car.velocity.rotate(-car.angle)[1]))
            outFile.write(",") 
            outFile.write(str(car.acceleration))
            outFile.write(",") 
            outFile.write(str(car.steering))
            outFile.write("\n")

            # Drawing
            self.screen.fill((150, 150, 150))

            
            pygame.draw.rect(self.screen,(255, 255, 255) , [50, 0, 13, 970])
            pygame.draw.rect(self.screen,(255, 255, 255) , [450, 0, 13, 970])


            lane_positions = [[250, 1000-i*80, 13, 50] for i in range(1000)]
            
            for p in lane_positions:
                p_disp = p
                p_disp[1] += car.position[1]
                pygame.draw.rect(self.screen,(255, 255, 255), p_disp)
            


            rotated  = pygame.transform.rotate(car_image, car.angle)
            rotated1 = car_image1 
            rotated2 = car_image2
            rotated3 = car_image3
            rect = rotated.get_rect()
            rect1 = rotated1.get_rect()
            rect2 = rotated1.get_rect()
            rect3 = rotated1.get_rect()
            
            self.screen.blit(rotated, car.position_disp * ppu - (rect.width / 2, rect.height / 2))
            self.screen.blit(rotated1, car1.position_disp * ppu - (rect1.width / 2, rect1.height / 2))
            self.screen.blit(rotated2, car2.position_disp * ppu - (rect2.width / 2, rect2.height / 2))
            self.screen.blit(rotated3, car3.position_disp * ppu - (rect3.width / 2, rect3.height / 2))
            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()
       # elapsed = (time.clock() - start)
       # print(elapsed)

################################################################################
if __name__ == '__main__':
    game = Start()
    game.run()
