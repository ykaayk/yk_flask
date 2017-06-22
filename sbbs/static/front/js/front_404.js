/**
 * Created by K_God on 2017/6/7.
 */

$(function () {

   $(".click-btn").click(function (event) {
        var imgBtn = $("#404-img");
        var imgPath = imgBtn.attr('src');
        event.preventDefault();
        var num = parseInt(Math.random()*12);
        var imgPath_new = '    /static/images/404/404-'+num+'.jpg';
       imgBtn.attr('src', imgPath_new);
   });
});
