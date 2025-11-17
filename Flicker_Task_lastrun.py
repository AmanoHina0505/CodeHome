#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2024.2.4),
    on June 10, 2025, at 20:14
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware
from psychopy.tools import environmenttools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER, priority)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2024.2.4'
expName = 'Flicker_Task'  # from the Builder filename that created this script
# information about this experiment
expInfo = {
    'participant': '',
    'session': '001',
    'date|hid': data.getDateStr(),
    'expName|hid': expName,
    'psychopyVersion|hid': psychopyVersion,
}

# --- Define some variables which will change depending on pilot mode ---
'''
To run in pilot mode, either use the run/pilot toggle in Builder, Coder and Runner, 
or run the experiment with `--pilot` as an argument. To change what pilot 
#mode does, check out the 'Pilot mode' tab in preferences.
'''
# work out from system args whether we are running in pilot mode
PILOTING = core.setPilotModeFromArgs()
# start off with values from experiment settings
_fullScr = True
_winSize = [1280, 720]
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
        # set window size
        _winSize = prefs.piloting['forcedWindowSize']

def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=expInfo, sortKeys=False, title=expName, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    # remove dialog-specific syntax from expInfo
    for key, val in expInfo.copy().items():
        newKey, _ = data.utils.parsePipeSyntax(key)
        expInfo[newKey] = expInfo.pop(key)
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath='F:\\Shibaura\\2023\\2022Fall\\Research\\Experiment\\Flicker_Experiment\\Flicker_Task_lastrun.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # set how much information should be printed to the console / app
    if PILOTING:
        logging.console.setLevel(
            prefs.piloting['pilotConsoleLoggingLevel']
        )
    else:
        logging.console.setLevel('warning')
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log')
    if PILOTING:
        logFile.setLevel(
            prefs.piloting['pilotLoggingLevel']
        )
    else:
        logFile.setLevel(
            logging.getLevel('exp')
        )
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if PILOTING:
        logging.debug('Fullscreen settings ignored as running in pilot mode.')
    
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=_winSize, fullscr=_fullScr, screen=0,
            winType='pyglet', allowGUI=False, allowStencil=False,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0,0,0]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    if expInfo is not None:
        # get/measure frame rate if not already in expInfo
        if win._monitorFrameRate is None:
            win._monitorFrameRate = win.getActualFrameRate(infoMsg='Attempting to measure frame rate of screen, please wait...')
        expInfo['frameRate'] = win._monitorFrameRate
    win.hideMessage()
    # show a visual indicator if we're in piloting mode
    if PILOTING and prefs.piloting['showPilotingIndicator']:
        win.showPilotingIndicator()
    
    return win


def setupDevices(expInfo, thisExp, win):
    """
    Setup whatever devices are available (mouse, keyboard, speaker, eyetracker, etc.) and add them to 
    the device manager (deviceManager)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    bool
        True if completed successfully.
    """
    # --- Setup input devices ---
    ioConfig = {}
    
    # Setup iohub keyboard
    ioConfig['Keyboard'] = dict(use_keymap='psychopy')
    
    # Setup iohub experiment
    ioConfig['Experiment'] = dict(filename=thisExp.dataFileName)
    
    # Start ioHub server
    ioServer = io.launchHubServer(window=win, **ioConfig)
    
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='iohub'
        )
    if deviceManager.getDevice('key_resp_2') is None:
        # initialise key_resp_2
        key_resp_2 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp_2',
        )
    if deviceManager.getDevice('key_resp') is None:
        # initialise key_resp
        key_resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp',
        )
    # return True if completed successfully
    return True

def pauseExperiment(thisExp, win=None, timers=[], playbackComponents=[]):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    playbackComponents : list, tuple
        List of any components with a `pause` method which need to be paused.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # start a timer to figure out how long we're paused for
    pauseTimer = core.Clock()
    # pause any playback components
    for comp in playbackComponents:
        comp.pause()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass='keyboard',
            deviceName='defaultKeyboard',
            backend='ioHub',
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win)
        # sleep 1ms so other threads can execute
        clock.time.sleep(0.001)
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    for comp in playbackComponents:
        comp.play()
    # reset any timers
    for timer in timers:
        timer.addTime(-pauseTimer.getTime())


