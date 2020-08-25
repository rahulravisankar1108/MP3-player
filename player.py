from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root =Tk()
root.title("Rspotify")
root.geometry("500x400")

#initialize pygame
pygame.mixer.init()

#craete a function to deal with time
def play_time():
    #check to see if song is stopped
    if stopped:
        return 

    #grab curr song time
    current_time = pygame.mixer.music.get_pos() / 1000
    #convert song time to time format
    converted__current_time=time.strftime('%M:%S', time.gmtime(current_time))
    #reconstruct song with dir structure stuff
    song = playlist_box.get(ACTIVE)
    song =f'D:/mp3/audio/{song}.mp3'
    #find curr song length
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length
    #convert to time format
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
    
    #check to see if song is over
    if int(song_slider.get()) == int(song_length):
        stop()
    #check to see if paused, if so pass 
    elif paused:
        pass
    
    else:
        #Move slider along one sec at a time
        next_time  = int(song_slider.get()) + 1
        #o/p new time value to slider and to length of a song
        song_slider.config(to=song_length,value=next_time)

        #convert slider pos to time format
        converted__current_time=time.strftime('%M:%S', time.gmtime(int(song_slider.get())))

        #o/p slider
        status_bar.config(text=f'Time Elapsed: {converted__current_time} of {converted_song_length}   ')


    #add curr time to status bar
    if(current_time>=1):
        status_bar.config(text=f'Time Elapsed: {converted__current_time} of {converted_song_length}   ')
    #create loop to check the time every second
    status_bar.after(1000,play_time)

#add 1 song to playlist
def add_song():
    song = filedialog.askopenfilename(initialdir='audio/', title="Choose A Song", filetype=(("mp3 Files", "*.mp3"), ) )
    #my_label.config(text=song)
    #strip out dir structure and .mp3 from song
    song=song.replace("D:/mp3/audio/", "")
    song=song.replace(".mp3", "")
    #add to end of playlist
    playlist_box.insert(END, song)


#add many songs to playlist
def add_many_song():
    songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose A Song", filetype=(("mp3 Files", "*.mp3"), ) )
    #my_label.config(text=song)

    #loop through song list and replace directory structure mp2 from song name
    for song in songs:
        #strip out dir structure and .mp3 from song
        song=song.replace("D:/mp3/audio/", "")
        song=song.replace(".mp3", "")
        #add to end of playlist
        playlist_box.insert(END, song)

#create a func to del a song from playlist
def delete_song():
    #delete highlighted song from playlist
    playlist_box.delete(ANCHOR)

#create a func to del all song from playlist
def delete_all_song():
    #del all songs
    playlist_box.delete(0, END)

def play():
    #set stopped to False since a song is now playing 
    global stopped 
    stopped = False
    #reconstruct song with dir structure stuff
    song = playlist_box.get(ACTIVE)
    song =f'D:/mp3/audio/{song}.mp3'
    #my_label.config(text=song)

    #play song woth pygame mixer
    pygame.mixer.music.load(song)
    #play a sing with pygame mixer
    pygame.mixer.music.play(loops=0)
    #get song time
    play_time()

#create stopped var
global stopped
stopped = False
#create stop function
def stop():
    #stop a song
    pygame.mixer.music.stop()
    #clear playlist bar
    playlist_box.selection_clear(ACTIVE)
    status_bar.config(text='')
    #set slider value to 0
    song_slider.config(value=0)
    #set stop var to true
    global stopped
    stopped = True

#create fun to play the next song
def forward():
    #reset slider pos and status bar
    status_bar.config(text='')
    song_slider.config(value=0)
    #get current song number
    next_one=playlist_box.curselection()
    #my_label.config(text=next_one)
    #add one to the current song number
    next_one=next_one[0] + 1 
    #grab the song title from playlist 
    song = playlist_box.get(next_one)
    #add directory structure stuff to the song 
    song =f'D:/mp3/audio/{song}.mp3'
    #play song woth pygame mixer
    pygame.mixer.music.load(song)
    #play a sing with pygame mixer
    pygame.mixer.music.play(loops=0)
    #clear acrive bar in playlist
    playlist_box.selection_clear(0,END)
    #move active bar to next song
    playlist_box.activate(next_one)
    #set active bar to next song 
    playlist_box.selection_set(next_one,last=None)

