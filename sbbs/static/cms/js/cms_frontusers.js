/**
 * Created by K_God on 2017/5/26.
 */

$(function () {
    $('.sort-select').change(function (event) {
        var value = $(this).val();
        var newHref = xtparam.setParam(window.location.href, 'sort', value);
        window.location = newHref;
    });
});
