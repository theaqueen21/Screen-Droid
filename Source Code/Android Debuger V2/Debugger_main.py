from tkinter import*
import subprocess,os,sys,netifaces,time,threading,random,imageio
from tkinter import messagebox;from PIL import Image, ImageTk
# import ctypes
# ctypes.windll.shcore.SetProcessDpiAwareness(True) # increases DPI for better image, Not optimized yet
try:
    os.chdir(f'{sys._MEIPASS}\\addons') # if compiled using pyinstaller (autopy2exe)
except:
    try:
        path_dir = input('Script Directory: ') # Where you saved the .py, should have icons and vids directory 
        os.chdir(path_dir)
    except:
        raise Exception(f"Directory Doesn't Exist.\nCurrent Directory: {os.getcwd()}")
adb_check = subprocess.run(['adb','kill-server'],shell=True,capture_output=True)
if adb_check.returncode == 1:
    raise Exception(f"Invalid Directory, Couldn't Find adb.exe\nCurrent Directroy[ {os.getcwd()} ]")
bg_color_main = "#000000"
Running_tasks_pid = {}
time_list = list(range(0,31))
time_list.reverse()
RESTART_TIMER = False
EXIT_END = False
STARTUP_CHECK = None
vid_playback_wireless = None
vid_playback_downloading = None
default_gateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
current_interface = netifaces.gateways()['default'][netifaces.AF_INET][1]
network_info = netifaces.ifaddresses(current_interface)[netifaces.AF_INET][0]
current_subnet = network_info['netmask']
changing_sub = current_subnet.split('.')
splittings_count = changing_sub.count('0')
splitted_gate = default_gateway.split('.')
for i in range(1,splittings_count+1):
    splitted_gate.pop(-1)
auto_complete_gateway = '.'.join(splitted_gate)+'.'

def vid_playback_4_wireless(path):
    global vid_playback_wireless
    frame_data = imageio.get_reader(path)
    size = (400,600)
    while vid_playback_wireless:
        for image in frame_data.iter_data():
            frame_image = ImageTk.PhotoImage(Image.fromarray(image).resize(size))
            vid_label_wireless.config(image=frame_image)
            vid_label_wireless.image = frame_image
            if vid_playback_wireless != True:
                break
            time.sleep(0.001)

def vid_playback_4_downloading(path):
    global vid_playback_downloading
    frame_data = imageio.get_reader(path)
    size = (48,48)
    while vid_playback_downloading:
        for image in frame_data.iter_data():
            frame_image = ImageTk.PhotoImage(Image.fromarray(image).resize(size))
            file_downloading_btn.config(image=frame_image)
            file_downloading_btn.image = frame_image
            if vid_playback_downloading == False:
                break
            time.sleep(0.03)
    else:
        file_downloading_btn.config(image=file_downloading_btn_complete_png)

def exiting():
    global EXIT_END
    EXIT_END = True
    main_window.destroy()

def ask_4_exit(event):
    if messagebox.askyesno('Exiting',message='Do You Wish To Exit?'):
        exiting()

def auto_refresh_checkup():
    global RESTART_TIMER,STARTUP_CHECK
    while EXIT_END != True:
        if STARTUP_CHECK == True:
            for i in time_list:
                if RESTART_TIMER == False:
                    auto_refresh.configure(state='normal')
                    auto_refresh.delete(0,END)
                    auto_refresh.insert(END,str(i))
                    auto_refresh.configure(state='disabled')
                    time.sleep(1)
                    if i == 0:
                        re_checkup()
                elif RESTART_TIMER:
                    RESTART_TIMER = False
                    auto_refresh_checkup()
            auto_refresh_checkup()
            break
        elif STARTUP_CHECK == None:
            re_checkup()
            STARTUP_CHECK = True
    else:
        exit()