def previous():
    #reset slider pos and status bar
    status_bar.config(text='')
    song_slider.config(value=0)
    #get current song number
    next_one=playlist_box.curselection()
    #my_label.config(text=next_one)
    #add one to the current song number
    next_one=next_one[0] - 1 
    #grab the song title from playlist 
    song = playlist_box.get(next_one)
    #add directory structure stuff to the song 
    song =f'D:/mp3/audio/{song}.mp3'
    #play song woth pygame mixer
    pygame.mixer.music.load(song)
    #play a sing with pygame mixer
    pygame.mixer.music.play(loops=0)

    #clear acrive bar in playlist
    playlist_box.selection_clear(0,END)
    #move active bar to next song
    playlist_box.activate(next_one)
    #set active bar to next song 
    playlist_box.selection_set(next_one,last=None)

#create paused var
global paused 
paused = False

#create pause function
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        #unpause
        pygame.mixer.music.unpause()
        paused=False
    else:
        #pause
        pygame.mixer.music.pause()
        paused=True

#create vol func
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())

#create slide func for song pos
def song_slide(x):
    #reconstruct song with dir structure stuff
    song = playlist_box.get(ACTIVE)
    song =f'D:/mp3/audio/{song}.mp3'
    #my_label.config(text=song)

    #play song with pygame mixer
    pygame.mixer.music.load(song)
    #play a sing with pygame mixer
    pygame.mixer.music.play(loops=0, start=song_slider.get())

#Create main frame
main_frame=Frame(root)
main_frame.pack(pady=20)

#create playlist box
playlist_box=Listbox(main_frame, bg="yellow", fg="green", width=60, selectbackground="green", selectforeground="yellow")
playlist_box.grid(row=0,column=0)

#Create volume slider frame
volume_frame = LabelFrame(main_frame, text="Volume")
volume_frame.grid(row=0,column=1,padx=20)

#create volume slider 
volume_slider=ttk.Scale(volume_frame,from_=1, to=0,orient=VERTICAL,value=1,length=125,command=volume)
volume_slider.pack(pady=10)

#create song slider
song_slider = ttk.Scale(main_frame,from_=0, to=100,orient=HORIZONTAL,value=0,length=360,command=song_slide)
song_slider.grid(row=2,column=0,pady=20)

#define button images for controls
back_btn_img=PhotoImage(file='images/back.png ')
forward_btn_img=PhotoImage(file='images/forward.png')
play_btn_img=PhotoImage(file='images/play.png')
pause_btn_img=PhotoImage(file='images/pause.png')
stop_btn_img=PhotoImage(file='images/stop.png')

#create button frame
control_frame=Frame(main_frame)
control_frame.grid(row=1,column=0,pady=20)

#create play/pause etc button 
back_button=Button(control_frame, image=back_btn_img,borderwidth=0,command=previous)
play_button=Button(control_frame, image=play_btn_img,borderwidth=0, command=play)
pause_button=Button(control_frame, image=pause_btn_img,borderwidth=0, command=lambda: pause(paused))
stop_button=Button(control_frame, image=stop_btn_img,borderwidth=0 , command=stop)
forward_button=Button(control_frame, image=forward_btn_img,borderwidth=0, command=forward)

back_button.grid(row=0,column=0,padx=10)
forward_button.grid(row=0,column=4,padx=10)
play_button.grid(row=0,column=1,padx=10)
pause_button.grid(row=0,column=2,padx=10)
stop_button.grid(row=0,column=3,padx=10)

#create menu
my_menu = Menu(root)
root.config(menu=my_menu)

#create add song menu dropdown
add_song_menu=Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Add Songs",menu=add_song_menu)
#add one song to playlist
add_song_menu.add_command(label="Add one song to playlist",command=add_song)
#add many song to playlist
add_song_menu.add_command(label="Add multiple songs to playlist",command=add_many_song)

#Create delete song menu dropdowns
remove_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove Songs", menu = remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete All Song From Playlist", command=delete_all_song)

#create status bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)



#Temporary label
my_label = Label(root, text="")
my_label.pack(pady=20)

root.mainloop()