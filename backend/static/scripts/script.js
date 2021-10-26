/*var elements = document.getElementsByClassName
Array.from(elements).forEach(function(element) {
      element.addEventListener('click', myFunction);
    });*/

let changes = []
$(document).ready(function () {

      $("textarea").change(function(){
            //console.log(this)
            changes.push(this.parentNode.action)
      })

});



$(document).on("click","[name='accept']", function (event) {
      let contextDiv = event.target.parentNode.parentNode
      url = contextDiv.action;
      let url2 = url.split("/")
      let title = $(`[action='/posts/${url2[4]}'] > [type='hidden']`).val()
      body = {
            "title": title
      }

      for(var i = 0; i<changes.length; i++){
            if(changes[i] == url){
                  var txt =$(`[action='/${url2[3]}/${url2[4]}']> textarea`).val()
                  body["text"] = txt
            }

      }
      url = `/accept/${url2[4]}`
      fetch(url, {
            method: "POST",
            credentials: 'include',
            body: JSON.stringify(body)

      }).then(res => {
            contextDiv.parentNode.classList.add('accept');
            /*$(".removed").remove()*/
            $("content").on("transitionend", function (evt) { 
                  $(".accept").remove()
            });  
            
            /*console.log($(".removed").remove())*/
      });


});


$(document).on("click","[name='reject']", function (event) {
      let contextDiv = event.target.parentNode.parentNode
      url = contextDiv.action;
      let url2 = url.split("/")
      let title = $(`[action='/posts/${url2[4]}'] > [type='hidden']`).val()
      body = {
            "title": title
      }

      for(var i = 0; i<changes.length; i++){
            if(changes[i] == url){
                  var txt =$(`[action='/${url2[3]}/${url2[4]}']> textarea`).val()
                  body["text"] = txt
            }

      }
      url = `/reject/${url2[4]}`
      fetch(url, {
            method: "POST",
            credentials: 'include',
            body: JSON.stringify(body)

      }).then(res => {
            contextDiv.parentNode.classList.add('remove');
            /*$(".removed").remove()*/
            $("content").on("transitionend", function (evt) { 
                  console.log(evt)
                  $(".remove").remove()
            });  
            
            /*console.log($(".removed").remove())*/
      });


});



$(document).ready(function() {

  var animating = false;
  var cardsCounter = 0;
  var numOfCards = 6;
  var decisionVal = 80;
  var pullDeltaX = 0;
  var deg = 0;
  var $card, $cardReject, $cardLike;
  var accept = false;
  var reject = false;

  function pullChange() {
    animating = true;
    deg = pullDeltaX / 10;
    $card.css("transform", "translateX("+ pullDeltaX +"px) rotate("+ deg +"deg)");

    var opacity = pullDeltaX / 100;
    var rejectOpacity = (opacity >= 0) ? 0 : Math.abs(opacity);
    var likeOpacity = (opacity <= 0) ? 0 : opacity;
    $cardReject.css("opacity", rejectOpacity);
    $cardLike.css("opacity", likeOpacity);

  };

  function release() {

    if (pullDeltaX >= decisionVal) {
      $card.addClass("to-right");
    } else if (pullDeltaX <= -decisionVal) {
      $card.addClass("to-left");
    }

    if (Math.abs(pullDeltaX) >= decisionVal) {
      $card.addClass("inactive");

      setTimeout(function() {
        $card.addClass("below").removeClass("inactive to-left to-right");
        cardsCounter++;
        if (cardsCounter === numOfCards) {
          cardsCounter = 0;
          $(".demo__card").removeClass("below");
        }
      }, 300);
    }

    if (Math.abs(pullDeltaX) < decisionVal) {
      $card.addClass("reset");
    }

    setTimeout(function() {
      $card.attr("style", "").removeClass("reset")
        .find(".demo__card__choice").attr("style", "");

      pullDeltaX = 0;
      animating = false;
    }, 300);

  };

  /*$(document).on("mousedown touchstart", ".demo__card:not(.inactive)", function(e) {*/
  $(document).on("mousedown touchstart", "img:not(.inactive)", function(e) {
    if (animating) return;

    $card = $(this);
    $cardReject = $(".demo__card__choice.m--reject", $card);
    $cardLike = $(".demo__card__choice.m--like", $card);

    var startX =  e.pageX || e.originalEvent.touches[0].pageX;

    $(document).on("mousemove touchmove", function(e) {
      var x = e.pageX || e.originalEvent.touches[0].pageX;
      pullDeltaX = (x - startX);
      if (pullDeltaX > 0){
            if (pullDeltaX > 250){
                  accept = true;
                  reject = false;
            e.target.parentNode.style.backgroundColor = `green`
            }

      }else if (pullDeltaX < 0){
            if (pullDeltaX < -250){
                  accept = false
                  reject = true
                  e.target.parentNode.style.backgroundColor = `red`

            }

      }
      if (!pullDeltaX) return;
      pullChange();

    });

    $(document).on("mouseup touchend", function() {
      $(document).off("mousemove touchmove mouseup touchend");
      if (!pullDeltaX) return; // prevents from rapid click events
      release();
      if (accept  && ! reject){
            $card[0].parentNode.parentNode.remove()
      
      }else if (! accept  && reject){
            $card[0].parentNode.parentNode.remove()


      }
      accept = false;
      reject = false;
    });
  });

});