def add_task_with_pid(window_name,id_dev):
    while EXIT_END != True:
        time.sleep(0.5)
        filter_id = f"WINDOWTITLE eq {window_name}*"
        global count_task_pid
        count_task_pid = 0
        def rerun():
            time.sleep(0.5)
            global count_task_pid
            add_task_pid = subprocess.run(['tasklist','/fi',filter_id,'/fo','list'],shell=True,capture_output=True).stdout.decode()
            if 'No tasks are running' not in add_task_pid:
                add_task_pid = add_task_pid.splitlines()
                for i in add_task_pid:
                    if 'PID:' in i:
                        i = i.removeprefix("PID:").strip(' ')
                        Running_tasks_pid[id_dev] = i
            else:
                if count_task_pid >= 10 and count_task_pid % 10 == 0:
                    if messagebox.askyesno('Timeout Error',message="5 Seconds Has Passed and The Task Still Doesn't Exist. Do You Wish To Terminate All and Queued Tasks? ") == True:
                        subprocess.run(['adb','kill-server'],shell=True,capture_output=True)
                    else:
                        count_task_pid +=1
                        rerun()
                else:
                    count_task_pid +=1
                    rerun()
        rerun()
        re_checkup()
        break
    else:
        subprocess.Popen(['adb','kill-server'],shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
        exit()

def wait_until_disconnect(id_dev,addr,window_name,port,adb_tcpip_out,adb_connect_out,wireless_frame_disconnect):
    global vid_playback_wireless
    while EXIT_END != True:
        if 'invalid' not in adb_tcpip_out.stdout.decode():
            if 'connected' in adb_connect_out.stdout.decode():
                def rereun():
                    global vid_playback_wireless
                    check_4_device_battery = subprocess.run(["adb","-s",addr,'shell','dumpsys','battery'],shell=True,capture_output=True).stdout.decode()
                    if 'USB powered: true' in check_4_device_battery or 'AC powered: true' in check_4_device_battery:
                        time.sleep(0.5)
                        rereun()
                    else:
                        vid_playback_wireless = False
                        wireless_frame_disconnect.pack_forget()
                        subprocess.Popen(['scrcpy','-s',addr,'--window-title',window_name,'-p',port],shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
                        add_task_with_pid_thread = threading.Thread(target=add_task_with_pid,args=(window_name,id_dev),daemon=True)
                        add_task_with_pid_thread.start()
                        re_checkup()
                rereun()
            else:
                vid_playback_wireless = False
                wireless_frame_disconnect.pack_forget()
                messagebox.showerror('Connection Error',message=f"Couldn't Connect To {addr}")
                re_checkup()
        else:
            vid_playback_wireless = False
            wireless_frame_disconnect.pack_forget()
            messagebox.showerror('Port Error',message=f"An Error Occured, Port Used {port}")
            re_checkup()
        break
    else:
        subprocess.Popen(['adb','kill-server'],shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
        exit()


def all_btn_activity(state):
    if state == 'normal':
        clr_btn.configure(state=state)
        rfrsh_btn.configure(state=state)
        wired_btn.configure(state=state)
        wireless_btn.configure(state=state)
        kill_btn.configure(state=state)
        whatsapp_btn.configure(state=state)
        file_download_btn.configure(state=state)
        file_upload_btn.configure(state=state)
        kill_btn.update(),wireless_btn.update(),wired_btn.update(),rfrsh_btn.update(),clr_btn.update(),file_upload_btn.update(),file_download_btn.update(),whatsapp_btn.update()
    elif state == 'disabled':
        clr_btn.configure(state=state)
        rfrsh_btn.configure(state=state)
        wired_btn.configure(state=state)
        wireless_btn.configure(state=state)
        kill_btn.configure(state=state)
        whatsapp_btn.configure(state=state)
        file_download_btn.configure(state=state)
        file_upload_btn.configure(state=state)
        kill_btn.update(),wireless_btn.update(),wired_btn.update(),rfrsh_btn.update(),clr_btn.update(),file_upload_btn.update(),file_download_btn.update(),whatsapp_btn.update()

def kill_process():
    all_btn_activity('disabled')
    subprocess.run(["adb","kill-server"],shell=True,capture_output=True)
    global Running_tasks_pid
    Running_tasks_pid = {}
    re_checkup()
def kill_process_bind(event):
    kill_process()

def wireless():
    while EXIT_END != True:
        all_btn_activity('disabled')
        try:
            current_selection = list_box.get(list_box.curselection())
            for index,i in enumerate(devices.values()):
                if i == current_selection:
                    id_dev = list(devices.keys())[index]
            window_name = f"{current_selection} {id_dev}"
            phone_ip = subprocess.run(['adb','-s',id_dev,'shell','ifconfig','wlan0'],shell=True,capture_output=True).stdout.decode()
            global bg_color_main,vid_playback_wireless
            if bg_color_main == "#000000":
                path_vid = r"vids\\White_phone_disconnect_v1.0.mp4"
            elif bg_color_main == "#ffffff":
                path_vid = r"vids\\Black_phone_disconnect_V3.1.mp4"
            if  len(phone_ip) == 0:
                messagebox.showerror('USB Connection Error',message=f"{current_selection} Isn't Connected Via A USB")
                re_checkup()
            elif 'inet addr:' not in phone_ip:
                messagebox.showerror('Network Error',message=f"{current_selection} Isn't Connected To A Netowork")
                re_checkup()
            else:
                if bool(Running_tasks_pid) != False:
                    try:
                        pid = Running_tasks_pid[id_dev]
                        filter_id = f"PID eq {pid}"
                        check_task_pid = subprocess.run(['tasklist','/fi',filter_id,'/fo','list'],shell=True,capture_output=True).stdout.decode()
                        if 'No tasks are running' in check_task_pid:
                            raw_full_addr = phone_ip.splitlines()[1]
                            raw_full_addr = raw_full_addr.removeprefix('          inet addr:')
                            raw_full_addr = raw_full_addr.split(' ')
                            phone_ip = raw_full_addr[0]
                            if auto_complete_gateway in phone_ip:
                                port = str(random.randint(5555,10000))
                                addr = f'{phone_ip}:{port}'
                                adb_tcpip_out = subprocess.run(['adb','-s',id_dev,'tcpip',port],shell=True,capture_output=True)
                                adb_connect_out = subprocess.run(['adb','connect',addr],shell=True,capture_output=True)
                                wireless_frame_disconnect.pack()
                                wireless_frame_disconnect.wait_visibility()
                                window_name = f"{current_selection} {addr}"
                                vid_playback_wireless = True
                                vid_playback_4_wireless_thread = threading.Thread(target=vid_playback_4_wireless,daemon=True,args=(path_vid,))
                                vid_playback_4_wireless_thread.start()
                                wait_until_disconnect_thread = threading.Thread(target=wait_until_disconnect,args=(id_dev,addr,window_name,port,adb_tcpip_out,adb_connect_out,wireless_frame_disconnect),daemon=True)
                                wait_until_disconnect_thread.start()
                            else:
                                messagebox.showerror('Network Error',message=f"{current_selection} Is Connected To A Different Netowork")
                                re_checkup()
                        else:
                            messagebox.showerror('Screen Share Error',message="Task Already Exists")
                            re_checkup()
                    except:
                        raw_full_addr = phone_ip.splitlines()[1]
                        raw_full_addr = raw_full_addr.removeprefix('          inet addr:')
                        raw_full_addr = raw_full_addr.split(' ')
                        phone_ip = raw_full_addr[0]
                        if auto_complete_gateway in phone_ip:
                            port = str(random.randint(5555,10000))
                            addr = f'{phone_ip}:{port}'
                            adb_tcpip_out = subprocess.run(['adb','-s',id_dev,'tcpip',port],shell=True,capture_output=True)
                            adb_connect_out = subprocess.run(['adb','connect',addr],shell=True,capture_output=True)
                            wireless_frame_disconnect.pack()
                            wireless_frame_disconnect.wait_visibility()
                            window_name = f"{current_selection} {addr}"
                            vid_playback_wireless = True
                            vid_playback_4_wireless_thread = threading.Thread(target=vid_playback_4_wireless,daemon=True,args=(path_vid,))
                            vid_playback_4_wireless_thread.start()
                            wait_until_disconnect_thread = threading.Thread(target=wait_until_disconnect,args=(id_dev,addr,window_name,port,adb_tcpip_out,adb_connect_out,wireless_frame_disconnect),daemon=True)
                            wait_until_disconnect_thread.start()
                        else:
                            messagebox.showerror('Network Error',message=f"{current_selection} Is Connected To A Different Netowork")
                            re_checkup()
                else:
                    raw_full_addr = phone_ip.splitlines()[1]
                    raw_full_addr = raw_full_addr.removeprefix('          inet addr:')
                    raw_full_addr = raw_full_addr.split(' ')
                    phone_ip = raw_full_addr[0]
                    if auto_complete_gateway in phone_ip:
                        port = str(random.randint(5555,10000))
                        addr = f'{phone_ip}:{port}'
                        adb_tcpip_out = subprocess.run(['adb','-s',id_dev,'tcpip',port],shell=True,capture_output=True)
                        adb_connect_out = subprocess.run(['adb','connect',addr],shell=True,capture_output=True)
                        wireless_frame_disconnect.pack()
                        wireless_frame_disconnect.wait_visibility()
                        window_name = f"{current_selection} {addr}"
                        vid_playback_wireless = True
                        vid_playback_4_wireless_thread = threading.Thread(target=vid_playback_4_wireless,daemon=True,args=(path_vid,))
                        vid_playback_4_wireless_thread.start()
                        wait_until_disconnect_thread = threading.Thread(target=wait_until_disconnect,args=(id_dev,addr,window_name,port,adb_tcpip_out,adb_connect_out,wireless_frame_disconnect),daemon=True)
                        wait_until_disconnect_thread.start()
                    else:
                        messagebox.showerror('Network Error',message=f"{current_selection} Is Connected To A Different Netowork")
                        re_checkup()
        except:
            re_checkup()
        break
    else:
        subprocess.Popen(['adb','kill-server'],shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
        exit()



def back_btn_wireless_func():
    pass





def wired():
    while EXIT_END != True:
        all_btn_activity('disabled')
        try:
            current_selection = list_box.get(list_box.curselection())
            for index,i in enumerate(devices.values()):
                if i == current_selection:
                    id_dev = list(devices.keys())[index]
            window_name = f"{current_selection} {id_dev}"
            if bool(Running_tasks_pid) != False:
                try:
                    pid = Running_tasks_pid[id_dev]
                    filter_id = f"PID eq {pid}"
                    check_task_pid = subprocess.run(['tasklist','/fi',filter_id,'/fo','list'],shell=True,capture_output=True).stdout.decode()
                    if 'No tasks are running' in check_task_pid:
                        subprocess.Popen(['scrcpy','--window-title',window_name,'--serial',id_dev],shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
                        add_task_with_pid_thread = threading.Thread(target=add_task_with_pid,args=(window_name,id_dev),daemon=True)
                        add_task_with_pid_thread.start()
                    else:
                        messagebox.showerror('Screen Share Error',message="Task Already Exists")
                        all_btn_activity('normal')
                except:
                    subprocess.Popen(['scrcpy','--window-title',window_name,'--serial',id_dev],shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
                    add_task_with_pid_thread = threading.Thread(target=add_task_with_pid,args=(window_name,id_dev),daemon=True)
                    add_task_with_pid_thread.start()
            else:
                subprocess.Popen(['scrcpy','--window-title',window_name,'--serial',id_dev],shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
                add_task_with_pid_thread = threading.Thread(target=add_task_with_pid,args=(window_name,id_dev),daemon=True)
                add_task_with_pid_thread.start()
        except:
            all_btn_activity('normal')
        break
    else:
        subprocess.Popen(['adb','kill-server'],shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
        exit()


def file_download():
    while EXIT_END != True:
        all_btn_activity('disabled')
        try:
            current_selection = list_box.get(list_box.curselection())
            for index,i in enumerate(devices.values()):
                if i == current_selection:
                    id_dev = list(devices.keys())[index]
            window_name = f"{current_selection} {id_dev}"
            if bool(Running_tasks_pid) != False:
                try:
                    pid = Running_tasks_pid[id_dev]
                    filter_id = f"PID eq {pid}"
                    check_task_pid = subprocess.run(['tasklist','/fi',filter_id,'/fo','list'],shell=True,capture_output=True).stdout.decode()
                    if 'No tasks are running' in check_task_pid:
                        # code without checking for task
                        pass
                    else:
                        messagebox.showerror('Multiple Tasks Requested',message="Another Task Already Exist")
                        all_btn_activity('normal')
                except:
                    # code without checking for task
                    pass
            else:
                # code without checking for task
                pass
        except:
            all_btn_activity('normal')
        break
    else:
        subprocess.Popen(['adb','kill-server'],shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
        exit()
    #file_downloading_btn.wait_visibility()
    # global vid_playback_downloading
    # if vid_playback_downloading != True:
    #     vid_playback_downloading = True
    #     path_vid_download = r"vids\\Downloading.mp4"
    #     vid_playback_4_downloading_thread = threading.Thread(target=vid_playback_4_downloading,daemon=True,args=(path_vid_download,))
    #     vid_playback_4_downloading_thread.start()
    pass

def file_upload():
    #global vid_playback_downloading
    #vid_playback_downloading = False
    pass

def checkup():
    attached = subprocess.run(['adb','devices'],shell=True,capture_output=True).stdout.decode()
    attached = attached.splitlines()
    attached.remove('List of devices attached'),attached.remove('')
    connected_devices = {}
    for id_shell in attached:
        if '\tdevice' not in id_shell:
            id_name = "Unauthorized"
        else:
            if ':' not in id_shell:
                id_shell = id_shell.removesuffix('\tdevice')
                if bool(Running_tasks_pid):
                    try:
                        pid = Running_tasks_pid[id_shell]
                        filter_id = f"PID eq {pid}"
                        check_task_pid = subprocess.run(['tasklist','/fi',filter_id,'/fo','list'],shell=True,capture_output=True).stdout.decode()
                        if 'No tasks are running' in check_task_pid:
                            id_name = subprocess.run(['adb','-s',id_shell,'shell','getprop','ro.product.model'],shell=True,capture_output=True).stdout.decode()
                            id_name = id_name.removesuffix('\r\n')
                            connected_devices[id_shell] = id_name
                    except:
                        id_name = subprocess.run(['adb','-s',id_shell,'shell','getprop','ro.product.model'],shell=True,capture_output=True).stdout.decode()
                        id_name = id_name.removesuffix('\r\n')
                        connected_devices[id_shell] = id_name
                else:
                    id_name = subprocess.run(['adb','-s',id_shell,'shell','getprop','ro.product.model'],shell=True,capture_output=True).stdout.decode()
                    id_name = id_name.removesuffix('\r\n')
                    connected_devices[id_shell] = id_name
    connected_devices_vals = list(connected_devices.values())
    def repeat_until_success(index,i,connected_devices_vals,n):
        if n == None:
            n = 1
        i = f'{i} {n}'
        if i in connected_devices_vals:
            i = i.removesuffix(f' {n}')
            n +=1
            repeat_until_success(index,i,connected_devices_vals,n)
        else:
            connected_devices_vals[index] = i
    for index,i in enumerate(connected_devices_vals):
        if connected_devices_vals.count(i) > 1:
            n = None
            repeat_until_success(index,i,connected_devices_vals,n)
    connected_devices = dict(zip(connected_devices.keys(),connected_devices_vals))
    for i in sorted(connected_devices.values()):
        list_box.insert(END,i)
        if i == "Unauthorized":
            unauthorized_noti_btn.configure(width=30,height=30,state='disabled')
            unauthorized_noti_btn.place(x=230,y=200)
    for i in range(list_box.size()):
        if i %2 ==0:
            list_box.itemconfigure(i,bg="#1a8cff")
        else:
            list_box.itemconfigure(i,bg="#ffff00")
    return connected_devices

def re_checkup():
    while EXIT_END != True:
        global devices,RESTART_TIMER
        all_btn_activity('disabled')
        unauthorized_noti_btn.place_forget()
        list_box.delete(0,END)
        RESTART_TIMER = True
        devices = checkup()
        all_btn_activity('normal')
        break
    else:
        exit()

def change_bg():
    global bg_color_main
    global current_mode_png
    if bg_color_main == "#000000":
        bg_color_main = "#ffffff"
        current_mode_png = light_mode_png
    elif bg_color_main == "#ffffff":
        bg_color_main = "#000000"
        current_mode_png = dark_mode_png
    clr_btn.forget
    clr_btn.configure(width=30,height=30,image=current_mode_png)
    clr_btn.place(x=40,y=40)
    main_window.forget
    main_window.title('ScreenDroid')
    main_window.geometry("400x600")
    main_window.configure(background=bg_color_main)

def re_checkup_bind(event):
    re_checkup()

main_window = Tk()
main_window.title('ScreenDroid')
main_window.geometry("400x600+200+10")
main_window.configure(background=bg_color_main)
main_window.maxsize(width=400,height=600)
main_window.minsize(width=400,height=600)
main_window.protocol('WM_DELETE_WINDOW',exiting)
main_window.bind('<Escape>',ask_4_exit)
main_window.bind('<F5>',re_checkup_bind)
main_window.bind('<F4>',kill_process_bind)

list_box = Listbox(main_window,bd=2,width=30,activestyle='none',selectbackground='#00c300')
list_box.place(x=100,y=200)

light_mode_png = PhotoImage(file=r'icons\\light_mode_FILL0_wght300_GRAD0_opsz36.png')
dark_mode_png = PhotoImage(file=r'icons\\dark_mode_FILL0_wght300_GRAD0_opsz36.png')
current_mode_png = dark_mode_png

clr_btn = Button(main_window,text='BGCOLOR',command=change_bg,bd=3,activebackground='#989898')
clr_btn.configure(width=30,height=30,image=current_mode_png)
clr_btn.place(x=40,y=40)

refresh_png = PhotoImage(file=r'icons\\refresh_FILL0_wght300_GRAD0_opsz36.png')
rfrsh_btn = Button(main_window,text='Refresh',image=refresh_png,command=re_checkup,bd=3,activebackground="#33d333")
rfrsh_btn.configure(width=30,height=30,state='normal')
rfrsh_btn.place(x=82,y=40)

unauthorized_noti_png = PhotoImage(file=r'icons\\security_update_warning_FILL0_wght300_GRAD0_opsz36.png')
unauthorized_noti_btn = Button(main_window,text='Error_Unauthor',image=unauthorized_noti_png)

wired_btn_png = PhotoImage(file=r'icons\\mobile_screen_share_FILL0_wght300_GRAD0_opsz48.png')
wired_btn = Button(main_window,text='scrcpy cable',image=wired_btn_png,command=wired)
wired_btn.configure(width=48,height=48,bd=3,activebackground="#377bb9")
wired_btn.place(x=50,y=400)

wireless_btn_png = PhotoImage(file=r'icons\\mobile_screen_wireless_share_FILL0_wght300_GRAD0_opsz48.png')
wireless_btn = Button(main_window,text='scrcpy wireless',image=wireless_btn_png,command=wireless)
wireless_btn.configure(width=48,height=48,bd=3,activebackground='#b0416e')
wireless_btn.place(x=120,y=400)

kill_btn_png = PhotoImage(file=r'icons\\cancel_FILL0_wght300_GRAD0_opsz36.png')
kill_btn = Button(main_window,text='end_all',image=kill_btn_png,command=kill_process,bd=3)
kill_btn.configure(width=30,height=30,activebackground="#ce1000")
kill_btn.place(x=124,y=40)



auto_refresh = Entry(main_window,width=2,font='Terminal')
auto_refresh.place(x=270,y=30)

file_download_btn_png = PhotoImage(file=r'icons\\file_download_FILL0_wght400_GRAD0_opsz48.png')
file_download_btn = Button(main_window,text='adb pull',image=file_download_btn_png,command=file_download)
file_download_btn.configure(width=48,height=48,bd=3,activebackground='#66ffcc')
file_download_btn.place(x=190,y=400)


file_upload_btn_png = PhotoImage(file=r'icons\\file_upload_FILL0_wght400_GRAD0_opsz48.png')
file_upload_btn = Button(main_window,text='adb push',image=file_upload_btn_png,command=file_upload)
file_upload_btn.configure(width=48,height=48,bd=3,activebackground='#ff9602')
file_upload_btn.place(x=260,y=400)

whatsapp_btn_png = PhotoImage(file=r'icons\\whats_trans_black_v3.png')
whatsapp_btn_pressed_png = PhotoImage(file=r'icons\\whats_trans_green_button.png')
whatsapp_btn = Button(main_window,text='adb pull whats',command=file_upload)
whatsapp_btn.configure(width=48,height=48,bd=3,activebackground='green',image=whatsapp_btn_png)
whatsapp_btn.place(x=50,y=470)
def change_pic_whats(event):
    whatsapp_btn.configure(image=whatsapp_btn_pressed_png)
def change_pic_whats_og(event):
    whatsapp_btn.configure(image=whatsapp_btn_png)
whatsapp_btn.bind("<ButtonPress>",change_pic_whats)
whatsapp_btn.bind("<ButtonRelease>",change_pic_whats_og)


file_downloading_btn_png = PhotoImage(file=r'icons\\downloading_FILL0_wght400_GRAD0_opsz48.png')
file_downloading_btn_complete_png = PhotoImage(file=r'icons\\file_download_done_FILL0_wght400_GRAD0_opsz48.png')
file_downloading_btn = Button(main_window,width=48,height=48,image=file_downloading_btn_png)
file_downloading_btn.place(x=100,y=100)




wireless_frame_disconnect = Frame(main_window,width=400,height=600)
wireless_frame_disconnect.configure(background=bg_color_main)
vid_label_wireless = Label(wireless_frame_disconnect)
vid_label_wireless.pack()





#file_download_btn.bind("<ButtonRelease>",back2normal)
#wireless_frame = Frame(main_window,width=400,height=600)
#wireless_frame.configure(background=bg_color_main)


#back_wireless_btn_png = PhotoImage(file='arrow_back_ios_new_FILL0_wght300_GRAD0_opsz36.png')
#back_wireless_btn = Button(wireless_frame,width=30,height=30,name='back_btn',image=back_wireless_btn_png,command=back_btn_wireless_func)
#back_wireless_btn.place(x=20,y=30)


#wireless_new_connect_btn = Button(wireless_frame,text='Connect',width=13,height=1,fg='black',background='#c0c0c0',justify='center',font='Terminal',border=6)
#wireless_new_connect_btn.place(x=106,y=500)

#wireless_new_coonect_address = Entry(wireless_frame,width=20,border=3,font='Terminal',bd=10)
#wireless_new_coonect_address.insert(END,auto_complete_gateway)
#wireless_new_coonect_address.place(x=70,y=300)

auto_refresh_checkup_thread = threading.Thread(target=auto_refresh_checkup,daemon=True)
auto_refresh_checkup_thread.start()
#print(datetime.now())
main_window.mainloop()
subprocess.run(['adb','kill-server'],shell=True,capture_output=True)