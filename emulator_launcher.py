#!/usr/bin/python
import sys
import subprocess
import time
import adb_helper

def make_init_check():
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        return False
    #elif:
    # TODO: emulator path check, adb path check...
    else:
        return True

def launch_emulator(emu_name):
    # TODO: if there's another emulator already running the checks
    # will pass right away. This might be a problem...
    
    emulator_is_online = adb_helper.wait_for_device(emu_name)

    if emulator_is_online:
        emulator_booted = adb_helper.wait_for_boot()

        if emulator_booted:
            print 'Now we are talking! Emulator signaled to be running good'

            # At this point it's good to wait a little bit more
            # because the emulator might not be settled enough yet
            print 'The emulator might not be settled enough yet so wait a little bit longer before trying to unlock the screen'
            # TODO: could this be done with some other prop check
            time.sleep(60)

            # Unlock screen lock if it's there
            print 'Lets unlock the screen if there\'s a screen lock'
            adb_helper.open_screen_lock()

            print 'Emulator is now ready to be used!'
        else:
            print 'Emulator was not booted at time so lets quit this crap...'
    else:
        print 'Emulator was not online at time so lets quit this crap...'
        

if __name__ == "__main__":
    if make_init_check():
        launch_emulator(sys.argv[1])
    else:
        print 'Init check failed'

