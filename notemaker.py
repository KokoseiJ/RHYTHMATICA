import os
import pygame
import subprocess


def cut_song(file, start, duration):
    start = max(0, start)
    args = [
        "ffmpeg",
        "-ss", str(start),
        "-t", str(duration),
        "-i", file,
        "-c:a", "copy",
        "-f", "wav", 
        "-"
    ]

    proc = subprocess.run(args, stdout=subprocess.PIPE)

    return proc.stdout


def main():
    name = input("Name: ")
    artist = input("Artist: ")
    bpm = int(input("BPM: "))

    music = os.path.join(name, "song.wav")

    pygame.init()
    pygame.display.set_mode((640, 480))

    notes = []
    notecount = 0
    current_chunk = None
    current_channel = None
    keydown = False

    bpm = bpm
    div = 1
    start_time = 0
    n = 0

    while True:
        spb = 60 / bpm / div
        start = start_time + spb * n
        wav = cut_song(music, start - spb, spb)
        current_chunk = pygame.mixer.Sound(wav)
        if current_channel is not None:
            current_channel.stop()
        current_channel = current_chunk.play()

        keys = []

        kill = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        kill = True
                        break

                    elif event.key == pygame.K_r:
                        current_channel.stop()
                        current_channel = current_chunk.play()

                    elif event.key == pygame.K_f:
                        pygame.mixer.Sound(cut_song(music, start, spb)).play()

                    elif event.key == pygame.K_SPACE:
                        n += 1
                        notes.append("/1")
                        break

                    elif event.key == pygame.K_i:
                        command = input("Command: ")
                        if command[0] == "b":
                            start_time = start
                            n = 0
                            bpm = float(command[1:])

                        elif command[0] == "d":
                            start_time = start
                            n = 0
                            div = int(command[1:])

                        elif command[0] == "w":
                            start_time = float(command[1:])
                            n = 0

                        elif command[0] == "/":
                            n += int(command[1:])

                        else:
                            print("Unknown Command")
                            continue

                        notes.append(command)
                        break

                    elif pygame.key.name(event.key) in "tyghbn":
                        keys.append("tyghbn".index(pygame.key.name(event.key)) + 1)
                        notecount += 1
                        keydown = True
                
                elif keydown and event.type == pygame.KEYUP and pygame.key.name(event.key) in "tyghbn":
                    keydown = False
                    notes.append("".join([str(x) for x in keys]))
                    n += 1
                    break

            else:
                continue
            break

        if kill:
            break

    with open(os.path.join(name, "info.txt"), "w") as f:
        f.write(name + "\n")
        f.write(artist + "\n")
        f.write(str(bpm) + "\n")
        f.write(str(notecount) + "\n")

    with open(os.path.join(name, "note.txt"), "w") as f:
        f.write("ver:A4\n")
        f.write("\n".join(notes) + "\n")

    return


main()
