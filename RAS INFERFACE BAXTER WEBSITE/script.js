var xcoord = 0;
var ycoord = 0;
$(function() {
$('.clickable').bind('click', function (ev) {
    var $div = $(ev.target);
    var $display = $div.find('.display');
    
    var offset = $div.offset();
    var x = Math.floor(ev.clientX - offset.left);
    var y = Math.floor(ev.clientY - offset.top);
    
    $display.text('x: ' + x + ', y: ' + y);
});
});

$(function() {
$('.minicolumn').bind('click', function (ev) {
    var $div = $(ev.target);
    var $display = $div.find('.display');
    
    var offset = $div.offset();
    var x = Math.floor(ev.clientX - offset.left);
    var y = Math.floor(ev.clientY - offset.top);
    
    $display.text('x: ' + x + ', y: ' + y);
});
});
$(function() {
$('.minicolumn2-1').bind('click', function (ev) {
    var $div = $(ev.target);
    var $display = $div.find('.display');
    
    var offset = $div.offset();
    var x = Math.floor(ev.clientX - offset.left);
    var y = Math.floor(ev.clientY - offset.top);
    
    $display.text('x: ' + x + ', y: ' + y);
});
});
$(function() {
$('.minicolumn2-2').bind('click', function (ev) {
    var $div = $(ev.target);
    var $display = $div.find('.display');
    
    var offset = $div.offset();
    var x = Math.floor(ev.clientX - offset.left);
    var y = Math.floor(ev.clientY - offset.top);
    var z = 2;
    $display.text('x: ' + x + ', y: ' + y);
});
});
$(function() {
$('.minicolumn2-3').bind('click', function (ev) {
    var $div = $(ev.target);
    var $display = $div.find('.display');
    
    var offset = $div.offset();
    var x = Math.floor(ev.clientX - offset.left);
    var y = Math.floor(ev.clientY - offset.top);
    
    $display.text('x: ' + x + ', y: ' + y);
});
});
$(function() {
$('.minicolumn3-1').bind('click', function (ev) {
    var $div = $(ev.target);
    var $display = $div.find('.display');
    
    var offset = $div.offset();
    var x = Math.floor(ev.clientX - offset.left);
    var y = Math.floor(ev.clientY - offset.top);
    
    $display.text('x: ' + x + ', y: ' + y);
});
});
$(function() {
$('.minicolumn3-2').bind('click', function (ev) {
    var $div = $(ev.target);
    var $display = $div.find('.display');
    
    var offset = $div.offset();
    var x = Math.floor(ev.clientX - offset.left);
    var y = Math.floor(ev.clientY - offset.top);
    
    $display.text('x: ' + x + ', y: ' + y);
});
});

$(function() {
  $('.Custom Voice').bind('click', function (ev) {
      var $div = $(ev.target);
      var $display = $div.find('.display');
      
      var offset = $div.offset();
      var xcoord = Math.floor(ev.clientX - offset.left);
      var ycoord = Math.floor(ev.clientY - offset.top);
      
  var jptopic = new ROSLIB.Topic({
      ros : rbServer,
      name : '/emociones_baxter',
      messageType : 'geometry_msgs/Twist'
  });
  var rasVoice = new ROSLIB.Topic({
      ros : rbServer,
      name : '/voice_message',
      messageType : 'std_msgs/String'
  });   
  
  var twist = new ROSLIB.Message({
      linear : {
        x : xcoord,
        y : ycoord,
        z : 2
      },
      angular : {
        x : 0,
        y : 0,
        z : 0
      }
    });
    var voicesMessage = new ROSLIB.Message({
      data : "Voice1"
    }); 
      $display.text('x: ' + xcoord + ', y: ' + ycoord);
      jptopic.publish(twist);
      rasVoice.publish(voicesMessage);
      console.log(twist);
  });
  });
  $(function() {
    $('.Introduction').bind('click', function (ev) {
        var $div = $(ev.target);
        var $display = $div.find('.display');
        
        var offset = $div.offset();
        var xcoord = Math.floor(ev.clientX - offset.left);
        var ycoord = Math.floor(ev.clientY - offset.top);
        
    var jptopic = new ROSLIB.Topic({
        ros : rbServer,
        name : '/emociones_baxter',
        messageType : 'geometry_msgs/Twist'
      });
    var rasVoice = new ROSLIB.Topic({
        ros : rbServer,
        name : '/voice_message',
        messageType : 'std_msgs/String'
      });  
    
    var twist = new ROSLIB.Message({
        linear : {
          x : xcoord,
          y : ycoord,
          z : 2
        },
        angular : {
          x : 0,
          y : 0,
          z : 0
        }
      });
    var voicesMessage = new ROSLIB.Message({
        data : "Voice2"
    });  
        $display.text('x: ' + xcoord + ', y: ' + ycoord);
        jptopic.publish(twist);
        rasVoice.publish(voicesMessage);
        console.log(twist);
    });
    });

