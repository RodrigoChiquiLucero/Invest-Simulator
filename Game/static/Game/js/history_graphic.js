
const s = function( sketch ) {

  sketch.setup = function() {
    let count = Object.keys(sketch.history).length;
    let height = count * (50) + 140;
    let width = count * (80);
    sketch.createCanvas(width,height);
    sketch.background(255);
  };

  sketch.draw = function() {
      //set color
      sketch.fill(0);
      //draw lines
      sketch.line(60, 20, 60, sketch.height - 20);
      sketch.line(20, sketch.height - 60, sketch.width - 20, sketch.height - 60);

      sketch.fill(0, 255, 0);
      var start = 70;
      var other = 330;
      let price = 0;
      //recorrer todos los datos de la history
      $.each(sketch.history, function(i, item) {
          sketch.text(item["day"], start, 360);
          sketch.text(-price, 30, other);
          start += 70;
          other -= 50;
          price -= 30;
      });

  };
};

