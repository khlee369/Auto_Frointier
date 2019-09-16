import cv2
import time
import matplotlib.pyplot as plt
import numpy as np
import sys
import win32api, win32con, win32gui
from util import *
from mss import mss

class NoxManager:
    def __init__(self, config):
        self.sct = mss()
        self.monitor = self.sct.monitors[0]
        self.nox_size = config['nox_size']
        self.nox_pos = self.get_nox_pos()
        # Double monitor Problem
        self.nox_pos[0] += self.monitor['top']
        self.nox_pos[1] += self.monitor['left']
        # Double monitor Problem
        self.nox_monitor = self.get_nox_monitor()
        
        self.get_main_menu_pos()
        
    def get_nox_pos(self):
        print('-------------------------------------')
        input('Run Nox Application and Press Any Key')
        print('Now Find Nox Position')
        screen = get_screen(self.sct, self.sct.monitors[0])
        nox_img = cv2.imread('./image_files/nox.PNG')
        nox_pos = find_img_pos(screen, nox_img, interval=10, verbose=True)[0][0]
        
        print('\n')
        print('Refining Nox Position')
        i, j = nox_img.shape[0:2]
        # Double Monitor Problem
        if nox_pos[0] - i < 0: i = nox_pos[0]
        if nox_pos[1] - j < 0: j = nox_pos[1]
        around_screen = screen[nox_pos[0]-i:nox_pos[0]+2*nox_img.shape[0],
                               nox_pos[1]-j:nox_pos[1]+2*nox_img.shape[1]]
        nox_pos -= np.array([i, j])
        nox_pos += find_img_pos(around_screen, nox_img, interval=1, verbose=True)[0][0]
        nox_pos[0] += nox_img.shape[0]
        
        print('\n')
        print('Finished')
        
        return nox_pos
        
    def get_nox_monitor(self):
        nox_monitor = self.monitor.copy()
        nox_monitor['height'] = self.nox_size[0]
        nox_monitor['width'] = self.nox_size[1]
        nox_monitor['top'] = self.nox_pos[0]
        nox_monitor['left'] = self.nox_pos[1]
        return nox_monitor
        
    def get_relative_pos(self, img, count=1, dist=None):
        screen = get_screen(self.sct, self.nox_monitor)
        pos, img_diff = find_img_pos(screen, img, count=count, dist=dist)
        pos += (np.array(img.shape[0:2])/2).astype('int')
        return pos, img_diff
    
    def get_main_menu_pos(self):
        print()
        print('------------------------------------------')
        input('Run Girl\'s Frontier and Move to Main Menu')
        print('Now Find Menu Positions')
        print()
        self.combat_pos = self.get_relative_pos(cv2.imread('./image_files/combat.PNG'))[0][0]
        print('Compat Pos Obtained')
        self.restore_pos = self.get_relative_pos(cv2.imread('./image_files/restore.PNG'))[0][0]
        print('Restore Pos Obtained')
        self.formation_pos = self.get_relative_pos(cv2.imread('./image_files/formation.PNG'))[0][0]
        print('Formation Pos Obtained')
        self.factory_pos = self.get_relative_pos(cv2.imread('./image_files/factory.PNG'))[0][0]
        print('Factory Pos Obtained')
        print()
        print('Finished')
        
    def relative_drag(self, pos1, pos2):
        drag(self.nox_pos+pos1, self.nox_pos+pos2)
        
    def get_relative_mouse_pos(self):
        pos = get_mouse_pos() - self.nox_pos
        return pos
        
    def click_relative_pos(self, pos):
        noisy_pos = self.nox_pos + pos + np.random.randint(-5, 5, 2)
        click(noisy_pos)
        
    def restore_warning(self):
        res_pos, res_diff = self.get_relative_pos(cv2.imread('./image_files/restore_warning.PNG'), 1)
        if res_diff[0] < 0.01:
            self.click_relative_pos(res_pos[0]); random_sleep(3)
            while True:
                add_pos = self.get_relative_pos(cv2.imread('./image_files/add_doll.PNG'))[0][0]
                self.click_relative_pos(add_pos); random_sleep(1.5)

                deadly_pos, deadly_diff = self.get_relative_pos(cv2.imread('./image_files/deadly.PNG'))
                if deadly_diff[0] > 0.02:
                    cancel_pos = self.get_relative_pos(cv2.imread('./image_files/cancel.PNG'))[0][0]
                    self.click_relative_pos(cancel_pos); random_sleep(1.5)
                    return_pos = self.get_relative_pos(cv2.imread('./image_files/return.PNG'))[0][0]
                    self.click_relative_pos(return_pos); random_sleep(3)
                    break

                self.click_relative_pos(deadly_pos[0]); random_sleep(1.5)

                res_confirm_pos = self.get_relative_pos(cv2.imread('./image_files/restore_confirm.PNG'))[0][0]
                self.click_relative_pos(res_confirm_pos); random_sleep(1.5)

                fast_res_pos = self.get_relative_pos(cv2.imread('./image_files/fast_restore.PNG'))[0][0]
                self.click_relative_pos(fast_res_pos); random_sleep(1.5)

                res_confirm_pos_ = self.get_relative_pos(cv2.imread('./image_files/restore_confirm_.PNG'))[0][0]
                self.click_relative_pos(res_confirm_pos_); random_sleep(1.5)

                close_pos = self.get_relative_pos(cv2.imread('./image_files/close.PNG'))[0][0]
                self.click_relative_pos(close_pos); random_sleep(1.5)
                
        self.click_relative_pos(np.array([396, 407])); random_sleep(1) # close pop-up
        
        
    def restore(self):
        self.click_relative_pos(self.restore_pos); random_sleep(3)
        
        add_pos = self.get_relative_pos(cv2.imread('./image_files/add_doll.PNG'))[0][0]
        self.click_relative_pos(add_pos); random_sleep(0.7)

        self.click_relative_pos([150, 50]); random_sleep(0.5)
        self.click_relative_pos([150, 170]); random_sleep(0.5)

        res_confirm_pos = self.get_relative_pos(cv2.imread('./image_files/restore_confirm.PNG'))[0][0]
        self.click_relative_pos(res_confirm_pos); random_sleep(0.5)

        fast_res_pos = self.get_relative_pos(cv2.imread('./image_files/fast_restore.PNG'))[0][0]
        self.click_relative_pos(fast_res_pos); random_sleep(0.5)

        res_confirm_pos_ = self.get_relative_pos(cv2.imread('./image_files/restore_confirm_.PNG'))[0][0]
        self.click_relative_pos(res_confirm_pos_); random_sleep(0.5)

        close_pos = self.get_relative_pos(cv2.imread('./image_files/close.PNG'))[0][0]
        self.click_relative_pos(close_pos); random_sleep(0.5)

        return_pos = self.get_relative_pos(cv2.imread('./image_files/return.PNG'))[0][0]
        self.click_relative_pos(return_pos); random_sleep(1.5)
        
        self.click_relative_pos(np.array([396, 407])); random_sleep(1) # close pop-up
        
        # restore
        # add dol
        # click dol
        # confirm right left
        # confirm middle
        # fast restore
        
    def waiting_result(self, timeout):
        t0 = time.clock()
        while True:
            r_pos, r_diff = self.get_relative_pos(cv2.imread('./image_files/stat_bar.PNG'), 1)
            if r_diff[0] < 0.01:
                random_sleep(0.4)
                break
                
            if time.clock() - t0 > timeout:
                break
            else:
                sys.stdout.write('\r                                   ')
                sys.stdout.write('\rtime : {}'.format(time.clock() - t0))
                
    def check_start(self):
        pos1, diff1 = self.get_relative_pos(cv2.imread('./image_files/command.PNG'), 1)
        pos2, diff2 = self.get_relative_pos(cv2.imread('./image_files/start.PNG'), 1)
        
        if diff1 < 0.013 or diff2 < 0.013:
            return True
        else:
            return False
        
    def check_support(self, period=1):
        print('Check support mission')
        print('Wait for {} seconds'.format(period))
        random_sleep(period);
        combat_pos, combat_diff = self.get_relative_pos(cv2.imread('./image_files/combat.PNG'), 1)
        if combat_diff < 0.01:
            print('Return to rutine')
            return 
        else:
            print('------------------------------')
            print('Can not find combat button')
            print('Check support mission')
            result_pos, result_diff = self.get_relative_pos(cv2.imread('./image_files/support_result.PNG'))
            for i in range(5):
                print('Wait result ({}/5)'.format(i+1))
                if result_diff < 0.01:
                    print('Result obtained')
                    break
                result_pos, result_diff = self.get_relative_pos(cv2.imread('./image_files/support_result.PNG'))
            self.click_relative_pos(result_pos[0]); random_sleep(0.8)
            
            confirm_pos, confirm_diff = self.get_relative_pos(cv2.imread('./image_files/support_confirm.PNG'))
            self.click_relative_pos(confirm_pos[0]); random_sleep(0.8)
            return
        
    def empty_barrack(self):
        print()
        print('------------------------------')
        print('Now empty Barrack\n')
        self.click_relative_pos(self.factory_pos); random_sleep(3.0)
        
        retire_pos = self.get_relative_pos(cv2.imread('./image_files/retire.PNG'))[0][0]
        self.click_relative_pos(retire_pos); random_sleep(3.0)
        
        add_doll_pos = self.get_relative_pos(cv2.imread('./image_files/add_doll_retire.PNG'), 1)[0][0]
        self.click_relative_pos(add_doll_pos); random_sleep(3.0)
        
        order_by_pos = self.get_relative_pos(cv2.imread('./image_files/order_by.PNG'), 1)[0][0]
        self.click_relative_pos(order_by_pos); random_sleep(0.5)
        
        by_rarity_pos = self.get_relative_pos(cv2.imread('./image_files/by_rarity.PNG'), 1)[0][0]
        self.click_relative_pos(by_rarity_pos); random_sleep(3.0)
        
        self.relative_drag(np.array([540, 370]), np.array([8, 370])); random_sleep(0.5)
        self.relative_drag(np.array([540, 370]), np.array([8, 370])); random_sleep(0.5)
        self.relative_drag(np.array([540, 370]), np.array([8, 370])); random_sleep(0.5)
        self.relative_drag(np.array([540, 370]), np.array([8, 370])); random_sleep(0.5)
        self.relative_drag(np.array([540, 370]), np.array([8, 370])); random_sleep(0.5)
        
        points1 = [496, 300, 115]
        points2 = [54, 163, 279, 387, 506, 623]
        
        for h in points1:
            for w in points2:
                self.click_relative_pos([h, w])
                random_sleep(0.4)
        
        retire_confirm_pos = self.get_relative_pos(cv2.imread('./image_files/retire_confirm.PNG'), 1)[0][0]
        self.click_relative_pos(retire_confirm_pos); random_sleep(2.0)
        
        disassemble_pos = self.get_relative_pos(cv2.imread('./image_files/disassemble.PNG'), 1)[0][0]
        self.click_relative_pos(disassemble_pos); random_sleep(2.0)
        
        return_pos = self.get_relative_pos(cv2.imread('./image_files/return_to_base.PNG'))[0][0]
        self.click_relative_pos(return_pos); random_sleep(3.5)
        
        return

    def run_5_4n(self, repeat, fast_restore=True):
        print('------------------------------')
        print('Return to Base for Running 5-4')
        input('Delete Cafe Icon and Press Any Key')
        firstrun = input('Is EP.05 Activated? [Y/N] ') == 'N'
        print()
        
        points = np.array([[194, 222],
                           [195, 402],
                           [207, 612],
                           [370, 622],
                           [505, 612]])
        
        for epoch in range(repeat):
            self.click_relative_pos(self.combat_pos), random_sleep(3)
            
            if firstrun:
                ep_pos = self.get_relative_pos(cv2.imread('./image_files/EP05.PNG'))[0][0]
                self.click_relative_pos(ep_pos); random_sleep(1.5)
                firstrun = False
            
            stage_pos = self.get_relative_pos(cv2.imread('./image_files/EP05-4.PNG'))[0][0]
            self.click_relative_pos(stage_pos); random_sleep(1.5)
            
            normal_pos = self.get_relative_pos(cv2.imread('./image_files/normal.PNG'))[0][0]
            self.click_relative_pos(normal_pos); random_sleep(3)
            
            command_pos = self.get_relative_pos(cv2.imread('./image_files/command.PNG'))[0][0]
            self.click_relative_pos(command_pos); random_sleep(3)
            
            dummy_pos = self.get_relative_pos(cv2.imread('./image_files/dummy.PNG'))[0][0]
            self.click_relative_pos(dummy_pos); random_sleep(1.5)
            
            confirm_pos = self.get_relative_pos(cv2.imread('./image_files/confirm.PNG'))[0][0]
            self.click_relative_pos(confirm_pos); random_sleep(1.5)     

            self.relative_drag(np.array([400, 10]), np.array([400, 700])); random_sleep(1.5)
            
            heliport_pos = self.get_relative_pos(cv2.imread('./image_files/heilport.PNG'))[0][0]
            self.click_relative_pos(heliport_pos); random_sleep(3)
            
            self.click_relative_pos(confirm_pos); random_sleep(1.5)
            
            start_pos = self.get_relative_pos(cv2.imread('./image_files/start.PNG'))[0][0]
            self.click_relative_pos(start_pos); random_sleep(3)
            
            points_ = np.vstack([[heliport_pos], points])
            
            ## combat phase
            
            for i in range(points.shape[0]):
                self.click_relative_pos(points_[i]); random_sleep(1.5)
                self.click_relative_pos(points_[i+1]); random_sleep(5)
                if i == 3:
                    self.click_relative_pos(np.array([300, 400])); random_sleep(1)
                random_sleep(25)
                for _ in range(4):
                    self.click_relative_pos(np.array([300, 400])); random_sleep(1)
                random_sleep(3)
                
            terminate_pos = self.get_relative_pos(cv2.imread('./image_files/terminate.PNG'))[0][0]
            self.click_relative_pos(terminate_pos); random_sleep(10)
            for _ in range(4):
                self.click_relative_pos(np.array([300, 400])); random_sleep(1)
            random_sleep(3)
            
            self.click_relative_pos(np.array([396, 407])); random_sleep(1) # close pop-up
            
            self.restore_warning()
            
            sys.stdout.write('\r{0}/{1}'.format(epoch+1, repeat))
            
    def run_4_3e(self, repeat, fast_restore=True, n_restore=2, retire=True):
        print('-------------------------------')
        print('Return to Base for Running 4-3E')
        input('Delete Cafe Icon and Press Any Key')
        print()
        
        points = np.array([[270, 594],
                           [104, 655],
                           [449, 634],
                           [284, 539],
                           [ 61, 550]])
        
        for epoch in range(repeat):
            t_start = time.clock()
            self.click_relative_pos(self.combat_pos); random_sleep(3)
            
            ep_pos, diff1 = self.get_relative_pos(cv2.imread('./image_files/EP04.PNG'),1)
            ep_act_pos, diff2 = self.get_relative_pos(cv2.imread('./image_files/EP04_act.PNG'),1)
            if diff1<diff2:
                self.click_relative_pos(ep_pos[0]); random_sleep(1.5)
            
            emerg_pos = self.get_relative_pos(cv2.imread('./image_files/emergency.PNG'))[0][0]
            self.click_relative_pos(emerg_pos); random_sleep(1.5)
            
            stage_pos = self.get_relative_pos(cv2.imread('./image_files/EP04-3E.PNG'))[0][0]
            self.click_relative_pos(stage_pos); random_sleep(1.5)
            
            normal_pos = self.get_relative_pos(cv2.imread('./image_files/normal.PNG'))[0][0]
            self.click_relative_pos(normal_pos); random_sleep(3)
            
            # Check wehter it started well or not
            if self.check_start() == False:
                print()
                print('-------------------------------')
                print('Can not find commander and start button')
                print('Checking barrack is full')
                full_barrack_pos, diff = self.get_relative_pos(cv2.imread('./image_files/full_barrack_EP04-3E.PNG'), 1)
                if diff < 0.01:
                    print('Barrack is full')
                    if retire:
                        print('Empty barrack')
                        back_pos = self.get_relative_pos(cv2.imread('./image_files/back.PNG'))[0][0]
                        self.click_relative_pos(back_pos); random_sleep(0.5)
                        back_pos = self.get_relative_pos(cv2.imread('./image_files/back.PNG'))[0][0]
                        self.click_relative_pos(back_pos); random_sleep(0.5)
                        return_pos = self.get_relative_pos(cv2.imread('./image_files/return_to_base.PNG'))[0][0]
                        self.click_relative_pos(return_pos); random_sleep(3.5)
                        self.check_support()
                        self.empty_barrack()
                        
                        # Start Combat again
                        self.check_support()
                        self.click_relative_pos(self.combat_pos), random_sleep(3.5)
                        self.click_relative_pos(emerg_pos); random_sleep(2.0)
                        self.click_relative_pos(stage_pos); random_sleep(2.0)
                        self.click_relative_pos(normal_pos); random_sleep(3)
                    else:
                        print('Stop running.')
                        break
                
                else:
                    print('Something wrong! Stop running.')
                    break
            
            command_pos = self.get_relative_pos(cv2.imread('./image_files/command.PNG'))[0][0]
            self.click_relative_pos(command_pos); random_sleep(1)
            
            dummy_pos = self.get_relative_pos(cv2.imread('./image_files/dummy.PNG'))[0][0]
            self.click_relative_pos(dummy_pos); random_sleep(0.5)
            
            confirm_pos = self.get_relative_pos(cv2.imread('./image_files/confirm.PNG'))[0][0]
            self.click_relative_pos(confirm_pos); random_sleep(0.5)     

            self.relative_drag(np.array([300, 700]), np.array([300, 100])); random_sleep(0.5)
            
            heliport_pos = self.get_relative_pos(cv2.imread('./image_files/heilport.PNG'))[0][0]
            self.click_relative_pos(heliport_pos); random_sleep(0.5)
            
            self.click_relative_pos(confirm_pos); random_sleep(0.5)
            
            start_pos = self.get_relative_pos(cv2.imread('./image_files/start.PNG'))[0][0]
            self.click_relative_pos(start_pos); random_sleep(4)

            self.click_relative_pos(heliport_pos); random_sleep(0.5)
            self.click_relative_pos(points[0]); self.waiting_result(25)          
            for _ in range(4):
                self.click_relative_pos(np.array([300, 400])); random_sleep(0.3)
            random_sleep(3)
            
            self.click_relative_pos(points[0]); random_sleep(0.5)
            self.click_relative_pos(points[1]); self.waiting_result(25)
            for _ in range(4):
                self.click_relative_pos(np.array([300, 400])); random_sleep(0.3)
            random_sleep(3)
            
            self.relative_drag(np.array([100, 400]), np.array([500, 400])); random_sleep(0.5)
            
            self.click_relative_pos(points[2]); random_sleep(0.5)
            self.click_relative_pos(points[3]); self.waiting_result(25)
            for _ in range(4):
                self.click_relative_pos(np.array([300, 400])); random_sleep(0.3)
            random_sleep(3)
            
            self.click_relative_pos(points[3]); random_sleep(0.5)
            self.click_relative_pos(points[4]); self.waiting_result(25)
            for _ in range(4):
                self.click_relative_pos(np.array([300, 400])); random_sleep(0.3)
            random_sleep(3)
                
            terminate_pos = self.get_relative_pos(cv2.imread('./image_files/terminate.PNG'))[0][0]
            self.click_relative_pos(terminate_pos); random_sleep(10)
            for _ in range(4):
                self.click_relative_pos(np.array([300, 400])); random_sleep(0.3)
            random_sleep(3)
            
            self.click_relative_pos(np.array([396, 407])); random_sleep(1) # close pop-up
            
            # Auto Support Reauire
            self.check_support()
            # Manually restore
            if (epoch+1)%n_restore == 0:
                self.restore()
                self.check_support()
            # self.restore_warning()
            sys.stdout.write('\r                                ')
            sys.stdout.write('\r{0}/{1}\ntotal time: {2}\n'.format(epoch+1, repeat, time.clock()-t_start))
            print()
            print('-------------------------------')
            
    def run_5_2e(self, repeat, fast_restore=True, n_restore=1, retire=True):
        print('-------------------------------')
        print('Return to Base for Running 5-2E')
        input('Delete Cafe Icon and Press Any Key')
        print()
        
        points = np.array([[327, 284],
                           [432, 358],
                           [456, 641],
                           [305, 695],
                           [141, 683]])
        
        for epoch in range(repeat):
            t_start = time.clock()
            self.click_relative_pos(self.combat_pos); random_sleep(3)
            
            ep_pos, diff1 = self.get_relative_pos(cv2.imread('./image_files/EP05.PNG'),1)
            ep_act_pos, diff2 = self.get_relative_pos(cv2.imread('./image_files/EP05_act.PNG'),1)
            if diff1<diff2:
                self.click_relative_pos(ep_pos[0]); random_sleep(1.5)
            
            emerg_pos = self.get_relative_pos(cv2.imread('./image_files/emergency.PNG'))[0][0]
            self.click_relative_pos(emerg_pos); random_sleep(1.5)
            
            stage_pos = self.get_relative_pos(cv2.imread('./image_files/EP05-2E.PNG'))[0][0]
            self.click_relative_pos(stage_pos); random_sleep(1.5)
            
            normal_pos = self.get_relative_pos(cv2.imread('./image_files/normal.PNG'))[0][0]
            self.click_relative_pos(normal_pos); random_sleep(3)
            
            # Check wehter it started well or not
            if self.check_start() == False:
                print()
                print('-------------------------------')
                print('Can not find commander and start button')
                print('Checking barrack is full')
                full_barrack_pos, diff = self.get_relative_pos(cv2.imread('./image_files/full_barrack_EP04-3E.PNG'), 1)
                if diff < 0.01:
                    print('Barrack is full')
                    if retire:
                        print('Empty barrack')
                        back_pos = self.get_relative_pos(cv2.imread('./image_files/back.PNG'))[0][0]
                        self.click_relative_pos(back_pos); random_sleep(0.5)
                        back_pos = self.get_relative_pos(cv2.imread('./image_files/back.PNG'))[0][0]
                        self.click_relative_pos(back_pos); random_sleep(0.5)
                        return_pos = self.get_relative_pos(cv2.imread('./image_files/return_to_base.PNG'))[0][0]
                        self.click_relative_pos(return_pos); random_sleep(3.5)
                        self.check_support()
                        self.empty_barrack()
                        
                        # Start Combat again
                        self.check_support()
                        self.click_relative_pos(self.combat_pos), random_sleep(3.5)
                        self.click_relative_pos(emerg_pos); random_sleep(2.0)
                        self.click_relative_pos(stage_pos); random_sleep(2.0)
                        self.click_relative_pos(normal_pos); random_sleep(3)
                    else:
                        print('Stop running.')
                        break
                
                else:
                    print('Something wrong! Stop running.')
                    break
            
            command_pos = self.get_relative_pos(cv2.imread('./image_files/command.PNG'))[0][0]
            self.click_relative_pos(command_pos); random_sleep(1)
            
            dummy_pos = self.get_relative_pos(cv2.imread('./image_files/dummy.PNG'))[0][0]
            self.click_relative_pos(dummy_pos); random_sleep(0.5)
            
            confirm_pos = self.get_relative_pos(cv2.imread('./image_files/confirm.PNG'))[0][0]
            self.click_relative_pos(confirm_pos); random_sleep(0.5)     

            self.relative_drag(np.array([500, 20]), np.array([100, 750])); random_sleep(0.5)
            
            heliport_pos = self.get_relative_pos(cv2.imread('./image_files/heilport.PNG'))[0][0]
            self.click_relative_pos(heliport_pos); random_sleep(0.5)
            
            self.click_relative_pos(confirm_pos); random_sleep(0.5)
            
            start_pos = self.get_relative_pos(cv2.imread('./image_files/start.PNG'))[0][0]
            self.click_relative_pos(start_pos); random_sleep(4)

            self.click_relative_pos(heliport_pos); random_sleep(0.5)
            self.click_relative_pos(points[0]); self.waiting_result(25)          
            for _ in range(4):
                self.click_relative_pos(np.array([300, 400])); random_sleep(0.3)
            random_sleep(3)
            
            self.click_relative_pos(points[0]); random_sleep(0.5)
            self.click_relative_pos(points[1]); self.waiting_result(25)
            for _ in range(4):
                self.click_relative_pos(np.array([300, 400])); random_sleep(0.3)
            random_sleep(3)
            
            self.click_relative_pos(points[1]); random_sleep(0.5)
            self.click_relative_pos(points[2]); self.waiting_result(25)
            for _ in range(4):
                self.click_relative_pos(np.array([300, 400])); random_sleep(0.3)
            random_sleep(3)
            
            self.click_relative_pos(points[2]); random_sleep(0.5)
            self.click_relative_pos(points[3]); self.waiting_result(25)
            for _ in range(4):
                self.click_relative_pos(np.array([300, 400])); random_sleep(0.3)
            random_sleep(3)
            
            self.click_relative_pos(points[3]); random_sleep(0.5)
            self.click_relative_pos(points[4]); self.waiting_result(25)
            for _ in range(4):
                self.click_relative_pos(np.array([300, 400])); random_sleep(0.3)
            random_sleep(3)
            
                
            terminate_pos = self.get_relative_pos(cv2.imread('./image_files/terminate.PNG'))[0][0]
            self.click_relative_pos(terminate_pos); random_sleep(10)
            for _ in range(4):
                self.click_relative_pos(np.array([300, 400])); random_sleep(0.3)
            random_sleep(3)
            
            self.click_relative_pos(np.array([396, 407])); random_sleep(1) # close pop-up
            
            # Auto Support Reauire
            self.check_support()
            # Manually restore
            if (epoch+1)%n_restore == 0:
                self.restore()
                self.check_support()
            # self.restore_warning()
            sys.stdout.write('\r                                ')
            sys.stdout.write('\r{0}/{1}\ntotal time: {2}\n'.format(epoch+1, repeat, time.clock()-t_start))
            print()
            print('-------------------------------')
            
            
    def run_2_3n(self, repeat, fast_restore=True, n_restore=2, retire=True):
        print('-------------------------------')
        print('Return to Base for Running 2-3N')
        input('Delete Cafe Icon and Press Any Key')
        print()
        
        points = np.array([[332, 552],
                           [357, 382],
                           [244, 194],
                           [449, 113]])
        
        for epoch in range(repeat):
            t_start = time.clock()
            self.click_relative_pos(self.combat_pos); random_sleep(3)
            
            ep_pos, diff1 = self.get_relative_pos(cv2.imread('./image_files/EP02.PNG'),1)
            ep_act_pos, diff2 = self.get_relative_pos(cv2.imread('./image_files/EP02_act.PNG'),1)
            if diff1<diff2:
                self.click_relative_pos(ep_pos[0]); random_sleep(1.5)
            
            stage_pos = self.get_relative_pos(cv2.imread('./image_files/EP02-3.PNG'))[0][0]
            self.click_relative_pos(stage_pos); random_sleep(1.5)
            
            normal_pos = self.get_relative_pos(cv2.imread('./image_files/normal.PNG'))[0][0]
            self.click_relative_pos(normal_pos); random_sleep(3)
            
            # Check wehter it started well or not
            if self.check_start() == False:
                print()
                print('-------------------------------')
                print('Can not find commander and start button')
                print('Checking barrack is full')
                full_barrack_pos, diff = self.get_relative_pos(cv2.imread('./image_files/full_barrack_EP04-3E.PNG'), 1)
                if diff < 0.01:
                    print('Barrack is full')
                    if retire:
                        print('Empty barrack')
                        back_pos = self.get_relative_pos(cv2.imread('./image_files/back.PNG'))[0][0]
                        self.click_relative_pos(back_pos); random_sleep(0.5)
                        back_pos = self.get_relative_pos(cv2.imread('./image_files/back.PNG'))[0][0]
                        self.click_relative_pos(back_pos); random_sleep(0.5)
                        return_pos = self.get_relative_pos(cv2.imread('./image_files/return_to_base.PNG'))[0][0]
                        self.click_relative_pos(return_pos); random_sleep(3.5)
                        self.check_support()
                        self.empty_barrack()
                        
                        # Start Combat again
                        self.check_support()
                        self.click_relative_pos(self.combat_pos), random_sleep(3.5)
                        self.click_relative_pos(emerg_pos); random_sleep(2.0)
                        self.click_relative_pos(stage_pos); random_sleep(2.0)
                        self.click_relative_pos(normal_pos); random_sleep(3)
                    else:
                        print('Stop running.')
                        break
                
                else:
                    print('Something wrong! Stop running.')
                    break
            
            command_pos = self.get_relative_pos(cv2.imread('./image_files/command.PNG'))[0][0]
            self.click_relative_pos(command_pos); random_sleep(1)
            
            dummy_pos = self.get_relative_pos(cv2.imread('./image_files/dummy.PNG'))[0][0]
            self.click_relative_pos(dummy_pos); random_sleep(0.5)
            
            confirm_pos = self.get_relative_pos(cv2.imread('./image_files/confirm.PNG'))[0][0]
            self.click_relative_pos(confirm_pos); random_sleep(0.5)     

            self.relative_drag(np.array([100, 650]),np.array([300, 300])); random_sleep(0.5)
            
            heliport_pos = self.get_relative_pos(cv2.imread('./image_files/heilport.PNG'))[0][0]
            self.click_relative_pos(heliport_pos); random_sleep(0.5)
            
            self.click_relative_pos(confirm_pos); random_sleep(0.5)
            
            start_pos = self.get_relative_pos(cv2.imread('./image_files/start.PNG'))[0][0]
            self.click_relative_pos(start_pos); random_sleep(4)

            self.click_relative_pos(heliport_pos); random_sleep(0.5)
            self.click_relative_pos(points[0]); self.waiting_result(25)          
            for _ in range(4):
                self.click_relative_pos(np.array([300, 400])); random_sleep(0.3)
            random_sleep(3)
            
            self.click_relative_pos(points[0]); random_sleep(0.5)
            self.click_relative_pos(points[1]); self.waiting_result(25)
            for _ in range(4):
                self.click_relative_pos(np.array([300, 400])); random_sleep(0.3)
            random_sleep(3)
            
            self.click_relative_pos(points[1]); random_sleep(0.5)
            self.click_relative_pos(points[2]); self.waiting_result(25)
            for _ in range(4):
                self.click_relative_pos(np.array([300, 400])); random_sleep(0.3)
            random_sleep(3)
            
            self.click_relative_pos(points[2]); random_sleep(0.5)
            self.click_relative_pos(points[3]); self.waiting_result(25)
            for _ in range(4):
                self.click_relative_pos(np.array([300, 400])); random_sleep(0.3)
            random_sleep(3)   
                
            terminate_pos = self.get_relative_pos(cv2.imread('./image_files/terminate.PNG'))[0][0]
            self.click_relative_pos(terminate_pos); random_sleep(10)
            for _ in range(4):
                self.click_relative_pos(np.array([300, 400])); random_sleep(0.3)
            random_sleep(3)
            
            self.click_relative_pos(np.array([396, 407])); random_sleep(1) # close pop-up
            
            # Auto Support Reauire
            self.check_support()
            # Manually restore
            if (epoch+1)%n_restore == 0:
                self.restore()
                self.check_support()
            # self.restore_warning()
            sys.stdout.write('\r                                ')
            sys.stdout.write('\r{0}/{1}\ntotal time: {2}\n'.format(epoch+1, repeat, time.clock()-t_start))
            print()
            print('-------------------------------')
            
            
    def run_3_5n(self, repeat, fast_restore=True, n_restore=2, retire=True):
        print('-------------------------------')
        print('Return to Base for Running 3-5N')
        input('Delete Cafe Icon and Press Any Key')
        print()
        
        points = np.array([[394, 435],
                           [236, 209],
                           [211, 419],
                           [115, 498]])
        
        for epoch in range(repeat):
            t_start = time.clock()
            self.click_relative_pos(self.combat_pos); random_sleep(3)
            
            ep_pos, diff1 = self.get_relative_pos(cv2.imread('./image_files/EP03.PNG'),1)
            ep_act_pos, diff2 = self.get_relative_pos(cv2.imread('./image_files/EP03_act.PNG'),1)
            if diff1<diff2:
                self.click_relative_pos(ep_pos[0]); random_sleep(1.5)
            
            stage_pos = self.get_relative_pos(cv2.imread('./image_files/EP03-5.PNG'))[0][0]
            self.click_relative_pos(stage_pos); random_sleep(1.5)
            
            normal_pos = self.get_relative_pos(cv2.imread('./image_files/normal.PNG'))[0][0]
            self.click_relative_pos(normal_pos); random_sleep(3)
            
            # Check wehter it started well or not
            if self.check_start() == False:
                print()
                print('-------------------------------')
                print('Can not find commander and start button')
                print('Checking barrack is full')
                full_barrack_pos, diff = self.get_relative_pos(cv2.imread('./image_files/full_barrack_EP04-3E.PNG'), 1)
                if diff < 0.01:
                    print('Barrack is full')
                    if retire:
                        print('Empty barrack')
                        back_pos = self.get_relative_pos(cv2.imread('./image_files/back.PNG'))[0][0]
                        self.click_relative_pos(back_pos); random_sleep(0.5)
                        back_pos = self.get_relative_pos(cv2.imread('./image_files/back.PNG'))[0][0]
                        self.click_relative_pos(back_pos); random_sleep(0.5)
                        return_pos = self.get_relative_pos(cv2.imread('./image_files/return_to_base.PNG'))[0][0]
                        self.click_relative_pos(return_pos); random_sleep(3.5)
                        self.check_support()
                        self.empty_barrack()
                        
                        # Start Combat again
                        self.check_support()
                        self.click_relative_pos(self.combat_pos), random_sleep(3.5)
                        self.click_relative_pos(emerg_pos); random_sleep(2.0)
                        self.click_relative_pos(stage_pos); random_sleep(2.0)
                        self.click_relative_pos(normal_pos); random_sleep(3)
                    else:
                        print('Stop running.')
                        break
                
                else:
                    print('Something wrong! Stop running.')
                    break
            
            command_pos = self.get_relative_pos(cv2.imread('./image_files/command.PNG'))[0][0]
            self.click_relative_pos(command_pos); random_sleep(1)
            
            dummy_pos = self.get_relative_pos(cv2.imread('./image_files/dummy.PNG'))[0][0]
            self.click_relative_pos(dummy_pos); random_sleep(0.5)
            
            confirm_pos = self.get_relative_pos(cv2.imread('./image_files/confirm.PNG'))[0][0]
            self.click_relative_pos(confirm_pos); random_sleep(0.5)     

            self.relative_drag(np.array([200, 650]),np.array([300, 95])); random_sleep(0.5)
            
            heliport_pos = self.get_relative_pos(cv2.imread('./image_files/heilport.PNG'))[0][0]
            self.click_relative_pos(heliport_pos); random_sleep(0.5)
            
            self.click_relative_pos(confirm_pos); random_sleep(0.5)
            
            start_pos = self.get_relative_pos(cv2.imread('./image_files/start.PNG'))[0][0]
            self.click_relative_pos(start_pos); random_sleep(4)

            self.click_relative_pos(heliport_pos); random_sleep(0.5)
            self.click_relative_pos(points[0]); self.waiting_result(25)          
            for _ in range(4):
                self.click_relative_pos(np.array([300, 400])); random_sleep(0.3)
            random_sleep(3)
            
            self.click_relative_pos(points[0]); random_sleep(0.5)
            self.click_relative_pos(points[1]); self.waiting_result(25)
            for _ in range(4):
                self.click_relative_pos(np.array([300, 400])); random_sleep(0.3)
            random_sleep(3)
            
            self.click_relative_pos(points[1]); random_sleep(0.5)
            self.click_relative_pos(points[2]); self.waiting_result(25)
            for _ in range(4):
                self.click_relative_pos(np.array([300, 400])); random_sleep(0.3)
            random_sleep(3)
            
            self.click_relative_pos(points[2]); random_sleep(0.5)
            self.click_relative_pos(points[3]); self.waiting_result(25)
            for _ in range(4):
                self.click_relative_pos(np.array([300, 400])); random_sleep(0.3)
            random_sleep(3)   
                
            terminate_pos = self.get_relative_pos(cv2.imread('./image_files/terminate.PNG'))[0][0]
            self.click_relative_pos(terminate_pos); random_sleep(10)
            for _ in range(4):
                self.click_relative_pos(np.array([300, 400])); random_sleep(0.3)
            random_sleep(3)
            
            self.click_relative_pos(np.array([396, 407])); random_sleep(1) # close pop-up
            
            # Auto Support Reauire
            self.check_support()
            # Manually restore
            if (epoch+1)%n_restore == 0:
                self.restore()
                self.check_support()
            # self.restore_warning()
            sys.stdout.write('\r                                ')
            sys.stdout.write('\r{0}/{1}\ntotal time: {2}\n'.format(epoch+1, repeat, time.clock()-t_start))
            print()
            print('-------------------------------')