$(function() {
$('.picture').bind('click', function (ev) {
    var $div = $(ev.target);
    var $display = $div.find('.display');
    
    var offset = $div.offset();
    var xcoord = Math.floor(ev.clientX - offset.left);
    var ycoord = Math.floor(ev.clientY - offset.top);
    
var jptopic = new ROSLIB.Topic({
    ros : rbServer,
    name : '/emociones_baxter',
    messageType : 'geometry_msgs/Twist'
  });

var twist = new ROSLIB.Message({
    linear : {
      x : xcoord,
      y : ycoord,
      z : 0
    },
    angular : {
      x : 0,
      y : 0,
      z : 0
    }
  });
    $display.text('x: ' + xcoord + ', y: ' + ycoord);
    jptopic.publish(twist);
    console.log(twist);
});
});


$( function() {
    var handle = $( "#custom-handle" );
    $( "#slider" ).slider({
      create: function() {
        handle.text( $( this ).slider( "value" ) );
      },
      slide: function( event, ui ) {
        handle.text( ui.value );
      }
    });
  } );

$( function() {
    var handle = $( "#custom-handle2" );
    $( "#slider2" ).slider({
      create: function() {
        handle.text( $( this ).slider( "value" ) );
      },
      slide: function( event, ui ) {
        handle.text( ui.value );
      }
    });
  });
$( function() {
    var handle = $( "#custom-handle3" );
    $( "#slider3" ).slider({
      create: function() {
        handle.text( $( this ).slider( "value" ) );
      },
      slide: function( event, ui ) {
        handle.text( ui.value );
      }
    });
  } );



$(function() {
	
var cmdheadpancommand = new ROSLIB.Topic({
    ros : rbServer,
    name : '/robot/head/command_head_pan',
    messageType : 'baxter_core_msgs/HeadPanCommand'
});

// These lines create a message that conforms to the structure of the HeadPanCommand defined in Baxter
// It initalizes all properties to zero. They will be set to appropriate values before we publish this message.

var headpancommand = new ROSLIB.Message({
target:0.0,
speed_ratio:0.0,
enable_pan_request:0
});
    var handle = $( "#custom-handle4" );
    $( "#slider4" ).slider({
      create: function() {
        handle.text( $( this ).slider( "value" ) );
      },
      slide: function( event, ui ) {
        handle.text( ((ui.value-50)/33.3).toFixed(2) );
	headpancommand.target = ((ui.value-50)/33.3);
    	headpancommand.speed_ratio = 1.0;
	headpancommand.enable_pan_request = 1;

    // Publish the message 
    cmdheadpancommand.publish(headpancommand);
	console.log(headpancommand);
      }
	 
    });
  } );

function Apilar(){
    var position = prompt("Digite la posición:", "1-2-3-4");
    var level = prompt("Digite el nivel:", "1-2-3-4");
    var pos = parseFloat(position);
    var lev = parseFloat(level);

var tomartopic = new ROSLIB.Topic({
    ros : rbServer,
    name : '/tomar',
    messageType : 'geometry_msgs/Twist'
  });

var twist = new ROSLIB.Message({
    linear : {
      x : pos,
      y : lev,
      z : 2
    },
    angular : {
      x : 0,
      y : 0,
      z : 0
    }
  });
    tomartopic.publish(twist);
    console.log(twist);
};

function Desapilar(){
    var position = prompt("Digite la posición:", "1-2-3-4");
    var level = prompt("Digite el nivel:", "1-2-3-4");
    var pos = parseFloat(position);
    var lev = parseFloat(level);

var soltartopic = new ROSLIB.Topic({
    ros : rbServer,
    name : '/soltar',
    messageType : 'geometry_msgs/Twist'
  });

var twist = new ROSLIB.Message({
    linear : {
      x : pos,
      y : lev,
      z : 1
    },
    angular : {
      x : 0,
      y : 0,
      z : 0
    }
  });
    soltartopic.publish(twist);
    console.log(twist);
};

function Coger(){
    var position = prompt("Digite la posición:", "1-2-3-4");
    var level = 1;
    var pos = parseFloat(position);
    var lev = parseFloat(level);

var cogertopic = new ROSLIB.Topic({
    ros : rbServer,
    name : '/coger',
    messageType : 'geometry_msgs/Twist'
  });

var twist = new ROSLIB.Message({
    linear : {
      x : pos,
      y : lev,
      z : 3
    },
    angular : {
      x : 0,
      y : 0,
      z : 0
    }
  });
    cogertopic.publish(twist);
    console.log(twist);
};

