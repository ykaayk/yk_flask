/**
 * Created by K_God on 2017/6/4.
 */
// 取消几个按钮的动作
$(function () {
    $('#ellipsis-a').click(function (event) {
        event.preventDefault();
    });
    $('#ellipsis-b').click(function (event) {
        event.preventDefault();
    });
    $('#ellipsis-d').click(function (event) {
        event.preventDefault();
    });
    $('#ellipsis-s').click(function (event) {
        event.preventDefault();
    });
});