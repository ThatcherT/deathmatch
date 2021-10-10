$ = jQuery;
var maxHealth = 1500,
  curHealth = maxHealth;
$('.total').html(maxHealth + "/" + maxHealth);
$(".health-bar-text").html("1500");
$(".enemy-health-bar-text").html("1500");
$(".enemy-health-bar").css({
  "width": "100%"
});
$(".health-bar").css({
  "width": "100%"
});

function applyChange(curHealth, enemy) {
  var a = curHealth * (100 / maxHealth);
  // if enemy is true, then the health bar is the enemy's health bar
  if (enemy) {
    $(".enemy-health-bar-text").html(curHealth);
    $(".enemy-health-bar-red").animate({
      'width': a + "%"
    }, 700);
    $(".enemy-health-bar").animate({
      'width': a + "%"
    }, 500);
    $(".enemy-health-bar-blue").animate({
      'width': a + "%"
    }, 300);
    $('.enemy-total').html(curHealth + "/" + maxHealth);
  } else {
    $(".health-bar-text").html(curHealth);
    $(".health-bar-red").animate({
      'width': a + "%"
    }, 700);
    $(".health-bar").animate({
      'width': a + "%"
    }, 500);
    $(".health-bar-blue").animate({
      'width': a + "%"
    }, 300);
    $('.total').html(curHealth + "/" + maxHealth);
  }
}

function restart() {
  //Was going to have a game over/restart function here. 
  $('.health-bar-red, .health-bar');
  $('.message-box').html("You've been knocked down! Thing's are looking bad.");
}