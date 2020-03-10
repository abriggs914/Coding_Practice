package com.example.abrig.minesweeper;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Rect;
import android.view.GestureDetector;
import android.view.MotionEvent;
import android.view.View;
import android.widget.TextView;

public class RangeBar extends View {

    public class Thumb {

        private boolean isLeft;
        private int xPos, yPos, tickPos;

        public Thumb() { }

        public boolean isLeft() {
            return isLeft;
        }

        public void setLeft(boolean left) {
            isLeft = left;
        }

        public int getxPos() {
            return xPos;
        }

        public void setxPos(int xPos) {
            this.xPos = xPos;
        }

        public int getyPos() {
            return yPos;
        }

        public void setyPos(int yPos) {
            this.yPos = yPos;
        }

        public String toString() {
            return ((isLeft)? "Left Thumb" : "Right Thumb");
        }

        public int getTickPos() {
            return tickPos;
        }

        public void setTickPos(int tickPos) {
            this.tickPos = tickPos;
        }
    }

    // design vars
    private int firstTick;
    private int lastTick;
    private int numTicks;
    private int tickLength;
    private double majorMinorRatio;
    private boolean majorMinor;
    private boolean snapTo;
    private boolean showTicks;
    private boolean showNumbers;
    private Rect bounds;
    private double spacePerTick;
    private int paletteSelection;

    private TextView reportTextView;

    // functionality vars
    private GestureDetector myGestureDetector;
    private MineSweeperGrid.AndroidGestureDetector androidGestureDetector;
    private Thumb leftThumb;
    private Thumb rightThumb;

    public RangeBar(Context context, int firstTick, int lastTick) {
        super(context);
        this.firstTick = firstTick;
        this.lastTick = lastTick;
        this.numTicks = lastTick - firstTick;

//        this.majorMinorRatio = 0.0;
//        this.majorMinor = false;
//        this.snapTo = false;
//        this.showTicks = true;
//        this.showNumbers = true;
//
//        init();
    }

    public RangeBar(Context context, int firstTick, int lastTick, TextView reportTextView) {
        super(context);
        this.firstTick = firstTick;
        this.lastTick = lastTick;
        this.numTicks = lastTick - firstTick;
        this.reportTextView = reportTextView;

        this.majorMinorRatio = 0.0;
        this.majorMinor = false;
        this.snapTo = false;
        this.showTicks = true;
        this.showNumbers = true;

        init();
    }

    public RangeBar(Context context,
                    int firstTick,
                    int lastTick,
                    int numTicks,
                    double majorMinorRatio,
                    boolean majorMinor,
                    boolean snapTo,
                    boolean showTicks,
                    boolean showNumbers) {
        super(context);

        this.firstTick = firstTick;
        this.lastTick = lastTick;
        this.numTicks = numTicks;

        this.majorMinorRatio = majorMinorRatio;
        this.majorMinor = majorMinor;
        this.snapTo = snapTo;
        this.showTicks = showTicks;
        this.showNumbers = showNumbers;

        init();
    }

    private void init() { //Rect bounds) {
//        System.out.println("init of RangeBar");
        this.tickLength = 15;
        this.leftThumb = new Thumb();
        this.rightThumb = new Thumb();
        this.leftThumb.setLeft(true);
        this.rightThumb.setLeft(false);
        leftThumb.setTickPos(firstTick);
        rightThumb.setTickPos(lastTick);

        if (lastTick <= firstTick) {
            int x = 1 / 0;
        }

        setBounds();

        setOnTouchListener(new OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (event.getAction() == MotionEvent.ACTION_DOWN) {
                    int xPos = (int) event.getX();
                    int yPos = (int) event.getY();
                    Thumb thumbInUse = getClosestThumb(xPos);
                    int deadZone = 15;
                    if (Utilities.inRange(bounds.left - deadZone, xPos, bounds.right + deadZone)) {
                        if (Utilities.inRange(bounds.top - deadZone, yPos, bounds.bottom + deadZone)) {
//                            System.out.println("RangeBar TOUCHED using: " + thumbInUse);
                        }
                    }
                }
                if (event.getAction() == MotionEvent.ACTION_MOVE) {
                    int xPos = (int) event.getX();
                    int yPos = (int) event.getY();
                    Thumb thumbInUse = getClosestThumb(xPos);
                    Thumb otherThumb = ((thumbInUse.equals(leftThumb))? rightThumb : leftThumb);
                    int deadZone = 35;
                    if (Utilities.inRange(bounds.left - deadZone, xPos, bounds.right + deadZone)) {
                        if (Utilities.inRange(bounds.top - deadZone, yPos, bounds.bottom + deadZone)) {
                            xPos = Math.max(xPos, bounds.left);
                            xPos = Math.min(xPos, bounds.right);
                            int newPos = unScale(xPos);
                            newPos += firstTick;
                            System.out.println("RangeBar MOVED using: " + thumbInUse + ", newPos: " + newPos + ", other: " + otherThumb + ", pos: " + otherThumb.getTickPos());
                            if (thumbInUse.isLeft()) {
                                if (newPos < otherThumb.getTickPos()) {
                                    // is left thumb and new value is less than right thumb
                                    thumbInUse.setTickPos(newPos);
                                }
                            }
                            else {
                                if (newPos > otherThumb.getTickPos()) {
                                    // is right thumb and new value is greater than left thumb
                                    thumbInUse.setTickPos(newPos);
                                }
                            }
                        }
                    }
                }
                invalidate();
                if (reportTextView != null) {
                    int[] range = getRange();
                    reportTextView.setText(("range: " + Utilities.keyify(range[0], range[1])));
                }
                return true;
            }
        });

