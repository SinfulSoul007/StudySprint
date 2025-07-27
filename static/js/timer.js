// Timer functionality for StudySprint
// Simple timer utility for 25-minute sprints

class SprintTimer {
    constructor(duration = 25 * 60) {  // 25 minutes in seconds
        this.duration = duration;
        this.timeLeft = duration;
        this.isRunning = false;
        this.interval = null;
        this.callbacks = {};
    }
    
    start() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        this.interval = setInterval(() => {
            this.timeLeft--;
            this.onTick();
            
            if (this.timeLeft <= 0) {
                this.stop();
                this.onFinish();
            }
        }, 1000);
        
        this.onStart();
    }
    
    pause() {
        if (!this.isRunning) return;
        
        clearInterval(this.interval);
        this.isRunning = false;
        this.onPause();
    }
    
    stop() {
        clearInterval(this.interval);
        this.isRunning = false;
        this.onStop();
    }
    
    reset() {
        this.stop();
        this.timeLeft = this.duration;
        this.onReset();
    }
    
    // Format time as MM:SS
    formatTime() {
        const minutes = Math.floor(this.timeLeft / 60);
        const seconds = this.timeLeft % 60;
        return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
    
    // Get progress as percentage
    getProgress() {
        return (this.duration - this.timeLeft) / this.duration;
    }
    
    // Event callbacks
    onStart() {
        if (this.callbacks.start) this.callbacks.start();
    }
    
    onPause() {
        if (this.callbacks.pause) this.callbacks.pause();
    }
    
    onStop() {
        if (this.callbacks.stop) this.callbacks.stop();
    }
    
    onTick() {
        if (this.callbacks.tick) this.callbacks.tick();
    }
    
    onFinish() {
        if (this.callbacks.finish) this.callbacks.finish();
    }
    
    onReset() {
        if (this.callbacks.reset) this.callbacks.reset();
    }
    
    // Set event callbacks
    on(event, callback) {
        this.callbacks[event] = callback;
    }
} 