function Bajar(){
    var position = prompt("Digite la posición:", "1-2-3-4");
    var level = 1;
    var pos = parseFloat(position);
    var lev = parseFloat(level);

var bajartopic = new ROSLIB.Topic({
    ros : rbServer,
    name : '/bajar',
    messageType : 'geometry_msgs/Twist'
  });

var twist = new ROSLIB.Message({
    linear : {
      x : pos,
      y : lev,
      z : 4
    },
    angular : {
      x : 0,
      y : 0,
      z : 0
    }
  });
    bajartopic.publish(twist);
    console.log(twist);
};

function Demo(){
    //var position = 1;
    //var level = 1;
    //var pos = parseFloat(position);
    //var lev = parseFloat(level);

var demotopic = new ROSLIB.Topic({
    ros : rbServer,
    name : '/demo',
    messageType : 'geometry_msgs/Twist'
  });

var twist = new ROSLIB.Message({
    linear : {
      x : 1,
      y : 1,
      z : 5
    },
    angular : {
      x : 0,
      y : 0,
      z : 0
    }
  });
    demotopic.publish(twist);
    console.log(twist);
};

function DemoEscalera(){

var demoEscaleratopic = new ROSLIB.Topic({
    ros : rbServer,
    name : '/demoEscalera',
    messageType : 'geometry_msgs/Twist'
  });

var twist = new ROSLIB.Message({
    linear : {
      x : 1,
      y : 1,
      z : 2
    },
    angular : {
      x : 0,
      y : 0,
      z : 0
    }
  });
    demoEscaleratopic.publish(twist);
    console.log(twist);
};

function moverAB(){

    var posicionA = prompt("Digite la posición inicial:", "1-2-3-4");
    var posicionB = prompt("Digite el posicion final:", "1-2-3-4");
    var posa = parseFloat(posicionA);
    var posb = parseFloat(posicionB);

var moverABtopic = new ROSLIB.Topic({
    ros : rbServer,
    name : '/moverAB',
    messageType : 'geometry_msgs/Twist'
  });

var twist = new ROSLIB.Message({
    linear : {
      x : posa,
      y : posb,
      z : 1
    },
    angular : {
      x : 0,
      y : 0,
      z : 0
    }
  });
    moverABtopic.publish(twist);
    console.log(twist);
};

function iniciarVentiladores()
{
    var iniciarVentiladores = new ROSLIB.Topic({
    ros : rbServer,
    name : '/iniciarVentiladores',
    messageType : 'geometry_msgs/Twist'
  });

var twist = new ROSLIB.Message({
    linear : {
      x : 1,
      y : 0,
      z : 0
    },
    angular : {
      x : 0,
      y : 0,
      z : 0
    }
  });

   iniciarVentiladores.publish(twist);
}

function moverBrazos()
{
    var moverBrazos = new ROSLIB.Topic({
    ros : rbServer,
    name : '/moverBrazos',
    messageType : 'geometry_msgs/Twist'
  });

var twist = new ROSLIB.Message({
    linear : {
      x : 1,
      y : 0,
      z : 0
    },
    angular : {
      x : 0,
      y : 0,
      z : 0
    }
  });
   moverBrazos.publish(twist);
}

function moverGrippers()
{
    var moverGrippers = new ROSLIB.Topic({
    ros : rbServer,
    name : '/moverGrippers',
    messageType : 'geometry_msgs/Twist'
  });

var twist = new ROSLIB.Message({
    linear : {
      x : 1,
      y : 0,
      z : 0
    },
    angular : {
      x : 0,
      y : 0,
      z : 0
    }
  });
   moverGrippers.publish(twist);
}

// This function connects to the rosbridge server running on the local computer on port 9090
var rbServer = new ROSLIB.Ros({
    url : 'ws://localhost:9090'
 });


 // This function is called upon the rosbridge connection event
 rbServer.on('connection', function() {
     // Write appropriate message to #feedback div when successfully connected to rosbridge
     var fbDiv = document.getElementById('feedback');
     fbDiv.innerHTML += "<p>Connected to websocket server.</p>";
 });

// This function is called when there is an error attempting to connect to rosbridge
rbServer.on('error', function(error) {
    // Write appropriate message to #feedback div upon error when attempting to connect to rosbridge
    var fbDiv = document.getElementById('feedback');
    fbDiv.innerHTML += "<p>Error connecting to websocket server.</p>";
});

// This function is called when the connection to rosbridge is closed
rbServer.on('close', function() {
    // Write appropriate message to #feedback div upon closing connection to rosbridge
    var fbDiv = document.getElementById('feedback');
    fbDiv.innerHTML += "<p>Connection to websocket server closed.</p>";
 });


