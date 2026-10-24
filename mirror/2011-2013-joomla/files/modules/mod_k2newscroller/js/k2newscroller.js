/************************************************
*   mooquee v.01                                 *
*   Http: WwW.developer.ps/moo/mooquee          *
*   Dirar Abu Kteish dirar@zanstudio.com        *
/***********************************************/

var mooquee = new Class({
    initialize: function(element, options) {
		this.setOptions({
			marHeight: 20,
			marWidth: 550, //or 100%...
			steps: 1,
			speed: 1,
			direction: 'left',
			pauseOnOver: true
	    }, options);
	    this.timer = null;
	    this.textElement = null;
	    this.mooqueeElement = element;	    	    
	    this.constructMooquee();
	},
	constructMooquee: function() {
		var el = this.mooqueeElement;
		el.setStyles({
		    'width' : this.options.marWidth
		    ,'height' : this.options.marHeight		    
		});
		this.textElement = new Element('div',{
		    'class' : 'mooquee-text'
		    ,'id' : 'mooquee-text'
		}).setHTML(el.innerHTML);
		el.setHTML('');
		this.textElement.injectInside(el);
		this.textElement = $('mooquee-text');
		(this.options.direction == 'left') ?  this.textElement.setStyle('left', ( -1 * this.textElement.getCoordinates().width.toInt())) : this.textElement.setStyle('left', el.getCoordinates().width.toInt());
		if(this.options.pauseOnOver){this.addMouseEvents();}
		//start marquee
		this.timer = this.startMooquee.delay(this.options.speed, this);
	},
	addMouseEvents : function(){
	    this.textElement.addEvents({
	        'mouseenter' : function(me){
	            this.clearTimer();
	        }.bind(this),
	        'mouseleave' : function(me){
	            this.timer = this.startMooquee.delay(this.options.speed, this);
	        }.bind(this)
	    });
	},
    startMooquee: function(){
        var pos = this.textElement.getStyle('left').toInt();
        this.textElement.setStyle('left', ( pos + ((this.options.direction == 'left') ? -1 * (this.options.steps) : this.options.steps)) + 'px');
        this.checkEnd(pos);
        this.timer = this.startMooquee.delay(this.options.speed, this);        
    },
    resumeMooquee: function(){
        this.stopMooquee();
        if(this.options.pauseOnOver){this.addMouseEvents();}
        this.timer = this.startMooquee.delay(this.options.speed, this);        
    },
    stopMooquee: function(){
        this.clearTimer();        
        this.textElement.removeEvents();        
    },
    clearTimer: function(){
        $clear(this.timer);
    },
    checkEnd: function(pos){
        if(this.options.direction == 'left'){
            if(pos < -1 * (this.textElement.getCoordinates().width.toInt())){
                this.textElement.setStyle('left', this.mooqueeElement.getCoordinates().width);
            }
        }
        else{
            if(pos > this.mooqueeElement.getCoordinates().width.toInt()){
                this.textElement.setStyle('left', -1 * (this.textElement.getCoordinates().width.toInt()) );                
            }
        }        
    },
    setDirection: function(dir){
        this.options.direction = dir;
    }
});
mooquee.implement(new Options);