//        draw();
        invalidate();
    }

    private double calcSpacePerTick() {
//        System.out.println(
//                "this.bounds.right - this.bounds.left: " + (this.bounds.right - this.bounds.left)
//                        + "\n(double) (this.bounds.right - this.bounds.left): " + ((double) (this.bounds.right - this.bounds.left))
//                        + "\n(double) (numTicks): " + ((double) (numTicks))
//                        + "\n((double) (this.bounds.right - this.bounds.left)) / (double) (numTicks): " + (((double) (this.bounds.right - this.bounds.left)) / (double) (numTicks)));
        return ((double) (this.bounds.right - this.bounds.left)) / (double) (numTicks);
    }

    private int scale(int tickPos) {
        tickPos -= firstTick;
        return this.bounds.left + ((int) Math.round((this.spacePerTick * tickPos)));
    }

    private int unScale(int pos) {
        return (int) Math.round((pos - this.bounds.left) / spacePerTick);
    }

    public void setBounds() {
        int width = getRight() - getLeft();
        int height = getBottom() - getTop();
        int tenPercentWidth = (int) (width * 0.1);
        int tenPercentHeight = (int) (height * 0.4);
        Rect bounds = new Rect(
                getLeft() + tenPercentWidth,
                getTop() + tenPercentHeight,
                getRight() - tenPercentWidth,
                getBottom() - tenPercentHeight);
        this.bounds = bounds;

        this.spacePerTick = calcSpacePerTick();

        int center = ((this.bounds.bottom - this.bounds.top) / 2) + this.bounds.top;
        String message =
                "\tbounds: " + this.bounds
                        + "\n\tcenter: " + center
                        + "\tspacePerTick: " + spacePerTick
                        + "\n\tfirstTick: " + firstTick
                        + "\tscaledTo: " + scale(firstTick)
                        + "\n\tleftTick: " + leftThumb.getTickPos()
                        + "\tscaledTo: " + scale(leftThumb.getTickPos())
                        + "\n\trightTick: " + rightThumb.getTickPos()
                        + "\tscaledTo: " + scale(rightThumb.getTickPos())
                        + "\n\tlastTick: " + lastTick
                        + "\tscaledTo: " + scale(lastTick)
                ;
        System.out.println(message);
        this.leftThumb.setxPos(scale(leftThumb.getTickPos()));
        this.leftThumb.setyPos(center);

        this.rightThumb.setxPos(scale(rightThumb.getTickPos()));
        this.rightThumb.setyPos(center);
        System.out.println("width: " + width + ", height: " + height + " , tenPercentWidth: " + tenPercentWidth + ", tenPercentHeight: " + tenPercentHeight + ", bounds: " + bounds);
    }

    private Rect getBounds() {
        return bounds;
    }

    public int getFirstTick() {
        return firstTick;
    }

    public void setFirstTick(int firstTick) {
        this.firstTick = firstTick;
    }

    public int getLastTick() {
        return lastTick;
    }

    public void setLastTick(int lastTick) {
        this.lastTick = lastTick;
    }

    public int getNumTicks() {
        return numTicks;
    }

    public void setNumTicks(int numTicks) {
        this.numTicks = numTicks;
    }

    public void setTickLength(int tickLength) {
        this.tickLength = tickLength;
    }

    public int getTickLength() {
        return tickLength;
    }

    public double getMajorMinorRatio() {
        return majorMinorRatio;
    }

    public void setMajorMinorRatio(double majorMinorRatio) {
        this.majorMinorRatio = majorMinorRatio;
    }

    public boolean isMajorMinor() {
        return majorMinor;
    }

    public void setMajorMinor(boolean majorMinor) {
        this.majorMinor = majorMinor;
    }

    public boolean isSnapTo() {
        return snapTo;
    }

    public void setSnapTo(boolean snapTo) {
        this.snapTo = snapTo;
    }

    public boolean isShowTicks() {
        return showTicks;
    }

    public void setShowTicks(boolean showTicks) {
        this.showTicks = showTicks;
    }

    public boolean isShowNumbers() {
        return showNumbers;
    }

    public void setShowNumbers(boolean showNumbers) {
        this.showNumbers = showNumbers;
    }

    public void setPaletteSelection(int paletteSelection) {
        this.paletteSelection = paletteSelection;
    }

    private Paint[] getColors() {
        Paint barPaint = new Paint();
        Paint thumbPaint = new Paint();
        Paint thumbTextPaint = new Paint();
        Paint tickTextPaint = new Paint();
        Paint tickNumberPaint = new Paint();

        Paint[] res = new Paint[] {barPaint, thumbPaint, thumbTextPaint, tickTextPaint, tickNumberPaint};

        switch (paletteSelection) {

            // dark gray / red / gray / black / dark red
            case 1 :
                barPaint.setColor(Color.DKGRAY);
                thumbPaint.setColor(Color.rgb(179, 18, 18));
                thumbTextPaint.setColor(Color.GRAY);
                tickTextPaint.setColor(Color.BLACK);
                tickTextPaint.setColor(Color.BLACK);
                tickNumberPaint.setColor(Color.rgb(143, 0, 0));
                break;

            // blue / green / white / black / dark green
            default : // case 0
                barPaint.setColor(Color.rgb(134, 232, 95));
                thumbPaint.setColor(Color.rgb(25, 42, 168));
                thumbTextPaint.setColor(Color.WHITE);
                tickTextPaint.setColor(Color.BLACK);
                tickNumberPaint.setColor(Color.rgb(15, 133, 9));
                break;

        }

        for (Paint p : res) {
            p.setStyle(Paint.Style.FILL);
            p.setStrokeWidth(5);
            p.setTextSize(40);
        }
        return res;
    }

    /////////////////////////////

    public int[] getRange() {
        return new int[] {leftThumb.getTickPos(), rightThumb.getTickPos()};
    }

    public String getStringRange() { return Utilities.keyify(getRange()[0], getRange()[1]); }

    public int getDistance() {
        return rightThumb.getxPos() - leftThumb.getxPos();
    }

    public Thumb getClosestThumb(int pos) {
        int leftDiff = Math.abs(leftThumb.getxPos() - pos);
        int rightDiff = Math.abs(rightThumb.getxPos() - pos);
        return ((leftDiff <= rightDiff)? leftThumb : rightThumb);
    }

    ////////////////////////////

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);

        Paint[] palette = getColors();
        Paint barPaint = palette[0];
        Paint thumbPaint = palette[1];
        Paint thumbTextPaint = palette[2];
        Paint tickTextPaint = palette[3];
        Paint tickNumberPaint = palette[4];

        setBounds();
        Rect bounds = getBounds();
        // bar
        canvas.drawRect(bounds, barPaint);

        int leftPos = leftThumb.getxPos();
        int rightPos = rightThumb.getxPos();
        int centerY = ((int) ((getBottom() - getTop()) * 0.5)) + getTop();
        int width = bounds.right - bounds.left;

        // thumb buttons
        canvas.drawCircle(leftPos, centerY, 35, thumbPaint);
        canvas.drawCircle(rightPos, centerY, 35, thumbPaint);

        // left and right thumb labels
        canvas.drawText("L", leftPos - 10, centerY + 11, thumbTextPaint);
        canvas.drawText("R", rightPos - 10, centerY + 11, thumbTextPaint);

        int numberHeight = ((int) ((getBottom() - getTop()) * 0.1));// + getTop();
        int tickHeight = ((int) ((getBottom() - getTop()) * 0.3));// + getTop();

        int everyNTicks = (int) Math.round(majorMinorRatio * (numTicks + 0.0));
        for (int t = 0; t <= numTicks; t++) {
            boolean numberShown = false;
            float x = bounds.left + ((float) (t * spacePerTick));
            if (showTicks) {
                int tickLen = tickLength;
//                System.out.println("(t + firstTick): " + (t + firstTick) + ", everyNTicks: " + everyNTicks + ", majorMinor: " + majorMinor + ", ((t + firstTick) % everyNTicks == 0): " + ((t + firstTick) % everyNTicks == 0));
                if (majorMinor) {
                    if (showNumbers) {
                        numberShown = true;
                    }
                    if ((t == 0 || t == numTicks) || (t + firstTick) % everyNTicks == 0) {
                        tickLen += 10;
                        if (showNumbers) {
                            canvas.drawText(((t + firstTick) + ""), x - 25, numberHeight, tickNumberPaint);
                        }
                    }
                }
                canvas.drawLine(x, tickHeight, x, tickHeight - tickLen, tickTextPaint);
            }
            if (!numberShown && showNumbers) {
                canvas.drawText(((t + firstTick) + ""), x - 25, numberHeight, tickNumberPaint);
            }
        }
    }
}