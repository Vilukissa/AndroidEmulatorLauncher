#!/usr/bin/python
import subprocess
from subprocess import CalledProcessError
import time

def wait_for_device(emu_name):
    # Launch the emulator process
    emu_cmd = 'emulator -avd {0}'.format(emu_name)
    emu_sproc = subprocess.Popen(emu_cmd.split())
    print 'Opening emulator ({0})...'.format(emu_name)

    # Launch the emulator waiting process
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    emu_wait_cmd = 'adb -e wait-for-device'
    emu_wait_sproc = subprocess.Popen(emu_wait_cmd.split(), startupinfo=startupinfo)
    print 'Waiting for emulator to start...'

    # Now we sit and wait for the emulator startup
    wait_passed = True
    emu_wait_secs = 0
    emu_wait_interval = 1
    emu_wait_max = 120 # 2 min
    while emu_wait_sproc.poll() is None:
        time.sleep(emu_wait_interval)
        emu_wait_secs += emu_wait_interval
        if emu_wait_secs >= emu_wait_max:
            wait_passed = False
            print 'Waited emulator launch for {0} secs!'.format(emu_wait_max)
            # TODO: should we stop the processes...
            break

    return wait_passed

def wait_for_boot():
    print 'Waiting for emulator to boot properly...'
    
    # Poll the init.svc.bootanim property
    wait_passed = True
    emu_boot_wait_secs = 0
    emu_boot_wait_interval = 5
    emu_boot_max = 600 # 10 min
    while check_boot() == 1:
        time.sleep(emu_boot_wait_interval)
        emu_boot_wait_secs += emu_boot_wait_interval
        if emu_boot_wait_secs >= emu_boot_max:
            wait_passed = False
            print 'Waited emulator boot for {0} secs!'.format(emu_boot_max)
            break

    return wait_passed

def check_boot():
    boot_poll_cmd = 'adb shell getprop init.svc.bootanim'
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        output = subprocess.check_output(boot_poll_cmd.split(), startupinfo=startupinfo)
        output = output.strip(' \t\n\r')
        #print output
    except CalledProcessError as err:
        #print 'error'
        #print err.returncode
        output = 'error'

    if output == 'stopped':
        #print 'boot OK'
        return 0
    else:
        #print 'boot not OK'
        return 1

def open_screen_lock():
    subprocess.call('adb shell input keyevent 82')
