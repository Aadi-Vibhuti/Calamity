# abandon hope all ye who enter here
initialisation_resetting_string='''heal_rect=heal_ball.get_rect(center=(-100,100))
superbreak=False
platform_rect=platform.get_rect(topleft=(0,750))
healthbar_rect=healthbar.get_rect(bottomleft=platform_rect.bottomleft)
bossbar_rect=bossbar.get_rect(bottomright=platform_rect.bottomright)
floating_platform1_rect=floating_platform1.get_rect(bottomleft=(0,500))
floating_platform2_rect=floating_platform2.get_rect(bottomright=(1550,500))
floating_platform3_rect=floating_platform3.get_rect(midbottom=(775,375))
floating_platform4_rect=floating_platform4.get_rect(midbottom=(0,160))
boss_rect=boss.get_rect(center=(1550/2,-500))
spike1=spikes.get_rect(bottomleft=platform_rect.topleft)
spike2=spikes.get_rect(bottomright=(1550,750))
boss_x_vel=0
boss_y_vel=0
playerbullets=[]
cooldown=0
death=False
bul_del=5
snake_pos_list=[]
bullet_velocity=20
left_heal=False
right_heal=False
floorvelocity=7
playerxvelocity=playeryvelocity=bossxmove=bossymove=bossmovetime=0
floor=750
jump=0
xacc =0
gravity=0.75
drag=0.75
delay=fpstime=time.time()
adown=ddown=spdown=sdown=False
immunity=False
immunetime=time.time()
gametick=fpstick=0
FPS=60
bossxfinal=bossyfinal=0
angle=10
laser_warning_set=[]
laser_set=[]
small_laser_set=[]
fireballs_rect_set=[]
for i in range(360):
    small_laser_set.append(pygame.transform.rotate(small_laser,i))
laser_index=0
delay=0
shoot=False
end_angle=0
sun_dance_angle=0
fireballs_speed_set=[]
for i in range(100):
    fireballs_rect_set.append(fireball.get_rect(midbottom=(random.randint(0,1550),-(random.randint(50,3000)))))
    fireballs_speed_set.append(5)
torchshoot=True
mid_torch=0
random_tackle_coords=[]
for i in range(50):
    random_tackle_coords.append((random.randint(0,300),random.randint(0,610)))
    random_tackle_coords.append((random.randint(1250,1550),random.randint(0,610)))
random_tackle_index=0
skewer_set=[]
circle_projectile_set1=[]
circle_projectile_set_randomiser=[]
for i in range(11):
    skewer_set.append(skewer.get_rect(bottomleft=(i*150,0)))
skewer_target=player_rect.centerx
skewerspeed_set=[0,0,0,0,0,0,0,0,0,0,0]
skewer_true_speed_set=[0,0,0,0,0,0,0,0,0,0,0]
skewer_delay_set=[0,0,0,0,0,0,0,0,0,0,0]
target2=player_rect.center
for i in range(8):
    circle_projectile_set1.append(circle_projectile.get_rect(center=(-100,-100)))
temp_angle=0
bullet_set=[]
bullet_move=[]
for i in range(50):
    bullet_set.append(bullet.get_rect(center=(1550/2,550)))
    bullet_move.append((0,0))
bullet_index=bullet_shoot_index=0
rand_skew_set=[]
for i in range(10):
    rand_skew_set.append(75+(150*i))
rand_skew_index=0
snake_set=[]
for i in range(20):
    snake_set.append(boss.get_rect(center=(-200,-200)))
hits=0
bossdrag=0.8
won=False
'''
try:
    for i in range(2):
        try:
            import pygame
            from sys import exit
            import time
            import math
            import random
            from datetime import datetime
            import os
            from copy import deepcopy
            
            scale_factor=1
            muted=True
            count=0
            bullet_damage=0.20
            try:
                with open("settings.txt" ,'r') as f:
                    f_readlines=f.readlines()
                    scale_factor=float(f_readlines[1][:-1])/100
                    muted=eval(f_readlines[3][:-1])
                    # bullet_damage=eval(f_readlines[5][:-1])
            except Exception as e:
                print(e)
            pygame.init()
            pygame.mixer.init()
            screen = pygame.display.set_mode((1550*scale_factor,810*scale_factor))
            pygame.display.set_caption("Calamity")
            
            clock= pygame.time.Clock()


            def dist(p1,p2):
                x1,y1=p1
                x2,y2=p2
                return ((x1-x2)**2+(y1-y2)**2)**0.5


            def get_pos_between(p1, p2, d):
                dist_p1_p2=math.dist(p1,p2)
                ratio = d / dist_p1_p2
                new_x = p1[0] + ratio * (p2[0] - p1[0])
                new_y = p1[1] + ratio * (p2[1] - p1[1])
                return (new_x, new_y)
            def get_move_pos(index,distance):
                i=index
                if i == 0:
                    return boss_rect.center
                m=0
                while m!=distance:
                    if m+dist(snake_pos_list[i].center,snake_pos_list[i-1].center)<distance:
                        m+=dist(snake_pos_list[i].center,snake_pos_list[i-1].center)
                        i-=1
                    elif m+dist(snake_pos_list[i].center,snake_pos_list[i-1].center)==distance:
                        return snake_pos_list[i-1].center
                    else:
                        return get_pos_between(snake_pos_list[i].center,snake_pos_list[i-1].center,distance-m)

            def newblit(img,rects):
                img=pygame.transform.scale(img, (int(img.get_rect().width * scale_factor), int(img.get_rect().height * scale_factor)))
                if type(rects)==pygame.rect.Rect:
                    rects=(rects.topleft[0]*scale_factor,rects.topleft[1]*scale_factor)
                    screen.blit(img,rects)
                else:
                    screen.blit(img,(rects[0]*scale_factor,rects[1]*scale_factor))


            def playerblit(damage):
                if playeryvelocity<0:
                    thruster_pos=list(player_rect.center)
                    thruster_pos[0]-=20
                    thruster_pos[1]-=10
                    newblit(thrust,thruster_pos)
                if damage:
                    img=player_damage_list[-int(playerxvelocity)]
                else:
                    img=player_list[-int(playerxvelocity)]
                rects=player_rect
                img=pygame.transform.scale(img, (int(img.get_rect().width * scale_factor), int(img.get_rect().height * scale_factor)))
                if type(rects)==pygame.rect.Rect:
                    rects=(rects.topleft[0]*scale_factor,rects.topleft[1]*scale_factor)
                    screen.blit(img,rects)
                else:
                    screen.blit(img,(rects[0]*scale_factor,rects[1]*scale_factor))
            def drawline(screen,color,pos1,pos2,thickness):
                pygame.draw.line(screen, color , pos1, pos2, int(thickness))
            def same(n):
                return n
            def get_at(tup):
                tup=(int(tup[0]*scale_factor),int(tup[1]*scale_factor))
                return screen.get_at(tup)
            def rotocrop(surface, angle):
                """
                Rotates a surface around its center without scaling,
                then crops the excess so the result has the same size as the original.
                """
                w, h = surface.get_size()

                # Step 1: Rotate (this expands the surface)
                rotated = pygame.transform.rotate(surface, angle)
                rw, rh = rotated.get_size()

                # Step 2: Compute cropping box (centered crop)
                x = (rw - w) // 2
                y = (rh - h) // 2

                # Step 3: Crop to original size
                cropped = rotated.subsurface((x, y, w, h)).copy()

                return cropped
            

            if not muted:
                background_music=pygame.mixer.Sound("Game/bgm.mp3")
            boss_woosh=pygame.mixer.Sound("Game/boss_woosh.wav")
            damage1=pygame.mixer.Sound("Game/damage.wav")
            #surface initializations

            thrust=pygame.image.load("Game/graphics/player/thrust.png").convert_alpha()
            space_surface = pygame.image.load("Game/graphics/backgrounds/space.png").convert()
            platform = pygame.image.load("Game/graphics/objects/platform.png").convert_alpha()
            star = pygame.image.load("Game/graphics/objects/star.png").convert_alpha()
            floating_platform1= pygame.image.load("Game/graphics/objects/floating_platform.png").convert_alpha()
            explosion= pygame.image.load("Game/graphics/objects/explosion.png").convert_alpha()
            floating_platform2= pygame.image.load("Game/graphics/objects/floating_platform.png").convert_alpha()
            floating_platform3= pygame.image.load("Game/graphics/objects/floating_platform.png").convert_alpha()
            floating_platform4= pygame.image.load("Game/graphics/objects/floating_platform.png").convert_alpha()
            healthbar=pygame.image.load("Game/graphics/player/healthbar.png").convert_alpha()
            bossbar=pygame.image.load("Game/graphics/player/bossbar.png").convert_alpha()
            player = pygame.image.load("Game/graphics/player/front.png").convert_alpha()
            # player2 = pygame.transform.rotozoom(player,-45,1)
            # player4 = pygame.transform.rotozoom(player,45,1)
            # player3=player
            #player2 = pygame.image.load("Game/graphics/player/ball2.png").convert_alpha()
            #player3 = pygame.image.load("Game/graphics/player/ball3.png").convert_alpha()
            #player4 = pygame.image.load("Game/graphics/player/ball4.png").convert_alpha()
            player_damage = pygame.image.load("Game/graphics/player/damaged.png").convert_alpha()
            # player_damage_2 = pygame.transform.rotozoom(player_damage,-45,1)
            # player_damage_4 = pygame.transform.rotozoom(player_damage,45,1)
            player_list=[rotocrop(player,i) for i in range(0,51,5)]
            player_list+=[rotocrop(player,i) for i in range(-51,0,5)]
            player_damage_list=[rotocrop(player_damage,i) for i in range(0,51,5)]
            player_damage_list+=[rotocrop(player_damage,i) for i in range(-51,0,5)]
            boss0=pygame.image.load("Game/graphics/boss.png").convert_alpha()
            boss1=pygame.image.load("Game/graphics/boss1.png").convert_alpha()
            boss2=pygame.image.load("Game/graphics/boss3.png").convert_alpha()
            boss3=pygame.image.load("Game/graphics/boss3.png").convert_alpha()
            bossded1=pygame.image.load("Game/graphics/bossded1.png").convert_alpha()
            bossded2=pygame.image.load("Game/graphics/bossded2.png").convert_alpha()
            bossded3=pygame.image.load("Game/graphics/bossded3.png").convert_alpha()
            bossded4=pygame.image.load("Game/graphics/bossded5.png").convert_alpha()
            bossded5=pygame.image.load("Game/graphics/bossded5.png").convert_alpha()
            laser=pygame.image.load("Game/graphics/red_laser1.png").convert_alpha()
            laser_warning=pygame.image.load("Game/graphics/laser_warning.png").convert_alpha()
            fireball=pygame.image.load("Game/graphics/objects/small_fireball.png").convert_alpha()
            skewer=pygame.image.load("Game/graphics/objects/yskewer.png").convert_alpha()
            circle_projectile=pygame.image.load("Game/graphics/objects/circle_projectile.png").convert_alpha()
            small_laser=pygame.image.load("Game/graphics/objects/small_laser.png").convert_alpha()
            spikes=pygame.image.load("Game/graphics/objects/spikes.png").convert_alpha()
            bullet=pygame.image.load("Game/graphics/objects/bullet.png").convert_alpha()
            skew_warning=pygame.image.load("Game/graphics/objects/skew_warning.png").convert_alpha()
            gameover=pygame.image.load("Game/graphics/none.png").convert_alpha()
            heal_ball=pygame.image.load("Game/graphics/objects/heal_ball.png").convert_alpha()
            snake_body=pygame.image.load("Game/graphics/snake_body.png").convert_alpha()
            instructions=pygame.image.load("Game/graphics/instructions.png").convert_alpha()
            player_bullet=pygame.image.load("Game/graphics/player/bullet.png").convert_alpha()
            boss=boss0
            pygame.display.set_icon(boss)
            #rect

            heal_rect=heal_ball.get_rect(center=(-100,100))
            superbreak=False

            platform_rect=platform.get_rect(topleft=(0,750))
            healthbar_rect=healthbar.get_rect(bottomleft=platform_rect.bottomleft)
            bossbar_rect=bossbar.get_rect(bottomright=platform_rect.bottomright)
            player_rect= player.get_rect(midbottom=((1550/2),700))
            floating_platform1_rect=floating_platform1.get_rect(bottomleft=(0,500))
            floating_platform2_rect=floating_platform2.get_rect(bottomright=(1550,500))
            floating_platform3_rect=floating_platform3.get_rect(midbottom=(775,375))
            floating_platform4_rect=floating_platform4.get_rect(midbottom=(0,160))
            boss_rect=boss.get_rect(center=(1550/2,-500))
            spike1=spikes.get_rect(bottomleft=platform_rect.topleft)
            spike2=spikes.get_rect(bottomright=(1550,750))
            boss_x_vel=0
            boss_y_vel=0
            playerbullets=[]
            bossHP=100

            cooldown=0
            death=False
            bul_del=5
            blast=pygame.mixer.Sound('game\\shoot.mp3')
            pew=pygame.mixer.Sound('game\\laser.mp3')




            def gun(pos):
                pygame.mixer.Sound.play(blast)
                diffx=player_rect.centerx-pos[0]
                diffy=player_rect.centery-pos[1]
                res=(diffx**2+diffy**2)**0.5
                try:
                    bul_vel=((diffx*bullet_velocity)/res,(diffy*bullet_velocity)/res)
                except:
                    # print("0 div err")
                    pass
                bullet_rotated=player_bullet.copy()
                try:
                    # angle=
                    angle=math.degrees(math.atan2(bul_vel[0],bul_vel[1]))
                except:
                    print("error")
                    # raise Exception
                # print("angle:",angle)
                bullet_rotated=rotocrop(bullet_rotated,angle)
                coords=list(player_rect.center)
                coords[0]-=38
                coords[1]-=38
                playerbullets.append([coords,bul_vel,bullet_rotated])
                


            #initializations
            snake_pos_list=[]


            bullet_velocity=20
            left_heal=False
            right_heal=False
            start=False
            mus_start=False
            floorvelocity=7
            playerxvelocity=playeryvelocity=bossxmove=bossymove=bossmovetime=0
            floor=750
            jump=0
            xacc =0
            gravity=0.75
            drag=0.75
            delay=fpstime=time.time()
            adown=ddown=spdown=sdown=False
            playerhealth=1000
            immunity=False
            immunetime=time.time()
            gametick=fpstick=0
            FPS=60
            bossxfinal=bossyfinal=0
            angle=10
            laser_warning_set=[]
            laser_set=[]
            small_laser_set=[]
            fireballs_rect_set=[]
            for i in range(360):
                small_laser_set.append(pygame.transform.rotate(small_laser,i))

            laser_index=0
            delay=0
            shoot=False
            end_angle=0
            sun_dance_angle=0
            fireballs_speed_set=[]
            for i in range(100):
                fireballs_rect_set.append(fireball.get_rect(midbottom=(random.randint(0,1550),-(random.randint(50,3000)))))
                fireballs_speed_set.append(5)
            torchshoot=True
            mid_torch=0
            ################################################################################d###################################################################################################################
            fighttime=208*60
            ###################################################################################################################################################################################################
            random_tackle_coords=[]
            for i in range(50):
                random_tackle_coords.append((random.randint(0,300),random.randint(0,610)))
                random_tackle_coords.append((random.randint(1250,1550),random.randint(0,610)))
            random_tackle_index=0
            skewer_set=[]
            circle_projectile_set1=[]
            circle_projectile_set_randomiser=[]
            for i in range(11):
                skewer_set.append(skewer.get_rect(bottomleft=(i*150,0)))
            skewer_target=player_rect.centerx
            skewerspeed_set=[0,0,0,0,0,0,0,0,0,0,0]
            skewer_true_speed_set=[0,0,0,0,0,0,0,0,0,0,0]
            skewer_delay_set=[0,0,0,0,0,0,0,0,0,0,0]
            target2=player_rect.center
            for i in range(8):
                circle_projectile_set1.append(circle_projectile.get_rect(center=(-100,-100)))
            temp_angle=0
            bullet_set=[]
            bullet_move=[]
            for i in range(50):
                bullet_set.append(bullet.get_rect(center=(1550/2,550)))
                bullet_move.append((0,0))
            bullet_index=bullet_shoot_index=0
            rand_skew_set=[]
            for i in range(10):
                rand_skew_set.append(75+(150*i))
            rand_skew_index=0

            snake_set=[]
            for i in range(20):
                snake_set.append(boss.get_rect(center=(-200,-200)))


            hits=0
            bossdrag=0.8

            won=False



            #functions


            def calc_dir(A, B):
                """
                Calculate the normalized direction vector from point A to point B.

                Args:
                A: tuple or list, point A (x1, y1).
                B: tuple or list, point B (x2, y2).

                Returns:
                tuple, direction vector (dx, dy).
                """
                # Calculate the difference in x and y components
                dx = B[0] - A[0]
                dy = B[1] - A[1]
                
                # Calculate the magnitude of the vector
                magnitude = math.sqrt(dx**2 + dy**2)
                
                # Normalize the vector (avoid division by zero)
                if magnitude == 0:
                    return (0, 0)
                
                direction_x = dx / magnitude
                direction_y = dy / magnitude
                
                return direction_x, direction_y

            def calc_vel(p1, p2, t, velocity_loss=bossdrag):
                if t<5:
                    t=5
                x1,y1=calc_dir(p2,p1)
                return x1*((dist(p1,p2)+(0.5*velocity_loss*t*t))/t),y1*((dist(p1,p2)+(0.5*velocity_loss*t*t))/t)
            def damage(x):
                global playerhealth
                global immunetime
                global immunity
                global hits
                if not immunity:
                    playerhealth-=x
                    if x>0:
                        hits+=1
                        damage1.play()
                    immunetime=time.time()
                    immunity=True
            explosions=[]
            ex_t=10
            def explode(pos):
                pos=pos[0]-165,pos[1]-200
                # newblit(explosion,pos)
                explosions.append([ex_t,list(pos),explosion.copy()])
            def boss_move(time,x,y,relativity):
                # if time<5:
                #     time=5
                time=time*FPS
                # global bossxmove 
                # global bossymove
                global bossmovetime
                global bossxfinal
                global bossyfinal
                global boss_x_vel
                global boss_y_vel
                bossmovetime=time
                p2=boss_rect.center
                if relativity==True:
                    bossxfinal=player_rect.centerx+x
                    bossyfinal=player_rect.centery+y
                    p1=(player_rect.centerx+x,player_rect.centery+y)    
                else:
                    bossxfinal=x
                    bossyfinal=y
                    p1=(x,y)
                boss_x_vel,boss_y_vel=calc_dir(p1,p2)
                ratio=dist(p1,p2)/time
                boss_x_vel*=ratio
                boss_y_vel*=ratio

                
            def get_coords_from_angle(pos1, angle):

                # Convert the angle to radians
                angle_rad = math.radians(angle)

                # Calculate the coordinates of the new position
                x2 = pos1[0] + 100 * math.cos(angle_rad)
                y2 = pos1[1] + 100 * math.sin(angle_rad)

                return (x2, y2)

            def laser_blit(coords,set,angle,centered):
                # pygame.mixer.Sound.play(pew)
                angle=angle%360
                if set==small_laser_set:            
                    if centered==True:
                        newblit(set[angle],(coords[0]-(set[angle].get_width()/2),coords[1]-(set[angle].get_height()/2)))
                    elif centered==False:
                        if 90<=angle<270:
                            x=coords[0]-(set[angle].get_width())
                            x+=abs((math.sin(math.radians(angle)))*73/2)
                        else:
                            x=coords[0]
                            x-=abs((math.sin(math.radians(angle)))*73/2)
                        if 0<=angle<180:
                            y=coords[1]-(set[angle].get_height())
                            y+=abs((math.cos(math.radians(angle)))*73/2)
                        else:
                            y=coords[1]
                            y-=abs((math.cos(math.radians(angle)))*73/2)
                        newblit(set[angle],(x,y))
                elif set==laser_set:
                    angle=angle+90
                    if centered:
                        for i in range(2):
                            pos1=coords
                            pos2=get_coords_from_angle(coords,angle+180)
                                # Calculate the direction of the line
                            dx = pos2[0] - pos1[0]
                            dy = pos2[1] - pos1[1]
                            # Calculate the points where the line intersects the screen boundaries
                            screen_width, screen_height = 1650,910

                            if dx == 0:  # Vertical line
                                if dy > 0:
                                    end_pos = (pos1[0], screen_height)
                                else:
                                    end_pos = (pos1[0], -100)
                            elif dy == 0:  # Horizontal line
                                if dx > 0:
                                    end_pos = (screen_width, pos1[1])
                                else:
                                    end_pos = (-100, pos1[1])
                            else:
                                if dx > 0:
                                    x1 = screen_width
                                    y1 = pos1[1] + (screen_width - pos1[0]) * dy / dx
                                else:
                                    x1 = -100
                                    y1 = pos1[1] + (-100 - pos1[0]) * dy / dx

                                if dy > 0:
                                    y2 = screen_height
                                    x2 = pos1[0] + (screen_height - pos1[1]) * dx / dy
                                else:
                                    y2 = -100
                                    x2 = pos1[0] + (-100 - pos1[1]) * dx / dy

                                if 0 <= y1 <= screen_height:
                                    end_pos = (x1, y1)
                                else:
                                    end_pos = (x2, y2)

                            # Draw the extended line
                            drawline(screen, (255,1,1) , clbrtpos(pos1), clbrtpos(end_pos), 50*scale_factor)
                            drawline(screen, (255,255,254) , clbrtpos(pos1), clbrtpos(end_pos), 35*scale_factor)
                            drawline(screen, (255,1,1) , clbrtpos(pos1), clbrtpos(end_pos), 30*scale_factor)
                            drawline(screen, (0,1,0) , clbrtpos(pos1), clbrtpos(end_pos), 20*scale_factor)
                            angle+=180
                        posset=[same(tuple(player_rect.center)),same((player_rect.left-1,player_rect.bottom+1)),same((player_rect.right+1,player_rect.bottom+1)),same((player_rect.left-1,player_rect.top-1)),same((player_rect.right+1,player_rect.top-1))]
                        for i in posset:
                            try:
                                if list(get_at(i))[:3] == [0,1,0]:
                                    damage(2.5)
                            except Exception as e:
                                # print(e)
                                pass
                        return
                    
                    pos1=coords
                    pos2=get_coords_from_angle(coords,angle)
                        # Calculate the direction of the line
                    dx = pos2[0] - pos1[0]
                    dy = pos2[1] - pos1[1]
                    # Calculate the points where the line intersects the screen boundaries
                    screen_width, screen_height = 1650,910

                    if dx == 0:  # Vertical line
                        if dy > 0:
                            end_pos = (pos1[0], screen_height)
                        else:
                            end_pos = (pos1[0], -100)
                    elif dy == 0:  # Horizontal line
                        if dx > 0:
                            end_pos = (screen_width, pos1[1])
                        else:
                            end_pos = (-100, pos1[1])
                    else:
                        if dx > 0:
                            x1 = screen_width
                            y1 = pos1[1] + (screen_width - pos1[0]) * dy / dx
                        else:
                            x1 = -100
                            y1 = pos1[1] + (-100 - pos1[0]) * dy / dx

                        if dy > 0:
                            y2 = screen_height
                            x2 = pos1[0] + (screen_height - pos1[1]) * dx / dy
                        else:
                            y2 = -100
                            x2 = pos1[0] + (-100 - pos1[1]) * dx / dy

                        if 0 <= y1 <= screen_height:
                            end_pos = (x1, y1)
                        else:
                            end_pos = (x2, y2)

                    # Draw the extended line
                    drawline(screen, (255,0,0) , clbrtpos(pos1), clbrtpos(end_pos), 20*scale_factor)

            def shoot_laser(pos1, pos2):
                pygame.mixer.Sound.play(pew)
                # Calculate the direction of the line
                dx = pos2[0] - pos1[0]
                dy = pos2[1] - pos1[1]
                # Calculate the points where the line intersects the screen boundaries
                screen_width, screen_height = 1650,910

                if dx == 0:  # Vertical line
                    if dy > 0:
                        end_pos = (pos1[0], screen_height)
                    else:
                        end_pos = (pos1[0], -100)
                elif dy == 0:  # Horizontal line
                    if dx > 0:
                        end_pos = (screen_width, pos1[1])
                    else:
                        end_pos = (-100, pos1[1])
                else:
                    if dx > 0:
                        x1 = screen_width
                        y1 = pos1[1] + (screen_width - pos1[0]) * dy / dx
                    else:
                        x1 = -100
                        y1 = pos1[1] + (-100 - pos1[0]) * dy / dx

                    if dy > 0:
                        y2 = screen_height
                        x2 = pos1[0] + (screen_height - pos1[1]) * dx / dy
                    else:
                        y2 = -100
                        x2 = pos1[0] + (-100 - pos1[1]) * dx / dy

                    if 0 <= y1 <= screen_height:
                        end_pos = (x1, y1)
                    else:
                        end_pos = (x2, y2)

                # Draw the extended line
                drawline(screen, (255,1,1) , clbrtpos(pos1), clbrtpos(end_pos), 50*scale_factor)
                drawline(screen, (255,255,254) , clbrtpos(pos1), clbrtpos(end_pos), 35*scale_factor)
                drawline(screen, (255,1,1) , clbrtpos(pos1), clbrtpos(end_pos), 30*scale_factor)

                drawline(screen, (0,1,0) , clbrtpos(pos1), clbrtpos(end_pos), 20*scale_factor)
                posset=[same(tuple(player_rect.center)),same((player_rect.left-1,player_rect.bottom+1)),same((player_rect.right+1,player_rect.bottom+1)),same((player_rect.left-1,player_rect.top-1)),same((player_rect.right+1,player_rect.top-1))]
                for i in posset:
                    try:
                        if list(get_at(i))[:3] == [0,1,0]:
                            damage(2.5)
                    except Exception as e:
                        # print(e)
                        pass



            def shoot_laser_warning(pos1, pos2):
                # Calculate the direction of the line
                dx = pos2[0] - pos1[0]
                dy = pos2[1] - pos1[1]
                # Calculate the points where the line intersects the screen boundaries
                screen_width, screen_height = 1650,910

                if dx == 0:  # Vertical line
                    if dy > 0:
                        end_pos = (pos1[0], screen_height)
                    else:
                        end_pos = (pos1[0], -100)
                elif dy == 0:  # Horizontal line
                    if dx > 0:
                        end_pos = (screen_width, pos1[1])
                    else:
                        end_pos = (-100, pos1[1])
                else:
                    if dx > 0:
                        x1 = screen_width
                        y1 = pos1[1] + (screen_width - pos1[0]) * dy / dx
                    else:
                        x1 = -100
                        y1 = pos1[1] + (-100 - pos1[0]) * dy / dx

                    if dy > 0:
                        y2 = screen_height
                        x2 = pos1[0] + (screen_height - pos1[1]) * dx / dy
                    else:
                        y2 = -100
                        x2 = pos1[0] + (-100 - pos1[1]) * dx / dy

                    if 0 <= y1 <= screen_height:
                        end_pos = (x1, y1)
                    else:
                        end_pos = (x2, y2)

                # Draw the extended line
                drawline(screen, (255,0,0) , clbrtpos(pos1), clbrtpos(end_pos), 20*scale_factor)


            def clbrtpos(pos):
                x,y=pos
                return (x*scale_factor,y*scale_factor)
            def unclbrt(pos):
                x,y=pos
                return (x/scale_factor,y/scale_factor)

            def skew(xpos,speed,delay):
                global skewerspeed_set
                global skewer_delay_set
                skewerspeed_set[(xpos%1600)//150]=750/(speed*60)
                skewer_delay_set[(xpos%1600)//150]=delay*60
                

            # def calculate_circle_points(radius, num_points):
            radius=25
            num_points=50
            circle_points = []
            angle_increment = 360 / num_points

            for i in range(num_points):
                angle_rad = math.radians(i * angle_increment)
                x_ = int(radius * math.cos(angle_rad))
                y_ = int(radius * math.sin(angle_rad))
                circle_points.append((x_, y_))

            # return circle_points

            death_particles=[]
            trail=[]
            for i in range(50):
                death_particles.append([star.copy(),[-100,-100],circle_points[i]])
                trail.append([-100,-100])


            count2=0




            pause=False

            scoretime=0


            attacklist={}

            while True:
                
                if count2>0:
                    count2+=1
                    if count2>3*60:
                        pygame.quit()
                        break

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        superbreak=True
                        w_l="Lost"
                        break
                        # exit()
                    if event.type == pygame.KEYDOWN and won==False:
                        if event.key == pygame.K_SPACE:
                            #jump
                            if jump==0 and player_rect.bottom!=floor:
                                playeryvelocity=-15
                                jump=1
                            spdown=True
                        if event.key == pygame.K_a or event.key==pygame.K_LEFT:
                            adown=True
                        if event.key == pygame.K_d or event.key==pygame.K_RIGHT:
                            ddown=True
                        if event.key==pygame.K_s or event.key==pygame.K_DOWN:
                            sdown=True
                        if event.key==pygame.K_p:
                            pause=not pause
                        if event.key==pygame.K_KP_ENTER or event.key==pygame.K_RETURN :
                            # print('start and muted',start,muted)
                            if not start and not muted and not mus_start:
                                background_music.play(loops=-1)
                                mus_start=True
                            start=True
                    if event.type ==pygame.KEYUP :
                        if event.key == pygame.K_SPACE:
                            spdown=False
                        if event.key== pygame.K_a or event.key==pygame.K_LEFT:
                            adown=False
                        if event.key== pygame.K_d or event.key==pygame.K_RIGHT:
                            ddown=False
                        if event.key== pygame.K_s or event.key==pygame.K_DOWN:
                            sdown=False
                    if event.type == pygame.MOUSEBUTTONDOWN and not pause and won==False:
                        if event.button==1 and cooldown==0:
                            gun(unclbrt(list(pygame.mouse.get_pos())))
                            cooldown=bul_del
                if superbreak:
                    break
                if not pause :     
                    #time
                    gametime=time.time()
                    gametick+=1
                    # print(fighttime)
                    if start:
                        scoretime+=1
                        fighttime+=1
                    else:
                        bossHP=100
                    fpstick+=1
                    #jump    
                    if player_rect.bottom==floor:
                        jump=0
                    #keydowns
                    if adown:
                        playerxvelocity-=1
                    if ddown:
                        playerxvelocity+=1
                        #jump
                    if spdown and player_rect.bottom==floor:
                        playeryvelocity-=15
                    if sdown and time.time()-delay>0.5 and player_rect.bottom==floor:
                        floor=750
                        delay=time.time()
                        
                    if cooldown>0:
                        cooldown-=1

                    #healthbar:
                    if playerhealth<0:
                        gameover=pygame.image.load("Game/graphics/loss.png").convert_alpha()
                        count2+=1
                        playerhealth=0
                    if playerhealth>100:
                        playerhealth=100
                    healthbar_rect.left=-(100-playerhealth)*6.96
                    bossbar_rect.right=1550+((100-bossHP)*6.96)

                    #boundaries
                    if player_rect.right>1550:
                        player_rect.right=1550
                    if player_rect.left<0:
                        player_rect.left=0
                    if player_rect.top<0:
                        player_rect.top=0
                        playeryvelocity=1

                    #drag    
                    if not(adown or ddown):    
                        if abs(playerxvelocity)>0.3:
                            playerxvelocity-= drag*(playerxvelocity/abs(playerxvelocity))
                        else:
                            playerxvelocity=0

                    #Gravity and floor working    
                    if player_rect.bottom>floor:
                        player_rect.bottom=floor
                        playeryvelocity=0
                    elif player_rect.bottom<floor:
                        playeryvelocity+=gravity


                    #floating platform solidifier
                    if (not sdown) and time.time()-delay>0.3:
                        if floating_platform4_rect.right>player_rect.left and player_rect.right>floating_platform4_rect.left and player_rect.centery<floating_platform4_rect.top:
                            floor=floating_platform4_rect.top 
                            if player_rect.bottom==floating_platform4_rect.top:
                                player_rect.centerx+=floorvelocity
                        elif floating_platform3_rect.right>player_rect.left and player_rect.right>floating_platform3_rect.left and player_rect.centery<floating_platform3_rect.top:
                            floor=floating_platform3_rect.top 
                        elif player_rect.right>floating_platform2_rect.left and player_rect.centery<floating_platform2_rect.top:
                            floor=floating_platform2_rect.top        
                        elif player_rect.left<floating_platform1_rect.right and player_rect.centery<floating_platform1_rect.top:
                            floor=floating_platform1_rect.top
                        else:
                            floor=750


                    #moving platform

                    floating_platform4_rect.left+=floorvelocity
                    if abs(floating_platform4_rect.right-400)<5:
                        floorvelocity=-7
                    if abs(floating_platform4_rect.left-1200)<5:
                        floorvelocity=7
                    if floating_platform4_rect.right<-10:
                        floating_platform4_rect.left=1550
                    if floating_platform4_rect.left>1560:
                        floating_platform4_rect.right=0    

                    #immuntiy
                    if gametime-immunetime>1:
                        immunity=False

                    #player xvelocity limit

                    if abs(playerxvelocity)>10:
                        playerxvelocity=10*(abs(playerxvelocity)/playerxvelocity)
                    if abs(playerxvelocity)<0.5:
                        playerxvelocity=0
                    player_rect.left+=playerxvelocity
                    player_rect.bottom+=playeryvelocity
                    #move boss
                    if bossmovetime>1:
                        bossmovetime-=1
                    boss_rect.centerx-=boss_x_vel
                    boss_rect.centery-=boss_y_vel
                    if bossmovetime<=1:

                        boss_x_vel*=bossdrag
                        boss_y_vel*=bossdrag
                    for i in range(len(skewerspeed_set)):
                        if skewer_delay_set[i]!=0:
                            skewer_delay_set[i]-=1
                        if skewer_delay_set[i]==1:
                            skewer_true_speed_set[i]=skewerspeed_set[i]
                        if skewer_set[i].bottom>platform_rect.top:
                            skewer_true_speed_set[i]*=-1 
                            explode(skewer_set[i].midbottom)
                        skewer_set[i].centery+=skewer_true_speed_set[i]
                        if skewer_set[i].bottom<0:
                            skewer_set[i].bottom=0
                            skewer_true_speed_set[i]=0
                            skewerspeed_set[i]=0
                        
                    #boss touch damage
                        

                    if abs(player_rect.centerx-boss_rect.centerx)**2+abs(player_rect.centery-boss_rect.centery)**2<115**2 and fighttime<263*60:
                        damage(5)

                    #check FPS

                    if time.time()-fpstime>2:
                        fpstime=time.time()
                        fpstick=0
                    newblit(space_surface,(0,0))
                    newblit(floating_platform1,floating_platform1_rect)
                    newblit(floating_platform2,floating_platform2_rect)
                    newblit(floating_platform3,floating_platform3_rect)
                    newblit(floating_platform4,floating_platform4_rect)
                    newblit(platform,platform_rect)
                    for v in range(len(playerbullets)):
                        try:
                            bul_pos,bul_vel,bul_img=playerbullets[v]
                            bul_pos[0]-=bul_vel[0]
                            bul_pos[1]-=bul_vel[1]
                            playerbullets[v]=[bul_pos,bul_vel,bul_img]
                            newblit(bul_img,bul_pos)
                            if dist(bul_pos,list(boss_rect.center))<150:
                                bossHP-=bullet_damage
                                if random.randint(1,100)==3:
                                    heal_rect.center=boss_rect.center
                                del playerbullets[v]
                            if 0>bul_pos[0]>1600 or 0>bul_pos[1]>850:
                                del playerbullets[v]
                        except:
                            pass
                    for i in range(len(explosions)):
                        try:
                            if explosions[i][0]>0:
                                explosions[i][0]-=1
                                newblit(explosions[i][2],explosions[i][1])
                            else:
                                del explosions[i]
                        except:
                            pass
                    #fight
                    newblit(heal_ball,heal_rect)
                    if dist(player_rect.center,heal_rect.center)<100:
                        playerhealth+=5
                        heal_rect.center=(-100,-100)

                    #ap laser-1:1-15
                    if fighttime==1*60:
                        boss_move(2,1550/2,500,False)
                        # pass
                    if fighttime%5==0 and 5*60<fighttime<15*60:
                        boss_move(2,0,0,True) 
                    if 5*60<fighttime<15*60 :
                        if 0<fighttime%100<20:
                            shoot_laser_warning(boss_rect.center,player_rect.center)
                            target=player_rect.center
                            delay=20
                        if delay>0:
                            delay-=1
                        if 10>delay>1:
                            shoot_laser(boss_rect.center,target)
                        # pass
                    
                    #ap follow 1:15-20

                    if 20*60>fighttime>15*60 :
                        boss_move(0.5,0,0,True)

                    #ap laser rapid: 20.1


                    if fighttime==20.1*60:
                        boss_move(0.5,1550/2,500,False)
                    if 22*60>fighttime>20*60:
                        shoot_laser_warning(boss_rect.center,player_rect.center)
                    if 27*60>fighttime>22*60:
                        if fighttime%10==0:
                            shoot=not shoot
                            if not shoot:
                                target=player_rect.center
                        if shoot:
                            shoot_laser(boss_rect.center,target)

                    #ap rapid follow 28-38
                    
                    if fighttime==28*60:

                        boss_move(0.5,0,0,True)
                    if fighttime==30*60:
                        boss_move(0.5,0,0,True)
                    if fighttime==32*60:
                        boss_move(0.3,0,0,True)
                    if fighttime==34*60:
                        boss_move(0.3,0,0,True)
                    if fighttime==36*60:
                        boss_move(0.5,0,0,True)
                    if fighttime==38*60:
                        boss_move(0.3,0,0,True)

                    #ap meteor shower 40-55

                    if fighttime==40*60:
                        boss_move(0.5,1550/2,-810/2,False)
                        try: del fireballs_rect_set
                        except:pass   
                        fireballs_rect_set=[]   
                        for i in range(100):
                            fireballs_rect_set.append(fireball.get_rect(midbottom=(random.randint(0,1550),-(random.randint(50,3000)))))
                    if 55*60>fighttime>41*60 or 190*60>fighttime>175*60 :
                        for i in range(len(fireballs_rect_set)):
                            newblit(fireball,fireballs_rect_set[i])
                            fireballs_rect_set[i].bottom+=fireballs_speed_set[i]
                            if fireballs_rect_set[i].bottom>0:
                                fireballs_speed_set[i]+=gravity
                            if fireballs_rect_set[i].top>1550:
                                fireballs_speed_set[i]=5
                        for i in fireballs_rect_set:
                            if (player_rect.centerx-i.midbottom[0])**2 + (player_rect.centery-i.midbottom[1])**2<1600:
                                damage(2.5)

                    #ap sun dance single 55-66

                    if fighttime==55*60:
                        boss_move(1,1550/2,500,False)
                    if 66*60>fighttime>56*60:
                        laser_blit(boss_rect.center,laser_set,sun_dance_angle,True)
                        if fighttime%2==0:
                            sun_dance_angle+=3
                        sun_dance_angle%=360


                    #ap random tackle +laser 66-80
                    if 80*60>fighttime>66*60:
                        if fighttime%(60)==0:
                            random_tackle_index+=1
                            random_tackle_index%=len(random_tackle_coords)
                            boss_move(0.5,random_tackle_coords[random_tackle_index][0],random_tackle_coords[(random_tackle_index+1)%len(random_tackle_coords)][1],False)
                            target2=player_rect.center
                        if fighttime%60>50 and fighttime>67*60:
                            shoot_laser(boss_rect.center,target2)

                    #ap skewer 1 81-90


                    if fighttime==81*60:
                        boss_move(0.1,1550/2,200,False)
                    if 90*60>fighttime>80*60 and fighttime%(0.5*60)==0:
                        skew(player_rect.centerx,0.5,0.2)
                    if 90*60>fighttime>80*60 or 210*60>fighttime>200*60 or 175*60>fighttime>165*60:
                        for i in range(len(skewer_set)):
                            newblit(skewer,skewer_set[i])
                            if player_rect.colliderect(skewer_set[i]):
                                damage(2.5)

                    #ap double sun dance 91-101
                    if fighttime==91*60:
                        boss_move(3,1550/2,475,False)
                    if 101*60>fighttime>91*60:
                        laser_blit(boss_rect.center,laser_set,sun_dance_angle,True)
                        laser_blit(boss_rect.center,laser_set,(sun_dance_angle+90)%360,True)
                        if fighttime%2==0:
                            sun_dance_angle+=3
                        sun_dance_angle%=360
            #ap simple follow 
                    if fighttime%5==0 and 101*60<fighttime<110*60:
                        boss_move(0.5,0,0,True) 

            #ap circle projectile

                    if fighttime==111*60:
                        boss_move(0.5,1550/2,810/2,False) 
                        pass
                        for i in range(len(circle_projectile_set1)):
                            circle_projectile_set1[i].center=(1550/2,500)
                    if 115*60>fighttime>112*60:
                        circle_projectile_set1[0].centerx+=10
                        circle_projectile_set1[0].centery+=0
                        circle_projectile_set1[1].centerx-=10
                        circle_projectile_set1[1].centery+=0
                        circle_projectile_set1[2].centery+=10
                        circle_projectile_set1[2].centerx+=0
                        circle_projectile_set1[3].centery-=10
                        circle_projectile_set1[3].centerx+=0
                        circle_projectile_set1[4].centerx+=10
                        circle_projectile_set1[4].centery+=10
                        circle_projectile_set1[5].centerx-=10
                        circle_projectile_set1[5].centery-=10
                        circle_projectile_set1[6].centerx+=10
                        circle_projectile_set1[6].centery-=10
                        circle_projectile_set1[7].centerx-=10
                        circle_projectile_set1[7].centery+=10
                        for i in circle_projectile_set1:
                            newblit(circle_projectile,i)
                            if (player_rect.centerx-i.centerx)**2+(player_rect.centery-i.centery)**2<1600:
                                damage(2.5)
                            if i[0]>1700 or i[0]<-200:
                                for i in range(len(circle_projectile_set1)):
                                    circle_projectile_set1[i].center=boss_rect.center
                    if fighttime==115*60:
                        try: del circle_projectile_set_randomiser
                        except:pass
                        circle_projectile_set_randomiser=[]
                        for i in range(16):
                            circle_projectile_set_randomiser.append(random.randint(5,15)*random.sample([1,-1],2)[0])
                    if 125*60>fighttime>115*60:
                        circle_projectile_set1[0].centerx+=circle_projectile_set_randomiser[0]
                        circle_projectile_set1[0].centery+=circle_projectile_set_randomiser[1]
                        circle_projectile_set1[1].centerx-=circle_projectile_set_randomiser[2]
                        circle_projectile_set1[1].centery+=-circle_projectile_set_randomiser[3]
                        circle_projectile_set1[2].centery+=circle_projectile_set_randomiser[4]
                        circle_projectile_set1[2].centerx+=-circle_projectile_set_randomiser[5]
                        circle_projectile_set1[3].centery-=circle_projectile_set_randomiser[6]
                        circle_projectile_set1[3].centerx+=circle_projectile_set_randomiser[7]
                        #diagonals
                        circle_projectile_set1[4].centerx+=circle_projectile_set_randomiser[8]
                        circle_projectile_set1[4].centery+=circle_projectile_set_randomiser[9]
                        circle_projectile_set1[5].centerx-=circle_projectile_set_randomiser[10]
                        circle_projectile_set1[5].centery-=circle_projectile_set_randomiser[11]
                        circle_projectile_set1[6].centerx+=circle_projectile_set_randomiser[12]
                        circle_projectile_set1[6].centery-=circle_projectile_set_randomiser[13]
                        circle_projectile_set1[7].centerx-=circle_projectile_set_randomiser[14]
                        circle_projectile_set1[7].centery+=circle_projectile_set_randomiser[15]
                        for i in circle_projectile_set1:
                            newblit(circle_projectile,i)
                            if (player_rect.centerx-i.centerx)**2+(player_rect.centery-i.centery)**2<1600:
                                damage(2.5)
                            if i[0]<1700 and i[0]>-200:
                                continue
                            else:
                                for i in range(len(circle_projectile_set1)):
                                    circle_projectile_set1[i].center=boss_rect.center
                                try: del circle_projectile_set_randomiser
                                except:pass
                                circle_projectile_set_randomiser=[]
                                for i in range(16):
                                    circle_projectile_set_randomiser.append(random.randint(5,15)*random.sample([1,-1],2)[0])
                    if fighttime==127*60:
                        fighttime= 140*60
                        #fighttime changing

                    #ap triple sun dance

                    if fighttime==143.5*60:
                        boss_move(1,1550/2,500,False)

                    if 155*60>fighttime>145*60:
                        if 155*60>fighttime>148*60:
                            laser_blit(boss_rect.center,laser_set,sun_dance_angle,True)
                            laser_blit(boss_rect.center,laser_set,(sun_dance_angle+120)%360,True)
                            laser_blit(boss_rect.center,laser_set,(sun_dance_angle+240)%360,True)
                        if 148*60>fighttime>145*60:
                            laser_blit(boss_rect.center,laser_warning_set,sun_dance_angle,True)
                            laser_blit(boss_rect.center,laser_warning_set,(sun_dance_angle+120)%360,True)
                            laser_blit(boss_rect.center,laser_warning_set,(sun_dance_angle+240)%360,True)
                        
                        if fighttime%100>50:
                            sun_dance_angle+=1
                        else:
                            sun_dance_angle-=1
                        sun_dance_angle%=360

                    #ap general grevious

                    if 165*60>fighttime>155*60 or 260*60>fighttime>250*60 :
                        boss_move(0.7,0,0,True)
                        
                        temp_angle+=2
                        for i in range(0,180,20):
                            laser_blit(boss_rect.center,small_laser_set,temp_angle+i,True)
                        if abs(player_rect.centerx-boss_rect.centerx)**2+abs(player_rect.centery-boss_rect.centery)**2<150**2:
                            damage(5)

                    #ap ground spikes activated

                    if fighttime>165*60:
                        newblit(spikes,spike1)
                        newblit(spikes,spike2)
                        if player_rect.colliderect(spike1) or player_rect.colliderect(spike2):
                            damage(2.5)

                    
                #ap slow skew
                    if fighttime==165*60:
                        boss_move(1,-100,-100,False)
                    if 175*60>fighttime>165*60 and fighttime%(1.5*60)==0:
                        skew(player_rect.centerx,0.5,0.2)
                #ap fast fireball
                    if fighttime==175*60:
                        boss_move(0.5,1550/2,-810/2,False)
                        try: del fireballs_rect_set
                        except: pass 
                        fireballs_rect_set=[]
                        for i in range(100):
                            fireballs_rect_set.append(fireball.get_rect(midbottom=(random.randint(0,1550),-(random.randint(50,3000)))))   

                    if fighttime==185*60:
                        boss_move(1.5,1550/2,500,False)
                    if fighttime==186.5*60 :
                        for i in bullet_set:
                            # bullet_shoot_index+=1
                            bullet_set[bullet_shoot_index].center=boss_rect.center
                            bullet_shoot_index+=1
                        else:
                            bullet_shoot_index=0
                    if 195*60>fighttime>186.5*60:
                        if fighttime%10==0:
                            vel_vect=(boss_rect.centerx-player_rect.centerx,boss_rect.centery-player_rect.centery)
                            vec_dx,vec_dy=vel_vect
                            scal=bullet_velocity/(vec_dx**2+vec_dy**2)**0.5
                            bullet_move[bullet_index]=((boss_rect.centerx-player_rect.centerx)*scal,(boss_rect.centery-player_rect.centery)*scal)
                            bullet_index+=1
                            bullet_index%=len(bullet_move)
                        
                    if fighttime>186.5*60:
                        for i in bullet_set:
                            if not -100>i.centerx>1600:
                                bullet_set[bullet_shoot_index].centerx-=bullet_move[bullet_shoot_index][0]
                                bullet_set[bullet_shoot_index].centery-=bullet_move[bullet_shoot_index][1]
                                bullet_shoot_index+=1
                                bullet_shoot_index%=len(bullet_set)
                        else:
                            bullet_shoot_index=0
                        for i in bullet_set:
                            if not -100>i.centerx>1600:
                                newblit(bullet,i)
                                if player_rect.colliderect(i):
                                    damage(2.5)

                    #ap random skew
                    if fighttime==195*60:
                        fighttime=200*60
                    if 210*60>fighttime>200*60:
                        if fighttime%(60)==0:
                            ra=random.randint(1,1550)
                            rb=random.randint(1,1550)
                            rc=random.randint(1,1550)
                            rd=random.randint(1,1550)
                            re=random.randint(1,1550)
                            skew(ra,0.2,1)
                            skew(rb,0.2,1)
                            skew(rc,0.2,1)
                            skew(rd,0.2,1)
                            skew(re,0.2,1)
                        if fighttime%60<40 and fighttime>201.5*60:
                            newblit(skew_warning,(ra-(ra%150),750-35))
                            newblit(skew_warning,(rb-(rb%150),750-35))
                            newblit(skew_warning,(rc-(rc%150),750-35))
                            newblit(skew_warning,(rd-(rd%150),750-35))
                            newblit(skew_warning,(re-(re%150),750-35))
                        
                    #ap jailtype lasers

                    if 220*60>fighttime>210*60:
                        if fighttime<211*60:
                            for i in range(0,1550,155):
                                shoot_laser_warning((i,-50),(i,810))
                        elif fighttime<213*60:
                            for i in range(0,1550,155):
                                shoot_laser((i,-50),(i,810))
                        if 214*60<fighttime<215*60:
                            for i in range(50,1550,155):
                                shoot_laser_warning((i,-50),(i,810))
                        elif 215*60<fighttime<218*60:
                            for i in range(50,1550,155):
                                shoot_laser((i,-50),(i,810))
                        if 218*60<fighttime<219*60:
                            for i in range(75,1550,155):
                                shoot_laser_warning((i,-50),(i,810))
                        elif 219*60<fighttime<220*60:
                            for i in range(75,1550,155):
                                shoot_laser((i,-50),(i,810))
                    #ap snake
                    if fighttime==221*60:
                        boss_move(0.5,1550/2,-200,False)
                    if fighttime==223*60:
                        boss_pos_v=boss_rect.center
                        snake_pos_list=[deepcopy(boss_rect)]
                        for i in range(len(snake_set)-1):
                            i2=deepcopy(boss_rect)
                            i2.center=(i2.center[0]+((i+1)*250),i2.center[1])
                            snake_pos_list.append(i2)
                    if 250*60>fighttime>225*60:
                        snake_speed=dist(boss_pos_v,boss_rect.center)
                        if snake_speed>0:
                            for i in range(len(snake_pos_list)-1,0,-1):
                                snake_pos_list[i].center=get_move_pos(i,snake_speed*((100-i)/100)) #dampening
                            snake_pos_list[0].center=get_move_pos(0,snake_speed)
                        for i in range(-1,-len(snake_set),-1):
                            newblit(snake_body,snake_pos_list[i])
                            if (player_rect.centerx-snake_pos_list[i].centerx)**2 + (player_rect.centery-snake_pos_list[i].centery)**2 < 155**2:
                                damage(2.5)
                        newblit(boss,boss_rect)
                        boss_pos_v=boss_rect.center[:]
                    if fighttime==225*60:
                        random_tackle_index=0
                        target2=player_rect.center
                    if 235*60>fighttime>225*60:
                        if fighttime%(60)==0:
                            random_tackle_index+=1
                            random_tackle_index%=len(random_tackle_coords)
                            boss_move(0.5,random_tackle_coords[random_tackle_index][0],random_tackle_coords[(random_tackle_index+1)%len(random_tackle_coords)][1],False)
                            target2=player_rect.center
                        if fighttime%60>50 and fighttime>67*60:
                            shoot_laser(boss_rect.center,target2)
                    if fighttime==236*60:
                        boss_move(1,3000,800,False)
                    if fighttime==240*60:
                        boss_move(1,-1500,800,False)
                    if fighttime==242*60:
                        boss_move(1,1600,550,False)
                    if fighttime==244*60:
                        boss_move(1,-1500,550,False)
                    if fighttime==246*60:
                        boss_move(1,1550/2,375,False)
                    if fighttime==248*60:
                        boss_move(1,1550/2,-4375,False)
                    if 260*60>fighttime>250*60 and fighttime%(3*60)==0:  
                        boss_move(0.5,0,0,True)
                    if fighttime==260*60:
                        boss_move(0.5,1550/2,500,False)
                    if fighttime==266*60:
                        boss_move(3,1550/2,950,False)
                        immunity=True
                    if bossHP<0 and not death:
                        won=True
                        immunity=True
                        fighttime=0
                        death=True
                        count=0
                        trans = pygame.Surface((1550*scale_factor,810*scale_factor), pygame.SRCALPHA)
                        trans.fill((0, 0, 0, 0))
                        for i in range(len(death_particles)):
                            death_particles[i][1]=list(boss_rect.center)
                            trail[i]=list(boss_rect.center)
                    if death:
                        trans.fill((0, 0, 0, 0))
                        print(count)
                        count+=1
                        for i in range(len(death_particles)):
                            pos_1=death_particles[i][1]
                            pos_1[0]+=death_particles[i][2][0]
                            pos_1[1]+=death_particles[i][2][1]
                            death_particles[i][1]=pos_1
                            if count>5:
                                pos_2=trail[i]
                                pos_2[0]+=death_particles[i][2][0]
                                pos_2[1]+=death_particles[i][2][1]
                                trail[i]=pos_2
                                pygame.draw.line(trans, (255, 255, 0, 255), clbrtpos(trail[i]), clbrtpos(death_particles[i][1]), 10)
                                pygame.draw.line(trans, (255, 255, 255, 255), clbrtpos(trail[i]), clbrtpos(death_particles[i][1]), 5)
                                temp=list(clbrtpos(death_particles[i][1]))
                                temp[0]-=25
                                temp[1]-=25
                                trans.blit(death_particles[i][0],temp)
                        screen.blit(trans,(0,0))
                        if count>180:
                            fighttime=271*60
                            won=None
                    if count>210:
                        pygame.quit()
                        break
                    if fighttime<263*60:
                        newblit(healthbar,healthbar_rect)
                        newblit(bossbar,bossbar_rect)
                        newblit(platform,platform_rect)
                        newblit(boss,boss_rect)
                    else:
                        newblit(boss,boss_rect)
                        newblit(bossbar,bossbar_rect)
                        newblit(healthbar,healthbar_rect)
                        newblit(platform,platform_rect)         
                    if immunity==False:
                        playerblit(damage=False)
                        # if playerxvelocity==0 and playeryvelocity==0:
                        #     playerblit(player,player_rect)
                        # else:
                        #     if playerxvelocity>0:
                        #         playerblit(player2,player_rect)
                        #     elif playerxvelocity<0:
                        #         playerblit(player4,player_rect)
                        #     else:
                        #         playerblit(player,player_rect)
                    if immunity==True and fighttime>263*60:
                        pass
                    elif immunity==True and fighttime %5<3:
                        playerblit(damage=True)
                        # playerblit(player_damage,player_rect)
                        # if playerxvelocity==0 and playeryvelocity==0:
                        #     playerblit(player_damage,player_rect)
                        # else:
                        #     if playerxvelocity>0:
                        #         playerblit(player_damage_2,player_rect)
                        #     elif playerxvelocity<0:
                        #         playerblit(player_damage_4,player_rect)
                        #     else:
                        #         playerblit(player,player_rect)
                    newblit(gameover,(0,0))
                if won==True and not muted:
                    background_music.stop()
                if fighttime>263*60 and fighttime!=271*60:
                    fighttime=60
                    exec(initialisation_resetting_string)
                    continue
                    #resetting
                if won:
                    boss.fill((0,0,0,0))
                if won is None:
                    immunity=True
                    gameover=pygame.image.load("Game/graphics/win3.png").convert_alpha()
                elif won is False:
                    if fighttime%60<15:
                        boss=boss0
                    elif 15<fighttime%60<30:
                        boss=boss1
                    elif 30<fighttime%60<45:
                        boss=boss2
                    else:
                        boss=boss3
                if start==False:
                    newblit(instructions,(0,0))
                pygame.display.update()
                clock.tick(60)
            scoretime=round(scoretime/60,3)
            w_l=bossHP<=0
            if w_l:
                w_l="Won"
            else:
                w_l="Lost"
            current_date = datetime.now().date()
            print(f"\nGame Over!")
            print(f"Result: {w_l}")
            print(f"Time: {scoretime} seconds")
            print(f"Hits taken: {hits}")
            break
        except Exception as e:
            try:
                pygame.quit()
            except:
                pass
            if type(e)==FileNotFoundError:
                import os
                print(" Asset files not found, trying to change directory to find files ...")
                dirch=os.path.abspath(__file__)
                try:
                    dirch=dirch.split("\\")
                    dirch='\\'.join(dirch[:-1])
                    os.chdir(dirch)
                    print("directory changed")
                except:
                    try:
                        dirch=dirch.replace("\\","/")
                        dirch=dirch.split("/")
                        dirch='/'.join(dirch[:-1])
                        os.chdir(dirch)
                        print("directory changed")
                    except:
                        pass
                continue
            else:
                print("Unhandled excpetion:\n",type(e),'\n',e)
                break
    input("Press Enter to exit:")
except Exception as e:
    print(type(e),e,sep='\n')
    input("Enter to exit: ")
               