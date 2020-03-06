import pyautogui as ag

def retrieveGoalBox():
    """
    Returns:
      Bounding box of the goal in coordinates

    """
    pass

def retrieve():
    pass

def articulatedTrajectory(x, y):
    """
    Executes the whole articulated mouse movement.
    
    Args:
    x : (int, None)
    y : (int, None)
    
    Returns
    None.
    """
    # Yield trajectory parameters from the controller network
    # angle = 
    # speed = 
    # x = 
    # y = 
    moveTo()
    

def moveTo(x, y, xOffset, yOffset, duration, tween=linear):
    """Handles the partial move event

    Args:
      moveOrDrag (str): Either 'move' or 'drag', for the type of action this is.
      x (int, float, None, optional): How far left (for negative values) or
        right (for positive values) to move the cursor. 0 by default.
      y (int, float, None, optional): How far up (for negative values) or
        down (for positive values) to move the cursor. 0 by default.
      xOffset (int, float, None, optional): How far left (for negative values) or
        right (for positive values) to move the cursor. 0 by default.
      yOffset (int, float, None, optional): How far up (for negative values) or
        down (for positive values) to move the cursor. 0 by default.
      duration (float, optional): The amount of time it takes to move the mouse
        cursor to the new xy coordinates. If 0, then the mouse cursor is moved
        instantaneously. 0.0 by default.
      tween (func, optional): The tweening function used if the duration is not
        0. A linear tween is used by default. See the tweens.py file for
        details.
      button (str, int, optional): The mouse button released. TODO

    Returns:
      None
    """

    # The move and drag code is similar, but OS X requires a special drag event instead of just a move event when dragging.
    # See https://stackoverflow.com/a/2696107/1893164
    assert moveOrDrag in ('move', 'drag'), "moveOrDrag must be in ('move', 'drag'), not %s" % (moveOrDrag)

    if sys.platform != 'darwin':
        moveOrDrag = 'move' # Only OS X needs the drag event specifically.

    xOffset = int(xOffset) if xOffset is not None else 0
    yOffset = int(yOffset) if yOffset is not None else 0

    if x is None and y is None and xOffset == 0 and yOffset == 0:
        return  # Special case for no mouse movement at all.

    startx, starty = position()

    x = int(x) if x is not None else startx
    y = int(y) if y is not None else starty

    # x, y, xOffset, yOffset are now int.
    x += xOffset
    y += yOffset

    width, height = size()

    # Make sure x and y are within the screen bounds.
    #x = max(0, min(x, width - 1))
    #y = max(0, min(y, height - 1))

    # If the duration is small enough, just move the cursor there instantly.
    steps = [(x, y)]

    if duration > MINIMUM_DURATION:
        # Non-instant moving/dragging involves tweening:
        num_steps = max(width, height)
        sleep_amount = duration / num_steps
        if sleep_amount < MINIMUM_SLEEP:
            num_steps = int(duration / MINIMUM_SLEEP)
            sleep_amount = duration / num_steps

        steps = [
            getPointOnLine(startx, starty, x, y, tween(n / num_steps))
            for n in range(num_steps)
        ]
        # Making sure the last position is the actual destination.
        steps.append((x, y))

    for tweenX, tweenY in steps:
        if len(steps) > 1:
            # A single step does not require tweening.
            time.sleep(sleep_amount)

        tweenX = int(round(tweenX))
        tweenY = int(round(tweenY))

        # Moving the cursor to a fail-safe corner as part of the planned
        # mouse movements shouldn't trigger the fail-safe. This may seem
        # ridiculous, but remember that (tweenX, tweenY) is the *calculated*
        # coordinate of where the mouse should be, while failSafeCheck()
        # uses the *actual position* of the mouse from position() to
        # decide if it should raise the fail-safe exception.
        if (tweenX, tweenY) not in FAILSAFE_POINTS:
            failSafeCheck()

        if moveOrDrag == 'move':
            platformModule._moveTo(tweenX, tweenY)
        elif moveOrDrag == 'drag':
            platformModule._dragTo(tweenX, tweenY, button)
        else:
            raise NotImplementedError('Unknown value of moveOrDrag: {0}'.format(moveOrDrag))

    if (tweenX, tweenY) not in FAILSAFE_POINTS:
        failSafeCheck()