def run(expInfo, thisExp, win, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # make sure window is set to foreground to prevent losing focus
    win.winHandle.activate()
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='ioHub'
        )
    eyetracker = deviceManager.getDevice('eyetracker')
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    
    # --- Initialize components for Routine "Instruction" ---
    image = visual.ImageStim(
        win=win,
        name='image', units='pix', 
        image='instruction.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(1920, 1080),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    key_resp_2 = keyboard.Keyboard(deviceName='key_resp_2')
    
    # --- Initialize components for Routine "Start" ---
    text_2 = visual.TextStim(win=win, name='text_2',
        text='',
        font='Open Sans',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "Initialize" ---
    image1_2 = visual.ImageStim(
        win=win,
        name='image1_2', 
        image='default.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(1.4, 1.05),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    Cimage1_2 = visual.ImageStim(
        win=win,
        name='Cimage1_2', 
        image='default.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(1.4, 1.05),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-1.0)
    # Run 'Begin Experiment' code from code
    stim1 = ''
    stim2 = ''
    
    # --- Initialize components for Routine "Neutral1" ---
    image1 = visual.ImageStim(
        win=win,
        name='image1', 
        image='default.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(1.4, 1.05),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    Cimage1 = visual.ImageStim(
        win=win,
        name='Cimage1', 
        image='default.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(1.4, 1.05),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-1.0)
    key_resp = keyboard.Keyboard(deviceName='key_resp')
    
    # create some handy timers
    
    # global clock to track the time since experiment started
    if globalClock is None:
        # create a clock if not given one
        globalClock = core.Clock()
    if isinstance(globalClock, str):
        # if given a string, make a clock accoridng to it
        if globalClock == 'float':
            # get timestamps as a simple value
            globalClock = core.Clock(format='float')
        elif globalClock == 'iso':
            # get timestamps in ISO format
            globalClock = core.Clock(format='%Y-%m-%d_%H:%M:%S.%f%z')
        else:
            # get timestamps in a custom format
            globalClock = core.Clock(format=globalClock)
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(
        format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6
    )
    
    # set up handler to look after randomisation of conditions etc
    trials_block = data.TrialHandler2(
        name='trials_block',
        nReps=1.0, 
        method='random', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions('PracticeBlock.xlsx'), 
        seed=None, 
    )
    thisExp.addLoop(trials_block)  # add the loop to the experiment
    thisTrials_block = trials_block.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrials_block.rgb)
    if thisTrials_block != None:
        for paramName in thisTrials_block:
            globals()[paramName] = thisTrials_block[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisTrials_block in trials_block:
        currentLoop = trials_block
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisTrials_block.rgb)
        if thisTrials_block != None:
            for paramName in thisTrials_block:
                globals()[paramName] = thisTrials_block[paramName]
        
        # --- Prepare to start Routine "Instruction" ---
        # create an object to store info about Routine Instruction
        Instruction = data.Routine(
            name='Instruction',
            components=[image, key_resp_2],
        )
        Instruction.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # create starting attributes for key_resp_2
        key_resp_2.keys = []
        key_resp_2.rt = []
        _key_resp_2_allKeys = []
        # store start times for Instruction
        Instruction.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        Instruction.tStart = globalClock.getTime(format='float')
        Instruction.status = STARTED
        thisExp.addData('Instruction.started', Instruction.tStart)
        Instruction.maxDuration = None
        # keep track of which components have finished
        InstructionComponents = Instruction.components
        for thisComponent in Instruction.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "Instruction" ---
        # if trial has changed, end Routine now
        if isinstance(trials_block, data.TrialHandler2) and thisTrials_block.thisN != trials_block.thisTrial.thisN:
            continueRoutine = False
        Instruction.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *image* updates
            
            # if image is starting this frame...
            if image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                image.frameNStart = frameN  # exact frame index
                image.tStart = t  # local t and not account for scr refresh
                image.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(image, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'image.started')
                # update status
                image.status = STARTED
                image.setAutoDraw(True)
            
            # if image is active this frame...
            if image.status == STARTED:
                # update params
                pass
            
            # *key_resp_2* updates
            waitOnFlip = False
            
            # if key_resp_2 is starting this frame...
            if key_resp_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                key_resp_2.frameNStart = frameN  # exact frame index
                key_resp_2.tStart = t  # local t and not account for scr refresh
                key_resp_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_resp_2.started')
                # update status
                key_resp_2.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_resp_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if key_resp_2.status == STARTED and not waitOnFlip:
                theseKeys = key_resp_2.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
                _key_resp_2_allKeys.extend(theseKeys)
                if len(_key_resp_2_allKeys):
                    key_resp_2.keys = _key_resp_2_allKeys[-1].name  # just the last key pressed
                    key_resp_2.rt = _key_resp_2_allKeys[-1].rt
                    key_resp_2.duration = _key_resp_2_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                Instruction.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Instruction.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Instruction" ---
        for thisComponent in Instruction.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for Instruction
        Instruction.tStop = globalClock.getTime(format='float')
        Instruction.tStopRefresh = tThisFlipGlobal
        thisExp.addData('Instruction.stopped', Instruction.tStop)
        # check responses
        if key_resp_2.keys in ['', [], None]:  # No response was made
            key_resp_2.keys = None
        trials_block.addData('key_resp_2.keys',key_resp_2.keys)
        if key_resp_2.keys != None:  # we had a response
            trials_block.addData('key_resp_2.rt', key_resp_2.rt)
            trials_block.addData('key_resp_2.duration', key_resp_2.duration)
        # the Routine "Instruction" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "Start" ---
        # create an object to store info about Routine Start
        Start = data.Routine(
            name='Start',
            components=[text_2],
        )
        Start.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        text_2.setText(group)
        # store start times for Start
        Start.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        Start.tStart = globalClock.getTime(format='float')
        Start.status = STARTED
        thisExp.addData('Start.started', Start.tStart)
        Start.maxDuration = None
        # keep track of which components have finished
        StartComponents = Start.components
        for thisComponent in Start.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "Start" ---
        # if trial has changed, end Routine now
        if isinstance(trials_block, data.TrialHandler2) and thisTrials_block.thisN != trials_block.thisTrial.thisN:
            continueRoutine = False
        Start.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 1.0:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *text_2* updates
            
            # if text_2 is starting this frame...
            if text_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                text_2.frameNStart = frameN  # exact frame index
                text_2.tStart = t  # local t and not account for scr refresh
                text_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text_2.started')
                # update status
                text_2.status = STARTED
                text_2.setAutoDraw(True)
            
            # if text_2 is active this frame...
            if text_2.status == STARTED:
                # update params
                pass
            
            # if text_2 is stopping this frame...
            if text_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > text_2.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    text_2.tStop = t  # not accounting for scr refresh
                    text_2.tStopRefresh = tThisFlipGlobal  # on global time
                    text_2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'text_2.stopped')
                    # update status
                    text_2.status = FINISHED
                    text_2.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                Start.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Start.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Start" ---
        for thisComponent in Start.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for Start
        Start.tStop = globalClock.getTime(format='float')
        Start.tStopRefresh = tThisFlipGlobal
        thisExp.addData('Start.stopped', Start.tStop)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if Start.maxDurationReached:
            routineTimer.addTime(-Start.maxDuration)
        elif Start.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.000000)
        
        # set up handler to look after randomisation of conditions etc
        trials_practice = data.TrialHandler2(
            name='trials_practice',
            nReps=1.0, 
            method='random', 
            extraInfo=expInfo, 
            originPath=-1, 
            trialList=data.importConditions(file), 
            seed=None, 
        )
        thisExp.addLoop(trials_practice)  # add the loop to the experiment
        thisTrials_practice = trials_practice.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisTrials_practice.rgb)
        if thisTrials_practice != None:
            for paramName in thisTrials_practice:
                globals()[paramName] = thisTrials_practice[paramName]
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        
        for thisTrials_practice in trials_practice:
            currentLoop = trials_practice
            thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
            if thisSession is not None:
                # if running in a Session with a Liaison client, send data up to now
                thisSession.sendExperimentData()
            # abbreviate parameter names if possible (e.g. rgb = thisTrials_practice.rgb)
            if thisTrials_practice != None:
                for paramName in thisTrials_practice:
                    globals()[paramName] = thisTrials_practice[paramName]
            
            # --- Prepare to start Routine "Initialize" ---
            # create an object to store info about Routine Initialize
            Initialize = data.Routine(
                name='Initialize',
                components=[image1_2, Cimage1_2],
            )
            Initialize.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            image1_2.setImage(Image1)
            Cimage1_2.setImage(Image2)
            # store start times for Initialize
            Initialize.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            Initialize.tStart = globalClock.getTime(format='float')
            Initialize.status = STARTED
            thisExp.addData('Initialize.started', Initialize.tStart)
            Initialize.maxDuration = None
            # keep track of which components have finished
            InitializeComponents = Initialize.components
            for thisComponent in Initialize.components:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "Initialize" ---
            # if trial has changed, end Routine now
            if isinstance(trials_practice, data.TrialHandler2) and thisTrials_practice.thisN != trials_practice.thisTrial.thisN:
                continueRoutine = False
            Initialize.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine and routineTimer.getTime() < 0.64:
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *image1_2* updates
                
                # if image1_2 is starting this frame...
                if image1_2.status == NOT_STARTED and tThisFlip >= 0.08-frameTolerance:
                    # keep track of start time/frame for later
                    image1_2.frameNStart = frameN  # exact frame index
                    image1_2.tStart = t  # local t and not account for scr refresh
                    image1_2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(image1_2, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'image1_2.started')
                    # update status
                    image1_2.status = STARTED
                    image1_2.setAutoDraw(True)
                
                # if image1_2 is active this frame...
                if image1_2.status == STARTED:
                    # update params
                    pass
                
                # if image1_2 is stopping this frame...
                if image1_2.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > image1_2.tStartRefresh + 0.24-frameTolerance:
                        # keep track of stop time/frame for later
                        image1_2.tStop = t  # not accounting for scr refresh
                        image1_2.tStopRefresh = tThisFlipGlobal  # on global time
                        image1_2.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'image1_2.stopped')
                        # update status
                        image1_2.status = FINISHED
                        image1_2.setAutoDraw(False)
                
                # *Cimage1_2* updates
                
                # if Cimage1_2 is starting this frame...
                if Cimage1_2.status == NOT_STARTED and tThisFlip >= 0.4-frameTolerance:
                    # keep track of start time/frame for later
                    Cimage1_2.frameNStart = frameN  # exact frame index
                    Cimage1_2.tStart = t  # local t and not account for scr refresh
                    Cimage1_2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(Cimage1_2, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'Cimage1_2.started')
                    # update status
                    Cimage1_2.status = STARTED
                    Cimage1_2.setAutoDraw(True)
                
                # if Cimage1_2 is active this frame...
                if Cimage1_2.status == STARTED:
                    # update params
                    pass
                
                # if Cimage1_2 is stopping this frame...
                if Cimage1_2.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > Cimage1_2.tStartRefresh + 0.24-frameTolerance:
                        # keep track of stop time/frame for later
                        Cimage1_2.tStop = t  # not accounting for scr refresh
                        Cimage1_2.tStopRefresh = tThisFlipGlobal  # on global time
                        Cimage1_2.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'Cimage1_2.stopped')
                        # update status
                        Cimage1_2.status = FINISHED
                        Cimage1_2.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        win=win, 
                        timers=[routineTimer], 
                        playbackComponents=[]
                    )
                    # skip the frame we paused on
                    continue
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    Initialize.forceEnded = routineForceEnded = True
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in Initialize.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "Initialize" ---
            for thisComponent in Initialize.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for Initialize
            Initialize.tStop = globalClock.getTime(format='float')
            Initialize.tStopRefresh = tThisFlipGlobal
            thisExp.addData('Initialize.stopped', Initialize.tStop)
            # Run 'End Routine' code from code
            stim1 = image1_2.image
            stim2 = Cimage1_2.image
            # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
            if Initialize.maxDurationReached:
                routineTimer.addTime(-Initialize.maxDuration)
            elif Initialize.forceEnded:
                routineTimer.reset()
            else:
                routineTimer.addTime(-0.640000)
            
            # set up handler to look after randomisation of conditions etc
            trials = data.TrialHandler2(
                name='trials',
                nReps=999.0, 
                method='sequential', 
                extraInfo=expInfo, 
                originPath=-1, 
                trialList=[None], 
                seed=None, 
            )
            thisExp.addLoop(trials)  # add the loop to the experiment
            thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
            # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
            if thisTrial != None:
                for paramName in thisTrial:
                    globals()[paramName] = thisTrial[paramName]
            if thisSession is not None:
                # if running in a Session with a Liaison client, send data up to now
                thisSession.sendExperimentData()
            
            for thisTrial in trials:
                currentLoop = trials
                thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
                if thisSession is not None:
                    # if running in a Session with a Liaison client, send data up to now
                    thisSession.sendExperimentData()
                # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
                if thisTrial != None:
                    for paramName in thisTrial:
                        globals()[paramName] = thisTrial[paramName]
                
                # --- Prepare to start Routine "Neutral1" ---
                # create an object to store info about Routine Neutral1
                Neutral1 = data.Routine(
                    name='Neutral1',
                    components=[image1, Cimage1, key_resp],
                )
                Neutral1.status = NOT_STARTED
                continueRoutine = True
                # update component parameters for each repeat
                image1.setImage(stim1)
                Cimage1.setImage(stim2)
                # create starting attributes for key_resp
                key_resp.keys = []
                key_resp.rt = []
                _key_resp_allKeys = []
                # store start times for Neutral1
                Neutral1.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
                Neutral1.tStart = globalClock.getTime(format='float')
                Neutral1.status = STARTED
                thisExp.addData('Neutral1.started', Neutral1.tStart)
                Neutral1.maxDuration = None
                # keep track of which components have finished
                Neutral1Components = Neutral1.components
                for thisComponent in Neutral1.components:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                frameN = -1
                
                # --- Run Routine "Neutral1" ---
                # if trial has changed, end Routine now
                if isinstance(trials, data.TrialHandler2) and thisTrial.thisN != trials.thisTrial.thisN:
                    continueRoutine = False
                Neutral1.forceEnded = routineForceEnded = not continueRoutine
                while continueRoutine and routineTimer.getTime() < 0.64:
                    # get current time
                    t = routineTimer.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    
                    # *image1* updates
                    
                    # if image1 is starting this frame...
                    if image1.status == NOT_STARTED and tThisFlip >= 0.08-frameTolerance:
                        # keep track of start time/frame for later
                        image1.frameNStart = frameN  # exact frame index
                        image1.tStart = t  # local t and not account for scr refresh
                        image1.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(image1, 'tStartRefresh')  # time at next scr refresh
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'image1.started')
                        # update status
                        image1.status = STARTED
                        image1.setAutoDraw(True)
                    
                    # if image1 is active this frame...
                    if image1.status == STARTED:
                        # update params
                        pass
                    
                    # if image1 is stopping this frame...
                    if image1.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > image1.tStartRefresh + 0.24-frameTolerance:
                            # keep track of stop time/frame for later
                            image1.tStop = t  # not accounting for scr refresh
                            image1.tStopRefresh = tThisFlipGlobal  # on global time
                            image1.frameNStop = frameN  # exact frame index
                            # add timestamp to datafile
                            thisExp.timestampOnFlip(win, 'image1.stopped')
                            # update status
                            image1.status = FINISHED
                            image1.setAutoDraw(False)
                    
                    # *Cimage1* updates
                    
                    # if Cimage1 is starting this frame...
                    if Cimage1.status == NOT_STARTED and tThisFlip >= 0.4-frameTolerance:
                        # keep track of start time/frame for later
                        Cimage1.frameNStart = frameN  # exact frame index
                        Cimage1.tStart = t  # local t and not account for scr refresh
                        Cimage1.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(Cimage1, 'tStartRefresh')  # time at next scr refresh
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'Cimage1.started')
                        # update status
                        Cimage1.status = STARTED
                        Cimage1.setAutoDraw(True)
                    
                    # if Cimage1 is active this frame...
                    if Cimage1.status == STARTED:
                        # update params
                        pass
                    
                    # if Cimage1 is stopping this frame...
                    if Cimage1.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > Cimage1.tStartRefresh + 0.24-frameTolerance:
                            # keep track of stop time/frame for later
                            Cimage1.tStop = t  # not accounting for scr refresh
                            Cimage1.tStopRefresh = tThisFlipGlobal  # on global time
                            Cimage1.frameNStop = frameN  # exact frame index
                            # add timestamp to datafile
                            thisExp.timestampOnFlip(win, 'Cimage1.stopped')
                            # update status
                            Cimage1.status = FINISHED
                            Cimage1.setAutoDraw(False)
                    
                    # *key_resp* updates
                    waitOnFlip = False
                    
                    # if key_resp is starting this frame...
                    if key_resp.status == NOT_STARTED and tThisFlip >= 0.08-frameTolerance:
                        # keep track of start time/frame for later
                        key_resp.frameNStart = frameN  # exact frame index
                        key_resp.tStart = t  # local t and not account for scr refresh
                        key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'key_resp.started')
                        # update status
                        key_resp.status = STARTED
                        # keyboard checking is just starting
                        waitOnFlip = True
                        win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
                        win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
                    
                    # if key_resp is stopping this frame...
                    if key_resp.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > key_resp.tStartRefresh + 0.56-frameTolerance:
                            # keep track of stop time/frame for later
                            key_resp.tStop = t  # not accounting for scr refresh
                            key_resp.tStopRefresh = tThisFlipGlobal  # on global time
                            key_resp.frameNStop = frameN  # exact frame index
                            # add timestamp to datafile
                            thisExp.timestampOnFlip(win, 'key_resp.stopped')
                            # update status
                            key_resp.status = FINISHED
                            key_resp.status = FINISHED
                    if key_resp.status == STARTED and not waitOnFlip:
                        theseKeys = key_resp.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
                        _key_resp_allKeys.extend(theseKeys)
                        if len(_key_resp_allKeys):
                            key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                            key_resp.rt = _key_resp_allKeys[-1].rt
                            key_resp.duration = _key_resp_allKeys[-1].duration
                            # a response ends the routine
                            continueRoutine = False
                    
                    # check for quit (typically the Esc key)
                    if defaultKeyboard.getKeys(keyList=["escape"]):
                        thisExp.status = FINISHED
                    if thisExp.status == FINISHED or endExpNow:
                        endExperiment(thisExp, win=win)
                        return
                    # pause experiment here if requested
                    if thisExp.status == PAUSED:
                        pauseExperiment(
                            thisExp=thisExp, 
                            win=win, 
                            timers=[routineTimer], 
                            playbackComponents=[]
                        )
                        # skip the frame we paused on
                        continue
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        Neutral1.forceEnded = routineForceEnded = True
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in Neutral1.components:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # --- Ending Routine "Neutral1" ---
                for thisComponent in Neutral1.components:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                # store stop times for Neutral1
                Neutral1.tStop = globalClock.getTime(format='float')
                Neutral1.tStopRefresh = tThisFlipGlobal
                thisExp.addData('Neutral1.stopped', Neutral1.tStop)
                # check responses
                if key_resp.keys in ['', [], None]:  # No response was made
                    key_resp.keys = None
                trials.addData('key_resp.keys',key_resp.keys)
                if key_resp.keys != None:  # we had a response
                    trials.addData('key_resp.rt', key_resp.rt)
                    trials.addData('key_resp.duration', key_resp.duration)
                # Run 'End Routine' code from code_2
                if key_resp.keys == "space":
                    trials.finished = True
                # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
                if Neutral1.maxDurationReached:
                    routineTimer.addTime(-Neutral1.maxDuration)
                elif Neutral1.forceEnded:
                    routineTimer.reset()
                else:
                    routineTimer.addTime(-0.640000)
                thisExp.nextEntry()
                
            # completed 999.0 repeats of 'trials'
            
            if thisSession is not None:
                # if running in a Session with a Liaison client, send data up to now
                thisSession.sendExperimentData()
            thisExp.nextEntry()
            
        # completed 1.0 repeats of 'trials_practice'
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        thisExp.nextEntry()
        
    # completed 1.0 repeats of 'trials_block'
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # mark experiment as finished
    endExperiment(thisExp, win=win)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # return console logger level to WARNING
    logging.console.setLevel(logging.WARNING)
    # mark experiment handler as finished
    thisExp.status = FINISHED
    logging.flush()


def quit(thisExp, win=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win,
        globalClock='float'
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win)
