/**
 * Created by K_God on 2017/6/5.
 */
// 用来加精和取消加精
$(function () {
    $('.highlight-btn').click(function (event) {
        event.preventDefault();
        var post_id = $(this).attr('data-post-id');
        var is_highlight = parseInt($(this).attr('data-is-highlight'));

        xtajax.post({
            'url': '/highlight/',
            'data': {
                'post_id': post_id,
                'is_highlight': !is_highlight
            },
            'success': function (data) {
                if(data['code'] == 200){
                    var msg = '';
                    if(is_highlight){
                        msg = '取消加精成功！'
                    }else {
                        msg = '加精成功！'
                    }
                    xtalert.alertSuccessToast(msg);
                    setTimeout(function () {
                        window.location.reload();
                    }, 600);
                }else {
                    xtalert.alertInfoToast(data['message']);
                }
            }
            }
        );
    });
});

// 移除帖子
$(function () {
    $('.removed-btn').click(function (event) {
        event.preventDefault();
        var post_id = $(this).attr('data-post-id');
        var is_removed = !(!parseInt($(this).attr('data-removed')));
        xtajax.post({
            'url': '/post_remove/',
            'data': {
                'post_id': post_id,
                'is_removed': is_removed
            },
            'success': function (data) {
                if(data['code'] == 200){
                    var msg = '';
                    if(is_removed){
                        msg = '帖子已经解除禁用！'
                    }else{
                        msg = '帖子已经被禁用！'
                    }
                    xtalert.alertSuccessToast(msg);
                    setTimeout(function () {
                        window.location.reload();
                    }, 600)
                }else {
                    xtalert.alertErrorToast(data['message']);
                }
            }
        });
    });
});

// 排序
$(function () {
    $('#sort-select').change(function (event) {
        var value = $(this).val();
        var newHref = xtparam.setParam(window.location.href,'sort',value);
        window.location = newHref;
    });
    $('#forbid-select').change(function (event) {
        var value = $(this).val();
        var newHref = xtparam.setParam(window.location.href,'forbid',value);
        window.location = newHref;
    });
    $('#board-filter-select').change(function (event) {
        var value = $(this).val();
        var newHref = xtparam.setParam(window.location.href,'board',value);
        window.location = newHref;
    });
});

$(function () {
   $('.no-move').click(function (event) {
       event.preventDefault();
   })
});












